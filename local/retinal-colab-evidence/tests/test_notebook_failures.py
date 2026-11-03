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


def test_colab_inline_backend_is_replaced_in_worker(tmp_path,monkeypatch):
 import image_pipeline
 tools=tmp_path/'tools';tools.mkdir()
 (tools/'run_noclean.sh').write_text("python -c \"import matplotlib; print('WORKER_BACKEND=' + str(matplotlib.get_backend())); assert str(matplotlib.get_backend()).lower() == 'agg'\"\nexit 7\n")
 monkeypatch.setattr(image_pipeline,'AUTOMORPH',tools)
 monkeypatch.setattr(image_pipeline,'PYTHON',Path(sys.executable))
 monkeypatch.setenv('MPLBACKEND','module://matplotlib_inline.backend_inline')
 image=tmp_path/'input.png';image.write_bytes(b'test');out=tmp_path/'analysis';out.mkdir()
 with pytest.raises(RuntimeError,match='WORKER_BACKEND=Agg|WORKER_BACKEND=agg'):
  image_pipeline.predict_upload(image,out)
 assert 'not a valid value for backend' not in (out/'extract.log').read_text()

def test_notebook_runner_configures_headless_plotting(tmp_path,monkeypatch):
 from notebook_runner import configure
 monkeypatch.setenv('MPLBACKEND','module://matplotlib_inline.backend_inline')
 configure(tmp_path)
 assert os.environ['MPLBACKEND']=='Agg'
