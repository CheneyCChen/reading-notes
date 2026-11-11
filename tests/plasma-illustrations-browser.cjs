const {chromium}=require('playwright'),assert=require('node:assert/strict'),path=require('node:path');
(async()=>{
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||undefined,headless:true,args:['--no-sandbox']});
const page=await browser.newPage({viewport:{width:1440,height:1000}}),errors=[];
page.on('pageerror',e=>errors.push(e.message));
await page.goto((process.env.BASE_URL||'http://localhost:8766')+'/reports/plasma-lectures/index.html');
await page.evaluate(()=>document.fonts.ready);
assert.equal(await page.locator('.plasma-illustration').count(),8);
// Force all lectures visible only for complete geometry checks; navigation is covered by course tests.
await page.addStyleTag({content:'.lecture,.study-section{display:block!important}.topbar{visibility:hidden!important}'});
for(const theme of ['light','dark']){
 await page.evaluate(t=>document.documentElement.dataset.theme=t,theme);
 for(const width of [1440,390,320]){
  await page.setViewportSize({width,height:1000});
  for(const fig of await page.locator('.plasma-illustration').all()){
   await fig.scrollIntoViewIfNeeded();
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
   assert(await fig.locator('svg').isVisible());
   const problems=await fig.locator('svg').evaluate(svg=>[...svg.querySelectorAll('text')].filter(t=>{let b=t.getBBox();return b.x<0||b.y<0||b.x+b.width>600||b.y+b.height>330}).map(t=>t.textContent));
   assert.deepEqual(problems,[]);
   if(width===1440)await fig.screenshot({path:path.join(process.env.QA_DIR||'/tmp',`plasma-lecture-diagram-${await fig.getAttribute('id')}-${theme}.png`)});
  }
 }
}
assert.deepEqual(errors,[]);await browser.close();console.log('PASS 8 diagrams in light/dark at 1440/390/320, bounded SVG labels, no viewport overflow or JS errors.');
})();
