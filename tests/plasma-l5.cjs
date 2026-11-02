'use strict';
const assert=require('node:assert/strict');
const {modules,gauss,bgk,lb,scattering,jump,lorentz,rates,kernel}=require('../assets/plasma-l5.js');
let checks=0;function near(a,b,e=1e-10){assert(Math.abs(a-b)<e,`${a} != ${b}`);checks++;}
function integrate(f,a=-12,b=12,n=24000){let sum=0;const h=(b-a)/n;for(let i=0;i<n;i++)sum+=f(a+(i+.5)*h)*h;return sum;}
for(const t of [0,.1,2,20])for(const nu of [.1,.4,1])for(const u of [-2,0,2]){
const s=bgk(t,nu,u,.5);near(integrate(s.f),1,1e-9);near(integrate(v=>v*s.f(v)),s.mean,1e-9);near(integrate(v=>v*v*s.f(v)),s.second,1e-9);
const g=lb(t,nu,u,.2);near(integrate(v=>gauss(v,g.mean,g.variance)),1,1e-9);assert(g.variance>0);checks++;
const j=jump(t,nu);near(j.reduce((a,b)=>a+b),1);assert(j.every(p=>p>=0&&p<=1));checks++;
const l=lorentz(t,nu,.9);near(integrate(l.p,-1,1),1,1e-9);near(integrate(x=>x*l.p(x),-1,1),l.mean,1e-8);
}
near(scattering(1,1).chi,Math.PI/2);for(const b of [.2,.5,1,5]){const s=scattering(b,3);near(s.fraction,1/4);near(s.mu,3/4);near(s.sigma,(1+b*b)**2/4);}
for(const T of [.5,1,4])for(const m of [10,1840,2000]){const r=rates(T,m);near(r[0],T**-1.5);near(r[2]/r[0],1/Math.sqrt(m));near(r[3]/r[0],1/m);}
for(let i=0;i<36;i++){const a=i*Math.PI/18,w=[Math.cos(a),Math.sin(a)];const zero=kernel(1,w,a);near(zero[0],0);near(zero[1],0);const v=[.3,.7],out=kernel(1,v,a);assert(v[0]*out[0]+v[1]*out[1]>=-1e-12);checks++;}
// Exercise every section-specific branch and every parameter endpoint without browser APIs.
const ctx=new Proxy({}, {get(target,k){if(k==='measureText')return s=>({width:s.length*20});if(k in target)return target[k];return(...args)=>{for(const a of args)if(typeof a==='number')assert(Number.isFinite(a),`${k}: ${a}`);};},set(t,k,v){t[k]=v;return true;}});
for(const m of Object.values(modules))for(const sectionId of m.sections)for(const edge of ['min','max'])for(const t of [0,20]){const p=Object.fromEntries(m.controls.map(c=>[c.key,c[edge]]));p.sectionId=sectionId;const status=m.draw(ctx,760,340,t,p);assert(status&&typeof status==='string');assert(!/NaN|Infinity/.test(status));checks++;}
console.log(`PASS ${checks} L5 assertions: distribution moments, probability, mass factors, Rutherford cross section, kernel positivity and all section draw branches/endpoints.`);
