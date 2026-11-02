const assert=require('node:assert/strict');
const {modules,continuity,tensor,langmuir,ionSound,cgl,boltzmann}=require('../assets/plasma-l6.js');
let count=0;function near(a,b,tol=1e-10){assert(Number.isFinite(a)&&Number.isFinite(b));assert(Math.abs(a-b)<tol,`${a} != ${b}`);count++;}
for(const a of [.05,.35,.55])for(let t=0;t<=20;t+=.03){let s=continuity(t,a);near(s.n*s.L,1);near(s.rate/s.L,s.gradient);const dt=1e-5;near((continuity(t+dt,a).n-continuity(t-dt,a).n)/(2*dt),-s.n*s.gradient,1e-8);}
for(const ratio of [.4,1,2.5])for(let angle=0;angle<=90;angle+=5){let p=tensor(ratio,angle);near(p.xx+p.zz+p.yy,p.trace);near(p.xx*p.zz-p.xz*p.xz,ratio);assert(p.xx>0&&p.zz>0);count++;}
for(let k=.02;k<=.3;k+=.01){let s=langmuir(k);near(s.omega*s.omega,1+3*k*k);near(s.phase*k,s.omega);let d=1e-6;near((langmuir(k+d).omega-langmuir(k-d).omega)/(2*d),s.group,1e-8);}
for(let k=.05;k<=4;k+=.05){let s=ionSound(k);near(s.omega*s.omega,k*k/(1+k*k));near(s.phase*k,s.omega);let d=1e-6;near((ionSound(k+d).omega-ionSound(k-d).omega)/(2*d),s.group,1e-8);assert(s.phase>=s.group&&s.omega<1);count++;}
for(const a of [.7,1,1.4])for(const l of [.7,1,1.4]){let s=cgl(a,l);near(s.flux,1);near(s.particles,1);near(s.perp/s.n/s.B,1);near(s.parallel*s.B*s.B/s.n**3,1);}
for(const l of [.7,1.4]){const s=cgl(1,l);near(s.B,1);near(s.perp/s.n,1);near(s.parallel/s.n,s.n*s.n);}
for(const a of [.7,1.4]){const s=cgl(a,1);near(s.B,s.n);near(s.perp/s.n,s.n);near(s.parallel/s.n,1);}
near(boltzmann(0),1);near(boltzmann(.3)*boltzmann(-.3),1);
// Exercise every drawing at endpoint controls; verify every numeric canvas argument is finite.
const ctx=new Proxy({}, {get:(o,k)=>{if(k in o)return o[k];return(...args)=>{args.filter(v=>typeof v==='number').forEach(v=>{assert(Number.isFinite(v),`nonfinite ${k}`);count++;});};},set:(o,k,v)=>{o[k]=v;return true;}});
for(const [id,m] of Object.entries(modules)){for(const endpoint of ['min','max','value'])for(const t of [0,1,20])for(const sectionId of m.sections){const p={...Object.fromEntries(m.controls.map(c=>[c.key,c[endpoint]])),sectionId};const status=m.draw(ctx,760,340,t,p);assert(status&&!/NaN|Infinity/.test(status),id);count++;}}
console.log(`PASS Lecture 6: ${count} numerical and finite-drawing assertions; 10 modules covering 20 units.`);
