/* Aggregate page views only; no cookies, visitor identifiers, referrers or campaigns. */
(() => {
 'use strict';
 const service='https://inam-visitor-insights.boxywatermelon2.chatgpt.site';
 const origins=['https://inamullah-colab.github.io','https://knowledge-opportunity-inam.boxywatermelon2.chatgpt.site'];
 const pref='inam-counter-choice-v2', noticeKey='inam-counter-notice-v2';
 function preference(storage){try {const value=storage.getItem(pref);if(value==='allow'||value==='deny')return value;return ['inam-visitor-statistics-v1','knowledge-visitor-statistics-v1'].some(k=>storage.getItem(k)==='deny')?'deny':'allow';}catch{return 'allow';}}
 function pagePath(location){let path=location.pathname;const post=new URLSearchParams(location.search).get('post');if(path==='/knowledge/articles/'&&post&&/^[a-zA-Z0-9_-]+$/.test(post))path='/knowledge/articles/'+post;return path;}
 function validData(d){return d&&['total','today','week','countryCount'].every(k=>Number.isSafeInteger(d[k])&&d[k]>=0)&&Array.isArray(d.countries)&&d.countries.every(c=>/^[A-Z]{2}$/.test(c.code)&&Number.isSafeInteger(c.views)&&c.views>=0);}
 if(typeof module==='object'&&module.exports){module.exports={preference,pagePath,validData};return;}
 if(window.__inamCounterV2){window.dispatchEvent(new Event('inam-counter-mount'));return;}
 window.__inamCounterV2=true;
 let storage;try{storage=window.localStorage;}catch{}
 let choice=preference(storage), blocked=navigator.globalPrivacyControl===true||navigator.doNotTrack==='1';
 let data=null,readError=false,readId=0,attempted=new Set(),recordError=false,requestPending=false;
 const flags=location.origin===origins[0]?'/assets/flags/':'https://inamullah-colab.github.io/assets/flags/';
 const privacy=location.pathname.startsWith('/knowledge/')?'/knowledge/privacy/':'/privacy/';
 const number=n=>n.toLocaleString('en-GB');
 const date=d=>new Date(d+'T12:00:00Z').toLocaleDateString('en-GB',{day:'numeric',month:'short',year:'numeric',timeZone:'UTC'});
 function slots(){return [...document.querySelectorAll('[data-site-counter]')];}
 function setChoice(value){choice=value;try{localStorage.setItem(pref,value);}catch{}render();notice();if(value==='allow')record();}
 function notice(){
  let seen=false;try{seen=localStorage.getItem(noticeKey)==='seen';}catch{}
  let box=document.getElementById('inam-counting-notice');
  if(blocked||choice==='deny'||seen){box?.remove();return;}
  if(box)return;
  box=document.createElement('aside');box.id='inam-counting-notice';box.className='counter-notice';box.setAttribute('aria-label','Page-view counting notice');
  box.innerHTML='<p>We count page views to improve this website, without tracking cookies or visitor IDs.</p><div><button type="button" data-counter-pause>Opt out</button><a href="'+privacy+'">Privacy details</a><button type="button" data-counter-dismiss aria-label="Dismiss counting notice">Dismiss</button></div>';
  box.querySelector('[data-counter-pause]').onclick=()=>setChoice('deny');
  box.querySelector('[data-counter-dismiss]').onclick=()=>{try{localStorage.setItem(noticeKey,'seen');}catch{}box.remove();};document.body.append(box);
 }
 function initialise(box){
  if(box.dataset.counterMounted)return;box.dataset.counterMounted='true';box.classList.add('world-counter');
  box.innerHTML='<div class="wc-heading"><div><p class="wc-eyebrow">OUR READERSHIP</p><h2>Visitors around the world</h2></div><button class="wc-refresh" type="button">↻ Refresh counts</button></div><p class="wc-scope">Portfolio + Knowledge &amp; Opportunity · one shared counter</p><div class="wc-totals"><div><strong data-total>—</strong><span>All-time page views</span></div><div><strong data-today>—</strong><span>Today · UTC</span></div><div><strong data-week>—</strong><span>Last 7 days</span></div><div><strong data-countryCount>—</strong><span>Countries</span></div></div><div class="wc-countries" aria-label="Page views by country"></div><p class="wc-unknown" hidden></p><p class="wc-status" role="status" aria-live="polite">Loading recorded counts…</p><details class="wc-details"><summary>What these numbers mean</summary><p>Page views count pages opened, not unique people. Repeat visits count again. Country estimates may reflect a VPN; unavailable locations are shown separately.</p><p class="wc-history">All recorded history is retained.</p><p>Earlier unrecorded visits cannot be recovered. The counter excludes opted-out browsers, privacy signals and detected bots. Blocked scripts or network errors can also reduce counts. Automatic refresh reads the totals; it does not add another view.</p></details><div class="wc-choice"><span></span><button type="button"></button><a href="'+privacy+'">Privacy details</a></div>';
  box.querySelector('.wc-refresh').onclick=refresh;box.querySelector('.wc-choice button').onclick=()=>setChoice(choice==='deny'?'allow':'deny');
 }
 function render(){for(const box of slots()){
  initialise(box);const status=box.querySelector('.wc-status');
  if(data){for(const key of ['total','today','week','countryCount'])box.querySelector('[data-'+key+']').textContent=number(data[key]);
   const list=box.querySelector('.wc-countries');list.replaceChildren();
   for(const c of data.countries){let name=c.code;try{name=new Intl.DisplayNames(['en'],{type:'region'}).of(c.code)||c.code;}catch{}
    const row=document.createElement('div');row.className='wc-country';row.setAttribute('aria-label',name+': '+number(c.views)+' page views');
    const img=document.createElement('img');img.src=flags+c.code.toLowerCase()+'.svg';img.alt='';img.width=28;img.height=20;img.onerror=()=>{img.hidden=true;};
    const text=document.createElement('span');text.textContent=name;const total=document.createElement('b');total.textContent=number(c.views);row.append(img,text,total);list.append(row);
   }
   if(!data.countries.length){const empty=document.createElement('p');empty.textContent='Country flags will appear when a country is recorded.';list.append(empty);}
   const u=box.querySelector('.wc-unknown');u.hidden=!data.unknownViews;u.textContent='Location unavailable: '+number(data.unknownViews||0)+' page views';
   box.querySelector('.wc-history').textContent=(data.firstRecordedDay?'Recorded since '+date(data.firstRecordedDay)+'. ':'')+'Improved aggregate counting from 12 Nov 2026; earlier totals include only statistics-enabled views.';
  }
  const time=data&&Number.isFinite(Date.parse(data.asOf))?new Date(data.asOf).toLocaleTimeString('en-GB',{hour:'2-digit',minute:'2-digit',second:'2-digit'}):'';
  status.textContent=readError?(data?'Could not refresh — showing the last fetched counts.':'Counts are temporarily unavailable. Try Refresh counts.'):(data?'Updated '+time+' · refreshes every 30 seconds':'Loading recorded counts…');
  if(recordError)status.textContent+=' This page could not be counted.';
  const state=box.querySelector('.wc-choice span');state.textContent=blocked?'Your browser privacy signal is respected; counting is off.':choice==='deny'?'Counting is paused for this browser.':'Aggregate counting is on. No tracking cookies or visitor IDs.';
  const button=box.querySelector('.wc-choice button');button.disabled=blocked;button.hidden=blocked;button.textContent=choice==='deny'?'Resume counting':'Pause counting';
  box.querySelector('.wc-refresh').disabled=requestPending;
 }}
 async function refresh(){const id=++readId;requestPending=true;render();const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),10000);
  try{const r=await fetch(service+'/api/public-summary?site=all',{credentials:'omit',cache:'no-store',referrerPolicy:'no-referrer',signal:controller.signal});const d=await r.json();if(!r.ok||!validData(d))throw Error();if(id===readId){data=d;readError=false;}}
  catch{if(id===readId)readError=true;}finally{clearTimeout(timer);if(id===readId){requestPending=false;render();}}
 }
 async function record(){if(blocked||choice==='deny'||document.visibilityState!=='visible'||!origins.includes(location.origin)||!slots().some(b=>b.dataset.counterDisabled!=='true'))return;
  const path=pagePath(location);if(/^\/(studio|api|publisher)(\/|$)/.test(path)||attempted.has(path))return;attempted.add(path);
  try{const r=await fetch(service+'/collect',{method:'POST',credentials:'omit',mode:'cors',keepalive:true,referrerPolicy:'no-referrer',headers:{'Content-Type':'text/plain'},body:JSON.stringify({mode:'aggregate',path})});if(!r.ok)throw Error();recordError=false;refresh();}catch{recordError=true;render();}
 }
 function mount(){if(!slots().length)return;render();notice();if(!data&&!requestPending)refresh();record();}
 window.addEventListener('inam-counter-mount',mount);
 window.addEventListener('storage',e=>{if([pref,'inam-visitor-statistics-v1','knowledge-visitor-statistics-v1'].includes(e.key)){choice=preference(storage);render();notice();record();}});
 document.addEventListener('visibilitychange',()=>{if(document.visibilityState==='visible'){refresh();record();}});
 setInterval(()=>{if(document.visibilityState==='visible'&&slots().length)refresh();},30000);
 mount();
})();
