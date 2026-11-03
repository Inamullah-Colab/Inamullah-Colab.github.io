"""Single-image extraction using the frozen study's original feature definitions."""
import os,sys,json,subprocess,shutil,shlex
from pathlib import Path
from types import SimpleNamespace
import numpy as np
import pandas as pd
import torch

STUDY=Path(os.environ.get('RETINAL_STUDY_ROOT','/home/i1n23/retinal_10k_study'))
AUTOMORPH=Path(os.environ.get('AUTOMORPH_ROOT','/home/i1n23/AutoMorph'))
RXG=Path(os.environ.get('RETINAL_RXG_ROOT','/home/i1n23/retina_graph_dr/github_ready_xai_graph_dr'))
PYTHON=Path(os.environ.get('AUTOMORPH_PYTHON','/home/i1n23/miniconda3/envs/automorph/bin/python'))

def write_progress(root,phase,device):
    target=Path(root)/'progress.json';temporary=target.with_suffix('.tmp')
    temporary.write_text(json.dumps({'phase':phase,'device':device}));temporary.replace(target)

def extraction_device():
    if os.getenv('RETINAL_EXTRACTION_DEVICE','auto')=='cpu':return 'cpu'
    try:
        if torch.cuda.is_available() and torch.cuda.mem_get_info()[0]>=8*1024**3:return 'cuda'
    except (RuntimeError,AssertionError):pass
    return 'cpu'

def predict_upload(image_path,workspace):
    root=Path(workspace);data=root/'automorph';device=extraction_device()
    for attempt in range(2):
        if attempt:shutil.rmtree(data)
        (data/'images').mkdir(parents=True)
        (data/'images/upload.png').symlink_to(Path(image_path).resolve())
        pd.DataFrame({'fundus':['upload.png'],'res':[0.008]}).to_csv(data/'resolution_information.csv',index=False)
        env=os.environ.copy();env.update(AUTOMORPH_DATA=str(data),PATH=str(PYTHON.parent)+os.pathsep+env['PATH'],OMP_NUM_THREADS='2',MKL_NUM_THREADS='2',MPLBACKEND='Agg')
        if device=='cpu':
            # Upstream shell scripts assign CUDA_VISIBLE_DEVICES=0 themselves.
            # A private interpreter launcher enforces CPU after those assignments.
            launchers=root/'cpu-bin';launchers.mkdir(exist_ok=True)
            launcher=launchers/'python'
            launcher.write_text('#!/bin/sh\nexport CUDA_VISIBLE_DEVICES=\nexec '+shlex.quote(str(PYTHON))+' \"$@\"\n')
            launcher.chmod(0o700)
            env['CUDA_VISIBLE_DEVICES']='';env['PATH']=str(launchers)+os.pathsep+env['PATH']
        write_progress(root,'extracting',device)
        logfile=root/f'extract-{attempt}.log'
        with logfile.open('w') as log:
            completed=subprocess.run(['bash','run_noclean.sh'],cwd=AUTOMORPH,env=env,stdout=log,stderr=subprocess.STDOUT)
        text=logfile.read_text(errors='replace')
        oom='out of memory' in text.lower() or 'cuda error' in text.lower()
        if device=='cuda' and oom and attempt==0:
            device='cpu';continue
        if oom:raise ValueError('The server ran out of processing memory. No grade was produced. Please retry later; this is a server resource failure, not an assessment of your image.')
        if completed.returncode or 'Traceback (most recent call last)' in text:
            raise ValueError('The server could not complete retinal extraction. No grade was produced. This processing failure does not establish that your photograph is unsuitable.')
        break
    write_progress(root,'grading',device)
    result=grade_extracted(image_path,root,data)
    result['processing_device']=device
    (root/'prediction.json').write_text(json.dumps(result))
    return result

