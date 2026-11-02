"""Optional CPU FastAPI deployment of the same assistant contract."""
import asyncio,os,time
from collections import deque
from starlette.responses import JSONResponse
from contextlib import asynccontextmanager
from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel,Field,ConfigDict
from assistant import GradeAssistant
from service import CASES,explain_case

@asynccontextmanager
async def lifespan(app):
    import torch
    torch.set_num_threads(int(os.getenv('MODEL_THREADS','2')))
    app.state.executor=ThreadPoolExecutor(max_workers=1)
    app.state.model=None;app.state.load_error=False;app.state.busy=asyncio.Lock()
    async def load():
        try:app.state.model=await asyncio.get_running_loop().run_in_executor(app.state.executor,GradeAssistant)
        except Exception:app.state.load_error=True
    task=asyncio.create_task(load())
    yield
    if not task.done():task.cancel()
    app.state.executor.shutdown(wait=False,cancel_futures=True)

recent_requests=deque()
app=FastAPI(title='Retinal Grade Explorer',lifespan=lifespan)
origins=os.getenv('ALLOWED_ORIGINS','https://inamullah-colab.github.io,http://127.0.0.1:8080,http://localhost:8080').split(',')
app.add_middleware(CORSMiddleware,allow_origins=[o.strip() for o in origins],allow_credentials=False,allow_methods=['GET','POST'],allow_headers=['Content-Type'])

class ChatRequest(BaseModel):
    model_config=ConfigDict(extra='forbid')
    question:str=Field(min_length=1,max_length=1200)
    case_id:str=Field(pattern=r'^grade-[0-4]$')

@app.get('/health')
async def health():return {'ready':app.state.model is not None,'load_error':app.state.load_error,'live_llm':app.state.model is not None}

@app.get('/api/cases')
async def cases():return list(CASES.values())

@app.post('/api/chat')
async def chat(request:ChatRequest):
    if app.state.model is None:raise HTTPException(503,'The model is starting. Please retry shortly.')
    if app.state.busy.locked():raise HTTPException(429,'The assistant is answering another question. Please retry shortly.',headers={'Retry-After':'5'})
    async with app.state.busy:
        try:return await asyncio.get_running_loop().run_in_executor(app.state.executor,explain_case,app.state.model,request.question,request.case_id)
        except ValueError as exc:raise HTTPException(422,str(exc)) from exc

@app.middleware('http')
async def public_limits(request,call_next):
    if request.method=='POST':
        try: size=int(request.headers.get('content-length','0'))
        except ValueError:return JSONResponse({'detail':'Invalid content length'},status_code=400)
        if size>8192:return JSONResponse({'detail':'Request too large'},status_code=413)
        body=await request.body()
        if len(body)>8192:return JSONResponse({'detail':'Request too large'},status_code=413)
        now=time.monotonic()
        while recent_requests and now-recent_requests[0]>60:recent_requests.popleft()
        if len(recent_requests)>=10:return JSONResponse({'detail':'Demo request limit reached. Retry in one minute.'},status_code=429,headers={'Retry-After':'60'})
        recent_requests.append(now)
    return await call_next(request)
