"""Build only inference artifacts; exclude retinal data, logs and credentials."""
from pathlib import Path
import hashlib,json,tarfile
HOME=Path('/home/i1n23');PROJECT=HOME/'retinal_colab_evidence';STUDY=HOME/'retinal_10k_study'
files=[]
for p in (HOME/'AutoMorph').iterdir():
 if p.is_file() and p.name in ['automorph_data.py','csv_merge.py','run_noclean.sh','LICENSE','README.md']:files.append((p,'AutoMorph/'+p.name))
for directory in ['M0_Preprocess','M1_Retinal_Image_quality_EyePACS','M2_Artery_vein','M2_Vessel_seg','M2_lwnet_disc_cup','M3_feature_zone','M3_feature_whole_pic']:
 for p in (HOME/'AutoMorph'/directory).rglob('*'):
  if p.is_file() and p.suffix in {'.py','.sh','.pth','.pt','.cfg','.config','.ini','.yaml','.yml','.json'} and '__pycache__' not in p.parts:
   files.append((p,'AutoMorph/'+p.relative_to(HOME/'AutoMorph').as_posix()))
for rel in ['feature_schema.json','features/preprocessors.joblib','results/image_selection_frozen.json','results/feature_selection_frozen.json','results/IMAGE_resnet152/checkpoint.pt']:
 files.append((STUDY/rel,'study/'+rel))
files.append((HOME/'external/huang_lcl_weights/lesion_based_CL_trained_weights/resnet50_128_08.pt','weights/huang.pt'))
files.append((HOME/'.cache/torch/hub/checkpoints/efficientnet-b4-6ed6700e.pth','torch/hub/checkpoints/efficientnet-b4-6ed6700e.pth'))
files.append((HOME/'retina_graph_dr/github_ready_xai_graph_dr/src/rxg/dr_xai_evidence.py','rxg/src/rxg/dr_xai_evidence.py'))
manifest={}
for source,relative in files:
 h=hashlib.sha256()
 with source.open('rb') as f:
  for block in iter(lambda:f.read(1048576),b''):h.update(block)
 manifest[relative]={'sha256':h.hexdigest(),'bytes':source.stat().st_size}
manifest_path=PROJECT/'artifacts/bundle_manifest.json';manifest_path.write_text(json.dumps({'version':1,'files':manifest},indent=2))
archive=PROJECT/'artifacts/retinal_models_v1.tar.gz'
with tarfile.open(archive,'w:gz',compresslevel=1) as tar:
 for source,relative in files:tar.add(source,arcname='model_bundle/'+relative,recursive=False)
 tar.add(manifest_path,arcname='model_bundle/bundle_manifest.json')
h=hashlib.sha256()
with archive.open('rb') as f:
 for block in iter(lambda:f.read(1048576),b''):h.update(block)
(PROJECT/'artifacts/archive.sha256').write_text(h.hexdigest()+'  '+archive.name+'\n')
print('Inference-only bundle:',archive,'bytes:',archive.stat().st_size,'files:',len(files),'SHA256:',h.hexdigest(),flush=True)
