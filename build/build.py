import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(H, '..')
sys.path.insert(0, H); from themes import T
from countries import info as cinfo
import base64, glob
ch = json.load(open(os.path.join(ROOT, 'data/channels.json'))); nv = json.load(open(os.path.join(ROOT, 'data/novita.json')))
comp = [[c['nome'], c['pos'], c['paese'], c['genere'], c['lingue'], c['ris'], 2 if c['stato']=='parziale' else 1,
         1 if c['ricezione']=='difficile' else 0, c['nota'], [c['pubblico']['paese'], c['pubblico']['ente']] if c['pubblico'] else 0, c['key'], (c['bouquet'] or [''])[0], cinfo(c['paese'])[0] or '', cinfo(c['paese'])[1], c.get('ms',''), c.get('isi'), c.get('pls','')] for c in ch['canali']]
ev = [dict(d=e['data'], p=e['pos'], t=e['tipo'], n=e['nome'], c=e['paese'], b=e['bouquet'], r=e['ris'], il=e['in_lista'], ch=e.get('chiuso', False), iso=cinfo(e['paese'])[0] or '', co=cinfo(e['paese'])[1]) for e in nv['eventi']]
data = dict(meta=ch['meta'], sats=ch['satelliti'], ch=comp, ev=ev)
DJ = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
base = open(os.path.join(H, 'base.css')).read(); core = open(os.path.join(H, 'core.js')).read()
# bandiere: solo quelle dei paesi presenti nei dati, come classi CSS con data URI (file autonomo)
used = sorted({x[12] for x in comp if x[12]} | {e['iso'] for e in ev if e['iso']})
FL = os.path.join(H, 'flags'); fcss = []
for iso in used:
    for ext, mime in (('svg', 'image/svg+xml'), ('png', 'image/png')):
        p = os.path.join(FL, iso + '.' + ext)
        if os.path.exists(p):
            fcss.append('.flg-%s{background-image:url(data:%s;base64,%s)}' % (iso, mime, base64.b64encode(open(p, 'rb').read()).decode())); break
GLOBE = "data:image/svg+xml;base64," + base64.b64encode(b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 18"><rect width="24" height="18" rx="2" fill="#1f2937"/><g fill="none" stroke="#9ca3af" stroke-width="1.2"><circle cx="12" cy="9" r="6.5"/><ellipse cx="12" cy="9" rx="2.8" ry="6.5"/><path d="M5.5 9h13M6.6 5.6h10.8M6.6 12.4h10.8"/></g></svg>').decode()
FLAGCSS = ('.flag{display:inline-block;flex:none;width:calc(30px * var(--fs,1));height:calc(22.5px * var(--fs,1));border-radius:4px;background:#222 center/cover no-repeat;box-shadow:0 0 0 1px rgba(255,255,255,.14)}'
           '.flag.sm{width:28px;height:21px}.flag.xs{width:22px;height:16.5px;border-radius:3px}.flg-none{background-image:url(%s)}' % GLOBE) + ''.join(fcss)
for n, t in T.items():
    html = f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Satelliti da Torino · Opzione {n} – {t['title']}</title><meta name="color-scheme" content="dark">
<style>{base}{FLAGCSS if t.get('flags') else ''}{t['css']}</style></head><body data-view="sat">
{t['body']}
<script>window.SATDATA={DJ};</script>
<script>{t['js']}</script>
<script>{core}</script></body></html>'''
    open(os.path.join(ROOT, f'opzione-{n}.html'), 'w').write(html)
cards = ''.join(f'''<a class="o" href="opzione-{n}.html"><img src="screens/opzione-{n}.png" alt="" onerror="this.style.display='none'"><div><span>Opzione {n}</span><h2>{t['title']}</h2><p>{t['desc']}</p></div></a>''' for n, t in T.items())
idx = f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Satelliti da Torino · 7 opzioni di design</title>
<style>body{{margin:0;background:#000;color:#eee;font-family:system-ui,sans-serif}}main{{max-width:1200px;margin:auto;padding:40px 22px}}h1{{font-size:40px;margin:0}}.sub{{color:#999}}
.g{{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:18px;margin-top:28px}}.o{{text-decoration:none;color:inherit;background:#0e0e0e;border:1px solid #222;border-radius:18px;overflow:hidden;transition:.15s}}
.o:hover{{border-color:#8ab4ff;transform:translateY(-3px)}}.o img{{width:100%;aspect-ratio:16/10;object-fit:cover;object-position:top;display:block;border-bottom:1px solid #222}}.o div{{padding:14px 16px 18px}}.o span{{color:#8ab4ff;font-size:12px;text-transform:uppercase;letter-spacing:.1em}}.o h2{{margin:4px 0 6px}}.o p{{margin:0;color:#aaa;font-size:14px;line-height:1.45}}
footer{{color:#777;font-size:12.5px;margin-top:30px;line-height:1.6}}</style></head><body><main><h1>Satelliti da Torino</h1>
<p class="sub">7 versioni dello stesso sito (stessi dati, stesse funzioni): scegli quella che ti piace di più. Ogni file funziona anche offline con doppio clic.</p>
<div class="g">{cards}</div><footer>Dati: {ch['meta']['fonte']} · aggiornati il {ch['meta']['aggiornato']} · {len(comp)} presenze di canali TV in chiaro/parzialmente in chiaro su {len(ch['satelliti'])} posizioni orbitali · {len(ev)} novità.<br>
Per aggiornare i dati: <code>python3 scraper/scrape.py && python3 build/build.py</code></footer></main></body></html>'''
open(os.path.join(ROOT, 'scelta-versioni.html'), 'w').write(idx)
# la versione scelta dall'utente (Minimal, opzione 1) è la homepage
import shutil; shutil.copyfile(os.path.join(ROOT, 'opzione-1.html'), os.path.join(ROOT, 'index.html'))
print('ok', len(DJ)//1024, 'KB data')
