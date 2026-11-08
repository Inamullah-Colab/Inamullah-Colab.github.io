(() => {
  'use strict';
  const form = document.getElementById('hub-filter-form');
  if (form) {
    const search = document.getElementById('hub-search');
    const category = document.getElementById('hub-category');
    const cards = Array.from(document.querySelectorAll('.hub-card'));
    const params = new URLSearchParams(location.search);
    search.value = params.get('search') || '';
    if (Array.from(category.options).some(o => o.value === params.get('category'))) category.value = params.get('category');
    function filter(updateURL = true) {
      const words = search.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
      let count = 0;
      for (const card of cards) {
        const visible = (category.value === 'all' || card.dataset.topic === category.value) && words.every(w => card.textContent.toLowerCase().includes(w));
        card.hidden = !visible;
        if (visible) count++;
      }
      document.getElementById('hub-results').textContent = count + (count === 1 ? ' article' : ' articles') + ' found';
      document.getElementById('hub-empty').hidden = count > 0;
      if (updateURL) {
        const url = new URL(location.href);
        url.searchParams.delete('search'); url.searchParams.delete('category');
        if (search.value.trim()) url.searchParams.set('search', search.value.trim());
        if (category.value !== 'all') url.searchParams.set('category', category.value);
        history.replaceState(null, '', url);
      }
    }
    form.addEventListener('submit', e => {e.preventDefault();filter();});
    form.addEventListener('reset', () => {setTimeout(filter, 0);});
    search.addEventListener('input', () => filter()); category.addEventListener('change', () => filter()); filter(false);
  }
  document.getElementById('copy-article-link')?.addEventListener('click', async () => {
    const url = document.querySelector('link[rel="canonical"]')?.href || location.origin + location.pathname;
    const status = document.getElementById('copy-status');
    try { await navigator.clipboard.writeText(url); status.textContent = 'Article link copied.'; }
    catch { status.textContent = 'Copy this link: ' + url; }
  });
})();
