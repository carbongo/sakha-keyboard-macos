// copy buttons (labels come from data-* on <html>, per language)
const L = document.documentElement.dataset;
document.querySelectorAll('.copy').forEach(b => b.addEventListener('click', async () => {
  const t = document.getElementById(b.dataset.copy).textContent;
  const label = b.querySelector('span');
  try { await navigator.clipboard.writeText(t); label.textContent = L.copied; }
  catch { label.textContent = L.copyFail; }
  setTimeout(() => label.textContent = L.copy, 1600);
}));

// tabs
const tabs = [...document.querySelectorAll('.tab')];
function select(tab) {
  tabs.forEach(t => {
    const on = t === tab;
    t.setAttribute('aria-selected', on);
    t.tabIndex = on ? 0 : -1;
    document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
  });
}
tabs.forEach((t, i) => {
  t.addEventListener('click', () => select(t));
  t.addEventListener('keydown', e => {
    const d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
    if (d) { const n = tabs[(i + d + tabs.length) % tabs.length]; select(n); n.focus(); }
  });
});

// hero: keycaps press while words type out
const caps = Object.fromEntries([...document.querySelectorAll('.cap')].map(c => [c.dataset.k, c]));
const out = document.getElementById('typed');
const words = ['Дорообо!', 'Саха тыла', 'ҕ ҥ ө ү һ'];
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
const sleep = ms => new Promise(r => setTimeout(r, ms));
function press(ch) {
  const c = caps[ch.toLowerCase()];
  if (!c) return;
  c.classList.add('down');
  setTimeout(() => c.classList.remove('down'), 160);
}
Object.entries(caps).forEach(([k, c]) => c.addEventListener('click', () => { press(k); out.textContent += k; }));
(async function loop() {
  if (reduce) { out.textContent = words[0]; return; }
  for (let w = 0; ; w = (w + 1) % words.length) {
    out.textContent = '';
    for (const ch of words[w]) { press(ch); out.textContent += ch; await sleep(ch === ' ' ? 90 : 140); }
    await sleep(1800);
    while (out.textContent) { out.textContent = out.textContent.slice(0, -1); await sleep(35); }
    await sleep(300);
  }
})();

// live version from the latest release
fetch('https://api.github.com/repos/carbongo/sakha-keyboard-macos/releases/latest')
  .then(r => r.ok ? r.json() : null).then(j => { if (j && j.tag_name) document.getElementById('ver').textContent = j.tag_name; })
  .catch(() => {});
