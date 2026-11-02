/* Run: node tests/lab-models.cjs (no dependencies). */
const assert=require('node:assert/strict');
const {gyroState,mirrorState,waveState}=require('../assets/lab-particles.js');
const {mxhPoint,oscillatorStep,oscillatorPath}=require('../assets/lab-geometry.js');
let checks=0;
const near=(a,b,e=1e-10)=>{assert(Math.abs(a-b)<=e,`${a} != ${b}`);checks++;};
for(const B of [.6,1,2])for(const E of [0,.25,.6])for(let t=0;t<=20;t+=.07){const s=gyroState(t,B,E);near(Math.hypot(s.x-s.gx,s.y-s.gy),1/B);near(s.vx**2+(s.vy-s.vd)**2,1);near(s.vd,-E/B);}
for(const R of [1.2,3,4,5])for(const angle of [10,30,50,80])for(let t=0;t<=20;t+=.07){const s=mirrorState(t,R,angle);near(s.parallel+s.perpendicular,1);near(s.perpendicular/s.B,s.mu);assert(Math.abs(s.z)<=1+1e-12);checks++;if(s.escaped){near(s.z,1);assert(s.v>0);}}
for(const t of [0,1,5,20]){const s=mirrorState(t,4,30);assert(s.threshold&&!s.trapped&&!s.escaped);near(s.amplitude,1);assert.equal(s.exitTime,Infinity);checks+=2;}
for(const k of [.1,.18,.25])for(const dk of [.02,.06,.08]){const s=waveState(k,dk);assert(s.phase>s.group);checks++;for(const t of [0,2,20])for(const x of [0,30,90,180])near(Math.cos(s.k1*x-s.w1*t)+Math.cos(s.k2*x-s.w2*t),2*Math.cos((dk*x-s.dw*t)/2)*Math.cos(k*x-s.wbar*t));}
for(const kap of [1,1.6,2])for(const s1 of [-.4,0,.4])for(const s2 of [-.2,0,.2])for(let a=0;a<=2*Math.PI;a+=.03){const p=mxhPoint(a,kap,s1,s2),m=mxhPoint(-a,kap,s1,s2);near(p.r,m.r);near(p.z,-m.z);assert(1+s1*Math.cos(a)+2*s2*Math.cos(2*a)>=.2-1e-12);checks++;}
for(const h of [.05,.18,.3]){let q=1,p=0;for(let n=0;n<10000;n++){[q,p]=oscillatorStep(q,p,h,'symplectic');near(q*q+p*p-h*q*p,1);assert((q*q+p*p)/2<.6);checks++;}const end=oscillatorPath(h,100,'forward').at(-1);near(end[0]**2+end[1]**2,(1+h*h)**100,1e-8);const a=oscillatorStep(1,0,h,'symplectic'),b=oscillatorStep(0,1,h,'symplectic');near(a[0]*b[1]-a[1]*b[0],1);}
console.log(`PASS ${checks} numerical assertions: gyro radius/drift; mirror μ/energy/threshold/escape; beating identity; MXH symmetry/monotonicity; symplectic determinant/modified energy; explicit Euler growth.`);
