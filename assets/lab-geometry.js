/* Reading Club: normalized teaching models, not fitted equilibrium / trained SNO outputs. */
(function (root) {
  'use strict';
  const TAU = 2 * Math.PI;
  const colors = {blue:'#1663b6',teal:'#087c73',orange:'#b74e20',ink:'#20334a',muted:'#64748b',line:'#d9e2ec'};
  function mxhPoint(theta, kappa, s1, s2) {
    const thetaR = theta + s1 * Math.sin(theta) + s2 * Math.sin(2 * theta);
    return {r:Math.cos(thetaR), z:kappa * Math.sin(theta), thetaR};
  }
  function oscillatorStep(q,p,h,method) {
    if (method === 'symplectic') { const nextP=p-h*q; return [q+h*nextP,nextP]; }
    if (method === 'forward') return [q+h*p,p-h*q];
    return [q*Math.cos(h)+p*Math.sin(h),p*Math.cos(h)-q*Math.sin(h)];
  }
  function oscillatorPath(h,n,method) {
    const points=[[1,0]];
    for(let i=0;i<n;i++) points.push(oscillatorStep(...points[points.length-1],h,method));
    return points;
  }
  function label(c,text,x,y,color=colors.ink) {c.fillStyle=color;c.font='20px system-ui, sans-serif';c.fillText(text,x,y);}
  function line(c,pts,color,width=2,dash=[]) {c.beginPath();pts.forEach((p,i)=>i?c.lineTo(...p):c.moveTo(...p));c.strokeStyle=color;c.lineWidth=width;c.setLineDash(dash);c.stroke();c.setLineDash([]);}
  function dot(c,x,y,color,r=5){c.beginPath();c.arc(x,y,r,0,TAU);c.fillStyle=color;c.fill();}
  function axes(c,x,y,w,h,xlabel,ylabel) {
    line(c,[[x,y],[x+w,y]],colors.line,1);line(c,[[x,y],[x,y-h]],colors.line,1);
    label(c,xlabel,x+w-36,y+24);label(c,ylabel,x+4,y-h-10);
  }
  const modules={
    mxh:{
      title:'把塑形写进角度：MXH 磁面',kicker:'几何 · 角度谐波',
      description:'蓝线保留 s₁、s₂，虚线仅保留 s₁（Miller）。移动的圆点标记参数 θ，不代表沿磁面运动的真实粒子。',
      equation:'R−R₀ = r cos θᴿ；Z−Z₀ = κr sin θ；θᴿ = θ + s₁ sin θ + s₂ sin 2θ；δ = sin s₁',
      limits:'仅显示上下对称的二维轮廓，r=1、R₀=Z₀=0。系数范围保证 dθᴿ/dθ ≥ 0.20；不求磁场、径向导数或输运，不是论文拟合结果。',
      question:'把 s₂ 调到 0，再改变 s₁：为何顶部的水平位移由 sin(s₁) 而非 s₁ 本身决定？',
      controls:[{key:'kappa',label:'伸长比 κ',min:1,max:2,step:.05,value:1.6},{key:'s1',label:'一阶角系数 s₁（弧度）',min:-.4,max:.4,step:.02,value:.3},{key:'s2',label:'二阶角系数 s₂（弧度）',min:-.2,max:.2,step:.01,value:.12}],
      draw(c,w,h,t,p){
        const {kappa,s1,s2}=p, cx=220,cy=180,scale=68;
        const map=a=>[cx+scale*a.r,cy-scale*a.z];
        line(c,[[80,cy],[360,cy]],colors.line,1);line(c,[[cx,30],[cx,325]],colors.line,1);
        label(c,'(R−R₀)/r',273,cy+25);label(c,'(Z−Z₀)/r',85,31);
        const curve=s=>Array.from({length:241},(_,i)=>map(mxhPoint(i*TAU/240,kappa,s1,s)));
        line(c,curve(0),colors.muted,2,[6,5]);line(c,curve(s2),colors.blue,3);
        const theta=(t*.65)%TAU,point=mxhPoint(theta,kappa,s1,s2),pos=map(point);
        line(c,[[cx,cy],pos],colors.teal,1.5,[4,4]);dot(c,...pos,colors.teal,6);
        label(c,'蓝线：s₁ + s₂',420,42,colors.blue);label(c,'虚线：Miller（s₂ = 0）',420,70,colors.muted);
        label(c,'角度修正 θᴿ − θ',420,118);
        const px=430,py=255,pw=320;
        line(c,[[px,py],[px+pw,py]],colors.line,1);label(c,'0',px,py+24);label(c,'2π',px+pw-22,py+24);
        const phase=Array.from({length:241},(_,i)=>{let a=i*TAU/240;return[px+pw*i/240,py-110*(s1*Math.sin(a)+s2*Math.sin(2*a))];});
        line(c,phase,colors.blue,2);dot(c,px+pw*theta/TAU,py-110*(point.thetaR-theta),colors.teal);
        label(c,'δ = '+Math.sin(s1).toFixed(3)+'；θ = '+theta.toFixed(2)+' rad',420,322);
        return 'θ = '+theta.toFixed(2)+' rad；θᴿ = '+point.thetaR.toFixed(2)+' rad；三角度 δ = '+Math.sin(s1).toFixed(3)+'。圆点是参数位置，不是粒子。';
      }
    },
    symplectic:{
      title:'保面积，不等于精确保能量',kicker:'数值结构 · 辛剪切',
      description:'对同一个简谐振子比较精确流、辛 Euler 和显式 Euler。辛方法的能量会振荡；显式 Euler 每一步都扩大相空间面积。',
      equation:'H=(q²+p²)/2；辛 Euler：pₙ₊₁=pₙ−hqₙ，qₙ₊₁=qₙ+hpₙ₊₁；det M辛=1，det M显式=1+h²',
      limits:'无量纲有限维简谐振子，初值 (q,p)=(1,0)，0<h<2 为本例辛 Euler 稳定区。最多演示 100 步；这不是 SNO 网络、训练结果或无限维定理的验证。',
      question:'增大步长 h：辛轨道仍有界时，为什么它的相位和能量仍然不完全正确？',
      controls:[{key:'h',label:'时间步长 h',min:.05,max:.3,step:.01,value:.18}],
      draw(c,w,h,t,p){
        const step=p.h,n=Math.min(100,Math.floor(t*5)),cx=205,cy=185,scale=67;
        label(c,'相空间（超出 ±2 的轨迹裁切）',35,25);
        line(c,[[65,cy],[345,cy]],colors.line,1);line(c,[[cx,45],[cx,325]],colors.line,1);label(c,'q',346,cy);label(c,'p',cx+8,47);
        label(c,'−2',61,cy+22);label(c,'2',330,cy+22);
        const types=['exact','symplectic','forward'],cols=[colors.muted,colors.blue,colors.orange];
        const paths=types.map(type=>oscillatorPath(step,100,type));
        c.save();c.beginPath();c.rect(cx-134,cy-134,268,268);c.clip();
        paths.forEach((path,j)=>{line(c,path.slice(0,n+1).map(([q,p])=>[cx+q*scale,cy-p*scale]),cols[j],j===0?2:2.5,j===0?[5,4]:[]);const [q,p]=path[n];dot(c,cx+q*scale,cy-p*scale,cols[j]);});c.restore();
        const x0=445,y0=285,pw=300,ph=220;
        axes(c,x0,y0,pw,ph,'步数 n','log₁₀(H/H₀)');
        [0,1,2,3,4].forEach(v=>{const y=y0-v*ph/4;line(c,[[x0,y],[x0+pw,y]],colors.line,1);label(c,String(v),x0-22,y+5);});
        label(c,'0',x0,y0+24);label(c,'100',x0+pw-30,y0+24);
        // The small negative energy excursions are retained below the zero line.
        paths.forEach((path,j)=>{line(c,path.slice(0,n+1).map(([q,p],i)=>[x0+pw*i/100,y0-Math.log10(q*q+p*p)*ph/4]),cols[j],2,j===0?[5,4]:[]);});
        line(c,[[x0+pw*n/100,54],[x0+pw*n/100,297]],colors.teal,1,[3,4]);
        label(c,'精确流',48,348,colors.muted);label(c,'辛 Euler',170,348,colors.blue);label(c,'显式 Euler',302,348,colors.orange);
        label(c,'n = '+n+' / 100；t = '+(n*step).toFixed(2),492,348);
        const energy=j=>{let [q,p]=paths[j][n];return q*q+p*p;};
        return '第 '+n+' / 100 步，物理时间 '+(n*step).toFixed(2)+'；H/H₀：精确 1，辛 '+energy(1).toFixed(3)+'，显式 '+energy(2).toFixed(3)+(n===100?'。已到 100 步；重置可再观察。':'。');
      }
    }
  };
  if (root) root.ReadingLabModules=Object.assign(root.ReadingLabModules||{},modules);
  if (typeof module!=='undefined' && module.exports) module.exports={mxhPoint,oscillatorStep,oscillatorPath,modules};
})(typeof window!=='undefined'?window:null);
