"""Measured evidence, coordinate-aware visualizations and bounded literature explanations."""
from pathlib import Path
import base64,io,json,re
import cv2,numpy as np
from PIL import Image,ImageDraw
REFERENCES=json.loads(Path(__file__).with_name('literature.json').read_text())

def summarize_skeletons(row):
    cv2.setNumThreads(1);out={'id_code':row.id_code}
    for kind in ['artery','vein','binary']:
        image=cv2.imread(getattr(row,f'x1_{kind}_skeleton_path'),cv2.IMREAD_GRAYSCALE)
        if image is None:raise ValueError('Vessel skeleton extraction failed')
        mask=(image>0).astype(np.uint8);neighbors=cv2.filter2D(mask,-1,np.ones((3,3),np.uint8))-mask
        prefix=f'x1_{kind}_global_'
        out.update({prefix+'present':1.,prefix+'density':float(mask.mean()),prefix+'components':float(cv2.connectedComponents(mask)[0]-1),prefix+'endpoints':float(((mask==1)&(neighbors==1)).sum()),prefix+'branchpoints':float(((mask==1)&(neighbors>=3)).sum())})
    vein=out['x1_vein_global_density'];out['x1_av_global_density_ratio']=out['x1_artery_global_density']/vein if vein>0 else np.nan
    return out

def png_data(array):
    image=Image.fromarray(np.uint8(np.clip(array,0,255)));image.thumbnail((384,384));buffer=io.BytesIO();image.save(buffer,format='PNG',optimize=True)
    return 'data:image/png;base64,'+base64.b64encode(buffer.getvalue()).decode()

def heat_overlay(base,heat):
    heat=cv2.resize(np.asarray(heat,np.float32),(base.shape[1],base.shape[0]),interpolation=cv2.INTER_LINEAR)
    color=cv2.cvtColor(cv2.applyColorMap(np.uint8(np.clip(heat,0,1)*255),cv2.COLORMAP_JET),cv2.COLOR_BGR2RGB)
    return np.uint8(.62*base+.38*color)

def skeleton_length(mask):
    m=mask>0
    return float((m[:,:-1]&m[:,1:]).sum()+(m[:-1,:]&m[1:,:]).sum()+np.sqrt(2)*((m[:-1,:-1]&m[1:,1:]).sum()+(m[:-1,1:]&m[1:,:-1]).sum()))

def metric_description(key):
    name=key.removeprefix('x4_macula__')
    zone='zone B' if name.endswith('_zone_b') else 'zone C' if name.endswith('_zone_c') else 'whole measured region'
    if 'Fractal_dimension' in name:meaning='Box-counting descriptor of vessel-pattern complexity; not a DR grade.';unit='dimensionless'
    elif 'Squared_curvature' in name:meaning='Squared-curvature tortuosity descriptor; sensitive to segmentation and scale.';unit='AutoMorph native units'
    elif 'Distance_tortuosity' in name:meaning='Vessel path-to-chord tortuosity descriptor; does not identify a lesion.';unit='dimensionless'
    elif 'Tortuosity_density' in name:meaning='AutoMorph tortuosity-density descriptor; no clinical normal range is supplied.';unit='AutoMorph native units'
    elif 'Vessel_density' in name:meaning='Fractional vessel occupancy from segmentation, distinct from X1 skeleton occupancy.';unit='fraction'
    elif 'AVR_' in name:meaning='Arteriole-to-venule caliber ratio estimated with the named formula.';unit='dimensionless'
    elif 'CDR_' in name:meaning='Cup-to-disc size ratio; not itself a DR severity criterion.';unit='dimensionless'
    else:meaning='Geometric size/caliber measurement from AutoMorph; physical scale is assumed, not calibrated.';unit='AutoMorph native units; assumed scale'
    return {'feature':key,'name':name.replace('_',' '),'region':zone,'meaning':meaning,'unit':unit}

