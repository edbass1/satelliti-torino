import asyncio, os
from playwright.async_api import async_playwright
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width':1440,'height':900})
        errs = []; pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: errs.append(m.text) if m.type=='error' else None)
        await pg.goto(f'file://{ROOT}/index.html'); await pg.evaluate('localStorage.clear()'); await pg.reload(); await pg.wait_for_timeout(500)
        r = {}
        cnt = lambda: pg.evaluate("document.querySelectorAll('#results .card').length")
        r['logos_gone'] = await pg.evaluate("document.querySelectorAll('#results .logo').length") == 0
        r['flags'] = await pg.evaluate("""(()=>{const f=[...document.querySelectorAll('#results .flag')]; if(!f.length) return 0;
           const ok=f.filter(x=>{const cs=getComputedStyle(x); return cs.backgroundImage.startsWith('url(') && x.getBoundingClientRect().width>20}); return ok.length===f.length ? f.length : -ok.length})()""")
        r['flag_title_it'] = await pg.evaluate("document.querySelector('#results .flg-it')?.title")
        r['globe'] = await pg.evaluate("document.querySelectorAll('#results .flg-none').length")
        r['lastupd'] = await pg.inner_text('#lastupd')
        r['chips'] = await pg.evaluate("[...document.querySelectorAll('#contsel .cont')].map(b=>b.textContent.trim())")
        r['hb_all'] = await cnt()
        await pg.click('[data-cont="Asia"]'); await pg.wait_for_timeout(200); r['hb_noAsia'] = await cnt()
        await pg.click('[data-cont="Africa"]'); await pg.wait_for_timeout(200); r['hb_noAsiaAfrica'] = await cnt()
        await pg.screenshot(path=f'{ROOT}/screens/opzione-1-continenti.png')
        await pg.reload(); await pg.wait_for_timeout(400); r['persist'] = await cnt() == r['hb_noAsiaAfrica']
        await pg.fill('#q', 'al jazeera'); await pg.wait_for_timeout(500); r['search_noAsia'] = await cnt()
        await pg.click('[data-cont="Asia"]'); await pg.wait_for_timeout(300); r['search_withAsia'] = await cnt()
        await pg.fill('#q', ''); await pg.wait_for_timeout(300)
        await pg.click('[data-view="news"]'); await pg.wait_for_timeout(300)
        r['news_types'] = await pg.evaluate("[...document.querySelectorAll('#n-type option')].map(o=>o.textContent)")
        r['news_labels'] = await pg.evaluate("[...new Set([...document.querySelectorAll('.evt')].map(e=>e.textContent.trim()))]")
        n1 = await pg.evaluate("document.querySelectorAll('.ev').length"); await pg.click('[data-cont="Non specificato"]'); await pg.wait_for_timeout(200)
        r['news_unk_off'] = (n1, await pg.evaluate("document.querySelectorAll('.ev').length"))
        await pg.click('[data-cont="Non specificato"]'); await pg.click('[data-cont="Africa"]'); await pg.wait_for_timeout(200)
        await pg.screenshot(path=f'{ROOT}/screens/opzione-1-novita.png')
        await pg.click('[data-view="pub"]'); await pg.wait_for_timeout(300)
        r['pub_rows_eu'] = await pg.evaluate("document.querySelectorAll('.pubrow').length")
        await pg.click('[data-cont="Europa"]'); await pg.wait_for_timeout(200)
        r['pub_rows_noeu'] = await pg.evaluate("document.querySelectorAll('.pubrow').length")
        await pg.click('[data-cont="Europa"]'); await pg.wait_for_timeout(200)
        await pg.screenshot(path=f'{ROOT}/screens/opzione-1-pubblici.png')
        await pg.click('[data-view="sat"]'); await pg.wait_for_timeout(300)
        f0 = await pg.evaluate("parseFloat(getComputedStyle(document.querySelector('#results .cn')).fontSize)")
        await pg.click('#fs-plus'); await pg.click('#fs-plus')
        r['font_up'] = (await pg.evaluate("parseFloat(getComputedStyle(document.querySelector('#results .cn')).fontSize)")) > f0*1.2
        await pg.click('#fs-reset')
        await pg.evaluate('scrollTo(0,3000)'); await pg.wait_for_timeout(700)
        r['totop'] = await pg.evaluate("getComputedStyle(document.getElementById('totop')).opacity") == '1'
        await pg.evaluate('scrollTo(0,0)'); await pg.wait_for_timeout(600)
        await pg.screenshot(path=f'{ROOT}/screens/opzione-1.png')
        await pg.set_viewport_size({'width':390,'height':844}); await pg.wait_for_timeout(300)
        await pg.screenshot(path=f'{ROOT}/screens/opzione-1-mobile.png')
        for k,v in r.items(): print(k, v)
        print('ERR', errs); await b.close()
asyncio.run(main())
