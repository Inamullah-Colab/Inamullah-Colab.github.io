import base64,io,json,sys
from pathlib import Path
import numpy as np
from PIL import Image
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'app'))
from evidence import explain_evidence,skeleton_length,metric_description
from assistant import GradeAssistant

def report():
 path=ROOT/'reports/example_report.json'
 if not path.exists():pytest.skip('Generate a local real-image report before running integration evidence checks')
 return json.loads(path.read_text())

def test_skeleton_length_has_correct_pixel_geometry():
 mask=np.zeros((8,8),dtype=np.uint8);mask[3,1:6]=255
 assert skeleton_length(mask)==4
 diagonal=np.eye(5,dtype=np.uint8)
 assert skeleton_length(diagonal)==pytest.approx(4*np.sqrt(2))

def test_stream_questions_route_to_evidence():
 for q in ['Explain X1','Show X2 Grad-CAM','What does X3 mean?','Explain X4 curvature','Explain lesion-based features']:
  assert GradeAssistant.supported_intent(q)=='evidence'
 assert GradeAssistant.supported_intent('Which medicine for these vessels?')=='treatment'

def test_actual_report_has_complete_features_and_honest_detector_status():
 r=report();e=r['evidence']
 assert len(e['X1']['features'])==16 and len(e['X2']['features'])==190
 assert len(e['X3']['embedding'])==2048 and len(e['X4']['features'])==72
 assert e['X2']['proxy_only'] is True
 assert e['X3']['lesion_detection']['status']=='not_available'
 assert e['X3']['lesion_detection']['detections'] is None
 assert len(e['images'])==9
 for panel in e['images']:
  image=Image.open(io.BytesIO(base64.b64decode(panel['data_url'].split(',')[1])))
  assert max(image.size)<=384 and image.format=='PNG'

def test_explanations_use_actual_numbers_and_avoid_unavailable_findings():
 e=report()['evidence']
 text,refs=explain_evidence('Explain X1 vessel length',e)
 assert f"{e['X1']['supplemental_measurements']['binary_skeleton_length_processed_px']:.1f}" in text
 assert 'processed pixels' in text and any(r['id']=='automorph' for r in refs)
 text,refs=explain_evidence('Explain X3 lesions',e)
 assert 'No lesion detector result is available' in text
 assert 'No lesions' not in text
 text,refs=explain_evidence('Explain X4 curvature and complexity',e)
 assert 'X4 measured biomarkers' in text and 'not labeled normal or abnormal' in text

def test_curvature_units_do_not_claim_calibrated_length():
 definition=metric_description('x4_macula__Squared_curvature_tortuosity_zone_c')
 assert definition['region']=='zone C'
 assert definition['unit']=='AutoMorph native units'
