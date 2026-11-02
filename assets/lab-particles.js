/* Analytic, normalized teaching models; no fitted or simulated paper results. */
(function (root) {
  'use strict';
  const TAU = 2 * Math.PI;
  const C = {blue:'#1762a6', teal:'#007e76', orange:'#b34d15', ink:'#23344a', muted:'#526479', grid:'#dce5ee'};
  function text(ctx,s,x,y,color=C.ink,size=20){ctx.fillStyle=color;ctx.font=`${size}px system-ui, sans-serif`;ctx.fillText(s,x,y);}
  function line(ctx,points,color,width=2,dash=[]){ctx.beginPath();ctx.strokeStyle=color;ctx.lineWidth=width;ctx.setLineDash(dash);points.forEach((p,i)=>i?ctx.lineTo(...p):ctx.moveTo(...p));ctx.stroke();ctx.setLineDash([]);}
  function dot(ctx,x,y,color,r=7){ctx.beginPath();ctx.arc(x,y,r,0,TAU);ctx.fillStyle=color;ctx.fill();}
  function arrow(ctx,x,y,dx,dy,color){line(ctx,[[x,y],[x+dx,y+dy]],color,2);const a=Math.atan2(dy,dx);line(ctx,[[x+dx-9*Math.cos(a-.45),y+dy-9*Math.sin(a-.45)],[x+dx,y+dy],[x+dx-9*Math.cos(a+.45),y+dy-9*Math.sin(a+.45)]],color,2);}
  function gyroState(t,B,E){const phase=B*t, vd=-E/B;return {x:Math.sin(phase)/B,y:(Math.cos(phase)-1)/B+vd*t,vx:Math.cos(phase),vy:-Math.sin(phase)+vd,gx:0,gy:-1/B+vd*t,vd,rho:1/B};}
  function mirrorState(t,R,angle){const a=angle*Math.PI/180,mu=Math.sin(a)**2,v0=Math.cos(a),omega=Math.sqrt(mu*(R-1)),threshold=Math.abs(mu*R-1)<=1e-12,amplitude=threshold?1:v0/omega;const trapped=mu*R>1+1e-12;const confined=trapped||threshold;const exitTime=confined?Infinity:Math.asin(1/amplitude)/omega;const time=Math.min(t,exitTime);const z=amplitude*Math.sin(omega*time),v=v0*Math.cos(omega*time),B=1+(R-1)*z*z;return {z,v,B,mu,perpendicular:mu*B,parallel:v*v,trapped,threshold,escaped:t>=exitTime,exitTime,amplitude,omega,critical:Math.asin(1/Math.sqrt(R))*180/Math.PI};}
  function waveState(k,dk){const k1=k-dk/2,k2=k+dk/2,w1=Math.sqrt(1+3*k1*k1),w2=Math.sqrt(1+3*k2*k2);return {k1,k2,w1,w2,kbar:k,wbar:(w1+w2)/2,dk,dw:w2-w1,phase:(w1+w2)/(2*k),group:(w2-w1)/dk,derivative:3*k/Math.sqrt(1+3*k*k)};}
  const modules={
    gyro:{
      title:'回旋与 E×B 漂移', kicker:'Lecture 2 · 单粒子运动',
      description:'磁场沿 +z 指向屏幕外，电场沿 +x。蓝点绕青色导心转动；增加电场，整条轨道向 −y 漂移。试着让电场为零，再增加磁场。',
      equation:'Ω = B，ρ = 1/B，v_E = −E/B；x = sin(Bt)/B，y = [cos(Bt)−1]/B − Et/B。',
      limits:'正电荷非相对论、均匀静态场；沿用讲义 Gaussian 单位，以 Ω₀⁻¹（Ω₀=qB₀/(mc)）、v₀≪c、v₀/Ω₀ 归一化时间、速度与长度，B 以 B₀、E 以 v₀B₀/c 归一化；初始相对导心速度为 +x 方向的 1。随导心平移的视窗，不是粒子被困在固定窗口；无碰撞、无梯度漂移。',
      question:'为什么 B 增大时回旋更快、半径更小，而 E×B 漂移更慢？',
      controls:[{key:'B',label:'磁场 B',min:0.6,max:2,step:0.1,value:1},{key:'E',label:'电场 E',min:0,max:0.6,step:0.05,value:0.25}],
      draw(ctx,w,h,t,p){const s=gyroState(t,p.B,p.E),scale=65,cx=w*.5,cy=h*.53;const X=x=>cx+x*scale,Y=y=>cy-(y-s.gy)*scale;
        for(let j=-3;j<=3;j++)line(ctx,[[cx+j*65,65],[cx+j*65,h-40]],C.grid,1);
        for(let j=-2;j<=2;j++)line(ctx,[[100,cy+j*65],[w-100,cy+j*65]],C.grid,1);
        text(ctx,'随导心平移的视窗 · B ⊙',22,28);arrow(ctx,w-145,60,65,0,C.orange);text(ctx,'E → +x',w-150,91,C.orange);
        arrow(ctx,65,135,0,-55,C.muted);text(ctx,'+y',48,70,C.muted);arrow(ctx,65,135,45,0,C.muted);text(ctx,'+x',90,160,C.muted);
        const pts=[];for(let i=0;i<=220;i++){const u=Math.max(0,t-10)+(t-Math.max(0,t-10))*i/220;const a=gyroState(u,p.B,p.E);pts.push([X(a.x),Y(a.y)]);}ctx.save();ctx.beginPath();ctx.rect(100,45,w-200,h-80);ctx.clip();line(ctx,pts,C.blue,2.5);ctx.restore();
        ctx.beginPath();ctx.strokeStyle=C.teal;ctx.setLineDash([5,5]);ctx.arc(cx,cy,s.rho*scale,0,TAU);ctx.stroke();ctx.setLineDash([]);dot(ctx,cx,cy,C.teal,5);dot(ctx,X(s.x),Y(s.y),C.blue,8);line(ctx,[[cx,cy],[X(s.x),Y(s.y)]],C.teal,1,[3,4]);text(ctx,'导心',cx+12,cy+25,C.teal);
        if(p.E>0)arrow(ctx,w-80,190,0,50,C.teal);text(ctx,'漂移 −y',w-135,270,C.teal);text(ctx,`ρ = ${s.rho.toFixed(2)}     Ω = ${p.B.toFixed(2)}     v_E,y = ${s.vd.toFixed(2)}`,22,h-14);
        return `t = ${t.toFixed(1)}；实验室坐标 x = ${s.x.toFixed(2)}，y = ${s.y.toFixed(2)}；导心向 −y 漂移，回旋半径 ${s.rho.toFixed(2)}。`;
      }
    },
    mirror:{
      title:'磁镜：反弹还是逃逸？',kicker:'Lecture 3 · 绝热不变量',
      description:'粒子从磁场最弱的中心向右出发。保持总动能和磁矩不变，磁场越强，垂直动能越多、平行动能越少；落入损失锥的粒子穿过边界，不会反弹。',
      equation:'B(z)=1+(R−1)z²；v∥²+v⊥²=1，μ=v⊥²/B=sin²α₀；z̈=−μ(R−1)z。镜内反弹：sin²α₀ > 1/R；等号恰在边界转向。',
      limits:'一维导心、静磁场、无电势与碰撞；μ 在此用 v⊥²/B 归一化。管宽仅表示磁通守恒趋势，不是完整三维磁场解。边界 |z|=1；逃逸后停留在出口标记，需重置再次发射。',
      question:'把初始俯仰角降到临界角以下，平行动能在出口还剩多少？',
      controls:[{key:'R',label:'镜比 R = B边界/B中心',min:1.2,max:5,step:0.1,value:3},{key:'angle',label:'中心俯仰角 α₀（度）',min:10,max:80,step:1,value:50}],
      draw(ctx,w,h,t,p){const s=mirrorState(t,p.R,p.angle),cx=w/2,cy=145,half=w*.37;const X=z=>cx+z*half;
        text(ctx,`临界角 αc = ${s.critical.toFixed(1)}° · ${s.threshold?'临界轨道：边界转向':s.trapped?'镜内反弹轨道':'损失锥内：将穿过右边界'}`,22,28,(s.trapped||s.threshold)?C.teal:C.orange);
        for(const sign of [-1,1]){const pts=[];for(let i=0;i<=120;i++){const z=-1+i/60;pts.push([X(z),cy+sign*56/Math.sqrt(1+(p.R-1)*z*z)]);}line(ctx,pts,C.blue,2.5);}
        line(ctx,[[X(-1),cy],[X(1),cy]],C.grid,1,[4,4]);for(const z of [-1,0,1]){line(ctx,[[X(z),70],[X(z),220]],C.grid,1,[3,4]);text(ctx,`z = ${z}`,X(z)-25,240,C.muted);}
        dot(ctx,X(s.z),cy,s.escaped?C.orange:C.teal,9);if(!s.escaped)arrow(ctx,X(s.z),cy-17,45*s.v,0,C.teal);else arrow(ctx,X(1)+10,cy,35,0,C.orange);
        text(ctx,s.escaped?'已穿过出口 · 无人工反射':`当前位置 B/B₀ = ${s.B.toFixed(2)}`,22,275,s.escaped?C.orange:C.ink);
        const barX=180,barY=297,barW=w-220;ctx.fillStyle=C.teal;ctx.fillRect(barX,barY,barW*s.perpendicular,22);ctx.fillStyle=C.orange;ctx.fillRect(barX+barW*s.perpendicular,barY,barW*s.parallel,22);text(ctx,'归一化动能',22,315);text(ctx,`垂直 ${s.perpendicular.toFixed(2)} + 平行 ${s.parallel.toFixed(2)} = 1`,180,344);
        return `${s.escaped?'粒子已逃逸':s.threshold?'临界轨道：边界转向':s.trapped?'镜内反弹':'尚在向出口运动'}；z = ${s.z.toFixed(3)}，v∥ = ${s.v.toFixed(3)}；动能和 = ${(s.parallel+s.perpendicular).toFixed(6)}，μ = ${s.mu.toFixed(3)}。`;
      }
    },
    waves:{
      title:'Langmuir 波：波峰与包络不同速',kicker:'Lecture 6 · 色散与压力闭合',
      description:'叠加两个振幅相同、波数相近的 Langmuir 波。蓝色细波峰快速移动，橙色拍频包络缓慢移动；它们不是同一个速度。',
      equation:'ω²=1+3k²；cos(k₁x−ω₁t)+cos(k₂x−ω₂t)=2cos[(Δkx−Δωt)/2]cos(k̄x−ω̄t)。v相=ω̄/k̄，v拍=Δω/Δk。',
      limits:'x 以 λD、t 以 ωp⁻¹ 归一化，vT²=Te/m；采用 γ=3、kλD ≪ 1 的流体近似，忽略 Landau 阻尼。两单色波形成无限拍频列，并非局域波包；拍速仅在 Δk→0 时趋于群速 dω/dk。',
      question:'为什么波峰会穿过包络，而不是与包络一起前进？',
      controls:[{key:'k',label:'中心波数 k̄ λD',min:0.10,max:0.25,step:0.01,value:0.18},{key:'dk',label:'波数间隔 Δk λD',min:0.02,max:0.08,step:0.01,value:0.06}],
      draw(ctx,w,h,t,p){const s=waveState(p.k,p.dk),left=55,right=w-25,mid=180,scale=52,xmax=180;const X=x=>left+x/xmax*(right-left);line(ctx,[[left,mid],[right,mid]],C.grid,1);
        for(let x=0;x<=xmax;x+=30){line(ctx,[[X(x),60],[X(x),300]],C.grid,1);text(ctx,String(x),X(x)-8,323,C.muted,20);}
        const curve=[],upper=[],lower=[];for(let i=0;i<=800;i++){const x=xmax*i/800,envelope=2*Math.cos((s.dk*x-s.dw*t)/2),value=Math.cos(s.k1*x-s.w1*t)+Math.cos(s.k2*x-s.w2*t);curve.push([X(x),mid-scale*value]);upper.push([X(x),mid-scale*envelope]);lower.push([X(x),mid+scale*envelope]);}line(ctx,upper,C.orange,2,[7,5]);line(ctx,lower,C.orange,2,[7,5]);line(ctx,curve,C.blue,2);
        text(ctx,'蓝：两波叠加     橙虚线：±2 cos[(Δkx−Δωt)/2]',22,28);text(ctx,`v相 = ${s.phase.toFixed(2)}     v拍 = ${s.group.toFixed(3)}     dω/dk = ${s.derivative.toFixed(3)}`,22,53);text(ctx,'x / λD',w-83,346,C.muted,20);
        return `tωp = ${t.toFixed(1)}；相速度 ${s.phase.toFixed(3)}，拍频包络速度 ${s.group.toFixed(3)}；两者均以 vT 归一化。`;
      }
    }
  };
  if(root)root.ReadingLabModules=Object.assign(root.ReadingLabModules||{},modules);
  if(typeof module!=='undefined'&&module.exports)module.exports={gyroState,mirrorState,waveState,modules};
})(typeof window!=='undefined'?window:null);
