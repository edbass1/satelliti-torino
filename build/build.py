import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(H, '..')
sys.path.insert(0, H); from themes import T
ch = json.load(open(os.path.join(ROOT, 'data/channels.json'))); nv = json.load(open(os.path.join(ROOT, 'data/novita.json')))
comp = [[c['nome'], c['pos'], c['paese'], c['genere'], c['lingue'], c['ris'], 2 if c['stato']=='parziale' else 1,
         1 if c['ricezione']=='difficile' else 0, c['nota'], [c['pubblico']['paese'], c['pubblico']['ente']] if c['pubblico'] else 0, c['key'], (c['bouquet'] or [''])[0]] for c in ch['canali']]
ev = [dict(d=e['data'], p=e['pos'], t=e['tipo'], n=e['nome'], c=e['paese'], b=e['bouquet'], r=e['ris'], il=e['in_lista']) for e in nv['eventi']]
data = dict(meta=ch['meta'], sats=ch['satelliti'], ch=comp, ev=ev)
DJ = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
base = open(os.path.join(H, 'base.css')).read(); core = open(os.path.join(H, 'core.js')).read()
for n, t in T.items():
    html = f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Satelliti da Torino · Opzione {n} – {t['title']}</title><meta name="color-scheme" content="dark">
<style>{base}{t['css']}</style></head><body data-view="sat">
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
open(os.path.join(ROOT, 'index.html'), 'w').write(idx)
print('ok', len(DJ)//1024, 'KB data')
