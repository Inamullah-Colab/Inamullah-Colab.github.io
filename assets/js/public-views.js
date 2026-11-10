/* Public aggregate counts from the existing visitor statistics service. */
(() => {
  'use strict';
  const boxes = document.querySelectorAll('.public-views');
  if (!boxes.length) return;
  fetch('https://inam-visitor-insights.boxywatermelon2.chatgpt.site/api/public-summary?site=github', {
    credentials: 'omit', cache: 'no-store'
  }).then(response => {
    if (!response.ok) throw new Error('Statistics request failed');
    return response.json();
  }).then(data => {
    if (!['total', 'today', 'countryCount'].every(key => Number.isSafeInteger(data[key]) && data[key] >= 0) || !Array.isArray(data.countries)) throw new Error('Invalid statistics');
    for (const box of boxes) {
      box.querySelector('[data-public-total]').textContent = data.total.toLocaleString();
      box.querySelector('[data-public-today]').textContent = data.today.toLocaleString();
      box.querySelector('[data-public-countries]').textContent = data.countryCount.toLocaleString();
      const period = box.querySelector('.counter-period');
      if (period && /^\d{4}-\d{2}-\d{2}$/.test(data.firstRecordedDay || '')) {
        const since = new Date(data.firstRecordedDay + 'T00:00:00Z').toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric', timeZone: 'UTC' });
        period.textContent = 'All recorded history · Since ' + since;
      }
      const list = box.querySelector('[data-public-country-list]');
      list.replaceChildren();
      for (const country of data.countries) {
        if (!/^[A-Z]{2}$/.test(country.code) || !Number.isSafeInteger(country.views) || country.views < 0) continue;
        let name = country.code;
        try { name = new Intl.DisplayNames(['en'], {type: 'region'}).of(country.code) || country.code; } catch { /* Use the code. */ }
        const item = document.createElement('span');
        item.dataset.country = country.code;
        item.title = name;
        item.setAttribute('aria-label', name + ': ' + country.views.toLocaleString() + ' page views');
        item.append(country.code + ' ');
        const count = document.createElement('b');
        count.textContent = country.views.toLocaleString();
        item.append(count);
        list.append(item);
      }
      if (!list.children.length) {
        const empty = document.createElement('span');
        empty.className = 'counter-empty';
        empty.textContent = 'No countries recorded yet.';
        list.append(empty);
      }
      const unknown = box.querySelector('[data-public-unknown]');
      if (Number.isSafeInteger(data.unknownViews) && data.unknownViews > 0) {
        unknown.textContent = 'Unknown location: ' + data.unknownViews.toLocaleString() + ' page views.';
        unknown.hidden = false;
      }
    }
  }).catch(() => {
    for (const box of boxes) {
      box.querySelector('[data-public-total]').textContent = 'Unavailable';
      box.querySelector('[data-public-error]').hidden = false;
    }
  });
})();
