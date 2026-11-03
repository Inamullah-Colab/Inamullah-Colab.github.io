"""Shared live-inference contract for Gradio ZeroGPU and a standalone API."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent
CASES={c['id']:c for c in json.loads((ROOT/'cases.json').read_text())}

def validate_request(question,case_id):
    if not isinstance(question,str) or not question.strip():raise ValueError('Enter a question about the selected example grade.')
    if len(question)>1200:raise ValueError('Keep the question within 1,200 characters.')
    if not isinstance(case_id,str) or case_id not in CASES:raise ValueError('Select one of the five example grades.')
    return question.strip(),CASES[case_id]

def explain_case(assistant,question,case_id):
    question,case=validate_request(question,case_id)
    response=assistant.answer(question,case['probabilities'],case['streams'])
    from knowledge import answer_knowledge
    from assistant import GradeAssistant
    knowledge=None if GradeAssistant.supported_intent(question) in ['treatment','history'] else answer_knowledge(question,{},assistant)
    if knowledge:
        response['answer']=knowledge['answer'];response['reference']=None
    return {'answer':response['answer'],'facts':response['facts'],'reference':response.get('reference'),
            'case_id':case_id,'example_context':True,'context_provenance':case['provenance'],
            'references':knowledge['references'] if knowledge else [],'knowledge_augmented':bool(knowledge),
            'retrieved_topics':knowledge['topic_ids'] if knowledge else [],'weights_finetuned':False,
            'model':assistant.cfg['model_id'],'model_revision':assistant.cfg['revision'],
            'live_llm':True,'method':'Live LLM response planning with explicit scope guards and factual rendering.',
            'detail_panel':response.get('llm_selected_detail_panel')}


def explain_prediction(assistant,question,prediction_id,prediction,previous_questions=None):
    if not isinstance(question,str) or not question.strip() or len(question)>1200:raise ValueError('Enter a question within 1,200 characters.')
    response=assistant.answer(question,prediction['class_probabilities'],prediction['streams_used'])
    from knowledge import answer_knowledge
    from assistant import GradeAssistant
    # Keep the existing treatment/patient-record boundary. Broader educational topics are retrieved separately.
    intent=GradeAssistant.supported_intent(question)
    knowledge=None if intent in ['treatment','history'] else answer_knowledge(question,prediction,assistant,previous_questions)
    if knowledge:
        return {'answer':knowledge['answer'],'facts':response['facts'],'reference':None,
                'prediction_id':prediction_id,'example_context':False,'references':knowledge['references'],
                'evidence_grounded':knowledge['evidence_grounded'],'knowledge_augmented':True,
                'knowledge_version':knowledge['knowledge_version'],'retrieved_topics':knowledge['topic_ids'],
                'retrieved_fact_ids':knowledge['retrieved_fact_ids'],'resolved_query':knowledge['resolved_query'],
                'context_provenance':'Current uploaded-image facts plus curated cited educational context; systemic diagnoses are not inferred.',
                'model':assistant.cfg['model_id'],'model_revision':assistant.cfg['revision'],'live_llm':True,
                'method':knowledge['answer_method'],'weights_finetuned':False,'detail_panel':None}
    from evidence import explain_evidence
    from assistant import GradeAssistant
    evidence_text,refs=('',[])
    if GradeAssistant.supported_intent(question)=='evidence':
        evidence_text,refs=explain_evidence(question,prediction.get('evidence'))
        if evidence_text:response['answer']+='\n\n'+evidence_text
    return {'answer':response['answer'],'facts':response['facts'],'reference':response.get('reference'),
            'prediction_id':prediction_id,'example_context':False,'references':refs,'evidence_grounded':bool(evidence_text),
            'context_provenance':'Actual uploaded-image prediction from the frozen '+prediction['model_stage']+' grader and newly extracted X1–X4 streams. Research output requiring clinical review.',
            'model':assistant.cfg['model_id'],'model_revision':assistant.cfg['revision'],'live_llm':True,
            'method':'Live LLM explanation planning with scope guards and server-held image grading facts.',
            'detail_panel':response.get('llm_selected_detail_panel')}