def grade_extracted(image_path,root,data):
    m3=data/'Results/M3/Macular_Features.csv'
    if not m3.exists():raise ValueError('The image did not pass retinal quality or feature extraction. Use a clear fundus photograph.')
    table=pd.read_csv(m3)
    if len(table)!=1:raise ValueError('The image did not produce a usable retinal feature measurement.')
    sys.path.insert(0,str(STUDY/'scripts'));sys.path.insert(0,str(RXG/'src'))
    from evidence import summarize_skeletons as summarize
    from rxg.dr_xai_evidence import DRXAIPreprocessor,LESION_CHANNELS,lesion_evidence_maps,lesion_map_embedding,map_stats
    schema=json.loads((STUDY/'feature_schema.json').read_text())
    x1dirs={'artery':'artery_vein/artery_binary_skeleton','vein':'artery_vein/vein_binary_skeleton','binary':'binary_vessel/binary_skeleton'}
    paths={f'x1_{k}_skeleton_path':str(data/'Results/M2'/v/'upload.png') for k,v in x1dirs.items()}
    if not all(Path(v).is_file() for v in paths.values()):raise ValueError('Vessel extraction failed; a grade cannot be produced.')
    x1=summarize(SimpleNamespace(id_code='upload',**paths))
    x4={k:float(pd.to_numeric(table.iloc[0].get(k.removeprefix('x4_macula__')),errors='coerce')) for k in schema['X4']}
    # Same strict all-feature-valid policy as the study: do not fabricate missing streams.
    if not all(np.isfinite(v) and v>=0 for v in x4.values()):raise ValueError('Some retinal biomarkers could not be measured reliably. This model requires a complete X1–X4 feature set; try a clearer fundus photograph.')
    rgb=DRXAIPreprocessor(image_size=448)(str(image_path));maps=lesion_evidence_maps(rgb);x2={}
    for name in LESION_CHANNELS:x2.update(map_stats(maps[name],f'x2_{name}'))
    stacked=np.stack([maps[n] for n in LESION_CHANNELS]);x2.update(x2_total_evidence_mean=float(stacked.mean()),x2_total_evidence_max=float(stacked.max()))
    x2.update({f'x2_map_embed_{j:03d}':float(v) for j,v in enumerate(lesion_map_embedding(maps,dim=128))})
    # Match EyePACS training, not the legacy APTOS 128px extractor.
    from torchvision import models,transforms
    from PIL import Image
    model=models.resnet50(weights=None);model.fc=torch.nn.Identity()
    state=torch.load(os.environ.get('HUANG_WEIGHTS','/home/i1n23/external/huang_lcl_weights/lesion_based_CL_trained_weights/resnet50_128_08.pt'),map_location='cpu',weights_only=False)
    missing,unexpected=model.load_state_dict(state,strict=False)
    if unexpected or any(not k.startswith('fc.') for k in missing):raise RuntimeError('Unexpected Huang extractor checkpoint')
    model.eval();torch.set_num_threads(2)
    transform=transforms.Compose([transforms.Resize((224,224),interpolation=transforms.InterpolationMode.BICUBIC),transforms.ToTensor(),transforms.Normalize((.485,.456,.406),(.229,.224,.225))])
    with Image.open(image_path) as im:tensor=transform(im.convert('RGB')).unsqueeze(0)
    with torch.inference_mode():x3=model(tensor).numpy()[0]
    raw={'X1':[x1[k] for k in schema['X1']],'X2':[x2[k] for k in schema['X2']],'X3':x3.tolist(),'X4':[x4[k] for k in schema['X4']]}
    if any(not np.isfinite(v).all() for v in raw.values()):raise ValueError('Incomplete feature extraction; no grade was produced.')
    from portable_predictor import ImagePredictor
    predictor=ImagePredictor(device='cpu')
    result=predictor.predict(str(image_path),raw)
    result.update(feature_dimensions={k:len(v) for k,v in raw.items()},resolution_assumption='0.008 mm/pixel assumed, matching the study; not measured',feature_policy='strict complete X1–X4',x2_provenance='weak lesion-evidence proxies, not verified lesion findings',x3_preprocessing='EyePACS training: torchvision ResNet50, 224px bicubic, ImageNet normalization',evaluation_status='Prior APTOS/Messidor results used a different X3 preprocessing pipeline; those scores are not validated performance estimates for this upload pipeline.')
    from evidence import build_evidence
    result['evidence']=build_evidence(image_path,data,x1,x2,x4,x3,maps,rgb,raw,predictor,result['predicted_grade'])
    (root/'prediction.json').write_text(json.dumps(result))
    return result

if __name__=='__main__':
    try:predict_upload(sys.argv[1],sys.argv[2])
    except ValueError as exc:
        (Path(sys.argv[2])/'failure.json').write_text(json.dumps({'detail':str(exc)}));sys.exit(2)
