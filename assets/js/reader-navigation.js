/* Connect the separately built reader to the shared site navigation. */
(() => {
  const root = document.getElementById('reader-root');
  if (!root) return;
  const labels = {Blog:'Journal',Scholarships:'Scholarships',Jobs:'Jobs',Learning:'Learning','Medical research':'Medical research'};
  let searchApplied = false;
  function connect() {
    const section = new URLSearchParams(location.search).get('section');
    const index = /\/knowledge\/?$/.test(location.pathname);
    const filtered = Boolean(labels[section]) && index;
    document.body.classList.toggle('hub-index', index);
    document.body.classList.toggle('hub-filtered', filtered);
    const nav = root.querySelector('.header nav');
    if (nav) nav.setAttribute('aria-label', 'Knowledge & Opportunity sections');
    for (const button of root.querySelectorAll('.tabs button')) {
      if (button.textContent === 'Blog') button.textContent = 'Journal';
    }
    const title = root.querySelector('#explore .section-heading h2');
    if (title) {
      const text = filtered ? labels[section] : 'Good things to know.';
      if (title.textContent !== text) title.textContent = text;
      title.setAttribute('aria-level', filtered ? '1' : '2');
    }
    for (const link of root.querySelectorAll('footer a')) {
      if (link.textContent === 'Publisher sign-in') {link.href='/publisher/';link.textContent='Owner tools';}
    }
    const term = new URLSearchParams(location.search).get('search');
    const input = root.querySelector('input[aria-label="Search articles and opportunities"]');
    if (!searchApplied && term && input) {
      searchApplied = true;
      Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(input,term);
      input.dispatchEvent(new Event('input',{bubbles:true}));
    }
  }
  new MutationObserver(connect).observe(root,{childList:true,subtree:true});
  window.addEventListener('popstate',connect);
  connect();
})();
