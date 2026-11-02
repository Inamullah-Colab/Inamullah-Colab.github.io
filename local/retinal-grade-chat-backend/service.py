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
    return {'answer':response['answer'],'facts':response['facts'],'reference':response.get('reference'),
            'case_id':case_id,'example_context':True,'context_provenance':case['provenance'],
            'model':assistant.cfg['model_id'],'model_revision':assistant.cfg['revision'],
            'live_llm':True,'method':'Live LLM response planning with explicit scope guards and factual rendering.',
            'detail_panel':response.get('llm_selected_detail_panel')}


def explain_prediction(assistant,question,prediction_id,prediction):
    if not isinstance(question,str) or not question.strip() or len(question)>1200:raise ValueError('Enter a question within 1,200 characters.')
    response=assistant.answer(question,prediction['class_probabilities'],prediction['streams_used'])
    return {'answer':response['answer'],'facts':response['facts'],'reference':response.get('reference'),
            'prediction_id':prediction_id,'example_context':False,
            'context_provenance':'Actual uploaded-image prediction from the frozen '+prediction['model_stage']+' grader and newly extracted X1–X4 streams. Research output requiring clinical review.',
            'model':assistant.cfg['model_id'],'model_revision':assistant.cfg['revision'],'live_llm':True,
            'method':'Live LLM explanation planning with scope guards and server-held image grading facts.',
            'detail_panel':response.get('llm_selected_detail_panel')}
