const assert=require('node:assert/strict');
const m=require('../assets/plasma-l12.js');let n=0;
function near(a,b,e=1e-10){assert(Math.abs(a-b)<e,`${a} != ${b}`);n++;}
for(const T of [.025,1,20]){near(m.thermal(T).log10,-14.5/T/Math.LN10);assert(m.thermal(T).kelvin>0);}
for(const tau of [.2,1,5]){near(m.shielding(0,tau).enclosed,1);near(m.shielding(0,tau).potentialFactor,1);for(let r=0;r<10;r+=.1){const s=m.shielding(r,tau);assert(s.enclosed>=s.potentialFactor&&s.enclosed<=1);n++;}}
near(m.shielding(0,1).lambda,1/Math.sqrt(2));
for(const density of [.5,1,4])for(let t=0;t<=20;t+=.03)near(m.oscillation(t,density).energy,1);
for(let x=1;x<=6;x+=.1){let s=m.hierarchy(x);assert(s.collision<1&&s.coupling<1&&s.close<1);n++;}
for(let p=0;p<=4;p+=.01){let s=m.relativity(p);assert(s.beta<1);near(s.gamma*s.gamma*(1-s.beta*s.beta),1);}
for(const B of [.8,1,2])for(const E of [0,.2,.5])for(const q of [-1,1])for(let t=0;t<=20;t+=.03){let s=m.gyro(t,B,E,q);near(Math.hypot(s.x-s.gx,s.y-s.gy),s.rho);near(s.vd,-E/B);}
for(const g of [0,.1,.2])for(const k of [0,-.05,-.2]){let a=m.drift(g,k,1),b=m.drift(g,k,-1);near(a.total,-b.total);}
for(const rate of [.05,.15,.2]){near(m.polarization(0,rate).displacement,0);near(m.polarization(2*Math.PI/rate,rate).displacement,0);}
near(m.flr(0).average,1);assert(Math.abs(m.flr(.1).average-m.flr(.1).second)<.000002);assert(m.flr(2).average>m.flr(2).second);
const ctx=new Proxy({},{get:(o,k)=>o[k]||(o[k]=()=>{}),set:(o,k,v)=>(o[k]=v,true)});
const coverage=[];
for(const[id,mod]of Object.entries(m.modules)){
 assert(mod.lecture===1||mod.lecture===2);assert(mod.sections.length);
 for(const sectionId of mod.sections){coverage.push({sectionId,moduleId:id,note:mod.description,kind:mod.animated||mod.controls.length?'interactive':'static'});for(const endpoint of ['min','max'])for(const t of [0,10,20]){let p=Object.fromEntries(mod.controls.map(c=>[c.key,c[endpoint]]));p.sectionId=sectionId;let status=mod.draw(ctx,760,340,t,p);assert(!/NaN|Infinity/.test(status));n++;}}
}
require('fs').writeFileSync('/tmp/plasma-l12-coverage.json',JSON.stringify(coverage,null,2));
assert.equal(new Set(coverage.map(c=>c.sectionId)).size,23);console.log(`PASS ${n} numerical/render-path assertions, 16 modules cover all 23 L1/L2 units.`);
