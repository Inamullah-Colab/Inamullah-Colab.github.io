(() => {
  'use strict';
  const now = new Date();
  const parts = new Intl.DateTimeFormat('en-GB', {timeZone:'Europe/London', year:'numeric', month:'2-digit', day:'2-digit'}).formatToParts(now);
  const part = type => Number(parts.find(p => p.type === type).value);
  const today = Date.UTC(part('year'), part('month') - 1, part('day'));
  document.querySelectorAll('[data-phd-deadline]').forEach(card => {
    const label = card.querySelector('[data-phd-status-label]');
    if (!label) return;
    const date = card.dataset.phdDeadline;
    const days = /^\d{4}-\d{2}-\d{2}$/.test(date) ? Math.round((Date.parse(date + 'T00:00:00Z') - today) / 86400000) : null;
    const exact = card.dataset.phdInstant ? Date.parse(card.dataset.phdInstant) : NaN;
    if (card.dataset.phdStatus === 'unverified') {
      card.classList.add('is-unverified');
      label.textContent = days !== null && days < 0 ? 'Advert date passed · confirm' : 'Confirm details';
      return;
    }
    if (card.dataset.phdKind === 'rolling') {
      label.textContent = 'Rolling · confirm availability';
      return;
    }
    if (days === null) return;
    if (days < 0 || (Number.isFinite(exact) && now.getTime() >= exact)) {
      card.classList.add('is-closed'); label.textContent = 'Deadline passed';
    } else if (days <= 7) {
      card.classList.add('is-urgent');
      label.textContent = days === 0 ? 'Closes today' : days === 1 ? 'Closes tomorrow' : 'Closes in ' + days + ' days';
    } else {
      const age = Math.floor((today - Date.parse(card.dataset.phdChecked + 'T00:00:00Z')) / 86400000);
      label.textContent = age > 14 ? 'Recheck availability' : 'Listed at last check';
    }
  });
})();
