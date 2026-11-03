"""Standalone frozen ResNet152 + X1–X4 inference and image-branch Grad-CAM."""
from pathlib import Path
import hashlib,json,os
import numpy as np
import joblib,torch
from torch import nn
from torchvision import models,transforms
from PIL import Image

class Fusion(nn.Module):
    def __init__(self,dims):
        super().__init__();self.backbone=models.resnet152(weights=None);self.backbone.fc=nn.Identity();self.dims=dims
        self.image_project=nn.Sequential(nn.Linear(2048,128),nn.ReLU())
        self.streams=nn.ModuleList([nn.Sequential(nn.Linear(v,64),nn.ReLU()) for v in dims])
        self.head=nn.Sequential(nn.Linear(128+64*len(dims),128),nn.ReLU(),nn.Dropout(.2),nn.Linear(128,5))
    def forward(self,image,tabular):
        pieces=[self.image_project(self.backbone(image))]+[encoder(v) for encoder,v in zip(self.streams,torch.split(tabular,self.dims,dim=1))]
        return self.head(torch.cat(pieces,dim=1))

def digest(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1048576),b''):h.update(block)
    return h.hexdigest()

class ImagePredictor:
    def __init__(self,device='cpu',root=None):
        self.root=Path(root or os.environ.get('RETINAL_STUDY_ROOT','/home/i1n23/retinal_10k_study'));self.device=torch.device(device)
        selection=json.loads((self.root/'results/image_selection_frozen.json').read_text());self.stage=selection['selected_stage']
        checkpoint=self.root/'results'/self.stage/'checkpoint.pt'
        if digest(checkpoint)!=selection['checkpoints'][self.stage]:raise ValueError('Frozen image checkpoint hash mismatch')
        prep=self.root/'features/preprocessors.joblib';fs=json.loads((self.root/'results/feature_selection_frozen.json').read_text())
        if digest(prep)!=fs['preprocessor_sha256']:raise ValueError('Frozen preprocessor hash mismatch')
        ck=torch.load(checkpoint,map_location='cpu',weights_only=False)
        if ck['architecture']!='resnet152':raise ValueError('This release supports only the frozen ResNet152 checkpoint')
        self.model=Fusion(ck['dims']);self.model.load_state_dict(ck['state_dict'],strict=True);self.model.to(self.device).eval();self.transforms=joblib.load(prep)
        self.image_transform=transforms.Compose([transforms.Resize((224,224),interpolation=transforms.InterpolationMode.BICUBIC),transforms.ToTensor(),transforms.Normalize((.485,.456,.406),(.229,.224,.225))])
    def prepare(self,image_path,raw):
        blocks=[]
        for stream in ['X1','X2','X3','X4']:
            v=np.asarray(raw[stream],dtype=float).reshape(1,-1);t=self.transforms[stream]
            if v.shape[1]!=t['imputer'].n_features_in_:raise ValueError('Wrong raw feature dimension: '+stream)
            v[~np.isfinite(v)]=np.nan
            if stream=='X4':v[v<0]=np.nan
            if np.isnan(v).all():raise ValueError('Missing stream '+stream)
            v=t['imputer'].transform(v)
            if t['pca'] is not None:v=t['pca'].transform(v)
            blocks.append(t['scaler'].transform(v).astype(np.float32))
        with Image.open(image_path) as im:image=self.image_transform(im.convert('RGB')).unsqueeze(0).to(self.device)
        return image,torch.from_numpy(np.concatenate(blocks,axis=1)).to(self.device)
    def predict(self,image_path,raw):
        image,tab=self.prepare(image_path,raw)
        with torch.inference_mode():p=torch.softmax(self.model(image,tab).float(),1).cpu().numpy()[0]
        return {'model_stage':self.stage,'predicted_grade':int(p.argmax()),'class_probabilities':p.tolist(),'streams_used':['raw_image','X1','X2','X3','X4'],'max_probability':float(p.max()),'calibration_status':'not clinically calibrated','clinical_review_required':True}
    def gradcam(self,image_path,raw,target):
        image,tab=self.prepare(image_path,raw);captured=[]
        hook=self.model.backbone.layer4.register_forward_hook(lambda module,inputs,output:captured.append(output))
        try:
            with torch.enable_grad():
                logits=self.model(image,tab);activations=captured[0]
                gradients=torch.autograd.grad(logits[0,int(target)],activations)[0]
                cam=torch.relu((gradients.mean(dim=(2,3),keepdim=True)*activations).sum(dim=1))[0]
                cam=cam.detach().float().cpu().numpy()
            maximum=float(cam.max());cam=cam/maximum if maximum>0 else np.zeros_like(cam)
            return cam,maximum>0
        finally:hook.remove()
