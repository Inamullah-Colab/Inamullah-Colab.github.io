(() => {
  'use strict';
  if (window.__inamInsightsLoaded) return;
  window.__inamInsightsLoaded = true;
  const key = 'inam-visitor-statistics-v1';
  const endpoint = 'https://inam-visitor-insights.boxywatermelon2.chatgpt.site/collect';
  const blocked = navigator.globalPrivacyControl === true || navigator.doNotTrack === '1';
  let choice = null;
  try { choice = localStorage.getItem(key); } catch { /* optional browser preference */ }
  let sent = false;
  function send() {
    if (sent || choice !== 'allow' || blocked || document.visibilityState !== 'visible' || location.origin !== 'https://inamullah-colab.github.io') return;
    sent = true;
    let referrer = '';
    try { referrer = document.referrer ? new URL(document.referrer).origin : ''; } catch { /* no referrer */ }
    const campaign = new URLSearchParams(location.search).get('utm_source') || '';
    fetch(endpoint, {method:'POST', credentials:'omit', mode:'cors', keepalive:true, headers:{'Content-Type':'text/plain'}, body:JSON.stringify({consent:true,path:location.pathname,referrer,campaign})}).catch(() => {});
  }
  const panel = document.createElement('section'); panel.className = 'visitor-choice'; panel.setAttribute('aria-labelledby','visitor-choice-title');
  panel.innerHTML = '<h2 id="visitor-choice-title">Help improve these resources?</h2><p>Allow optional statistics about the pages read, referring website and approximate country. No names or precise locations are collected. <a href="/privacy/">Privacy details</a></p><div><button type="button" data-choice="allow">Allow statistics</button><button type="button" data-choice="deny">No thanks</button></div>';
  const preferences = document.createElement('button'); preferences.type='button'; preferences.className='visitor-preferences'; preferences.textContent='Visitor statistics preferences';
  document.body.append(panel,preferences);
  panel.hidden = choice !== null || blocked;
  preferences.addEventListener('click', () => {
    if (blocked) { preferences.textContent = 'Statistics are off: your browser requests no tracking.'; return; }
    panel.hidden = false; panel.querySelector('button').focus();
  });
  panel.querySelectorAll('button').forEach(button => button.addEventListener('click', () => {
    choice = button.dataset.choice;
    try {localStorage.setItem(key,choice);} catch { /* applies on this page only */ }
    panel.hidden = true;
    preferences.textContent = choice === 'allow' ? 'Visitor statistics: allowed · Change' : 'Visitor statistics: off · Change';
    preferences.focus(); send();
  }));
  document.addEventListener('visibilitychange',send); send();
})();
