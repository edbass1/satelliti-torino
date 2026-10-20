"""Prepara build/flags/ (una tantum, in locale): bandiere da flag-icons (MIT, github.com/lipis/flag-icons).
SVG piccoli (<=3 KB) restano SVG; quelli con stemmi complessi vengono rasterizzati in PNG 48x36 per tenere leggero l'HTML.
Uso: python3 make_flags.py /percorso/flag-icons/flags/4x3"""
import sys, os, asyncio, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from countries import C
SRC = sys.argv[1]; OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flags')
os.makedirs(OUT, exist_ok=True)
codes = sorted({v[0] for v in C.values()})
big = []
for c in codes:
    s = open(os.path.join(SRC, c + '.svg'), 'rb').read()
    if len(s) <= 3072: open(os.path.join(OUT, c + '.svg'), 'wb').write(s)
    else: big.append(c)
async def rast():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width':48,'height':36})
        for c in big:
            svg = base64.b64encode(open(os.path.join(SRC, c + '.svg'), 'rb').read()).decode()
            await pg.set_content(f'<html><body style="margin:0"><img src="data:image/svg+xml;base64,{svg}" style="width:48px;height:36px;display:block"></body></html>')
            await pg.wait_for_timeout(50)
            await pg.screenshot(path=os.path.join(OUT, c + '.png'), clip={'x':0,'y':0,'width':48,'height':36})
        await b.close()
asyncio.run(rast())
print(len(codes), 'bandiere,', len(big), 'rasterizzate')
