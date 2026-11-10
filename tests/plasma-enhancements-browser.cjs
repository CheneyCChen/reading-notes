/* Course map and added derivations: desktop/mobile, filters, math and no-JS. */
const {chromium}=require('playwright'),assert=require('node:assert/strict'),path=require('node:path'),fs=require('node:fs');
const base=process.env.BASE_URL||'http://localhost:8766';
const courseUrl=base.replace(/\/$/,'')+'/reports/plasma-lectures/index.html';
const output=process.env.QA_DIR||'/tmp';
fs.mkdirSync(output,{recursive:true});
// Component screenshots omit sticky site chrome; functional checks keep it intact.
const captureStyle='.topbar{visibility:hidden!important}';
async function waitForScrollIdle(page){
 let last=null,stable=0;
 for(let i=0;i<100;i++){
  const y=await page.evaluate(()=>scrollY);
  stable=y===last?stable+1:0;if(stable===3)return;last=y;
  await new Promise(resolve=>setTimeout(resolve,100));
 }
 throw Error('Anchor scrolling did not settle');
}
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||undefined,headless:true,args:['--no-sandbox']});
 const page=await browser.newPage({viewport:{width:1440,height:1100}}),errors=[],external=[];
 page.on('pageerror',e=>errors.push(e.message));page.on('request',r=>{if(/^https?:/.test(r.url())&&!r.url().startsWith(base))external.push(r.url())});
 await page.goto(courseUrl);await page.evaluate(()=>document.fonts.ready);
 assert.equal(await page.locator('.course-map-node').count(),7);
 assert.equal(await page.locator('.course-map-edge').count(),8);
 assert.equal(await page.locator('.derivation-supplement').count(),17);
 assert.equal(await page.locator('.derivation-details').count(),3);
 assert.equal(await page.locator('.derivation-supplement .katex').count(),266);
 assert.equal(await page.locator('.katex-error').count(),0);
 assert.equal(await page.locator('.quiz details').count(),63);
 await page.locator('#course-map').screenshot({style:captureStyle,path:path.join(output,'plasma-map-desktop.png')});
 // The native link clears stale filters/search before scrolling to its target.
 await page.locator('[data-filter="2"]').click();await page.locator('#search').fill('no-such-term-00');
 await page.locator('.course-map-node-7').click();
 assert.equal(new URL(page.url()).hash,'#lecture7');assert.equal(await page.locator('#search').inputValue(),'');
 assert.equal(await page.locator('.lecture:visible').count(),7);
 await page.goBack();await page.goForward();assert.equal(new URL(page.url()).hash,'#lecture7');
 // Keyboard activation retains browser-native fragment navigation.
 await page.locator('.course-map-node-3').focus();await page.keyboard.press('Enter');
 assert.equal(new URL(page.url()).hash,'#lecture3');
 // Cross-lecture links work when only their originating lecture is visible.
 for(const link of await page.locator('.supplement-crosslinks a').all()){
  const origin=await link.evaluate(el=>el.closest('.lecture').dataset.lecture);
  const target=await link.getAttribute('href');
  await page.locator(`[data-filter="${origin}"]`).click();await link.click();
  assert.equal(new URL(page.url()).hash,target);assert(await page.locator(target).isVisible());
  assert.equal(await page.locator('.lecture:visible').count(),7);
 }
 console.log('PASS: map/filter/history/keyboard and all six cross-links.');
 // Every native disclosure can repeatedly open and close; all derivation steps remain.
 for(const details of await page.locator('.derivation-details').all()){
  for(let repeat=0;repeat<2;repeat++){
   await details.locator('summary').click();assert(await details.evaluate(el=>el.open));
   assert(await details.locator('.derivation-equation').first().isVisible());
   await details.locator('summary').click();assert(!(await details.evaluate(el=>el.open)));
  }
 }
 for(const width of [390,320]){
  await page.setViewportSize({width,height:844});
  await page.locator('#course-map').scrollIntoViewIfNeeded();
  assert.equal(await page.locator('.course-map-network').evaluate(el=>getComputedStyle(el).display),'flex');
  assert(await page.locator('.course-map-dependency').first().isVisible());
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
  await page.locator('#course-map').screenshot({style:captureStyle,path:path.join(output,`plasma-map-${width}.png`)});
  for(const details of await page.locator('.derivation-details').all()){
   if(!(await details.evaluate(el=>el.open)))await details.locator('summary').click();
  }
  for(const supplement of await page.locator('.derivation-supplement').all()){
   await supplement.scrollIntoViewIfNeeded();
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),`Page overflow ${width} ${await supplement.getAttribute('id')}`);
  }
  const scrollable=await page.locator('.derivation-equation').evaluateAll(elements=>elements.filter(el=>el.scrollWidth>el.clientWidth+1).map(el=>{el.scrollLeft=15;const moved=el.scrollLeft>0;el.scrollLeft=0;return moved}));
  assert(scrollable.length>0);assert(scrollable.every(Boolean),'Long formulas must scroll inside their own containers');
  await page.locator('#supplement-l7-a').screenshot({style:captureStyle,path:path.join(output,`plasma-bgk-${width}.png`)});
  await page.locator('#supplement-l5-c').screenshot({style:captureStyle,path:path.join(output,`plasma-rosenbluth-${width}.png`)});
 }
 await page.locator('#theme').click();assert.equal(await page.locator('html').getAttribute('data-theme'),'dark');
 await page.locator('#course-map').screenshot({style:captureStyle,path:path.join(output,'plasma-map-dark.png')});await page.locator('#theme').click();
 await page.emulateMedia({media:'print'});
 assert.equal(await page.locator('.course-map-network').evaluate(el=>getComputedStyle(el).display),'grid');
 assert.equal(await page.locator('.derivation-supplement').count(),17);
 await page.close();
 const nojs=await browser.newPage({javaScriptEnabled:false,viewport:{width:390,height:844}});
 nojs.on('request',r=>{if(/^https?:/.test(r.url())&&!r.url().startsWith(base))external.push(r.url())});
 await nojs.goto(courseUrl);await nojs.evaluate(()=>document.fonts.ready);assert.equal(await nojs.locator('.derivation-supplement .katex').count(),266);
 await nojs.locator('.course-map-node-5').click();assert.equal(new URL(nojs.url()).hash,'#lecture5');await waitForScrollIdle(nojs);
 const detail=nojs.locator('#supplement-l5-c details'),summary=detail.locator('summary');
 // Finish the long anchor journey with a user-like instantaneous scroll.
 // Mouse coordinates avoid racing CSS smooth scrolling in no-JS mode.
 await summary.evaluate(el=>el.scrollIntoView({behavior:'instant',block:'center'}));
 const box=await summary.boundingBox();assert(box&&box.y>=0&&box.y+box.height<=844);
 await nojs.mouse.click(box.x+Math.min(30,box.width/2),box.y+box.height/2);
 assert(await detail.evaluate(el=>el.open));assert(await detail.locator('.derivation-equation').first().isVisible());
 await summary.focus();await nojs.keyboard.press('Enter');assert(!(await detail.evaluate(el=>el.open)));
 await nojs.keyboard.press('Enter');assert(await detail.evaluate(el=>el.open));
 await nojs.screenshot({path:path.join(output,'plasma-nojs-390.png')});
 assert.deepEqual(errors,[]);assert.deepEqual(external,[]);
 await browser.close();console.log('PASS: seven-node map, stale filters, six cross-links, keyboard/Back/Forward, repeated disclosures, 17 derivations and 266 offline formulas at 1440/390/320px, dark/print/no-JS, no page errors or remote requests.');
})().catch(e=>{console.error(e);process.exit(1)});
