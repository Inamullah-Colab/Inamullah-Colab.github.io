"""Bounded ephemeral upload jobs. Never trust client-supplied grading facts."""
import asyncio,io,json,os,secrets,signal,tempfile,time,warnings
from pathlib import Path
from PIL import Image,UnidentifiedImageError
from fastapi import HTTPException,Request
PYTHON=Path(os.environ.get('AUTOMORPH_PYTHON','/home/i1n23/miniconda3/envs/automorph/bin/python'))

MAX_BYTES=10*1024*1024
TTL=1800
jobs={}
lock=asyncio.Lock()
tasks=set()

def prune():
    now=time.monotonic()
    for key in list(jobs):
        if jobs[key]['expires']<now and jobs[key]['status']!='processing':del jobs[key]

def get_job(token):
    prune()
    if token not in jobs:raise HTTPException(404,'This prediction has expired or does not exist. Upload the image again.')
    return jobs[token]

def decode_image(payload):
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('error',Image.DecompressionBombWarning)
            with Image.open(io.BytesIO(payload)) as im:
                if im.format not in ('PNG','JPEG'):raise ValueError('Upload a JPG or PNG fundus photograph.')
                if min(im.size)<128 or im.width*im.height>30_000_000:raise ValueError('Use an image at least 128 pixels on each side and at most 30 megapixels.')
                if getattr(im,'n_frames',1)!=1:raise ValueError('Animated images are not supported.')
                im.load();return im.convert('RGB')
    except (UnidentifiedImageError,OSError,Image.DecompressionBombError,Image.DecompressionBombWarning) as exc:
        raise ValueError('This file is not a valid JPG or PNG image.') from exc

async def run_job(token,image):
    job=jobs[token];process=None
    try:
        with tempfile.TemporaryDirectory(prefix='retinal-upload-') as directory:
            root=Path(directory);image.save(root/'input.png');image.close()
            env=os.environ.copy();env.update(OMP_NUM_THREADS='2',MKL_NUM_THREADS='2')
            with (root/'worker.log').open('wb') as log:
                process=await asyncio.create_subprocess_exec(str(PYTHON),str(Path(__file__).with_name('image_pipeline.py')),str(root/'input.png'),str(root),env=env,stdout=log,stderr=log,start_new_session=True)
                try:code=await asyncio.wait_for(process.wait(),timeout=1020)
                except (asyncio.TimeoutError,asyncio.CancelledError):
                    os.killpg(process.pid,signal.SIGTERM)
                    try:await asyncio.wait_for(process.wait(),10)
                    except asyncio.TimeoutError:os.killpg(process.pid,signal.SIGKILL);await process.wait()
                    raise
            if code==0 and (root/'prediction.json').exists():
                prediction=json.loads((root/'prediction.json').read_text())
                job.update(status='ready',prediction=prediction)
            else:
                detail='The retinal processing pipeline could not complete. No grade was produced. Please try a clear fundus photograph.'
                if (root/'failure.json').exists():detail=json.loads((root/'failure.json').read_text())['detail']
                job.update(status='failed',detail=detail)
    except asyncio.TimeoutError:job.update(status='failed',detail='Retinal processing timed out. No grade was produced.')
    except Exception:job.update(status='failed',detail='Image processing is unavailable. No grade was produced. Please retry later.')
    finally:
        image.close();job['expires']=time.monotonic()+TTL
        lock.release()

def register(app):
    @app.post('/api/predict',status_code=202)
    async def upload(request:Request):
        prune()
        if app.state.model is None:raise HTTPException(503,'The assistant is starting. Retry shortly.')
        if lock.locked():raise HTTPException(429,'Another retinal image is processing. Please retry in a few minutes.',headers={'Retry-After':'30'})
        if len(jobs)>=20:raise HTTPException(429,'The demo has reached its temporary session limit. Please retry later.')
        await lock.acquire()
        try:
            payload=bytearray()
            async for chunk in request.stream():
                if len(payload)+len(chunk)>MAX_BYTES:raise HTTPException(413,'Maximum upload size is 10 MB.')
                payload.extend(chunk)
            try:image=await asyncio.to_thread(decode_image,bytes(payload))
            except ValueError as exc:raise HTTPException(422,str(exc)) from exc
            token=secrets.token_urlsafe(32)
            jobs[token]={'status':'processing','expires':time.monotonic()+TTL}
            task=asyncio.create_task(run_job(token,image));tasks.add(task);task.add_done_callback(tasks.discard)
            return {'prediction_id':token,'status':'processing','poll_after_seconds':3}
        except BaseException:lock.release();raise

    @app.get('/api/predictions/{token}')
    async def prediction(token:str):
        job=get_job(token)
        result={'prediction_id':token,'status':job['status']}
        if job['status']=='ready':result.update(prediction=job['prediction'],example_context=False)
        if job['status']=='failed':result['detail']=job['detail']
        return result