def build_evidence(image_path,data,x1,x2,x4,x3,maps,rgb,raw,predictor,grade):
    cropped=np.asarray(Image.open(data/'Results/M0/images/upload.png').convert('RGB'))
    overlay=cv2.resize(cropped,(384,384));skeleton=np.zeros_like(overlay);lengths={}
    for kind,folder,color in [('binary','binary_vessel/binary_skeleton',(80,230,140)),('artery','artery_vein/artery_binary_skeleton',(255,75,75)),('vein','artery_vein/vein_binary_skeleton',(80,145,255))]:
        mask=cv2.imread(str(data/'Results/M2'/folder/'upload.png'),0)
        lengths[kind+'_skeleton_length_processed_px']=skeleton_length(mask)
        resized=cv2.resize(mask,(384,384),interpolation=cv2.INTER_NEAREST)>0
        visible=cv2.dilate(resized.astype(np.uint8),np.ones((2,2),np.uint8))>0
        overlay[visible]=color;skeleton[visible]=color
    images=[{'id':'vessel_overlay','title':'X1 · Vessel skeleton overlay','caption':'AutoMorph cropped coordinates. Arteries red, veins blue, remaining binary vessels green. Segmentation predictions, not expert annotations.','data_url':png_data(overlay)},
            {'id':'vessel_skeleton','title':'X1 · Vessel topology','caption':'Skeleton map in the same cropped coordinate frame. Junction-pixel counts are not verified anatomical bifurcation counts.','data_url':png_data(skeleton)}]
    for name,heat in maps.items():images.append({'id':'proxy_'+name,'title':'X2 proxy · '+name.replace('_',' '),'caption':'Weak heuristic evidence on the DR-XAI-preprocessed image. Color is proxy strength, not lesion probability or verified detection.','data_url':png_data(heat_overlay(rgb,heat))})
    cam,active=predictor.gradcam(str(image_path),raw,grade)
    with Image.open(image_path) as im:base=np.asarray(im.convert('RGB').resize((224,224)))
    images.append({'id':'gradcam','title':f'Grad-CAM · predicted grade {grade}','caption':'Actual frozen ResNet152 fusion-image branch attribution; raw-image coordinates resized to 224px. Tabular streams held fixed. '+('Positive attribution shown.' if active else 'No positive attribution at this layer; a zero map is shown.'),'data_url':png_data(heat_overlay(base,cam))})
    top=np.argsort(np.abs(x3))[-16:][::-1];plot=Image.new('RGB',(384,240),'#fafcf9');draw=ImageDraw.Draw(plot);maximum=max(float(np.max(np.abs(x3))),1e-9)
    for row,index in enumerate(top):
        y=10+row*14;draw.text((5,y),str(int(index)),fill='black');draw.rectangle((40,y,40+int(300*abs(float(x3[index]))/maximum),y+8),fill='#387961')
    images.append({'id':'embedding','title':'X3 · Lesion-trained representation','caption':'Largest-magnitude embedding components (indices shown), not named lesions, lesion counts or detection confidence.','data_url':png_data(np.asarray(plot))})
    return {'version':1,'X1':{'role':'Vessel morphology and topology','features':{k:float(v) for k,v in x1.items() if k!='id_code'},'supplemental_measurements':lengths,'length_note':'8-neighbor skeleton edge length in processed pixels; supplementary, not part of the frozen model inputs.','reference_ids':['automorph']},
            'X2':{'role':'Weak lesion-evidence proxy features','features':{k:float(v) for k,v in x2.items()},'proxy_only':True,'training_features_unchanged':True,'gradcam_note':'Real Grad-CAM is added as a separate post-hoc explanation; it does not replace the 190 frozen X2 features.','reference_ids':['gradcam']},
            'X3':{'role':'Lesion-based contrastive encoder representation','dimension':len(x3),'embedding_l2_norm':float(np.linalg.norm(x3)),'embedding':np.asarray(x3).astype(float).tolist(),'top_components':[{'index':int(i),'value':float(x3[i])} for i in top],
                  'lesion_detection':{'status':'not_available','detections':None,'reason':'The configured Huang checkpoint is an encoder, not the separate lesion detector. No boxes, lesion counts or disease findings are inferred from embedding components.'},'reference_ids':['lcl']},
            'X4':{'role':'Measured retinal vascular biomarkers','features':{k:float(v) for k,v in x4.items()},'definitions':[metric_description(k) for k in x4],'reference_ids':['automorph']},
            'images':images,'references':REFERENCES,'interpretation_policy':'Observed measurements and model attribution are kept separate from literature context. No normal/abnormal thresholds or lesion diagnoses are invented. Physical calibration is assumed.'}

