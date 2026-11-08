(() => {
  'use strict';
  document.getElementById('new-post-form').addEventListener('submit', event => {
    event.preventDefault();
    const title = document.getElementById('post-title').value.trim();
    const description = document.getElementById('post-description').value.trim();
    if (!title || !description) return;
    const date = new Date().toISOString().slice(0,10);
    const slug = title.toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'').slice(0,90) || 'new-article';
    const topic = document.getElementById('post-topic').value;
    const body = ['---','layout: hub-article','title: '+JSON.stringify(title),'description: '+JSON.stringify(description),'date: '+date,'permalink: /blog/'+slug+'/','hub_category: '+JSON.stringify(topic),'published: false','comments: false','---','','Write your introduction here.','','## What readers need to know','','Explain the main idea in your own words.','','## Practical next steps','','Add a clear example or an application checklist.','','## Sources','','- [Official source title](https://example.com) — checked '+date+'.','','For an opportunity notice, state its deadline, eligibility, funding coverage and official application link. Remove this instruction before publishing.',''].join('\n');
    const url = new URL('https://github.com/Inamullah-Colab/Inamullah-Colab.github.io/new/master');
    url.searchParams.set('filename','_posts/'+date+'-'+slug+'.md');url.searchParams.set('value',body);
    location.assign(url.href);
  });
  let share = '';
  document.getElementById('share-link-form').addEventListener('submit', event => {
    event.preventDefault();const out=document.getElementById('share-result');
    try {
      const url=new URL(document.getElementById('share-url').value);
      if(url.origin!=='https://inamullah-colab.github.io') throw new Error('Use an article address from your GitHub website.');
      url.searchParams.set('utm_source',document.getElementById('share-source').value);share=url.href;out.textContent=share;document.getElementById('copy-share-link').hidden=false;
    } catch {out.textContent='Enter a valid https://inamullah-colab.github.io/ article address.';share='';document.getElementById('copy-share-link').hidden=true;}
  });
  document.getElementById('copy-share-link').addEventListener('click',async()=>{try{await navigator.clipboard.writeText(share);document.getElementById('copy-share-link').textContent='Copied';}catch{document.getElementById('copy-share-link').textContent='Select and copy the link above';}});
})();
