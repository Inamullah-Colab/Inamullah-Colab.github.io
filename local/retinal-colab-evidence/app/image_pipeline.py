"""Single-image extraction using the frozen study's original feature definitions."""
import os,sys,json,subprocess
from pathlib import Path
from types import SimpleNamespace
import numpy as np
import pandas as pd
import torch

STUDY=Path(os.environ.get('RETINAL_STUDY_ROOT','/home/i1n23/retinal_10k_study'))
AUTOMORPH=Path(os.environ.get('AUTOMORPH_ROOT','/home/i1n23/AutoMorph'))
RXG=Path(os.environ.get('RETINAL_RXG_ROOT','/home/i1n23/retina_graph_dr/github_ready_xai_graph_dr'))
PYTHON=Path(os.environ.get('AUTOMORPH_PYTHON','/home/i1n23/miniconda3/envs/automorph/bin/python'))

def ungraded_result(status,reason,available=None,missing=None,quality=None):
    return {'status':status,'predicted_grade':None,'class_probabilities':None,
            'grading_available':False,'reason':reason,'available_features':available or {},
            'missing_features':missing or [],'quality_assessment':quality or {},
            'next_step':'Use a clear, well-focused fundus photograph with the retina fully visible. A quality-model rejection is not a disease diagnosis.',
            'evidence':{'images':[],'references':[]},'clinical_review_required':True}

def write_result(root,result):
    (Path(root)/'prediction.json').write_text(json.dumps(result,allow_nan=False))
    return result

def predict_upload(image_path,workspace):
    root=Path(workspace);data=root/'automorph';(data/'images').mkdir(parents=True,exist_ok=True)
    staged=data/'images/upload.png'
    if staged.is_symlink() or staged.exists():
        if staged.resolve()!=Path(image_path).resolve():raise ValueError('This analysis folder already belongs to a different image; use a new output folder.')
    else:staged.symlink_to(Path(image_path).resolve())
    pd.DataFrame({'fundus':['upload.png'],'res':[0.008]}).to_csv(data/'resolution_information.csv',index=False)
    env=os.environ.copy();env.update(AUTOMORPH_DATA=str(data),PATH=str(PYTHON.parent)+os.pathsep+env['PATH'],OMP_NUM_THREADS='2',MKL_NUM_THREADS='2',MPLBACKEND='Agg')
    def run_stage(arguments,mode):
        with (root/'extract.log').open(mode) as log:
            completed=subprocess.run(['bash','run_noclean.sh']+arguments,cwd=AUTOMORPH,env=env,stdout=log,stderr=subprocess.STDOUT)
        if completed.returncode:
            tail='\n'.join((root/'extract.log').read_text(errors='replace').splitlines()[-60:])
            raise RuntimeError(f'AutoMorph extraction exited with code {completed.returncode}. The actual extraction log follows:\n{tail}')
    run_stage(['--no_segmentation','--no_feature'],'w')
    quality_file=data/'Results/M1/results_ensemble.csv'
    if not quality_file.exists():raise RuntimeError('The quality stage did not produce its assessment file. Inspect extract.log.')
    quality_table=pd.read_csv(quality_file)
    quality={}
    if len(quality_table)==1:
        quality={str(k):float(v) for k,v in quality_table.iloc[0].items() if k!='Name' and pd.api.types.is_number(v) and np.isfinite(v)}
    if not (data/'Results/M1/Good_quality/upload.png').is_file():
        return write_result(root,ungraded_result('quality_rejected','AutoMorph quality assessment did not accept this photograph. No vessel segmentation or DR grade was produced.',quality=quality))
    run_stage(['--no_process','--no_quality'],'a')
    return grade_extracted(image_path,root,data)

def grade_extracted(image_path,root,data):
    m3=data/'Results/M3/Macular_Features.csv'
    if not m3.exists():return write_result(root,ungraded_result('feature_incomplete','No macular measurements were produced; no DR grade was produced.'))
    table=pd.read_csv(m3)
    if len(table)!=1:return write_result(root,ungraded_result('feature_incomplete','No unique usable retinal measurement was produced; no DR grade was produced.'))
    sys.path.insert(0,str(STUDY/'scripts'));sys.path.insert(0,str(RXG/'src'))
    from evidence import summarize_skeletons as summarize
    from rxg.dr_xai_evidence import DRXAIPreprocessor,LESION_CHANNELS,lesion_evidence_maps,lesion_map_embedding,map_stats
    schema=json.loads((STUDY/'feature_schema.json').read_text())
    x1dirs={'artery':'artery_vein/artery_binary_skeleton','vein':'artery_vein/vein_binary_skeleton','binary':'binary_vessel/binary_skeleton'}
    paths={f'x1_{k}_skeleton_path':str(data/'Results/M2'/v/'upload.png') for k,v in x1dirs.items()}
    if not all(Path(v).is_file() for v in paths.values()):return write_result(root,ungraded_result('feature_incomplete','Required vessel maps were unavailable; no DR grade was produced.'))
    x1=summarize(SimpleNamespace(id_code='upload',**paths))
    x4={k:float(pd.to_numeric(table.iloc[0].get(k.removeprefix('x4_macula__')),errors='coerce')) for k in schema['X4']}
    # Same strict all-feature-valid policy as the study: do not fabricate missing streams.
    missing=[k.removeprefix('x4_macula__') for k,v in x4.items() if not np.isfinite(v) or v<0]
    if missing:return write_result(root,ungraded_result('feature_incomplete','Some required X4 biomarkers could not be measured. Available values are retained; no DR grade was produced.',available={'X1':{k:float(v) for k,v in x1.items() if k!='id_code' and np.isfinite(v)},'X4':{k:float(v) for k,v in x4.items() if np.isfinite(v) and v>=0}},missing=missing))
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
    result.update(status='graded',grading_available=True,feature_dimensions={k:len(v) for k,v in raw.items()},resolution_assumption='0.008 mm/pixel assumed, matching the study; not measured',feature_policy='strict complete X1–X4',x2_provenance='weak lesion-evidence proxies, not verified lesion findings',x3_preprocessing='EyePACS training: torchvision ResNet50, 224px bicubic, ImageNet normalization',evaluation_status='Prior APTOS/Messidor results used a different X3 preprocessing pipeline; those scores are not validated performance estimates for this upload pipeline.')
    from evidence import build_evidence
    result['evidence']=build_evidence(image_path,data,x1,x2,x4,x3,maps,rgb,raw,predictor,result['predicted_grade'])
    (root/'prediction.json').write_text(json.dumps(result))
    return result

if __name__=='__main__':
    try:predict_upload(sys.argv[1],sys.argv[2])
    except ValueError as exc:
        (Path(sys.argv[2])/'failure.json').write_text(json.dumps({'detail':str(exc)}));sys.exit(2)
