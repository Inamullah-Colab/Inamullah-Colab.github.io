"""Run inside the isolated Python3.11 model environment, without a web server."""
import argparse,os,sys,json
from pathlib import Path

def configure(bundle):
    bundle=Path(bundle).resolve()
    os.environ.update(RETINAL_STUDY_ROOT=str(bundle/'study'),AUTOMORPH_ROOT=str(bundle/'AutoMorph'),RETINAL_RXG_ROOT=str(bundle/'rxg'),HUANG_WEIGHTS=str(bundle/'weights/huang.pt'),TORCH_HOME=str(bundle/'torch'),AUTOMORPH_PYTHON=sys.executable)

def main():
    p=argparse.ArgumentParser();p.add_argument('--bundle',required=True);p.add_argument('--image',required=True);p.add_argument('--output',required=True);args=p.parse_args();configure(args.bundle)
    import torch
    if not torch.cuda.is_available():raise RuntimeError('Enable a Colab GPU runtime before running the AutoMorph pipeline.')
    torch.set_num_threads(2)
    from image_pipeline import predict_upload
    out=Path(args.output).resolve();out.mkdir(parents=True,exist_ok=True)
    prediction=predict_upload(Path(args.image).resolve(),out)
    (out/'evidence_report.json').write_text(json.dumps(prediction,indent=2))
    print('Ready. Grade:',prediction['predicted_grade'],'Evidence panels:',len(prediction['evidence']['images']),flush=True)
if __name__=='__main__':main()
