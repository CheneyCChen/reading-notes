// Temporary focused diagnostics; it never changes the source or publishes a fix.
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:320,height:844}});
for(const name of ['flux-surface-fitting-reading','mxh-2021-reading','modified-pinn-conservation-reading','neural-operator-splitting-reading','ai-gx-reading','mxh-veq-reading']){
 await p.goto(`http://localhost:8766/reports/${name}/report.html`);await p.evaluate(()=>document.fonts.ready);
 const measure=()=>p.evaluate(()=>document.documentElement.scrollWidth);
 const baseline=await measure();console.log('BASE',name,baseline);
 console.log('ROOT-OVERFLOW',JSON.stringify(await p.evaluate(()=>[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();if(r.right<=innerWidth+1)return false;for(let a=e.parentElement;a&&a!==document.body;a=a.parentElement){const c=getComputedStyle(a);if(c.overflowX!=='visible'||c.clipPath!=='none'||c.clip!=='auto')return false}return true}).slice(0,12).map(e=>({tag:e.tagName,class:e.className,html:e.outerHTML.slice(0,140),right:e.getBoundingClientRect().right,width:getComputedStyle(e).width,display:getComputedStyle(e).display,overflow:getComputedStyle(e).overflowX,minWidth:getComputedStyle(e).minWidth,maxWidth:getComputedStyle(e).maxWidth,ancestors:[e.parentElement,e.parentElement?.parentElement,e.parentElement?.parentElement?.parentElement].filter(Boolean).map(a=>({tag:a.tagName,class:a.className,width:getComputedStyle(a).width,overflow:getComputedStyle(a).overflowX}))})))));
 const candidates={
  noMathML:'.katex-mathml{display:none!important}',
  tables:'.reading-report table{display:block!important;min-width:0!important;width:100%!important;max-width:100%!important;overflow-x:auto!important}',
  containers:'.reading-report :is(.table-wrap,.math-display,.equation){width:100%!important;max-width:100%!important;min-width:0!important;position:relative!important;contain:inline-size}',
  mathDisplay:'.reading-report .katex-display{max-width:100%!important;overflow-x:auto!important}',
  proseBlocks:'.reading-report :is(main,section,nav,header,article,div){min-width:0!important;max-width:100%!important}',
  hideMainOverflow:'.reading-report main{overflow-x:hidden!important}'
 };
 for(const [key,css] of Object.entries(candidates)){const style=await p.addStyleTag({content:css});console.log('PROBE',name,key,await measure());await style.evaluate(e=>e.remove())}
}
await b.close()})().catch(e=>{console.error(e);process.exit(1)});
