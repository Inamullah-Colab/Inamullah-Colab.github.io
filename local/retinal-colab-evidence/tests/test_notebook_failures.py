import os,sys,subprocess,json
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'app'))

def test_extraction_exposes_original_error_and_allows_same_image_retry(tmp_path,monkeypatch):
 import image_pipeline
 tools=tmp_path/'tools';tools.mkdir();(tools/'run_noclean.sh').write_text('echo "ORIGINAL TEST ERROR: missing dependency"\nexit 7\n')
 monkeypatch.setattr(image_pipeline,'AUTOMORPH',tools)
 image=tmp_path/'input.png';image.write_bytes(b'test')
 out=tmp_path/'analysis';out.mkdir()
 for _ in range(2):
  with pytest.raises(RuntimeError,match='ORIGINAL TEST ERROR: missing dependency'):
   image_pipeline.predict_upload(image,out)
 assert 'ORIGINAL TEST ERROR' in (out/'extract.log').read_text()

def test_runner_reports_gpu_error_instead_of_only_subprocess_status(tmp_path):
 env=os.environ.copy();env['CUDA_VISIBLE_DEVICES']=''
 out=tmp_path/'analysis'
 result=subprocess.run([sys.executable,str(ROOT/'app/notebook_runner.py'),'--bundle',str(tmp_path/'bundle'),'--image',str(tmp_path/'image.png'),'--output',str(out)],env=env,capture_output=True,text=True)
 assert result.returncode==1
 assert 'Enable a Colab GPU runtime' in result.stderr
 assert 'RETINAL ANALYSIS FAILED' in result.stderr
 assert 'Enable a Colab GPU runtime' in json.loads((out/'failure.json').read_text())['detail']
