/* Local functional and responsive regression checks. Requires Playwright and Chromium. */
const {chromium}=require('playwright'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const base=process.env.BASE_URL||'http://localhost:8766';
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||undefined,headless:true,args:['--no-sandbox']});
 const page=await browser.newPage({viewport:{width:1440,height:1000},colorScheme:'light'}),errors=[];
 page.on('pageerror',error=>errors.push(error.message));
 const layoutFailures=[];
 const checkWidth=async()=>{const issue=await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1?null:{width:innerWidth,scrollWidth:document.documentElement.scrollWidth,elements:[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return r.right>innerWidth+1||r.left<0}).slice(0,12).map(e=>({tag:e.tagName,class:e.className,text:e.textContent.slice(0,80)}))});if(issue){layoutFailures.push({url:page.url(),...issue});console.log('OVERFLOW',JSON.stringify(layoutFailures.at(-1)))}};
 await page.goto(base);await page.locator('.card').last().waitFor();await page.evaluate(()=>document.fonts.ready);
 assert.equal(await page.locator('.card').count(),24);assert.equal(await page.locator('html').getAttribute('data-theme'),'light');
 assert(await page.evaluate(()=>document.fonts.check('20px Newsreader')));
 await page.screenshot({path:'/tmp/reading-club-desktop.png',fullPage:false});
 await page.locator('#search').fill('cuGMEC');assert.equal(await page.locator('.card').count(),1);
 await page.locator('.star').click();assert.equal(await page.locator('.star').getAttribute('aria-pressed'),'true');assert.equal(await page.evaluate(()=>document.activeElement.className),'star');
 await page.locator('.status').selectOption('reading');await page.reload();
 await page.locator('[data-view=starred]').click();assert.equal(await page.locator('.card').count(),1);
 await page.locator('[data-view=reading]').click();assert.equal(await page.locator('.card').count(),1);
 await page.locator('.status').selectOption('done');assert.equal(await page.locator('.card').count(),0);assert(await page.locator('#empty').isVisible());
 await page.locator('#reset').click();assert.equal(await page.locator('.card').count(),24);
 for(const topic of ['equilibrium','kinetic','learning','comparison']){await page.locator(`[data-topic=${topic}]`).click();assert(await page.locator('.card').count()>0);assert(await page.locator('.card').evaluateAll((cards,t)=>cards.every(c=>c.dataset.kind===t),topic))}
 await page.locator('[data-topic=all]').click();await page.locator('#sort').selectOption('title');
 const titles=await page.locator('.card h2').allTextContents();assert.deepEqual(titles,[...titles].sort((a,b)=>a.localeCompare(b,'zh-CN')));
 await page.locator('#sort').selectOption('year');const years=await page.locator('.category').allTextContents();assert.deepEqual(years.map(x=>+x.match(/\d{4}$/)[0]),years.map(x=>+x.match(/\d{4}$/)[0]).sort((a,b)=>b-a));
 await page.locator('#search').fill('no-such-title-000');assert(await page.locator('#empty').isVisible());await page.locator('#reset').click();
 await page.locator('.brand').focus();await page.keyboard.press('/');assert.equal(await page.evaluate(()=>document.activeElement.id),'search');
 await page.locator('[data-theme-toggle]').click();assert.equal(await page.locator('html').getAttribute('data-theme'),'dark');await page.screenshot({path:'/tmp/reading-club-dark.png'});
 await page.locator('[data-theme-toggle]').click();assert.equal(await page.locator('html').getAttribute('data-theme'),'light');
 for(const width of [390,320]){await page.setViewportSize({width,height:844});await checkWidth();await page.screenshot({path:`/tmp/reading-club-mobile-${width}.png`})}
 const urls=await page.locator('.card h2 a').evaluateAll(links=>links.map(a=>a.href));urls.push(base+'/reports/hybrid-comparison/m3d/report.html');
 let formulas=0,figures=0;
 for(const url of urls){
  await page.goto(url);await page.locator('h1').waitFor();await page.evaluate(()=>document.fonts.ready);
  assert.equal(await page.locator('html').getAttribute('data-theme'),'light');
  await checkWidth();
  const images=await page.locator('img').evaluateAll(async imgs=>{imgs.forEach(img=>img.loading='eager');await Promise.all(imgs.map(img=>img.decode().catch(()=>{})));return imgs.filter(img=>!img.complete||img.naturalWidth===0).map(img=>img.getAttribute('src'))});assert.deepEqual(images,[],url);
  formulas+=await page.locator('.katex,math').count();figures+=await page.locator('figure').count();
  assert(await page.locator('.reading-masthead a,.reading-course .brand').count()>0);
  if(url.includes('plasma-lectures')){
   assert.equal(await page.locator('.study-visual,canvas,#plasma-visual-coverage').count(),0);
   const originalSize=await page.evaluate(()=>getComputedStyle(document.body).fontSize);await page.locator('#larger').click();assert.notEqual(await page.evaluate(()=>getComputedStyle(document.body).fontSize),originalSize);await page.locator('#smaller').click();
   await page.locator('#theme').click();assert.equal(await page.locator('html').getAttribute('data-theme'),'dark');await page.locator('#theme').click();
   await page.locator('#menu').click();assert(await page.locator('.sidebar').isVisible());await page.locator('.sidebar #search').fill('Debye');assert(await page.locator('.study-section:visible').count()>0);
   await page.locator('.sidebar #search').fill('');await page.locator('#menu').click();
  }else{
   await page.locator('[data-theme-toggle]').click();await checkWidth();await page.locator('[data-theme-toggle]').click();
  }
 }
 await page.setViewportSize({width:1440,height:1000});await page.goto(base+'/reports/ai-gx-reading/report.html');await page.screenshot({path:'/tmp/reading-club-report-desktop.png'});await page.setViewportSize({width:390,height:844});await page.screenshot({path:'/tmp/reading-club-report-mobile.png'});
 await page.locator('.reading-masthead a').click();assert.equal(await page.locator('.card').count(),24);await page.goBack();assert(await page.locator('.reading-masthead').isVisible());await page.goForward();assert.equal(await page.locator('.card').count(),24);
 await page.goto(base+'/reports/plasma-lectures/index.html');await page.setViewportSize({width:1440,height:1000});await page.screenshot({path:'/tmp/reading-club-course-desktop.png'});await page.setViewportSize({width:390,height:844});await page.screenshot({path:'/tmp/reading-club-course-mobile.png'});
 await page.emulateMedia({media:'print'});assert.equal(await page.evaluate(()=>getComputedStyle(document.body).backgroundColor),'rgb(255, 255, 255)');
 const nojs=await browser.newPage({javaScriptEnabled:false,viewport:{width:390,height:844}});await nojs.goto(base+'/reports/ai-gx-reading/report.html');assert(await nojs.locator('h1').isVisible());assert.equal(await nojs.evaluate(()=>getComputedStyle(document.body).backgroundColor),'rgb(241, 239, 231)');
 assert.deepEqual(errors,[]);assert.deepEqual(layoutFailures,[]);await browser.close();console.log(`PASS: 24 records; search, filters, sort, saved state, keyboard, themes, Back/Forward; 25 report URLs at 320px; ${formulas} math nodes and ${figures} figures; course navigation; print and no-JS reading; no page errors.`);
})().catch(error=>{console.error(error);process.exit(1)});
