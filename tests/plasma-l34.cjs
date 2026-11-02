const assert=require('node:assert/strict');
const {modules,mirror,adiabatic,covariance,potentialBoundary,jacobian,exchange,fieldMomentum,harmonicState}=require('../assets/plasma-l34.js');
let count=0;function near(a,b,e=1e-10){assert(Math.abs(a-b)<e,`${a} != ${b}`);count++;}
for(let B=.5;B<=3;B+=.05){const a=adiabatic(B);near(B*a.rho*a.rho,1);near(a.v*a.v/B,1);near(a.energy/B,.5);near(a.rho*a.v,1);}
for(const R of [1.2,3,4,5])for(const angle of [10,30,50,80])for(let t=0;t<=20;t+=.1){const s=mirror(t,R,angle);near(s.parallel+s.perp,1);near(s.perp/s.B,s.mu);assert(Math.abs(s.z)<=1+1e-12);count++;if(s.escaped){near(s.z,1);assert(s.v>0);count++;}}
for(const t of [0,1,5,20]){const s=mirror(t,4,30);assert(s.threshold&&!s.escaped&&!s.trapped);count++;near(s.parallel+s.perp,1);}
for(const phi of [0,Math.PI/2,Math.PI,2*Math.PI]){let avg=0;for(let i=0;i<1000;i++)avg+=Math.cos(2*Math.PI*i/1000)*Math.cos(2*Math.PI*i/1000+phi)/1000;near(avg,covariance(phi));}
for(const s of [.5,1,2.5]){const a=jacobian(s);near(a.f*a.J,a.N);}
for(let t=0;t<20;t+=.02){const a=exchange(t);near(a.particle+a.field,1);near((exchange(t+1e-5).particle-exchange(t-1e-5).particle)/2e-5,a.power,1e-9);}
near(potentialBoundary(1,1,2,0),0);assert(potentialBoundary(1,1,2,.5)>0);count++;
for(const E of [0,1,2])for(const B of [0,1,2]){const f=fieldMomentum(E,B);near(f.Gz,E*B);near(f.sigma.reduce((a,b)=>a+b),-(E*E+B*B));f.sigma.forEach((x,i)=>near(x+f.Tem[i],0));}
for(let t=0;t<20;t+=.1){const a=harmonicState(1,t);near(a.x*a.x+a.v*a.v,1);near((harmonicState(1,t+1e-5).x-harmonicState(1,t-1e-5).x)/2e-5,a.v,1e-9);}
const expected=[...Array.from({length:12},(_,i)=>`lecture3-s${i+1}`),...Array.from({length:16},(_,i)=>`lecture4-s${i+1}`)];const covered=Object.values(modules).flatMap(m=>m.sections);assert.deepEqual([...covered].sort(),expected.sort());count++;
// Rendering smoke test at all control endpoints and time endpoints; not browser QA.
const methods=['beginPath','moveTo','lineTo','stroke','fill','arc','ellipse','fillText','fillRect','strokeRect'];
const ctx={};for(const m of methods)ctx[m]=(...args)=>{for(const v of args)if(typeof v==='number')assert(Number.isFinite(v));};
for(const [id,m]of Object.entries(modules))for(const endpoint of ['min','max','value'])for(const t of [0,10,20])for(const sectionId of m.sections){const p=Object.fromEntries(m.controls.map(c=>[c.key,c[endpoint]]));p.sectionId=sectionId;const status=m.draw(ctx,760,340,t,p);assert(typeof status==='string'&&!/NaN|Infinity/.test(status),id);count++;}
console.log(`PASS L3–L4: ${count} assertions; 17 modules; all 28 units mapped; analytic invariants, threshold, signs, and drawing endpoint smoke tests.`);
