"""Optional browser-level smoke test. Uses in-memory page fixture because this
sandbox disallows Chromium navigation to localhost; this does not test actual
HTTP serving. Install with: pip install playwright && playwright install chromium
Run: python tests/test_ui.py
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'index.html').read_text(encoding='utf8').replace('<script type="module" src="./app.js" defer></script>','').replace('<link rel="stylesheet" href="./styles.css">','')
CSS=(ROOT/'styles.css').read_text(encoding='utf8')
JS=(ROOT/'ml.js').read_text(encoding='utf8').replace('export function predict','function predict')+'\n'+(ROOT/'app.js').read_text(encoding='utf8').replace("import {predict} from './ml.js';",'')
MODEL=(ROOT/'model/model.json').read_text(encoding='utf8')

def new_page(browser,width=1440,height=900):
    page=browser.new_page(viewport={'width':width,'height':height})
    errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
    page.set_content(HTML)
    page.add_style_tag(content=CSS)
    # Replace only the model fetch with local bundled bytes. In deployment this
    # is a standard fetch('./model/model.json') from the web server.
    page.evaluate('(s)=>{window.fetch=async()=>({ok:true,json:async()=>JSON.parse(s)})}',MODEL)
    page.add_script_tag(content=JS)
    page.locator('#score').wait_for(state='visible')
    return page,errors

def main():
    with sync_playwright() as playwright:
        b=playwright.chromium.launch(headless=True, executable_path="/usr/bin/chromium" if Path("/usr/bin/chromium").exists() else None, args=["--no-sandbox"])
        page,errors=new_page(b)
        assert page.locator('#model-status').inner_text()=='MODEL READY'
        assert int(page.locator('#score').inner_text())>=65
        assert page.locator('.evidence-item').count()>=3
        page.locator('[data-example="safe"]').click()
        assert int(page.locator('#score').inner_text())<43
        page.locator('[data-example="zh"]').click()
        assert page.locator('.evidence-item').count()>=3
        page.locator('#what-if').click()
        assert 'ML signal' in page.locator('#counterfactual').inner_text()
        mobile,errors_mobile=new_page(b,390,844)
        assert mobile.evaluate('document.documentElement.scrollWidth')<=390
        assert errors==[] and errors_mobile==[],(errors,errors_mobile)
        b.close()
    print('PASS: UI risk flows, bilingual evidence, what-if, responsive layout and no JS exceptions')

if __name__=='__main__':main()
