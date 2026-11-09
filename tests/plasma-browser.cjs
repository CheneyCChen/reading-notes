/* Original course controls, offline PDFs, and removal regression checks. */
const {chromium}=require('playwright'),assert=require('node:assert/strict');
const base=process.env.BASE_URL||'http://localhost:8766';
const courseUrl=base.endsWith('.html')?base:base.replace(/\/$/,'')+'/reports/plasma-lectures/index.html';
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||undefined,headless:true,args:['--no-sandbox']});
 const page=await browser.newPage({viewport:{width:1440,height:1000},colorScheme:'light'}),errors=[];
 page.on('pageerror',error=>errors.push(error.message));
 await page.goto(courseUrl);await page.locator('#lecture1-s1').waitFor();
 assert.equal(await page.locator('.study-visual,canvas,#plasma-visual-coverage').count(),0);
 assert.equal(await page.locator('[data-done]').count(),108);
 assert.equal(await page.locator('details').count(),63);
 assert.equal(await page.locator('.katex').count(),1853);
 const brokenImages=await page.locator('img').evaluateAll(async images=>{
   images.forEach(img=>img.loading='eager');
   await Promise.race([
     Promise.all(images.map(img=>img.decode().catch(()=>{}))),
     new Promise((_,reject)=>setTimeout(()=>reject(new Error('Course image decode timed out')),15000))
   ]);
   return images.filter(img=>!img.complete||!img.naturalWidth).map(img=>img.getAttribute('src'));
 });assert.deepEqual(brokenImages,[]);
 // All seven PDFs are still embedded and every PDF button opens its own source.
 const pdfs=await page.locator('#pdf-data').evaluate(el=>JSON.parse(el.textContent));
 assert.equal(pdfs.length,7);
 for(const pdf of pdfs)assert(Buffer.from(pdf.base64,'base64').subarray(0,5).equals(Buffer.from('%PDF-')));
 await page.evaluate(()=>{window.pdfOpens=[];window.open=url=>{window.pdfOpens.push(url);return {}}});
 for(let i=0;i<7;i++)await page.locator(`.pdf-button[data-pdf="${i}"]`).click();
 const opened=await page.evaluate(()=>window.pdfOpens);
 assert.equal(new Set(opened).size,7);assert(opened.every(url=>url.startsWith('blob:')&&url.endsWith('#page=1')));
 // Repeat the remaining lesson controls, including a reload of saved progress.
 const done=page.locator('[data-done="lecture1-s1"]');await done.check();await page.reload();assert(await done.isChecked());
 assert.match(await page.locator('#progress-label').textContent(),/1 \/ 108/);await done.uncheck();
 for(let lecture=1;lecture<=7;lecture++){
   await page.locator(`[data-filter="${lecture}"]`).click();
   assert.equal(await page.locator('.lecture:visible').count(),1);
   assert.equal(await page.locator('.lecture:visible').getAttribute('id'),'lecture'+lecture);
 }
 await page.locator('[data-filter="all"]').click();
 await page.locator('#search').fill('no-such-concept-000');assert(await page.locator('#empty').isVisible());
 await page.locator('#search').fill('Debye');assert(await page.locator('.study-section:visible').count()>0);
 await page.locator('#search').fill('');assert.equal(await page.locator('.lecture:visible').count(),7);
 for(let i=0;i<2;i++){const quiz=page.locator('#lecture1-quiz details').first();await quiz.locator('summary').click();assert(await quiz.evaluate(el=>el.open));await quiz.locator('summary').click();assert(!(await quiz.evaluate(el=>el.open)))}
 const fontSize=await page.evaluate(()=>getComputedStyle(document.body).fontSize);await page.locator('#larger').click();assert.notEqual(await page.evaluate(()=>getComputedStyle(document.body).fontSize),fontSize);await page.locator('#smaller').click();
 for(let i=0;i<2;i++){await page.locator('#theme').click();assert.equal(await page.locator('html').getAttribute('data-theme'),'dark');await page.locator('#theme').click();assert.equal(await page.locator('html').getAttribute('data-theme'),'light')}
 // Verify L7 is searchable, its source is intact, and every original self-test expands.
 await page.locator('#search').fill('Braginskii');assert(await page.locator('#lecture7').isVisible());
 await page.locator('#search').fill('');await page.locator('[data-filter="7"]').click();
 assert.equal(await page.locator('#lecture7 [data-equation]').count(),73);
 assert.equal(await page.locator('#lecture7 .footnote-ref').count(),5);
 const l7done=page.locator('[data-done="lecture7-s1"]');await l7done.check();await page.reload();assert(await l7done.isChecked());await l7done.uncheck();
 await page.locator('[data-filter="7"]').click();
 for(const quiz of await page.locator('#lecture7-quiz details').all()){
   await quiz.locator('summary').click();assert(await quiz.evaluate(el=>el.open));
   assert(await quiz.locator('.answer').isVisible());await quiz.locator('summary').click();
 }
 const foot=page.locator('#lecture7 .footnote-ref').first();const target=await foot.getAttribute('href');
 await foot.click();assert.equal(new URL(page.url()).hash,target);
 await page.locator(target+' .footnote-back').click();assert.equal(new URL(page.url()).hash,'#l7-s4-fnref1');
 await page.locator('#lecture7').scrollIntoViewIfNeeded();
 await page.screenshot({path:'/tmp/plasma-lecture7-desktop.png'});
 await page.locator('[data-filter="all"]').click();
 await page.screenshot({path:'/tmp/plasma-lecture-desktop.png'});
 for(const width of [390,320]){
   await page.setViewportSize({width,height:844});
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
   await page.locator('#menu').click();assert(await page.locator('.sidebar').isVisible());
   await page.locator('.sidebar a[href="#lecture7"]').click();assert(!(await page.locator('body').evaluate(el=>el.classList.contains('nav-open'))));
   await page.screenshot({path:`/tmp/plasma-lecture-mobile-${width}.png`});
   for(const target of ['#eq-L7-9','#eq-L7-52k','#lecture7-quiz']){
     await page.locator(target).scrollIntoViewIfNeeded();
     assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),`L7 overflow at ${target}, ${width}`);
   }
   await page.locator('#lecture7-s18').scrollIntoViewIfNeeded();
   await page.screenshot({path:`/tmp/plasma-lecture7-transport-${width}.png`});
 }
 await page.emulateMedia({media:'print'});assert.equal(await page.evaluate(()=>getComputedStyle(document.body).backgroundColor),'rgb(255, 255, 255)');
 const nojs=await browser.newPage({javaScriptEnabled:false,viewport:{width:390,height:844}});await nojs.goto(courseUrl);assert(await nojs.locator('h1').isVisible());assert.equal(await nojs.locator('.katex').count(),1853);
 assert.deepEqual(errors,[]);await browser.close();
 console.log('PASS: no visual demos; original lessons, formulas, images, seven PDFs, saved progress, filters, self-tests, themes, mobile navigation, print and no-JS reading.');
})().catch(error=>{console.error(error);process.exit(1)});
