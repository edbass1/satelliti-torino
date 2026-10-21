import asyncio, os, sys
from playwright.async_api import async_playwright
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
async def launch(p):
    try: return await p.chromium.launch()
    except Exception: return await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--headless=new'])
async def main():
    async with async_playwright() as p:
        b = await launch(p)
        ok = True
        for n in range(1, 8):
            pg = await b.new_page(viewport={'width':1440,'height':900})
            errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.on('console', lambda m: errs.append(m.text) if m.type=='error' else None)
            await pg.goto(f'file://{ROOT}/opzione-{n}.html'); await pg.wait_for_timeout(500)
            r = {}
            cnt = lambda: pg.evaluate("document.querySelectorAll('#results .card,#results .tile,#results .row').length")
            r['13E'] = await cnt()
            await pg.evaluate("localStorage.clear()")
            fsz = lambda: pg.evaluate("parseFloat(getComputedStyle(document.querySelector('#results .cn')).fontSize)")
            f0 = await fsz(); await pg.click('#fs-plus'); await pg.click('#fs-plus'); f2 = await fsz()
            await pg.click('#fs-minus'); await pg.click('#fs-minus'); await pg.click('#fs-minus'); fm = await fsz()
            await pg.click('#fs-reset'); fr = await fsz()
            r['font'] = f2 > f0 * 1.2 and fm < f0 and abs(fr - f0) < .1
            await pg.click('#fs-plus'); await pg.reload(); await pg.wait_for_timeout(400)
            r['font_persist'] = abs(await fsz() - f0*1.1) < .3 and (await pg.inner_text('#fs-val')).strip()=='110%'
            await pg.click('#fs-reset')
            vis = lambda: pg.evaluate("getComputedStyle(document.getElementById('totop')).opacity")
            r['totop_hidden_at_top'] = float(await vis()) == 0
            await pg.evaluate("window.scrollTo(0, 3000)"); await pg.wait_for_timeout(700)
            r['totop_visible'] = float(await vis()) == 1
            await pg.screenshot(path=f'{ROOT}/screens/opzione-{n}-scroll.png')
            await pg.click('#totop'); await pg.wait_for_timeout(1500)
            r['totop_scrolls'] = (await pg.evaluate("scrollY")) < 5
            await pg.screenshot(path=f'{ROOT}/screens/opzione-{n}.png')
            # cambia satellite via API comune (equivalente al click) + click reale su un selettore
            el = await pg.query_selector('[data-sat="19.2E"]')
            if el and await el.is_visible(): await el.click()
            else: await pg.evaluate("SATAPP.setSat('19.2E')")
            await pg.wait_for_timeout(200); r['19.2E'] = await cnt()
            await pg.select_option('#f-genre', 'Notizie'); await pg.wait_for_timeout(200); r['genre_news'] = await cnt()
            await pg.select_option('#f-lang', 'Inglese'); await pg.wait_for_timeout(200); r['news_eng'] = await cnt()
            await pg.click('#f-reset'); await pg.wait_for_timeout(200)
            await pg.fill('#q', 'france 24'); await pg.wait_for_timeout(500); r['search_france24'] = await cnt()
            await pg.fill('#q', ''); await pg.wait_for_timeout(400)
            await pg.click('[data-view="pub"]'); await pg.wait_for_timeout(300)
            await pg.fill('#pub-text', 'francesi'); await pg.wait_for_timeout(300)
            r['pub_fr_rows'] = await pg.evaluate("document.querySelectorAll('#results .pubrow').length")
            r['pub_fr_badges'] = await pg.evaluate("document.querySelectorAll('#results .sbdg').length")
            await pg.screenshot(path=f'{ROOT}/screens/opzione-{n}-pubblici.png')
            await pg.click('[data-view="news"]'); await pg.wait_for_timeout(300)
            r['news_all'] = await pg.evaluate("document.querySelectorAll('#results .ev').length")
            await pg.click('[data-nsat="13E"]'); await pg.wait_for_timeout(200)
            r['news_13E'] = await pg.evaluate("document.querySelectorAll('#results .ev').length")
            await pg.screenshot(path=f'{ROOT}/screens/opzione-{n}-novita.png')
            await pg.set_viewport_size({'width':390,'height':844}); await pg.click('[data-view="sat"]'); await pg.wait_for_timeout(300)
            await pg.evaluate("window.scrollTo(0, 2500)"); await pg.wait_for_timeout(700)
            r['mobile_no_overlap'] = await pg.evaluate('''(()=>{const a=document.getElementById('fontctl').getBoundingClientRect(),b=document.getElementById('totop').getBoundingClientRect();
              const fl=getComputedStyle(document.getElementById('fontctl')).position==='fixed'; if(!fl) return true; return a.bottom<=b.top||b.bottom<=a.top||a.right<=b.left||b.right<=a.left;})()''')
            await pg.screenshot(path=f'{ROOT}/screens/opzione-{n}-mobile-scroll.png')
            await pg.evaluate("window.scrollTo(0, 0)"); await pg.wait_for_timeout(500)
            await pg.screenshot(path=f'{ROOT}/screens/opzione-{n}-mobile.png')
            print(n, r, 'ERR:' , errs)
            if errs or not all(r.values()): ok = False
            await pg.close()
        await b.close(); print('ALL OK' if ok else 'PROBLEMS')
asyncio.run(main())
