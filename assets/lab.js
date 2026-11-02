/* No dependencies, fetches, storage, or automatic motion. Works from file://. */
(() => {
  'use strict';
  const modules = window.ReadingLabModules || {};
  const selected = new URLSearchParams(location.search).get('module');
  const embedded = !!selected && window.parent !== window;
  if (embedded) document.body.classList.add('embedded');
  const sources = {
    gyro: ['../reports/plasma-lectures/index.html#lecture2-s5', 'Lecture 2 · E×B 漂移'],
    mirror: ['../reports/plasma-lectures/index.html#lecture3-s8', 'Lecture 3 · 镜力与损失锥'],
    waves: ['../reports/plasma-lectures/index.html#lecture6-s10', 'Lecture 6 · Langmuir 色散'],
    mxh: ['../reports/mxh-2021-reading/report.html#model', 'MXH · 方法核心'],
    symplectic: ['../reports/symplectic-neural-operator-reading/report.html#lab-symplectic', '辛神经算子 · 几何结构']
  };
  const root = document.querySelector('#experiments');
  const states = [];
  let parentVisible = !embedded;
  function el(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }
  Object.entries(modules).filter(([id]) => !selected || selected === id).forEach(([id, m]) => {
    const card = el('section', 'experiment'); card.id = id;
    const heading = el('h2', '', m.title); heading.id = `${id}-title`; card.setAttribute('aria-labelledby', heading.id);
    card.append(el('p', 'eyebrow', m.kicker), heading, el('p', 'description', m.description), el('p', 'equation', m.equation));
    const canvas = el('canvas'); canvas.width = 800; canvas.height = 360; canvas.setAttribute('role', 'img');
    canvas.setAttribute('aria-label', `${m.title}示意图；图形变化的数值摘要在下方。`);
    canvas.textContent = '浏览器不支持画布，请阅读下方公式和状态摘要。';
    const controls = el('div', 'lab-controls');
    const actions = el('div', 'lab-actions');
    const play = el('button', '', '播放'); play.type = 'button'; play.setAttribute('aria-pressed', 'false');
    const reset = el('button', '', '重置'); reset.type = 'button';
    const step = el('button', '', '前进 0.1'); step.type = 'button';
    const timeLabel = el('label', 'lab-time', '时间');
    const time = el('input'); time.type = 'range'; time.min = 0; time.max = 20; time.step = .01; time.value = 0; time.setAttribute('aria-label', `${m.title}归一化时间`);
    const timeValue = el('output', '', '0.00'); timeLabel.append(time, timeValue);
    actions.append(play, reset, step, timeLabel);
    const status = el('p', 'lab-status');
    const state = {card, m, canvas, context: canvas.getContext('2d'), params:{}, inputs:[], playing:false, visible:false, t:0, last:null, raf:0};
    function render() {
      const ctx = state.context;
      if (!ctx) { status.textContent = '画布不可用。仍可阅读公式、模型说明与原文。'; return; }
      ctx.clearRect(0,0,800,360); ctx.save();
      status.textContent = m.draw(ctx,800,360,state.t,state.params) || '';
      ctx.restore(); time.value = state.t; timeValue.value = state.t.toFixed(2);
    }
    function stop() { state.playing=false; state.last=null; play.textContent='播放'; play.setAttribute('aria-pressed','false'); cancelAnimationFrame(state.raf); state.raf=0; }
    function tick(now) {
      state.raf=0;
      if (!state.playing || !state.visible || !parentVisible || document.hidden) { state.last=null; return; }
      if(state.last !== null) state.t=Math.min(20,state.t+Math.min((now-state.last)/1000,.05));
      state.last=now; render();
      if(state.t>=20) stop(); else state.raf=requestAnimationFrame(tick);
    }
    state.wake=()=>{state.last=null;if(state.playing && state.visible && parentVisible && !document.hidden && !state.raf) state.raf=requestAnimationFrame(tick);};
    m.controls.forEach(c=>{
      const label=el('label','lab-control',c.label), output=el('output','',String(c.value)), input=el('input');
      input.type='range'; Object.assign(input,{min:c.min,max:c.max,step:c.step,value:c.value}); input.setAttribute('aria-label',`${m.title}：${c.label}`);
      state.params[c.key]=c.value;
      input.addEventListener('input',()=>{state.params[c.key]=Number(input.value);output.value=input.value;render();});
      state.inputs.push({input,output,c});label.append(output,input);controls.append(label);
    });
    play.addEventListener('click',()=>{if(state.playing) stop();else {if(state.t>=20)state.t=0;state.playing=true;play.textContent='暂停';play.setAttribute('aria-pressed','true');state.wake();}});
    reset.addEventListener('click',()=>{stop();state.t=0;state.inputs.forEach(({input,output,c})=>{input.value=c.value;output.value=c.value;state.params[c.key]=c.value;});render();});
    step.addEventListener('click',()=>{stop();state.t=Math.min(20,state.t+.1);render();});
    time.addEventListener('input',()=>{stop();state.t=Number(time.value);render();});
    card.append(canvas,controls,actions,status,el('p','lab-question',`试着想一想：${m.question}`),el('p','lab-limits',`模型边界：${m.limits}`));
    const source=el('p','lab-source');const a=el('a','',`回到阅读：${sources[id][1]}`);a.href=sources[id][0];if(embedded)a.target='_parent';source.append(a);
    const standalone=el('a','standalone-link',' · 打开完整实验室 ↗');standalone.href=`index.html#${id}`;standalone.target='_parent';source.append(standalone);card.append(source);
    root.append(card); states.push(state);render();
  });
  if (!states.length) root.append(el('p','','未找到这个实验。请从实验目录选择。'));
  const observer = new IntersectionObserver(entries=>entries.forEach(entry=>{const s=states.find(x=>x.card===entry.target);s.visible=entry.isIntersecting;s.wake();}),{threshold:0});
  states.forEach(s=>observer.observe(s.card));
  document.addEventListener('visibilitychange',()=>states.forEach(s=>s.wake()));
  const reduced=matchMedia('(prefers-reduced-motion: reduce)');
  reduced.addEventListener('change',()=>{if(reduced.matches)states.forEach(s=>{if(s.playing)s.card.querySelector('.lab-actions button').click();});});
  window.addEventListener('message',event=>{if(event.source!==parent || event.data?.type!=='reading-lab-visible')return;parentVisible=!!event.data.visible;states.forEach(s=>s.wake());});
  if(embedded){const resize=new ResizeObserver(()=>parent.postMessage({type:'reading-lab-height',height:Math.ceil(document.body.getBoundingClientRect().height)},'*'));resize.observe(document.body);parent.postMessage({type:'reading-lab-ready'},'*');}
})();
