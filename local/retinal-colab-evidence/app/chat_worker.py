"""One persistent local LLM per notebook session; JSON over stdin/stdout, no public API."""
import os,sys,json
from pathlib import Path
from assistant import GradeAssistant
from service import explain_prediction
prediction=json.loads(Path(sys.argv[1]).read_text())
assistant=GradeAssistant(device=os.environ.get('NOTEBOOK_LLM_DEVICE','cuda'))
print(json.dumps({'ready':True,'model':assistant.cfg['model_id']}),flush=True)
for line in sys.stdin:
    try:
        question=json.loads(line)['question']
        result=explain_prediction(assistant,question,'notebook-local-session',prediction)
        print(json.dumps(result),flush=True)
    except Exception as exc:print(json.dumps({'error':str(exc)}),flush=True)