def explain_evidence(question,evidence):
    if not evidence:return '',[]
    q=question.lower();parts=[];ids=set()
    want1=bool(re.search(r'\bx1\b|morph|skeleton|branch|length|vessel|arter|vein',q))
    want2=bool(re.search(r'\bx2\b|grad.?cam|attribut|heat.?map|xai|proxy',q))
    want3=bool(re.search(r'\bx3\b|lesion|embedding|contrastive',q))
    want4=bool(re.search(r'\bx4\b|biomarker|tortuos|curvat|densit|complex|fractal|calib|width',q))
    general=not any([want1,want2,want3,want4])
    if want1 or general:
        values=evidence['X1']['features'];length=evidence['X1']['supplemental_measurements']['binary_skeleton_length_processed_px']
        parts.append(f"X1 measured vessel structure: binary skeleton occupancy {values['x1_binary_global_density']:.4%}; connected components {values['x1_binary_global_components']:.0f}; endpoint pixels {values['x1_binary_global_endpoints']:.0f}; junction pixels {values['x1_binary_global_branchpoints']:.0f}. Supplementary skeleton edge length is {length:.1f} processed pixels, not a calibrated physical length. These describe the segmented network, not confirmed vascular disease.");ids.add('automorph')
    if want2 or general:
        features=evidence['X2']['features'];channels=['microaneurysm','hemorrhage','hard_exudate','cotton_wool_spot','neovascularization'];scores=', '.join(n.replace('_',' ')+f" proxy mean {features['x2_'+n+'_mean']:.4f}" for n in channels)
        parts.append('X2 weak evidence summaries: '+scores+'. These values do not establish lesion presence or absence. The separate Grad-CAM view uses the predicted-class gradient of the actual fusion model image branch; it is attribution, not lesion segmentation.');ids.update(['gradcam','saliency-checks'])
    if want3 or general:
        parts.append(f"X3 is a {evidence['X3']['dimension']}-dimensional lesion-trained contrastive representation (L2 norm {evidence['X3']['embedding_l2_norm']:.4f}). The available checkpoint does not produce lesion boxes or lesion counts. A high embedding component cannot be interpreted as a specific lesion. No lesion detector result is available for this image.");ids.update(['lcl','lcl-code'])
    if want4 or general:
        values=evidence['X4']['features'];groups=[('Fractal_dimension','network complexity descriptor'),('Distance_tortuosity','path-to-chord tortuosity'),('Squared_curvature_tortuosity','curvature descriptor'),('Vessel_density','vessel occupancy'),('Average_width','width in AutoMorph native units with assumed scale')]
        chosen=[]
        for key,label in groups:
            full='x4_macula__'+key
            if full in values:chosen.append(label+f" = {values[full]:.6g}")
        parts.append('X4 measured biomarkers in the whole measured region: '+'; '.join(chosen)+'. Region-specific artery/vein and zone B/C measurements are available in the results table. No clinical reference range is supplied, so these values are not labeled normal or abnormal. Physical scale is assumed. Longitudinal research has studied vascular geometry in relation to DR progression, but cohort associations cannot establish this individual image diagnosis or risk.');ids.update(['automorph','vascular-cohort'])
    return '\n\n'.join(parts),[ref for ref in REFERENCES if ref['id'] in ids]
