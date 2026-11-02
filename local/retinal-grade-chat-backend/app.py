"""Hugging Face Gradio/ZeroGPU backend; API endpoint: /explain."""
import spaces  # Load before torch: ZeroGPU provides CUDA emulation at startup.
import os
import gradio as gr
import torch
from assistant import GradeAssistant
from service import CASES,explain_case

torch.set_num_threads(int(os.getenv('MODEL_THREADS','2')))
assistant=GradeAssistant(device=os.getenv('MODEL_DEVICE','cuda' if os.getenv('SPACE_ID') else 'cpu'))

@spaces.GPU(duration=20)
def respond(question,case_id):
    try:return explain_case(assistant,question,case_id)
    except ValueError as exc:raise gr.Error(str(exc)) from exc

with gr.Blocks(title='Retinal Grade Explorer — live backend') as demo:
    gr.Markdown('# Retinal Grade Explorer\nLive question answering about five illustrative grading contexts. No image upload or patient history. Research demonstration, not clinical diagnosis.')
    context=gr.Dropdown(choices=[(f"Grade {c['grade']} · {c['label']}",c['id']) for c in CASES.values()],value='grade-2',label='Illustrative grade context')
    question=gr.Textbox(label='Question',placeholder='What does this grade mean?',max_lines=4)
    submit=gr.Button('Ask the grade assistant',variant='primary')
    answer=gr.JSON(label='Grounded response')
    submit.click(respond,inputs=[question,context],outputs=answer,api_name='explain',concurrency_limit=1)
    gr.Examples([['What does this grade mean?','grade-2'],['How confident is this result?','grade-2'],['Which evidence streams were used?','grade-2']],inputs=[question,context])

if __name__=='__main__':
    demo.queue(max_size=8).launch(server_name='0.0.0.0',server_port=int(os.getenv('PORT','7860')),show_error=False,ssr_mode=False)
