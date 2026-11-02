'use strict';
(() => {
  const config=window.GRADE_DEMO_CONFIG;
  const $=id=>document.getElementById(id);
  const state={cases:[],caseId:'grade-2',connected:false,busy:false,controller:null};
  const shortLabels=['No DR','Mild','Moderate','Severe','Proliferative'];
  const subLabels=['Grade 0','Grade 1','Grade 2','Grade 3','Grade 4'];
  const base=config.backendURL.replace(/\/$/,'');
  function connection(message,mode='') {
    $('connection').className=`connection ${mode}`;
    $('connection').querySelector('span').textContent=message;
  }
  function controls() {
    $('question').disabled=!state.connected||state.busy;
    $('send').disabled=!state.connected||state.busy||!$('question').value.trim();
    document.querySelectorAll('[data-question]').forEach(b=>b.disabled=!state.connected||state.busy);
    document.querySelectorAll('.grade-choice').forEach(b=>b.disabled=state.busy);
    $('thinking').hidden=!state.busy;
  }
  function message(role,text,reference=null) {
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
    $('chat-log').append(article);$('chat-log').scrollTop=$('chat-log').scrollHeight;
    return article;
  }
  function choose(caseId) {
    if(state.busy)return;
    state.caseId=caseId;
    document.querySelectorAll('.grade-choice').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.case===caseId)));
    const sample=state.cases.find(c=>c.id===caseId);
    $('probability').textContent=`${Math.round(100*sample.probabilities[sample.grade])}%`;
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
    question=question.trim();if(!question||state.busy||!state.connected)return;
    state.busy=true;state.controller=new AbortController();controls();message('user',question);$('question').value='';
    const timer=setTimeout(()=>state.controller.abort(),120000);
    try {
      let result;
      if(config.transport==='gradio')result=await gradio(question,state.caseId,state.controller.signal);
      else {
        const response=await fetch(base+'/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question,case_id:state.caseId}),signal:state.controller.signal});
        if(!response.ok)throw new Error(response.status===429?'The assistant is busy. Please retry shortly.':'The live backend could not answer. Please retry shortly.');
        result=await response.json();
      }
      if(result.live_llm!==true||typeof result.answer!=='string'||result.case_id!==state.caseId)throw new Error('The backend response did not match the selected live example.');
      message('assistant',result.answer,result.reference);
    } catch(error) {
      message('error',error.name==='AbortError'?'This request timed out while waiting for the hosted model. You can retry; no saved answer has been substituted.':error.message);
    } finally {clearTimeout(timer);state.busy=false;state.controller=null;controls();$('question').focus();}
  }
  async function init() {
    $('backend-link').href=config.spaceURL;
    try {
      const response=await fetch('./cases.json');if(!response.ok)throw new Error('Examples could not be loaded.');
      state.cases=await response.json();
      state.cases.forEach(c=>{
        const button=document.createElement('button');button.type='button';button.className='grade-choice';button.dataset.case=c.id;button.setAttribute('aria-pressed','false');
        const number=document.createElement('span');number.className='grade-number';number.textContent=c.grade;
        const text=document.createElement('span');const strong=document.createElement('strong');strong.textContent=shortLabels[c.grade];const small=document.createElement('small');small.textContent=subLabels[c.grade];text.append(strong,small);button.append(number,text);button.addEventListener('click',()=>choose(c.id));$('grade-options').append(button);
      });choose(state.caseId);await checkConnection();
    } catch(error) {connection('Examples unavailable','offline');message('error',error.message);}
  }
  $('chat-form').addEventListener('submit',event=>{event.preventDefault();ask($('question').value);});
  $('question').addEventListener('input',controls);
  $('question').addEventListener('keydown',event=>{if(event.key==='Enter'&&!event.shiftKey){event.preventDefault();ask($('question').value);}});
  $('retry').addEventListener('click',checkConnection);
  document.querySelectorAll('[data-question]').forEach(button=>button.addEventListener('click',()=>ask(button.dataset.question)));
  controls();init();
})();
