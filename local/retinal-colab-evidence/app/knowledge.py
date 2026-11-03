"""Extractive retrieval-augmented answers. LLM selects source fact IDs, not medical claims."""
from pathlib import Path
import json,re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
ROOT=Path(__file__).resolve().parent
DATABASE=json.loads((ROOT/'knowledge_base.json').read_text())
TOPICS=DATABASE['topics']
TEXTS=[' '.join([t['title']]+t['keywords']) for t in TOPICS]
VECTORIZER=TfidfVectorizer(analyzer='char_wb',ngram_range=(3,5)).fit(TEXTS)
MATRIX=VECTORIZER.transform(TEXTS)

def retrieve(question,limit=2):
    q=question.lower();similarity=cosine_similarity(VECTORIZER.transform([q]),MATRIX)[0];ranked=[]
    for index,topic in enumerate(TOPICS):
        matches=[k for k in topic['keywords'] if re.search(r'(?<!\w)'+re.escape(k)+r'(?!\w)',q)]
        score=float(similarity[index])+2*len(matches)
        # Distinctive spelling variants may match via character retrieval, but vague questions abstain.
        if matches or similarity[index]>=.24:ranked.append((score,topic))
    ranked.sort(key=lambda value:value[0],reverse=True)
    if not ranked:return []
    best=ranked[0][0]
    return [topic for score,topic in ranked[:limit] if score>=best*.25]

def measured_context(question,prediction,topic_ids):
    e=prediction.get('evidence') or {};q=question.lower()
    if not re.search(r'\bmy\b|this image|uploaded|result|measurement|\bvalue\b|\bx[1-4]\b',q):return ''
    x4=e.get('X4',{}).get('features',{});x1=e.get('X1',{}).get('features',{})
    chosen=[];prefix='Artery_' if re.search(r'arter|arteriol',q) else 'Vein_' if re.search(r'vein|venul',q) else ''
    suffix='_zone_b' if re.search(r'zone\s*b\b',q) else '_zone_c' if re.search(r'zone\s*c\b',q) else ''
    def metric(name,label):
        key='x4_macula__'+prefix+name+suffix
        if key in x4 and np.isfinite(x4[key]):chosen.append(label+f' = {x4[key]:.6g}')
    if 'fractal' in topic_ids:metric('Fractal_dimension','fractal dimension')
    if 'tortuosity' in topic_ids:
        if re.search(r'curv',q):metric('Squared_curvature_tortuosity','squared-curvature descriptor (native units)')
        else:metric('Distance_tortuosity','path-to-chord tortuosity')
    if 'density' in topic_ids:
        if 'x1' in q and 'x1_binary_global_density' in x1:chosen.append(f"binary skeleton occupancy = {x1['x1_binary_global_density']:.4%}")
        else:metric('Vessel_density','segmented-vessel occupancy (fraction)')
    if 'length' in topic_ids:
        value=e.get('X1',{}).get('supplemental_measurements',{}).get('binary_skeleton_length_processed_px')
        if value is not None:chosen.append(f'supplementary skeleton edge length = {value:.1f} processed pixels')
        for term,name in [('endpoint','endpoints'),('junction','branchpoints'),('branch','branchpoints'),('component','components')]:
            key='x1_binary_global_'+name
            if term in q and key in x1:chosen.append(name+f' pixels/count = {x1[key]:.0f}')
    if 'glaucoma' in topic_ids:
        for name in ['CDR_vertical','CDR_horizontal']:
            if 'x4_macula__'+name in x4:chosen.append(name+f" = {x4['x4_macula__'+name]:.6g}")
    if 'lesion-representation' in topic_ids and e.get('X3'):
        chosen.append(f"X3 representation dimension = {e['X3']['dimension']}; lesion detections = not available")
    if 'streams' in topic_ids and not chosen:
        if 'x1' in q and 'x1_binary_global_density' in x1:chosen.append(f"X1 binary skeleton occupancy = {x1['x1_binary_global_density']:.4%}")
        if 'x4' in q:chosen.append(f"X4 measured biomarkers available = {len(x4)}")
    if not chosen:return ''
    return 'For your uploaded image: '+ '; '.join(dict.fromkeys(chosen))+'. These are measurements, not validated normal/abnormal judgments.'

def answer_knowledge(question,prediction,assistant=None,previous_questions=None):
    query=question
    if len(question.split())<7 and re.search(r'\bit\b|\bthat\b|\bthose\b|\bthey\b|what about',question.lower()) and previous_questions:
        query=previous_questions[-1]+' '+question
    topics=retrieve(query)
    if topics and topics[0]['id']!='streams' and not re.search(r'framework|streams|fusion',query.lower()):topics=[t for t in topics if t['id']!='streams']
    if not topics:return None
    candidates=[]
    for topic in topics:
        for index,fact in enumerate(topic['facts']):candidates.append({'id':topic['id']+':'+str(index),'text':fact,'topic':topic['id']})
    planned=[]
    if assistant is not None and hasattr(assistant,'select_knowledge_facts'):
        planned=assistant.select_knowledge_facts(question,candidates)
    # The primary topic's definition is always present; optional facts are selected from a strict whitelist.
    allowed={fact['id'] for fact in candidates};selected=[topics[0]['id']+':0']+[i for i in planned if i in allowed]
    if len(set(selected))<2:selected += [topics[0]['id']+':1']
    if len(topics)>1:selected.append(topics[1]['id']+':0')
    selected=list(dict.fromkeys(selected))[:4];paragraphs=[];refs=[]
    for topic in topics:
        facts=[f['text'] for f in candidates if f['topic']==topic['id'] and f['id'] in selected]
        if not facts:continue
        paragraphs.append(topic['title']+'\n'+' '.join(facts)+'\n'+topic['boundary'])
        refs.append(topic['source'])
    measurement=measured_context(query,prediction,[t['id'] for t in topics])
    if measurement:paragraphs.append(measurement)
    return {'answer':'\n\n'.join(paragraphs),'references':refs,'topic_ids':[t['id'] for t in topics],
            'retrieved_fact_ids':selected,'evidence_grounded':bool(measurement),
            'knowledge_version':DATABASE['version'],'knowledge_augmented':True,
            'answer_method':'Extractive retrieval-augmented explanation; local LLM selects whitelisted source facts; measurements are rendered from the current report.',
            'weights_finetuned':False,'resolved_query':query}
