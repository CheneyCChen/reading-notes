const {chromium}=require('playwright');
const assert=require('node:assert/strict');
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH || '/usr/bin/chromium',headless:true,args:['--no-sandbox']});
 const errors=[];const page=await browser.newPage({viewport:{width:1440,height:1080}});
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://localhost:8765/labs/index.html');
 await page.locator('.experiment').last().waitFor();
 assert.equal(await page.locator('.experiment').count(),5);
 for(const id of ['gyro','mirror','waves','mxh','symplectic']){
  const card=page.locator('#'+id);await card.scrollIntoViewIfNeeded();
  assert.equal(await card.locator('.lab-actions button').first().textContent(),'播放');
  for(const input of await card.locator('.lab-controls input').all())for(const endpoint of ['min','max']){await input.evaluate((e,k)=>{e.value=e[k];e.dispatchEvent(new Event('input',{bubbles:true}));},endpoint);assert(!/NaN|Infinity/.test(await card.locator('.lab-status').textContent()));}
  for(let n=0;n<3;n++){await card.getByRole('button',{name:'播放',exact:true}).click();await page.waitForTimeout(150);await card.getByRole('button',{name:'暂停',exact:true}).click();assert(Number(await card.locator('.lab-time input').inputValue())>0);await card.getByRole('button',{name:'重置',exact:true}).click();assert.equal(await card.locator('.lab-time input').inputValue(),'0');}
  await card.getByRole('button',{name:'前进 0.1',exact:true}).click();assert.equal(await card.locator('.lab-time input').inputValue(),'0.1');
  await card.screenshot({path:'/tmp/reading-lab-'+id+'-desktop.png'});
 }
 // Offscreen animation suspends logical time.
 const gyro=page.locator('#gyro');await gyro.scrollIntoViewIfNeeded();await gyro.getByRole('button',{name:'播放',exact:true}).click();await page.waitForTimeout(200);await page.locator('#symplectic').scrollIntoViewIfNeeded();await page.waitForTimeout(150);const frozen=await gyro.locator('.lab-time input').inputValue();await page.waitForTimeout(300);assert.equal(await gyro.locator('.lab-time input').inputValue(),frozen);
 await page.goto('http://localhost:8765/index.html');await page.screenshot({path:'/tmp/reading-lab-home-desktop.png'});
 await page.goto('http://localhost:8765/reports/mxh-2021-reading/report.html#lab-mxh');
 const frame=page.frameLocator('iframe');await frame.locator('#mxh').waitFor();await page.locator('iframe').scrollIntoViewIfNeeded();await frame.getByRole('button',{name:'播放',exact:true}).click();await page.waitForTimeout(300);assert(Number(await frame.locator('.lab-time input').inputValue())>0);await frame.getByRole('button',{name:'暂停',exact:true}).click();
 await page.screenshot({path:'/tmp/reading-lab-embed-desktop.png'});
 await page.setViewportSize({width:390,height:844});await page.goto('http://localhost:8765/labs/index.html');
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 for(const id of ['gyro','mirror','waves','mxh','symplectic']){await page.locator('#'+id).screenshot({path:'/tmp/reading-lab-'+id+'-mobile.png'});}
 await page.goto('http://localhost:8765/reports/mxh-2021-reading/report.html#lab-mxh');await frame.locator('#mxh').waitFor();await page.locator('iframe').scrollIntoViewIfNeeded();await page.waitForTimeout(200);assert(await frame.locator('body').evaluate(e=>e.scrollWidth<=innerWidth));await page.screenshot({path:'/tmp/reading-lab-embed-mobile.png'});
 await page.emulateMedia({reducedMotion:'reduce'});await page.goto('http://localhost:8765/labs/index.html');await page.waitForTimeout(200);assert.equal(await page.locator('[aria-pressed="true"]').count(),0);
 assert.deepEqual(errors,[]);console.log('PASS: 5 modules; min/max sliders; 15 play/pause/reset cycles; step; offscreen suspend; desktop/mobile embed; reduced motion; no page errors.');await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
