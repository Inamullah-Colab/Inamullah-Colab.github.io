import io,sys,asyncio
from pathlib import Path
import pytest
from PIL import Image
from fastapi.testclient import TestClient
package_root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(package_root/'backend' if (package_root/'backend').is_dir() else package_root))
from uploads import decode_image,jobs
from api import app,ChatRequest,recent_requests
from service import explain_prediction

class Assistant:
 cfg={'model_id':'test','revision':'test'}
 def answer(self,q,p,s):return {'answer':'Grade explanation','facts':{'class_probabilities':p,'predicted_grade':max(range(5),key=lambda i:p[i]),'streams_used':s}}

def test_decode_rejects_non_images_and_small_images():
 with pytest.raises(ValueError):decode_image(b'not an image')
 b=io.BytesIO();Image.new('RGB',(10,10)).save(b,format='PNG')
 with pytest.raises(ValueError):decode_image(b.getvalue())

def test_decode_preserves_pixels_without_metadata():
 b=io.BytesIO();Image.new('RGB',(128,128),(10,20,30)).save(b,format='PNG')
 decoded=decode_image(b.getvalue());assert decoded.getpixel((0,0))==(10,20,30);decoded.close()

def test_contexts_are_exclusive_and_probabilities_cannot_be_injected():
 from pydantic import ValidationError
 token='a'*43
 for data in ({},{'case_id':'grade-2','prediction_id':token},{'prediction_id':token,'probabilities':[1,0,0,0,0]}):
  with pytest.raises(ValidationError):ChatRequest(question='Explain',**data)

def test_prediction_explanation_uses_server_result():
 pred={'model_stage':'IMAGE_resnet152','class_probabilities':[.01,.02,.9,.03,.04],'streams_used':['raw_image','X1','X2','X3','X4']}
 result=explain_prediction(Assistant(),'Explain','a'*43,pred)
 assert result['example_context'] is False
 assert result['facts']['predicted_grade']==2
 assert result['facts']['class_probabilities']==pred['class_probabilities']

def test_api_upload_validation_and_missing_prediction():
 app.state.model=Assistant();app.state.busy=asyncio.Lock();recent_requests.clear()
 client=TestClient(app)
 assert client.post('/api/predict',content=b'not an image').status_code==422
 assert client.get('/api/predictions/'+'z'*43).status_code==404
 assert client.post('/api/chat',json={'question':'Explain','prediction_id':'z'*43}).status_code==404
 assert client.post('/api/chat',json={'question':'Explain','case_id':'grade-2','prediction_id':'z'*43}).status_code==422
 assert client.post('/api/predict',content=b'x',headers={'Content-Length':str(11*1024*1024)}).status_code==413
