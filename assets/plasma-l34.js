/* Lectures 3–4: section-linked analytic teaching diagrams, never research outputs. */
(function(root){'use strict';
const T=2*Math.PI,C={ink:'#19364d',blue:'#1468ad',teal:'#007d78',orange:'#b9511b',gray:'#5a6e7e',line:'#d6e1e9'};
function text(c,s,x,y,color=C.ink){c.font='21px system-ui,sans-serif';c.fillStyle=color;c.fillText(String(s).replace(/ḃ/g,'db/dt').replace(/V̇_E/g,'dV_E/dt').replace(/μ̇/g,'dμ/dt').normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[₀₁₂₃₄₅₆₇₈₉]/g,ch=>'₀₁₂₃₄₅₆₇₈₉'.indexOf(ch)),x,y);}
function line(c,pts,color=C.blue,width=2){c.beginPath();pts.forEach((p,i)=>i?c.lineTo(...p):c.moveTo(...p));c.strokeStyle=color;c.lineWidth=width;c.stroke();}
function circle(c,x,y,r,color=C.blue,fill=false){c.beginPath();c.arc(x,y,r,0,T);if(fill){c.fillStyle=color;c.fill();}else{c.strokeStyle=color;c.lineWidth=2;c.stroke();}}
function box(c,x,y,w,h,label,color=C.blue){c.fillStyle='#f0f5f8';c.fillRect(x,y,w,h);c.strokeStyle=color;c.strokeRect(x,y,w,h);text(c,label,x+14,y+h/2+7,color);}
function arrow(c,x,y,dx,dy,color=C.blue){line(c,[[x,y],[x+dx,y+dy]],color);const a=Math.atan2(dy,dx);line(c,[[x+dx-10*Math.cos(a-.5),y+dy-10*Math.sin(a-.5)],[x+dx,y+dy],[x+dx-10*Math.cos(a+.5),y+dy-10*Math.sin(a+.5)]],color);}
function graph(c,fn,x=65,y=270,w=620,h=190,xmax=1,ymax=1,color=C.blue){line(c,[[x,y-h],[x,y],[x+w,y]],C.line);const pts=[];for(let i=0;i<=160;i++)pts.push([x+w*i/160,y-h*fn(xmax*i/160)/ymax]);line(c,pts,color,2.5);}
function ctl(key,label,min,max,step,value){return{key,label,min,max,step,value};}
function mirror(t,R,angle){const a=angle*Math.PI/180,mu=Math.sin(a)**2,v0=Math.cos(a),omega=Math.sqrt(mu*(R-1)),threshold=Math.abs(mu*R-1)<=1e-12,trapped=mu*R>1+1e-12,amp=threshold?1:v0/omega,exit=(trapped||threshold)?Infinity:Math.asin(1/amp)/omega,tt=Math.min(t,exit),z=amp*Math.sin(omega*tt),v=v0*Math.cos(omega*tt),B=1+(R-1)*z*z;return{mu,z,v,B,threshold,trapped,escaped:t>=exit,exit,perp:mu*B,parallel:v*v,omega};}
function adiabatic(B){return{rho:1/Math.sqrt(B),v:Math.sqrt(B),energy:B/2,flux:Math.PI,action:.5};}
function covariance(phi){return Math.cos(phi)/2;}
function potentialBoundary(vpar,vperp,R,psi){return vpar*vpar-(R-1)*vperp*vperp+psi;}
function jacobian(s){return{J:s,f:1/s,N:1};}
function fieldMomentum(E,B){const xx=E*E-B*B,yy=-xx,zz=-(E*E+B*B);return{Gz:E*B,sigma:[xx,yy,zz],Tem:[-xx,-yy,-zz]};}
function harmonicState(r,t){return{x:r*Math.cos(t),v:-r*Math.sin(t)};}
function exchange(t){return{particle:Math.sin(t)**2,field:Math.cos(t)**2,power:Math.sin(2*t)};}
const modules={};
function add(id,lecture,sections,spec){modules[id]={lecture,anchor:sections[0],sections,animated:false,...spec};}
add('adiabatic-order',3,['lecture3-s1','lecture3-s5','lecture3-s12'],{
 title:'先比较时间尺度，再使用不变量',description:'回旋、反弹、漂移依次变慢；滑块比较外场变化时间与三种轨道时间。这是适用条件图，不是假装求解不变量失效。',equation:'τ回旋 ≪ τ反弹 ≪ τ漂移；εμ=τ回旋/τ场 ≪ 1；相关共振与分界附近还需单独检查。',limits:'时间尺度仅为示意：1、10、100；满足慢变比值不是充分条件，规则闭轨道、弱扰动及非共振条件仍不可省略。',question:'一个场对回旋足够慢，是否也一定对反弹和漂移足够慢？',controls:[ctl('tau','外场变化时间 τ场 / τ回旋',2,500,2,100)],draw(c,w,h,t,p){const X=z=>90+180*Math.log10(z);line(c,[[80,170],[690,170]],C.line);[1,10,100].forEach((v,i)=>{circle(c,X(v),170,7,C.blue,true);text(c,['回旋','反弹','漂移'][i],X(v)-25,130);text(c,String(v),X(v)-10,215);});arrow(c,X(p.tau),270,0,-70,C.orange);text(c,'场变化 '+p.tau,Math.min(X(p.tau)-65,570),310,C.orange);text(c,'对数时间轴；越靠右，变化越慢',80,42);return `τ场/τ回旋=${p.tau}；τ反弹/τ场=${(10/p.tau).toFixed(3)}；τ漂移/τ场=${(100/p.tau).toFixed(3)}。比值不小的层级不能直接套用绝热论证。`;}});
add('mu-action',3,['lecture3-s2','lecture3-s3','lecture3-s4','lecture3-s6'],{
 title:'μ 不变：回旋圆变小，动量椭圆等面积',description:'调节缓变场的瞬时 B：垂直能量随 B 增大，回旋半径缩小；固定参数的闭轨道在正则相空间中保留作用量。',equation:'μ=mv⊥²/(2B)；K⊥=μB；ρ∝B⁻¹ᐟ²；Bπρ²=常数；J=(2π)⁻¹∮P dQ=K⊥/|Ω|。',limits:'展示绝热近似下的一族瞬时轨道，非真实时间积分；长度、速度、场分别以 ρ₀、v₀、B₀ 归一化，Ω₀=|q|B₀/(mc)，v₀≪c。μ̇ 的严格误差与 Faraday 功率抵消见正文。',question:'B 加倍时能量增大，为什么不能因此断言 μ 也增大？',controls:[ctl('B','磁场 B / B₀',.5,3,.05,1)],draw(c,w,h,t,p){const a=adiabatic(p.B);text(c,'真实空间：回旋圆',35,35);text(c,'正则相空间：闭轨道',410,35);circle(c,190,170,85*a.rho);c.beginPath();c.ellipse(560,170,85*a.rho,60*a.v,0,0,T);c.strokeStyle=C.teal;c.stroke();line(c,[[420,170],[705,170]],C.line);line(c,[[560,55],[560,285]],C.line);text(c,'Q',700,197);text(c,'P',575,65);text(c,'ρ/ρ₀ = '+a.rho.toFixed(2),65,305);text(c,'面积 ∮P dQ 不变',440,305,C.teal);return `B/B₀=${p.B.toFixed(2)}；K⊥/K⊥₀=${p.B.toFixed(2)}；ρ/ρ₀=${a.rho.toFixed(3)}；磁通与作用量的归一化比值均为 1。`;}});
add('magnetization',3,['lecture3-s7'],{
 title:'回旋电流相消，边界留下磁化电流',description:'相邻电流环的内部方向相反，宏观磁矩沿 −B；β 衡量压力相对磁场能量的量级。',equation:'M=−p⊥ b/B；jM=c∇×M；|4πM|/B=β⊥/2，β⊥=8πp⊥/B²。',limits:'电流环是几何示意，非真实密排粒子轨道；β/2 是磁化量级比，不是自洽求解后的 ΔB/B，更不能把大 β 线性外推为负磁场。',question:'导心没有净平移时，为什么仍可有磁化电流？',controls:[ctl('beta','压力参数 β⊥',0,2,.05,.5)],draw(c,w,h,t,p){for(let i=0;i<4;i++)for(let j=0;j<2;j++){circle(c,90+i*90,120+j*90,45,C.blue);arrow(c,80+i*90,75+j*90,20,0,C.blue);}text(c,'内部相邻环：方向抵消',40,285);arrow(c,540,235,0,-125,C.blue);text(c,'B',560,112);arrow(c,630,110,0,Math.min(125,125*p.beta/2),C.orange);text(c,'M',650,240,C.orange);text(c,'抗磁：M 与 B 反向',430,45);return `β⊥=${p.beta.toFixed(2)}，|4πM|/B=${(p.beta/2).toFixed(3)}；该比值是量级诊断，不是有限 β 平衡解。`;}});
add('mirror-bounce',3,['lecture3-s8','lecture3-s10'],{
 title:'磁镜有效势与反弹作用量',description:'中心发射粒子；被俘获者在镜内反弹，损失锥内粒子穿过右侧出口。临界轨道恰在边界转向。',equation:'B=1+(R−1)z²；v∥²+v⊥²=1；μ*=v⊥²/B=sin²α₀；z̈=−μ*(R−1)z；J反弹=∮m v∥ ds。',limits:'一维解析导心模型，z 以半镜长、速度以初速归一化；μ*=2μB₀/(mv₀²)。无电势与碰撞；出射后只保留出口标记，不人工反射；有界二次势内反弹周期有限，不模拟分离曲线周期发散。',question:'损失锥内的运动不是闭轨道，为什么不能使用同一个反弹作用量？',animated:true,controls:[ctl('R','镜比 R',1.2,5,.1,3),ctl('angle','中心俯仰角 α₀ / 度',10,80,1,50)],draw(c,w,h,t,p){const s=mirror(t,p.R,p.angle),X=z=>380+270*z,ymax=Math.max(1,s.mu*p.R),Y=e=>265-170*e/ymax;graph(c,z=>s.mu*(1+(p.R-1)*(2*z-1)**2),110,265,540,170,1,ymax,C.blue);line(c,[[110,Y(1)],[650,Y(1)]],C.gray);text(c,'总动能 = 1',500,Y(1)-18);circle(c,X(s.z),Y(s.perp),8,C.orange,true);text(c,'有效势 μ* B(z)',25,40);text(c,'−1',100,300);text(c,'0',375,300);text(c,'+1 出口',620,300);text(c,s.escaped?'已出射':s.threshold?'临界：边界转向':s.trapped?'镜内反弹':'驶向出口',280,40,C.orange);return `z=${s.z.toFixed(3)}；v∥=${s.v.toFixed(3)}；垂直能量 ${s.perp.toFixed(3)} + 平行能量 ${s.parallel.toFixed(3)} = 1；${s.trapped?'反弹周期 '+(T/s.omega).toFixed(2):s.threshold?'临界边界转向':'开放出射轨道，无闭合反弹作用量'}。`;}});
add('potential-loss',3,['lecture3-s9'],{
 title:'电势把直线损失锥改成双曲边界',description:'速度平面上，橙色点可以到达出口，蓝色点在出口前已遇到能量禁区；边界对应出口平行速度为零。',equation:'v∥,出口²=v∥₀²−(R−1)v⊥₀²+Ψ；Ψ=2q(φ₀−φ出口)/m；边界：(R−1)v⊥₀²−v∥₀²=Ψ。',limits:'速度以任意 v₀ 归一化，Ψ 以 v₀² 归一化；只检查中心与出口能量条件。若沿途有效势非单调，出口条件未必保证全程可达；本图假定有效势最大值在出口。',question:'正 Ψ 是加速粒子还是增加势垒？这与电荷符号有什么关系？',controls:[ctl('R','镜比 R',1.2,4,.1,2),ctl('psi','电势参数 Ψ / v₀²',-1,1,.05,0)],draw(c,w,h,t,p){for(let i=0;i<=30;i++)for(let j=0;j<=15;j++){let vp=-2+i*4/30,vt=j*2/15,val=potentialBoundary(vp,vt,p.R,p.psi);circle(c,100+140*(vp+2),275-100*vt,4,val>=0?C.orange:C.blue,true);}text(c,'v⊥₀',35,60);text(c,'v∥₀',650,300);text(c,'橙：出口可达',80,35,C.orange);text(c,'蓝：出口能量不足',360,35,C.blue);return `Ψ=${p.psi.toFixed(2)}；Ψ>0 增加出口平行动能，扩大出口可达区；Ψ<0 增加势垒。边界不是任意情况下的全轨道判据。`;}});
add('canonical-flux',3,['lecture3-s11'],{
 title:'严格守恒的是总正则角动量',description:'把机械项与磁通项放进同一账本。增大机械份额时，固定总正则角动量要求磁通项减小。',equation:'pθ=L机械+qΦ/(2πc)；轴对称 ⇒ ṗθ=0；只有 |L机械|≪|pθ| 时才有 Φ≈常数。',limits:'这是守恒关系的代数分配图，非动力学轨迹。正则角动量以常数 pθ=1 归一化；磁通项归一化为 qΦ/(2πcpθ)。不将强旋转误当成近似磁通守恒。',question:'机械角动量占一半时，还能把 pθ 守恒直接说成 Φ 守恒吗？',controls:[ctl('fraction','机械角动量份额 L机械 / pθ',0,.8,.02,.1)],draw(c,w,h,t,p){c.fillStyle=C.orange;c.fillRect(70,120,620*p.fraction,70);c.fillStyle=C.blue;c.fillRect(70+620*p.fraction,120,620*(1-p.fraction),70);text(c,'机械项 '+p.fraction.toFixed(2),60,80,C.orange);text(c,'磁通项 '+(1-p.fraction).toFixed(2),390,80,C.blue);text(c,'总正则角动量 = 1（严格）',175,255);text(c,p.fraction<.1?'机械项小：磁通近似较好':'机械项不可忽略：不能只保留磁通',115,305);return `L机械/pθ=${p.fraction.toFixed(2)}，qΦ/(2πcpθ)=${(1-p.fraction).toFixed(2)}；总和严格为 1。`;}});
add('phase-flow',4,['lecture4-s2','lecture4-s3','lecture4-s6','lecture4-s9'],{
 title:'相空间剪切：形状改变，体积不变',description:'不同速度的粒子以不同速率平移。色带逐渐细化，但 f 沿特征线不变；不能把看不清细丝误认成细粒度熵增加。',equation:'x(t)=x₀+vt（mod 2π），v(t)=v₀；det ∂(x,v)/∂(x₀,v₀)=1；f(t,x,v)=f₀(x−vt,v)。',limits:'周期 x、一维自由输运；没有自洽电场，因此不是 Landau 阻尼计算。色彩表示 f；任何数值栅格只用于显示，细粒度 Casimir 守恒由解析映射保证。',question:'色带越来越细，为何 ∫f² dx dv 和细粒度熵仍不变？',animated:true,controls:[ctl('shear','速度展宽系数',.2,2,.1,1)],draw(c,w,h,t,p){for(let i=0;i<64;i++)for(let j=0;j<24;j++){const x=T*i/64,v=1-2*j/23,f=1+.7*Math.cos(x-v*p.shear*t);c.fillStyle=`rgb(${Math.round(230-130*(f-.3)/1.4)},${Math.round(240-85*(f-.3)/1.4)},245)`;c.fillRect(70+i*9.5,65+j*8,9.7,8.2);}text(c,'v',30,80);text(c,'−1',25,255);text(c,'+1',25,60);text(c,'0',70,290);text(c,'2π（周期 x）',540,290);text(c,'细粒度 f 沿轨道守恒；图像分辨率不是碰撞',70,325);return `剪切时间=${(p.shear*t).toFixed(2)}；流映射行列式=1；周期域平均 f=1、平均 f²=1.245，均保持不变。`;}});
add('kvn-transport',4,['lecture4-s4'],{
 title:'算符形式仍是经典搬运，不是量子衍射',description:'一个实的周期分布随常速平移。算符中的 i 不会把实初值变成量子波，也不会把密度定义替换为 |F|²。',equation:'i∂tF=−iu∂xF ⇒ ∂tF+u∂xF=0；F(t,x)=exp[cos(x−ut)]；周期边界消去分部积分的边界项。',limits:'一维周期平移给出 Hermitian 性所需边界条件的例子；实际讲义算符作用于完整相空间。∫|F|² 不变是范数性质，本例 F 本身仍是所输运的实分布。',question:'为什么出现 i 并不意味着粒子已经量子化？',animated:true,controls:[ctl('u','平移速度 u',.2,2,.1,1)],draw(c,w,h,t,p){graph(c,x=>Math.exp(Math.cos(x-p.u*t)),70,265,620,180,T,3);text(c,'实分布 F',70,40);text(c,'x：周期 0 → 2π',400,310);text(c,'只平移，不展宽、不衍射',180,80,C.teal);return `平移相位 ut=${(p.u*t).toFixed(2)}；实初值保持实值；周期边界下 ∫F dx 与 ∫F² dx 都不随时间变化。`;}});
add('coordinate-jacobian',4,['lecture4-s5'],{
 title:'换坐标：格子变宽，坐标密度变低',description:'同一批粒子用不同坐标表示。把坐标长度放大 s 倍，体积元放大 s 倍，每单位坐标体积的密度须除以 s。',equation:'z=sZ；Jcoord=|∂z/∂Z|=s；dN=F dZ=f dz；f=F/Jcoord。',limits:'一维线性坐标变换示意，不是粒子流动或物理压缩。讲义三维 (q,p)→(x,v) 的特例是 Jcoord=m⁻³、f=m³F。坐标变换 Jacobian 不等于流映射 Jacobian。',question:'图上单位长度密度变小，为什么粒子数没有变化？',controls:[ctl('s','坐标伸缩 s',.5,2.5,.1,1.5)],draw(c,w,h,t,p){box(c,70,70,200,65,'Z：ΔZ = 1');box(c,70,210,200*p.s,65,'z：Δz = '+p.s.toFixed(1),C.teal);for(let i=0;i<8;i++){circle(c,83+i*24,115,4,C.orange,true);circle(c,70+p.s*(13+i*24),255,4,C.orange,true);}text(c,'F = 1',390,110);text(c,'f = '+(1/p.s).toFixed(3),Math.max(390,95+200*p.s),250,C.teal);text(c,'两个格子包含同一批粒子',100,320);return `Jcoord=${p.s.toFixed(2)}；f=${(1/p.s).toFixed(3)}；fΔz=FΔZ=1。`;}});
add('fluctuation-correlation',4,['lecture4-s7'],{
 title:'平均涨落为零，乘积平均仍可非零',description:'两条波形各自平均为零。调节相位差，看它们的相关项由正变零再变负；这解释平均方程为何留下关联项。',equation:'δa=cosθ，g=cos(θ+φ)；⟨δa⟩=⟨g⟩=0；⟨δa·g⟩=cosφ/2；C=−⟨δa·∇vf⟩。',limits:'g 仅代表一个速度梯度涨落分量。此图演示平均运算，未推导真实碰撞核，也不宣称任意相关项都有耗散或 H 定理。',question:'φ=π/2 时关联为零，能否据此断言所有涨落都没有作用？',controls:[ctl('phase','相位差 φ / π',0,2,.05,0)],draw(c,w,h,t,p){const phase=p.phase*Math.PI;graph(c,x=>1+Math.cos(x),70,255,620,170,T,2,C.blue);graph(c,x=>1+Math.cos(x+phase),70,255,620,170,T,2,C.orange);text(c,'蓝：δa；橙：g（两条曲线均上移 1 显示）',70,40);text(c,'乘积平均 = '+covariance(phase).toFixed(3),180,310,C.teal);return `⟨δa⟩=⟨g⟩=0；⟨δa g⟩=${covariance(phase).toFixed(3)}。平均为零的两项不保证相关项为零。`;}});
add('invariant-equilibrium',4,['lecture4-s8'],{
 title:'用运动积分构造平衡分布',description:'简谐振子的每条圆轨道具有固定 H；令 f=exp(−H/T)，同一轨道上的分布值便完全相同。',equation:'H=(x²+v²)/2；ẋ=v，v̇=−x；dH/dt=0 ⇒ df(H)/dt=f′(H)dH/dt=0。',limits:'外加、时间不变的谐振势示例；满足轨道上的 Vlasov 方程不等于已经满足 Poisson/Maxwell 自洽场方程。T 是归一化分布宽度。',question:'若势能显含时间，还能不加条件地令 f=exp(−H/T) 为静态解吗？',animated:true,controls:[ctl('temp','分布宽度 T',.5,2,.1,1)],draw(c,w,h,t,p){for(let j=1;j<=4;j++){let r=j*.4;circle(c,250,170,r*75,C.blue);const orbit=harmonicState(r,t);circle(c,250+75*orbit.x,170-75*orbit.v,5,C.orange,true);text(c,'H='+(.5*r*r).toFixed(2)+'  f='+Math.exp(-.5*r*r/p.temp).toFixed(2),450,65+j*45);}text(c,'x–v 相空间',120,30);text(c,'同一圆上 f 恒定',110,320,C.teal);return `f(H)=exp(−H/${p.temp.toFixed(1)})；各闭轨道上的 H 和 f 都不变，但尚未验证场的自洽性。`;}});
add('gardner-swap',4,['lecture4-s10'],{
 title:'等体积交换：把更大的 f 放到较低能量',description:'交换两块等体积相空间单元，保留分布值及其占据体积。能量下降来自重新排列，不是把所有粒子压进零速度。',equation:'ΔK=ΔV(Ea−Eb)(fb−fa)；Ea<Eb、fa<fb ⇒ ΔK<0。',limits:'两个离散等体积单元的重排说明；Gardner 最低能态给可用能上界，实际动力学还可能受其他不变量与可达性约束，不保证全部能量能够提取。',question:'如果允许压缩单元体积，为什么得到的“最低能量”就不再是同一个问题？',controls:[ctl('swap','交换状态（0 原位，1 交换）',0,1,1,0),ctl('fb','高能单元原始分布 fb',1.2,3,.1,2)],draw(c,w,h,t,p){const a=p.swap?p.fb:1,b=p.swap?1:p.fb;box(c,90,85,220,130,'Ea = 1');box(c,440,85,220,130,'Eb = 3');c.fillStyle=C.teal;c.fillRect(110,240,180,25*a);c.fillStyle=C.orange;c.fillRect(460,240,180,25*b);text(c,'fa = '+a.toFixed(1),135,65,C.teal);text(c,'fb = '+b.toFixed(1),485,65,C.orange);text(c,'等体积 ΔV = 1，值的集合始终为 {1, '+p.fb.toFixed(1)+'}',80,330);return `原始 K=${(1+3*p.fb).toFixed(2)}；交换后 K=${(p.fb+3).toFixed(2)}；当前 K=${(a+3*b).toFixed(2)}；ΔK=${(2-2*p.fb).toFixed(2)}。`;}});
add('selfconsistent-loop',4,['lecture4-s1','lecture4-s11'],{
 title:'分布与场必须闭合成回路',description:'选择推导步骤，查看分布函数、速度矩、场方程和轨道输运之间的关系。这里只画模型依赖，不假装完成数值求解。',equation:'fs → ρ=Σqs∫fsdv、j=Σqs∫vfsdv → (E,B) → 洛伦兹力 → fs。',limits:'静态模型结构图。Vlasov–Poisson 采用静电近似，不等同于任意情况下忽略所有磁效应；闭合还需要初值与满足约束的边界条件。',question:'只把轨道代入一个给定的 E，为什么还不能叫作自洽 Vlasov–Maxwell 解？',controls:[ctl('stage','依赖环节',1,4,1,1)],draw(c,w,h,t,p){const labels=['分布 fₛ','矩：ρ、j','场：E、B','力与轨道'];const pos=[[80,55],[450,55],[450,225],[80,225]];pos.forEach(([x,y],i)=>box(c,x,y,230,65,labels[i],p.stage===i+1?C.orange:C.blue));arrow(c,320,87,115,0);arrow(c,565,130,0,75);arrow(c,435,257,-115,0);arrow(c,195,210,0,-75);return `当前环节 ${p.stage}：${['从分布描述出发','速度积分给电荷和电流','求解 Maxwell 或合适近似下的 Poisson 方程','用场推动特征线并更新分布'][p.stage-1]}。这是闭合关系，不是模拟结果。`;}});
add('energy-exchange',4,['lecture4-s12','lecture4-s13'],{
 title:'粒子能与场能：同一份 j·E，一正一负',description:'在无边界流失的归一化振荡例子中，粒子动能和场能相互转化，总和保持为 1。',equation:'∂tK+∇·Q=j·E；∂tU+∇·S=−j·E；U=(E²+B²)/(8π)，S=cE×B/(4π)。',limits:'用 K=sin²τ、U=cos²τ 说明封闭系统的交换账本，不是一般 Vlasov–Maxwell 解。仅在总边界能流为零时才能把局域守恒转为体积总能量恒定；磁力不直接做功。',question:'j·E<0 时，粒子是在从场吸能，还是把能量交还给场？',animated:true,controls:[ctl('rate','归一化振荡频率',.3,1.5,.1,1)],draw(c,w,h,t,p){const e=exchange(t*p.rate);text(c,'粒子 K',80,55,C.orange);text(c,'电磁场 U',450,55,C.blue);c.fillStyle=C.orange;c.fillRect(90,260-175*e.particle,210,175*e.particle);c.fillStyle=C.blue;c.fillRect(450,260-175*e.field,210,175*e.field);line(c,[[70,260],[690,260]],C.line);text(c,e.particle.toFixed(3),140,300,C.orange);text(c,e.field.toFixed(3),505,300,C.blue);text(c,'总能量 = 1',295,40,C.teal);arrow(c,e.power>=0?435:320,155,e.power>=0?-110:110,0,C.gray);return `K=${e.particle.toFixed(3)}，U=${e.field.toFixed(3)}；K+U=1；归一化功率 j·E=${(p.rate*e.power).toFixed(3)}（以动画时间计）。`;}});
add('stress-symmetry',4,['lecture4-s16'],{
 title:'动量通量对称，内部力矩源项相消',description:'查看总动量通量的两个交叉分量。对称时它们相等，角动量方程的内部源项为零；人为加入反对称扰动则暴露源项。',equation:'M=Π+Tem，Tem=−σMaxwell；∂tgi+∂jMij=0；角动量 z 源项 = Myx−Mxy。',limits:'张量分量账本，不是构造一个实际具有反对称 Maxwell 应力的电磁场。真实粒子通量 Πij=∫mvivjf dv 与标准 Tem 都是对称张量；非零扰动仅用作反事实对照。边界仍可输送角动量。',question:'内部源项为零，是否意味着开放边界内的角动量也绝对不变？',controls:[ctl('asym','人为反对称扰动 a（真实模型为 0）',-.5,.5,.05,0)],draw(c,w,h,t,p){box(c,95,80,230,70,'Mxy = '+(1+p.asym).toFixed(2),C.blue);box(c,435,80,230,70,'Myx = '+(1-p.asym).toFixed(2),C.orange);arrow(c,330,115,95,0,C.gray);text(c,'角动量源项 Myx − Mxy',200,220);text(c,(-2*p.asym).toFixed(3)+(p.asym===0?'：相消':'：反事实内部力矩'),215,270,p.asym===0?C.teal:C.orange);text(c,'注意：场动量通量 Tem = −σMaxwell',115,325);return `Mxy=${(1+p.asym).toFixed(2)}，Myx=${(1-p.asym).toFixed(2)}；角动量 z 源项=${(-2*p.asym).toFixed(3)}。a=0 才对应本讲标准对称通量。`;}});


add('particle-momentum-flux',4,['lecture4-s14'],{
 title:'粒子穿过面，携带各方向的动量',description:'竖直面法向为 +x。穿面速率由 vx 决定，每粒子携带的 y 动量为 mvy；两者相乘得到 Πyx。',equation:'Πij=m∫vi vj f dv；单束归一化 Πyx=vy vx；交换 i、j 后 Πxy=vx vy，故 Πxy=Πyx。',limits:'m=n=1 的单速度束几何示意；不是热平衡分布或完整动力学。真实通量须对速度分布积分，并包含有序流与随机运动。',question:'穿过 x 法向面的 y 动量通量，应取 vx² 还是 vyvx？',controls:[ctl('vx','穿面速度 vx',.3,1.5,.1,1),ctl('vy','携带 y 动量的速度 vy',-1,1,.1,.6)],draw(c,w,h,t,p){
 line(c,[[380,50],[380,315]],C.gray,4);arrow(c,390,180,110,0,C.gray);text(c,'n = +x',475,210);
 for(let j=0;j<3;j++){circle(c,380-70*p.vx,115+j*65,7,C.blue,true);arrow(c,380-70*p.vx,115+j*65,140*p.vx,-65*p.vy,C.blue);}
 text(c,'速度束：v=(vx,vy)',45,35);text(c,'携带 mvy',55,305,C.orange);text(c,'穿面速率 ∝ vx',420,75,C.teal);text(c,'Πyx = '+(p.vx*p.vy).toFixed(2),460,130);
 return `Πyx=vy vx=${(p.vx*p.vy).toFixed(3)}；Πxy=vx vy 同样为 ${(p.vx*p.vy).toFixed(3)}。这不是只保留热压的通量。`;
}});
add('field-momentum-stress',4,['lecture4-s15'],{
 title:'场动量方向与 Maxwell 应力的符号',description:'取 E 沿 +x、B 沿 +y，场动量指向 +z（屏幕外）。右侧把标准应力 σ 与守恒式里的通量 Tem=−σ 分开。',equation:'G=E×B/(4πc)；σ=(EE+BB)/(4π)−(E²+B²)I/(8π)；Tem=−σ。',limits:'均匀正交场的瞬时代数例子，不是边界受力求解。E、B 同以 B₀ 归一化；G 以 B₀²/(4πc)、应力以 B₀²/(8π) 归一化；保持 Gaussian 量纲。',question:'同一组场，为什么把 σ 直接当作 Tem 代入守恒式会把符号翻转？',controls:[ctl('E','电场 E/B₀',0,2,.1,1),ctl('B','磁场 B/B₀',0,2,.1,1)],draw(c,w,h,t,p){
 arrow(c,135,190,75*p.E,0,C.orange);arrow(c,135,190,0,-60*p.B,C.blue);text(c,'E → +x',135,235,C.orange);text(c,'B ↑ +y',55,40,C.blue);circle(c,135,190,17,C.teal);circle(c,135,190,4,C.teal,true);text(c,'G ⊙ +z',50,290,C.teal);
 const [sx,sy,sz]=fieldMomentum(p.E,p.B).sigma;
 text(c,'分量       σ        Tem = −σ',390,45);
 [sx,sy,sz].forEach((v,i)=>text(c,['xx','yy','zz'][i]+'       '+v.toFixed(2)+'        '+(-v).toFixed(2),390,110+i*65));
 return `归一化 Gz=EB=${(p.E*p.B).toFixed(3)}；σzz=${sz.toFixed(3)}，Tem,zz=${(-sz).toFixed(3)}。两种张量约定在每个分量上都相反，不能混用。`;
}});

// Shared models retain section-specific visual emphasis rather than repeating a gallery card.
const baseMu=modules['mu-action'].draw;
modules['mu-action'].draw=function(c,w,h,t,p){
 const a=adiabatic(p.B),id=p.sectionId;
 if(id==='lecture3-s2'){
  const vals=[.3,a.energy,.2],labs=['沿场动能','μB：回旋能','E×B 漂移动能'];
  vals.forEach((v,i)=>{text(c,labs[i],45,65+i*90);c.fillStyle=[C.gray,C.blue,C.teal][i];c.fillRect(260,35+i*90,210*v,48);text(c,v.toFixed(2),280+210*v,68+i*90);});
  return `本节分解 K=K∥+μB+KE：示意值 ${(.5+a.energy).toFixed(2)}=${.3}+${a.energy.toFixed(2)}+${.2}。调场改变回旋能，不等于 μ 改变；其余两项仅作固定参考。`;
 }
 if(id==='lecture3-s3'){
  text(c,'电场功率侧',70,35,C.blue);text(c,'能量导数侧：匹配后相减',400,35,C.teal);
  const terms=['μ V_E · ∇B','m v∥ V_E · ḃ','m V_E · V̇_E','μ ∂t B（Faraday）'];
  terms.forEach((term,i)=>{text(c,term,70,85+i*50,C.blue);text(c,term,420,85+i*50,C.teal);arrow(c,300,78+i*50,80,0,C.gray);});
  text(c,'四组项抵消 ⇒ B μ̇ = O(ε²)',150,315,C.orange);
  return '逐项配对：梯度漂移、曲率方向变化、极化漂移、固定瞬时回旋圆盘的 Faraday 感应。μ∂tB 是偏导项，不能替换为收缩轨道总磁通导数；当前 B/B₀='+p.B.toFixed(2)+' 不改变这一符号抵消关系。';
 }
 if(id==='lecture3-s6'){
  circle(c,220,160,80*a.rho);arrow(c,220-30,160-80*a.rho,60,0,C.blue);text(c,'局部回旋电流环',80,35);text(c,'Bπρ² / (B₀πρ₀²) = 1',70,305,C.teal);
  arrow(c,490,240,0,-120,C.blue);text(c,'外场 B',510,130);arrow(c,620,115,0,120,C.orange);text(c,'μdip = −μb',510,280,C.orange);
  return `本节重点：磁偶极矩反向于 B，且局部拉莫尔磁通不变；当前 ρ/ρ₀=${a.rho.toFixed(3)}。电流环箭头是以 B 出屏为参照的顺时针方向。右侧单独比较 B 与磁偶极方向。`;
 }
 return baseMu(c,w,h,t,p);
};
const baseMirror=modules['mirror-bounce'].draw;
modules['mirror-bounce'].draw=function(c,w,h,t,p){
 if(p.sectionId!=='lecture3-s10')return baseMirror(c,w,h,t,p);
 const s=mirror(t,p.R,p.angle),a=Math.cos(p.angle*Math.PI/180)/s.omega;
 text(c,'反弹相平面：闭轨道面积对应 ∮v∥ dz',45,35);line(c,[[90,175],[680,175]],C.line);line(c,[[380,60],[380,285]],C.line);text(c,'z',680,205);text(c,'v∥',395,65);
 if(s.trapped||s.threshold){c.beginPath();c.ellipse(380,175,Math.min(260,260*a),100*Math.cos(p.angle*Math.PI/180),0,0,T);c.strokeStyle=C.blue;c.stroke();}
 else{const pts=[];for(let i=0;i<=100;i++){const q=mirror(s.exit*i/100,p.R,p.angle);pts.push([380+260*q.z,175-100*q.v]);}line(c,pts,C.orange);}
 circle(c,380+260*s.z,175-100*s.v,7,C.teal,true);
 text(c,s.trapped||s.threshold?'闭合：可定义反弹作用量':'开放：不能用闭合反弹作用量',110,325,s.trapped?C.blue:C.orange);
 return s.trapped||s.threshold?`闭轨道归一化面积 J*=πv∥₀²/ωb=${(Math.PI*Math.cos(p.angle*Math.PI/180)**2/s.omega).toFixed(3)}；τb=${(T/s.omega).toFixed(3)}。这里 J* 未除以 2π，与正文 ∮mv∥ds 约定对应。`:'粒子穿过出口，所画轨道未闭合；本节反弹作用量的前提不成立。';
};
const baseFlow=modules['phase-flow'].draw;
modules['phase-flow'].draw=function(c,w,h,t,p){
 const id=p.sectionId,k=t*p.shear*.1;
 if(id==='lecture4-s2'){
  const X=x=>250+60*x,Y=v=>180-120*v,verts=[[-.6,-.5],[.6,-.5],[.6,.5],[-.6,.5]];
  line(c,[...verts,verts[0]].map(([x,v])=>[X(x),Y(v)]),C.gray);
  line(c,[...verts,verts[0]].map(([x,v])=>[X(x+k*v),Y(v)]),C.blue,3);
  text(c,'灰：初始；蓝：Hamilton 剪切后',55,35);text(c,'矩形 → 平行四边形',390,130);text(c,'det [[1, t],[0, 1]] = 1',390,185);text(c,'面积始终为 1.2',390,240,C.teal);
  return `剪切量=${k.toFixed(2)}；ΔxΔv=1.2；顶边和底边相对滑移，而相空间面积不变。绘图采用 0.1 倍时间缩放避免出屏。`;
 }
 if(id==='lecture4-s3'){
  for(let j=0;j<6;j++)for(let i=0;i<6;i++){const v=-.5+j*.2,x=-.5+i*.2;circle(c,250+80*(x+k*v),180-130*v,5,C.blue,true);}
  text(c,'跟随同一批 36 个示意粒子',65,35);text(c,'随体单元被剪切',440,145);text(c,'粒子数不变',440,200,C.teal);text(c,'连续极限：Df/Dt = 0',170,310);
  return '本节重点是随体粒子数守恒：36 个标记始终属于同一个剪切流体元；离散标记只用于展示，不是 PIC 求解。';
 }
 if(id==='lecture4-s6'){
  for(let j=0;j<5;j++){const v=1-j*.5;for(let i=0;i<5;i++)arrow(c,125+i*105,75+j*45,24*p.shear*v,0,C.blue);circle(c,100+((t*p.shear*v*25+1000)%500),75+j*45,5,C.orange,true);}
  text(c,'u=(v,0)：同一速度层水平平移',65,35);text(c,'∂x v + ∂v 0 = 0',220,315,C.teal);
  return '本节自由输运例子：x 方向流速虽随 v 改变，但散度取 ∂x v，而非 ∂v v；因此位置–速度相空间流不可压缩。';
 }
 return baseFlow(c,w,h,t,p);
};

if(root)root.PlasmaVisualModules=Object.assign(root.PlasmaVisualModules||{},modules);
if(typeof module!=='undefined'&&module.exports)module.exports={modules,mirror,adiabatic,covariance,potentialBoundary,jacobian,exchange,fieldMomentum,harmonicState};
})(typeof window!=='undefined'?window:null);
