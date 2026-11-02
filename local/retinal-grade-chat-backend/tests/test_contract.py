import sys
from pathlib import Path
import pytest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'backend'))
from service import CASES,validate_request,explain_case
from assistant import GradeAssistant

class DummyAssistant:
    cfg={'model_id':'test-double','revision':'test'}
    def answer(self,question,probabilities,streams):
        grade=max(range(5),key=lambda i:probabilities[i])
        return {'answer':'A unit-test answer','facts':{'predicted_grade':grade,'class_probabilities':probabilities,'streams_used':streams},'reference':None,'llm_selected_detail_panel':'definition'}

def test_fixed_contexts_are_explicit_and_normalized():
    assert len(CASES)==5
    for sample in CASES.values():
        assert abs(sum(sample['probabilities'])-1)<1e-9
        assert max(range(5),key=lambda i:sample['probabilities'][i])==sample['grade']
        result=explain_case(DummyAssistant(),'Explain this grade',sample['id'])
        assert result['case_id']==sample['id'] and result['example_context'] is True
        assert result['facts']['predicted_grade']==sample['grade']

@pytest.mark.parametrize('question,case',[('', 'grade-2'),(' '*5,'grade-2'),('a'*1201,'grade-2'),('hello','grade-5'),('hello',{}),(None,'grade-2')])
def test_invalid_requests_rejected(question,case):
    with pytest.raises(ValueError):validate_request(question,case)

def test_typical_follow_up_is_supported():
    assert GradeAssistant.supported_intent('What does this mean?')=='grade'
    assert GradeAssistant.supported_intent('Which medication should I take?')=='treatment'
    assert GradeAssistant.supported_intent('Show my old records')=='history'

def test_fastapi_rejects_caller_supplied_grades():
    from api import ChatRequest
    from pydantic import ValidationError
    with pytest.raises(ValidationError):ChatRequest(question='Explain',case_id='grade-2',probabilities=[1,0,0,0,0])
