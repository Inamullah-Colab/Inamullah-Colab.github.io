import json,sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'app'))

def test_quality_rejection_is_successful_report_and_stops_segmentation(tmp_path,monkeypatch):
 import image_pipeline as pipeline
 tools=tmp_path/'tools';tools.mkdir()
 (tools/'run_noclean.sh').write_text('''echo "$@" >> "$AUTOMORPH_DATA/calls.txt"
mkdir -p "$AUTOMORPH_DATA/Results/M1"
printf 'Name,Prediction,softmax_bad,usable_sd\\nupload.png,2,0.9,0.1\\n' > "$AUTOMORPH_DATA/Results/M1/results_ensemble.csv"
''')
 monkeypatch.setattr(pipeline,'AUTOMORPH',tools);monkeypatch.setattr(pipeline,'PYTHON',Path(sys.executable))
 image=tmp_path/'input.png';image.write_bytes(b'test');out=tmp_path/'analysis';out.mkdir()
 result=pipeline.predict_upload(image,out)
 assert result['status']=='quality_rejected' and result['predicted_grade'] is None
 assert result['class_probabilities'] is None and result['quality_assessment']['Prediction']==2
 assert (out/'automorph/calls.txt').read_text().splitlines()==['--no_segmentation --no_feature']
 assert json.loads((out/'prediction.json').read_text())['grading_available'] is False

def test_quality_acceptance_continues_to_grading(tmp_path,monkeypatch):
 import image_pipeline as pipeline
 tools=tmp_path/'tools';tools.mkdir()
 (tools/'run_noclean.sh').write_text('''echo "$@" >> "$AUTOMORPH_DATA/calls.txt"
mkdir -p "$AUTOMORPH_DATA/Results/M1/Good_quality"
printf 'Name,Prediction\\nupload.png,0\\n' > "$AUTOMORPH_DATA/Results/M1/results_ensemble.csv"
touch "$AUTOMORPH_DATA/Results/M1/Good_quality/upload.png"
''')
 monkeypatch.setattr(pipeline,'AUTOMORPH',tools);monkeypatch.setattr(pipeline,'PYTHON',Path(sys.executable))
 monkeypatch.setattr(pipeline,'grade_extracted',lambda *args:{'status':'graded','predicted_grade':2})
 image=tmp_path/'input.png';image.write_bytes(b'test');out=tmp_path/'analysis';out.mkdir()
 assert pipeline.predict_upload(image,out)['predicted_grade']==2
 assert (out/'automorph/calls.txt').read_text().splitlines()==['--no_segmentation --no_feature','--no_process --no_quality']

def test_empty_measurements_are_normal_abstention(tmp_path):
 from image_pipeline import grade_extracted
 data=tmp_path/'automorph';(data/'Results/M3').mkdir(parents=True)
 (data/'Results/M3/Macular_Features.csv').write_text('Name,Disc_height\n')
 result=grade_extracted(tmp_path/'input.png',tmp_path,data)
 assert result['status']=='feature_incomplete' and result['predicted_grade'] is None
 assert result['available_features']=={}

def test_notebook_continues_display_chat_and_download_after_rejection(tmp_path,monkeypatch,capsys):
 n=json.loads((ROOT/'notebooks/Retinal_Evidence_Explorer.ipynb').read_text())
 report={'status':'quality_rejected','reason':'Quality model rejected this image','available_features':{},'missing_features':[]}
 scope={'REPORT':report,'json':json,'RUN_DIR':tmp_path}
 for cell in n['cells']:
  if cell['cell_type']!='code':continue
  text=''.join(cell['source'])
  if 'EVIDENCE=REPORT' in text or 'CHAT_LOG=(RUN_DIR/' in text:exec(compile(text,'<rejected-image cell>','exec'),scope)
 assert 'No grade produced' in capsys.readouterr().out
 assert 'CHAT' not in scope
