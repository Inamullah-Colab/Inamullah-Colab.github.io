"""One persistent local LLM per notebook session; JSON over stdin/stdout, no public API."""
import os,sys,json
from pathlib import Path
from assistant import GradeAssistant
from service import explain_prediction
report_path=Path(sys.argv[1])
prediction=json.loads(report_path.read_text())
assistant=GradeAssistant(device=os.environ.get('NOTEBOOK_LLM_DEVICE','cuda'))
from knowledge import DATABASE
conversation=[]
print(json.dumps({'ready':True,'model':assistant.cfg['model_id'],'knowledge_topics':len(DATABASE['topics']),'knowledge_version':DATABASE['version']}),flush=True)
for line in sys.stdin:
    try:
        question=json.loads(line)['question']
        result=explain_prediction(assistant,question,'notebook-local-session',prediction,previous_questions=conversation[-3:])
        conversation.append(question)
        saved=prediction.setdefault('conversation',[])
        saved.append({'question':question,'answer':result['answer'],'references':result.get('references',[]),'reference':result.get('reference'),'model':assistant.cfg['model_id'],'knowledge_version':result.get('knowledge_version'),'live_llm':result.get('live_llm',False)})
        if len(saved)>100:del saved[:-100]
        temporary=report_path.with_suffix('.json.tmp')
        temporary.write_text(json.dumps(prediction,indent=2));temporary.replace(report_path)
        print(json.dumps(result),flush=True)
    except Exception as exc:print(json.dumps({'error':str(exc)}),flush=True)
