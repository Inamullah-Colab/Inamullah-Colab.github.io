/* Deadline labels only; actual opening status is reviewed against employer adverts. */
(() => {
  'use strict';
  const parts = new Intl.DateTimeFormat('en-GB', {timeZone:'Europe/London',year:'numeric',month:'2-digit',day:'2-digit'}).formatToParts(new Date());
  const value = type => parts.find(p => p.type === type).value;
  const today = Date.UTC(Number(value('year')),Number(value('month'))-1,Number(value('day')));
  document.querySelectorAll('[data-job-deadline]').forEach(card => {
    const label = card.querySelector('[data-job-status-label]');
    if (!label) return;
    if (card.dataset.jobStatus === 'closed') {card.classList.add('is-closed');label.textContent='Closed';return;}
    if (!/^\d{4}-\d{2}-\d{2}$/.test(card.dataset.jobDeadline)) return;
    const days = Math.round((Date.parse(card.dataset.jobDeadline+'T00:00:00Z')-today)/86400000);
    if (days < 0) {card.classList.add('is-closed');label.textContent='Deadline passed';}
    else if (card.dataset.jobStatus === 'unverified') {label.textContent='Needs recheck';}
    else if (days <= 7) {card.classList.add('is-urgent');label.textContent=days===0?'Closes today':days===1?'Closes tomorrow':'Closes in '+days+' days';}
  });
})();
