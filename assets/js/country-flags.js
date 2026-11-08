/* Locally hosted flag-icons SVGs; attribution in /assets/flags/README.md. */
(() => {
  'use strict';
  const codes = 'AD AE AF AG AI AL AM AO AQ AR AS AT AU AW AX AZ BA BB BD BE BF BG BH BI BJ BL BM BN BO BQ BR BS BT BV BW BY BZ CA CC CD CF CG CH CI CK CL CM CN CO CP CR CU CV CW CX CY CZ DE DG DJ DK DM DO DZ EC EE EG EH ER ES ET EU FI FJ FK FM FO FR GA GB GD GE GF GG GH GI GL GM GN GP GQ GR GS GT GU GW GY HK HM HN HR HT HU IC ID IE IL IM IN IO IQ IR IS IT JE JM JO JP KE KG KH KI KM KN KP KR KW KY KZ LA LB LC LI LK LR LS LT LU LV LY MA MC MD ME MF MG MH MK ML MM MN MO MP MQ MR MS MT MU MV MW MX MY MZ NA NC NE NF NG NI NL NO NP NR NU NZ OM PA PC PE PF PG PH PK PL PM PN PR PS PT PW PY QA RE RO RS RU RW SA SB SC SD SE SG SH SI SJ SK SL SM SN SO SR SS ST SV SX SY SZ TC TD TF TG TH TJ TK TL TM TN TO TR TT TV TW TZ UA UG UM UN US UY UZ VA VC VE VG VI VN VU WF WS XK XX YE YT ZA ZM ZW'.split(' ');
  const supported = new Set(codes);
  const names = new Map(codes.map(code => [code, code]));
  try {
    const regions = new Intl.DisplayNames(['en'], {type: 'region'});
    for (const code of codes) names.set(regions.of(code), code);
  } catch { /* Country codes remain a usable fallback. */ }
  function decorate() {
    for (const item of document.querySelectorAll('.public-country-list > span, .readership-countries > span')) {
      const label = [...item.childNodes].filter(node => node.nodeType === Node.TEXT_NODE)
        .map(node => node.textContent).join('').split(' · ')[0].trim();
      const code = item.dataset.country || names.get(label);
      if (!supported.has(code) || item.querySelector('.country-flag')) continue;
      const flag = document.createElement('img');
      flag.className = 'country-flag';
      flag.src = '/assets/flags/' + code.toLowerCase() + '.svg';
      flag.alt = ''; // The adjacent country name supplies the accessible label.
      flag.width = 24;
      flag.height = 18;
      flag.loading = 'lazy';
      flag.decoding = 'async';
      flag.addEventListener('error', () => { flag.hidden = true; }, {once: true});
      item.prepend(flag);
    }
  }
  new MutationObserver(decorate).observe(document.body, {childList: true, subtree: true});
  decorate();
})();
