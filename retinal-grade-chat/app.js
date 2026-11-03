'use strict';
(() => {
  const config=window.GRADE_DEMO_CONFIG;
  const $=id=>document.getElementById(id);
  const state={cases:[],caseId:'grade-2',connected:false,busy:false,controller:null,predictionId:null,uploading:false,previewURL:null,report:null};
  const shortLabels=['No DR','Mild','Moderate','Severe','Proliferative'];
  const subLabels=['Grade 0','Grade 1','Grade 2','Grade 3','Grade 4'];
  const base=config.backendURL.replace(/\/$/,'');
  function connection(message,mode='') {
    $('connection').className=`connection ${mode}`;
    $('connection').querySelector('span').textContent=message;
  }
  function controls() {
    const unavailable=!state.connected||state.busy||state.uploading||(!state.caseId&&!state.predictionId);
    $('question').disabled=unavailable;
    $('upload-button').disabled=!state.connected||state.busy||state.uploading||!$('retinal-file').files.length;
    $('retinal-file').disabled=state.busy||state.uploading;
    $('send').disabled=unavailable||!$('question').value.trim();
    document.querySelectorAll('[data-question]').forEach(b=>b.disabled=unavailable);
    document.querySelectorAll('.grade-choice').forEach(b=>b.disabled=state.busy||state.uploading);
    $('thinking').hidden=!state.busy;
  }
  function message(role,text,reference=null,references=[]) {
    const article=document.createElement('article');article.className=`message ${role}`;
    const label=document.createElement('div');label.className='message-label';label.textContent=role==='user'?'You':role==='error'?'Connection update':'Grade assistant';
    const body=document.createElement('div');body.className='message-text';body.textContent=text;
    article.append(label,body);
    if(reference?.url) {
      try {
        const url=new URL(reference.url);
        if(url.protocol==='https:') {
          const a=document.createElement('a');a.href=url.href;a.target='_blank';a.rel='noopener noreferrer';a.textContent='Read the grading reference ↗';a.title=reference.title||'';article.append(a);
        }
      } catch (_) { /* Ignore malformed reference URLs. */ }
    }
    references.forEach(ref=>{try{const url=new URL(ref.url);if(url.protocol==='https:'){const a=document.createElement('a');a.href=url.href;a.target='_blank';a.rel='noopener noreferrer';a.textContent=ref.title;article.append(document.createElement('br'),a);}}catch(_){}});
    $('chat-log').append(article);$('chat-log').scrollTop=$('chat-log').scrollHeight;
    return article;
  }
  function choose(caseId) {
    if(state.busy||state.uploading)return;
    state.predictionId=null;state.caseId=caseId;
    $('image-result').hidden=true;$('evidence-panel').hidden=true;state.report=null;
    document.querySelectorAll('.grade-choice').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.case===caseId)));
    const sample=state.cases.find(c=>c.id===caseId);
    $('probability').textContent=`${Math.round(100*sample.probabilities[sample.grade])}%`;
    document.querySelector('.profile').style.setProperty('--score',`${100*sample.probabilities[sample.grade]}%`);
    $('chat-log').replaceChildren();
    const welcome=message('assistant',`You’ve selected an illustrative grade ${sample.grade} context: ${sample.label.toLowerCase()}. Ask what the category means, how to interpret the model probability, or which inputs the grader used.\n\nThe example supplies the grading facts. The live language model helps plan the explanation.`);
    welcome.classList.add('welcome');$('question').value='';controls();
  }
  async function checkConnection() {
    state.connected=false;connection('Connecting…');$('retry').hidden=true;controls();
    const control=new AbortController();const timer=setTimeout(()=>control.abort(),20000);
    try {
      const endpoint=config.transport==='gradio'?'/gradio_api/info':'/health';
      const response=await fetch(base+endpoint,{signal:control.signal,cache:'no-store'});
      if(!response.ok)throw new Error('The model backend is starting or unavailable.');
      const data=await response.json();
      if(config.transport==='gradio'&&!data.named_endpoints?.['/explain'])throw new Error('The live explanation endpoint is not ready.');
      if(config.transport!=='gradio'&&!data.ready)throw new Error('The model is still loading.');
      state.connected=true;connection('Live model connected','online');
    } catch (_) {
      connection('Backend unavailable','offline');$('retry').hidden=false;
    } finally {clearTimeout(timer);controls();}
  }
  async function gradio(question,caseId,signal) {
    const response=await fetch(base+'/gradio_api/call/explain',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({data:[question,caseId]}),signal});
    if(!response.ok)throw new Error('The backend could not accept this request. It may be waking up or have reached its visitor quota.');
    const {event_id:eventId}=await response.json();
    if(typeof eventId!=='string'||!/^[A-Za-z0-9_-]{1,128}$/.test(eventId))throw new Error('The backend returned an invalid request identifier.');
    const events=await fetch(`${base}/gradio_api/call/explain/${eventId}`,{signal});
    if(!events.ok||!events.body)throw new Error('Unable to receive the model response.');
    const reader=events.body.getReader();const decoder=new TextDecoder();let buffer='';
    while(true) {
      const {value,done}=await reader.read();
      buffer+=decoder.decode(value||new Uint8Array(),{stream:!done}).replace(/\r\n/g,'\n');
      let boundary;
      while((boundary=buffer.indexOf('\n\n'))!==-1) {
        const block=buffer.slice(0,boundary);buffer=buffer.slice(boundary+2);
        const lines=block.split('\n');const event=lines.find(l=>l.startsWith('event:'))?.slice(6).trim();
        const payload=lines.filter(l=>l.startsWith('data:')).map(l=>l.slice(5).trimStart()).join('\n');
        if(event==='complete') {
          const result=JSON.parse(payload);return Array.isArray(result)?result[0]:result;
        }
        if(event==='error')throw new Error('The live model could not complete this request. The demo server may be busy or unavailable. Please retry later.');
      }
      if(done)throw new Error('The connection ended before the model returned an answer.');
    }
  }
  async function ask(question) {
    question=question.trim();if(!question||state.busy||state.uploading||!state.connected||(!state.caseId&&!state.predictionId))return;
    state.busy=true;state.controller=new AbortController();controls();message('user',question);$('question').value='';
    const timer=setTimeout(()=>state.controller.abort(),120000);
    try {
      let result;
      if(config.transport==='gradio')result=await gradio(question,state.caseId,state.controller.signal);
      else {
        const response=await fetch(base+'/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(state.predictionId?{question,prediction_id:state.predictionId}:{question,case_id:state.caseId}),signal:state.controller.signal});
        if(!response.ok){const detail=await response.json().catch(()=>({}));throw new Error(detail.detail||'The live backend could not answer. Please retry shortly.');}
        result=await response.json();
      }
      if(result.live_llm!==true||typeof result.answer!=='string'||(state.predictionId?result.prediction_id!==state.predictionId||result.example_context!==false:result.case_id!==state.caseId))throw new Error('The backend response did not match the selected live example.');
      message('assistant',result.answer,result.reference,result.references||[]);
    } catch(error) {
      message('error',error.name==='AbortError'?'This request timed out while waiting for the hosted model. You can retry; no saved answer has been substituted.':error.message);
    } finally {clearTimeout(timer);state.busy=false;state.controller=null;controls();$('question').focus();}
  }
  function renderEvidence(evidence) {
    if(!evidence)return;
    $('evidence-panel').hidden=false;$('stream-summaries').replaceChildren();$('evidence-images').replaceChildren();$('evidence-tables').replaceChildren();$('evidence-references').replaceChildren();
    const descriptions={X1:'Vessel skeleton occupancy, junction and endpoint pixels, connected components, and supplementary processed-pixel length.',X2:'Five weak lesion-evidence proxy channels. A separate real Grad-CAM view attributes the frozen grader image branch; it does not replace the trained X2 inputs.',X3:'Lesion-trained contrastive embedding. The configured checkpoint does not detect lesion boxes or counts; these are explicitly unavailable.',X4:'72 measured biomarkers covering vessel density, tortuosity, curvature, fractal complexity, width, caliber ratios and region-specific structure.'};
    ['X1','X2','X3','X4'].forEach(stream=>{
      const card=document.createElement('article');card.className='stream-card';const title=document.createElement('h3');title.textContent=stream+' · '+evidence[stream].role;const text=document.createElement('p');text.textContent=descriptions[stream];card.append(title,text);$('stream-summaries').append(card);
      const details=document.createElement('details');details.className='evidence-details';const summary=document.createElement('summary');summary.textContent=stream+' · Full measured values and definitions';details.append(summary);
      const wrap=document.createElement('div');wrap.className='feature-table-wrap';const table=document.createElement('table');table.className='feature-table';const head=document.createElement('thead');const tr=document.createElement('tr');['Feature','Value','Meaning / units'].forEach(label=>{const th=document.createElement('th');th.textContent=label;tr.append(th);});head.append(tr);table.append(head);const body=document.createElement('tbody');
      const values=stream==='X3'?Object.fromEntries(evidence.X3.top_components.map(v=>['embedding component '+v.index,v.value])):{...evidence[stream].features,...(evidence[stream].supplemental_measurements||{})};
      Object.entries(values).forEach(([key,value])=>{const row=document.createElement('tr');const definition=(evidence[stream].definitions||[]).find(d=>d.feature===key);const meaning=definition?definition.meaning+' '+definition.unit:stream==='X2'?'Weak proxy feature, not a lesion diagnosis':stream==='X3'?'Embedding activation, not a named lesion':key.includes('length')?'Supplemental length in processed pixels':key.includes('density')?'Skeleton occupancy fraction':key.includes('branchpoints')?'Junction pixels; not verified bifurcation count':'Computed skeleton descriptor';[key,Number(value).toPrecision(7),meaning].forEach(text=>{const td=document.createElement('td');td.textContent=text;row.append(td);});body.append(row);});
      table.append(body);wrap.append(table);details.append(wrap);$('evidence-tables').append(details);
    });
    evidence.images.forEach(asset=>{if(!/^data:image\/png;base64,[A-Za-z0-9+/=]+$/.test(asset.data_url))return;const figure=document.createElement('figure');const img=document.createElement('img');img.src=asset.data_url;img.alt=asset.title;img.loading='lazy';const caption=document.createElement('figcaption');const title=document.createElement('strong');title.textContent=asset.title;caption.append(title,document.createTextNode(asset.caption));figure.append(img,caption);$('evidence-images').append(figure);});
    const note=document.createElement('p');note.textContent=evidence.interpretation_policy;$('evidence-references').append(note);
    evidence.references.forEach(ref=>{const p=document.createElement('p');const a=document.createElement('a');a.href=ref.url;a.textContent=ref.title;a.target='_blank';a.rel='noopener noreferrer';p.append(a,document.createTextNode(' — '+ref.summary+' '+ref.limits));$('evidence-references').append(p);});
  }
  $('download-report').addEventListener('click',()=>{if(!state.report)return;const url=URL.createObjectURL(new Blob([JSON.stringify(state.report,null,2)],{type:'application/json'}));const link=document.createElement('a');link.href=url;link.download='retinal-evidence-report.json';link.click();setTimeout(()=>URL.revokeObjectURL(url),5000);});
  async function uploadImage(event) {
    event.preventDefault();const file=$('retinal-file').files[0];
    if(!file||state.busy||state.uploading||!state.connected)return;
    if(file.size>10*1024*1024){$('upload-status').textContent='Choose a file no larger than 10 MB.';return;}
    state.uploading=true;state.caseId=null;state.predictionId=null;$('image-result').hidden=true;$('evidence-panel').hidden=true;state.report=null;
    document.querySelectorAll('.grade-choice').forEach(b=>b.setAttribute('aria-pressed','false'));
    $('chat-log').replaceChildren();$('probability').textContent='—';
    document.querySelector('.profile').style.setProperty('--score','0%');controls();
    const start=Date.now();let timer;
    try {
      $('upload-status').textContent='Uploading photograph…';
      const controller=new AbortController();timer=setTimeout(()=>controller.abort(),60000);
      const response=await fetch(base+'/api/predict',{method:'POST',headers:{'Content-Type':file.type||'application/octet-stream'},body:file,signal:controller.signal});
      clearTimeout(timer);
      const data=await response.json();if(!response.ok)throw new Error(data.detail||'Upload failed.');
      if(typeof data.prediction_id!=='string'||!/^[A-Za-z0-9_-]{40,64}$/.test(data.prediction_id))throw new Error('Invalid upload response.');
      let ready=null;
      while(Date.now()-start<19*60*1000) {
        $('upload-status').textContent=`Extracting X1–X4 and grading… ${Math.floor((Date.now()-start)/1000)} seconds. Keep this page open.`;
        await new Promise(resolve=>setTimeout(resolve,3000));
        const poll=await fetch(base+'/api/predictions/'+data.prediction_id,{cache:'no-store',signal:AbortSignal.timeout(20000)});
        const job=await poll.json();if(!poll.ok)throw new Error(job.detail||'Unable to retrieve prediction.');
        if(job.status==='failed')throw new Error(job.detail||'Processing failed. No grade was produced.');
        if(job.status==='ready'){ready=job;break;}
      }
      if(!ready)throw new Error('Image processing timed out. No result is shown.');
      const result=ready.prediction;const probs=result.class_probabilities;
      if(!Array.isArray(probs)||probs.length!==5||!probs.every(v=>Number.isFinite(v)&&v>=0&&v<=1)||!Number.isInteger(result.predicted_grade)||result.predicted_grade<0||result.predicted_grade>4)throw new Error('Invalid grading response.');
      state.predictionId=data.prediction_id;state.report=ready;renderEvidence(result.evidence);
      $('predicted-grade').textContent=`Grade ${result.predicted_grade} · ${shortLabels[result.predicted_grade]}`;
      $('class-probabilities').replaceChildren();
      probs.forEach((probability,grade)=>{
        const row=document.createElement('div');row.className='probability-row';
        const label=document.createElement('span');label.textContent=`${grade} · ${shortLabels[grade]}`;
        const bar=document.createElement('div');bar.className='probability-bar';const fill=document.createElement('span');fill.style.width=`${probability*100}%`;bar.append(fill);
        const value=document.createElement('span');value.textContent=`${(100*probability).toFixed(1)}%`;row.append(label,bar,value);$('class-probabilities').append(row);
      });
      $('prediction-model').textContent=`${result.model_stage} · Inputs: ${result.streams_used.join(', ')}`;
      $('image-result').hidden=false;$('probability').textContent=`${(100*probs[result.predicted_grade]).toFixed(1)}%`;
      document.querySelector('.profile').style.setProperty('--score',`${100*probs[result.predicted_grade]}%`);
      $('upload-status').textContent='Image graded. Ask about this actual prediction below. This session expires in 30 minutes.';
      message('assistant',`Your uploaded photograph was graded by the trained retinal model as grade ${result.predicted_grade} (${shortLabels[result.predicted_grade]}), with ${(100*probs[result.predicted_grade]).toFixed(1)}% model probability. All X1–X4 streams were extracted from this image. This is an uncalibrated research prediction requiring clinical review. Ask me to explain the grade, probability, or inputs.`);
    } catch(error) {
      $('upload-status').textContent=error.name==='AbortError'?'The upload connection timed out. Please retry.':error.message;
      message('error','No grading result is available. '+$('upload-status').textContent);
    } finally {clearTimeout(timer);state.uploading=false;controls();}
    if(state.predictionId)await ask('What does this grade mean?');
  }
  $('upload-form').addEventListener('submit',uploadImage);
  $('retinal-file').addEventListener('change',()=>{
    if(state.previewURL)URL.revokeObjectURL(state.previewURL);
    const file=$('retinal-file').files[0];$('image-preview').hidden=!file;
    if(file){
      state.previewURL=URL.createObjectURL(file);$('image-preview').src=state.previewURL;
      state.caseId=null;state.predictionId=null;$('image-result').hidden=true;$('evidence-panel').hidden=true;state.report=null;
      document.querySelectorAll('.grade-choice').forEach(b=>b.setAttribute('aria-pressed','false'));
      $('chat-log').replaceChildren();message('assistant','New photograph selected. Choose Analyze retinal image to extract X1–X4 and obtain its grading result.');
      $('probability').textContent='—';document.querySelector('.profile').style.setProperty('--score','0%');
    }
    controls();
  });
  async function init() {
    $('backend-link').href=config.spaceURL;
    try {
      const response=await fetch('./cases.json');if(!response.ok)throw new Error('Examples could not be loaded.');
      state.cases=await response.json();
      state.cases.forEach(c=>{
        const button=document.createElement('button');button.type='button';button.className='grade-choice';button.dataset.case=c.id;button.setAttribute('aria-pressed','false');
        const number=document.createElement('span');number.className='grade-number';number.textContent=c.grade;
        const text=document.createElement('span');const strong=document.createElement('strong');strong.textContent=shortLabels[c.grade];const small=document.createElement('small');small.textContent=subLabels[c.grade];text.append(strong,small);button.append(number,text);button.addEventListener('click',()=>choose(c.id));$('grade-options').append(button);
      });state.caseId=null;document.querySelector('.profile').style.setProperty('--score','0%');message('assistant','Upload a retinal photograph and select Analyze retinal image. The trained model will extract X1–X4 and predict a grade; I will then explain that actual result. You can also open the illustrative examples to explore the chat.');await checkConnection();
    } catch(error) {connection('Examples unavailable','offline');message('error',error.message);}
  }
  $('chat-form').addEventListener('submit',event=>{event.preventDefault();ask($('question').value);});
  $('question').addEventListener('input',controls);
  $('question').addEventListener('keydown',event=>{if(event.key==='Enter'&&!event.shiftKey){event.preventDefault();ask($('question').value);}});
  $('retry').addEventListener('click',checkConnection);
  document.querySelectorAll('[data-question]').forEach(button=>button.addEventListener('click',()=>ask(button.dataset.question)));
  controls();init();
})();
