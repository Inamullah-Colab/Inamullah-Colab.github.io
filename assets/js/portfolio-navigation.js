(() => {
  const button = document.querySelector('.menu-toggle');
  const nav = document.getElementById('main-navigation');
  if (!button || !nav) return;
  button.hidden = false;
  document.documentElement.classList.add('enhanced-navigation');
  const close = () => {button.setAttribute('aria-expanded', 'false'); nav.classList.remove('is-open');};
  button.addEventListener('click', () => {const open = button.getAttribute('aria-expanded') !== 'true'; button.setAttribute('aria-expanded', String(open)); nav.classList.toggle('is-open', open);});
  nav.addEventListener('click', event => {if (event.target.closest('a')) close();});
  document.addEventListener('keydown', event => {if (event.key === 'Escape' && button.getAttribute('aria-expanded') === 'true') {close(); button.focus();}});
})();
