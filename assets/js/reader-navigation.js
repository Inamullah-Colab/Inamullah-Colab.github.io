/* Connect the separately built reader to the shared site navigation. */
(() => {
  const root = document.getElementById('reader-root');
  if (!root) return;
  const labels = {Blog:'Blog',Scholarships:'Scholarships',Jobs:'Jobs',Learning:'Learning','Medical research':'Medical research'};
  let searchApplied = false;
  function connect() {
    const section = new URLSearchParams(location.search).get('section');
    const index = /\/knowledge\/?$/.test(location.pathname);
    const filtered = Boolean(labels[section]) && index;
    document.body.classList.toggle('hub-index', index);
    document.body.classList.toggle('hub-filtered', filtered);
    const readershipHeading = root.querySelector('#readership-heading');
    if (readershipHeading && readershipHeading.textContent !== 'Visitors Around the World') readershipHeading.textContent = 'Visitors Around the World';
    const counterLabels = ['Page views:', 'Countries:', 'Today (UTC):'];
    root.querySelectorAll('.readership-totals > div > span').forEach((label, i) => {
      if (counterLabels[i] && label.textContent !== counterLabels[i]) label.textContent = counterLabels[i];
    });
    const counterNote = root.querySelector('.readership-footer > p:not([role])');
    const note = 'All recorded history · Statistics-enabled page views, not unique people.';
    if (counterNote && counterNote.textContent !== note) counterNote.textContent = note;
    const nav = root.querySelector('.header nav');
    if (nav) {
      nav.setAttribute('aria-label', 'Knowledge & Opportunity sections');
      const blog = nav.querySelector('a[href$="?section=Blog"]');
      if (blog && blog.textContent !== 'Blog') blog.textContent = 'Blog';
    }
    const heroTitle = root.querySelector('.hero-copy h1');
    if (heroTitle && heroTitle.textContent !== 'Knowledge & Opportunity') heroTitle.textContent = 'Knowledge & Opportunity';
    const heroCopy = root.querySelector('.hero-copy');
    if (heroCopy && !heroCopy.querySelector('.science-quote')) {
      const source = 'https://blog.oup.com/2018/07/newtons-laws-discovery/';
      const quote = document.createElement('figure');
      quote.className = 'science-quote';
      const words = document.createElement('blockquote');
      words.cite = source;
      words.textContent = '“If I have seen further it is by standing on the shoulders of Giants.”';
      const caption = document.createElement('figcaption');
      const attribution = document.createElement('a');
      attribution.href = source;
      attribution.textContent = 'Isaac Newton';
      attribution.setAttribute('aria-label', 'Isaac Newton — quotation source at Oxford University Press');
      caption.append(attribution);
      quote.append(words, caption);
      heroCopy.append(quote);
    }
    const eyebrow = root.querySelector('#explore .section-heading .eyebrow');
    if (eyebrow && eyebrow.textContent !== 'Blog & resources') {
      eyebrow.textContent = 'Blog & resources';
    }
    const title = root.querySelector('#explore .section-heading h2');
    if (title) {
      const text = filtered ? labels[section] : 'Latest posts & opportunities';
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
  new MutationObserver(connect).observe(root,{childList:true,subtree:true,attributes:true,attributeFilter:['aria-pressed']});
  window.addEventListener('popstate',connect);
  connect();
})();
