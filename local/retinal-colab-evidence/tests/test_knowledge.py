from pathlib import Path
import json,sys
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'app'))
from knowledge import retrieve,answer_knowledge,DATABASE

@pytest.mark.parametrize('question,expected',[
 ('What is glaucoma?','glaucoma'),('What is AMD?','amd'),('Explain cataracts','cataract'),
 ('Explain my fractal dimension','fractal'),('Explain my vessel density','density'),
 ('Explain X4 curvature','tortuosity'),('Explain X1 vessel length','length'),
 ('What is oculomics?','oculomics'),('How does this relate to heart disease?','cardiovascular'),
 ('Explain X3 lesions','lesion-representation'),('Explain X2 proxies','proxy'),
 ('What is dry eye?','dry-eye'),('Explain myopia','refraction'),('What is retinal detachment?','detachment'),
 ('What does blood pressure have to do with eye health?','systemic-diabetes'),
 ('What is macular edema?','macular-edema'),('What is CRVO?','vein-occlusion'),
 ('Explain RETFound foundation models','foundation-research')])
def test_distinct_topics_retrieved(question,expected):
 assert retrieve(question)[0]['id']==expected

def test_unrelated_question_abstains():assert answer_knowledge('Write a recipe for pasta',{}) is None

def test_only_existing_source_facts_can_be_selected():
 class Planner:
  def select_knowledge_facts(self,*args):return ['invented:0','glaucoma:1','glaucoma:1']
 result=answer_knowledge('What is glaucoma?',{},Planner())
 assert 'invented:0' not in result['retrieved_fact_ids']
 assert 'optic nerve' in result['answer'] and 'diagnose glaucoma' in result['answer']
 assert all(r['url'].startswith('https://') for r in result['references'])

def test_metric_answers_are_specific_and_use_unchanged_values():
 pred={'evidence':{'X4':{'features':{'x4_macula__Fractal_dimension':1.51735,'x4_macula__Vessel_density':.0852726,'x4_macula__Squared_curvature_tortuosity':14.4825}}}}
 fractal=answer_knowledge('Explain my fractal dimension',pred)
 density=answer_knowledge('Explain my vessel density',pred)
 curvature=answer_knowledge('Explain my curvature value',pred)
 assert '1.51735' in fractal['answer'] and '14.4825' not in fractal['answer']
 assert '0.0852726' in density['answer'] and '1.51735' not in density['answer']
 assert '14.4825' in curvature['answer']
 assert len({r['answer'] for r in [fractal,density,curvature]})==3
 assert 'The grader used' not in fractal['answer']

def test_short_follow_up_resolves_previous_topic():
 result=answer_knowledge('What about that?',{},previous_questions=['Explain glaucoma'])
 assert 'glaucoma' in result['topic_ids']

def test_systemic_context_does_not_fabricate_diagnosis():
 for q in ['What is my heart attack risk?','Can you diagnose kidney disease?','Do I have Alzheimer disease?']:
  result=answer_knowledge(q,{})
  assert result and 'no ' in result['answer'].lower()
  assert not result['weights_finetuned']

def test_every_knowledge_topic_has_source_and_scope_boundary():
 assert len(DATABASE['topics'])==26
 assert len({t['id'] for t in DATABASE['topics']})==26
 for topic in DATABASE['topics']:
  assert topic['source']['url'].startswith('https://') and topic['boundary'] and topic['reviewed']
