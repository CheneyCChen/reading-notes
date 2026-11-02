/* In-page, lazy-rendered teaching diagrams. No gallery, network, storage or autoplay. */
(() => {
'use strict';
const modules=window.PlasmaVisualModules||{};
const coverage=JSON.parse(document.getElementById('plasma-visual-coverage').textContent);
const states=[];
const el=(tag,cls,text)=>{const n=document.createElement(tag);if(cls)n.className=cls;if(text!==undefined)n.textContent=text;return n;};
for(const item of coverage){
 const host=document.getElementById('visual-'+item.sectionId),base=modules[item.moduleId];
 const m=base?{...base,...(base.sectionOverrides||{})[item.sectionId]}:null;
 if(!host||!m)continue;
 const animated=m.animated&&item.kind!=='static';
 const title=el('h4','pv-heading',m.title);title.id='visual-title-'+item.sectionId;host.setAttribute('aria-labelledby',title.id);
 host.append(el('div','pv-kind',animated?'本节可视化 · 时间演化':'本节可视化 · 参数关系／概念图'),title,el('p','pv-context',item.note),el('p','pv-description',m.description),el('p','pv-equation',m.equation));
 const wrap=el('div','pv-canvas-wrap');wrap.tabIndex=0;wrap.setAttribute('aria-label','图示区域，放大后可横向滚动');
 const canvas=el('canvas');canvas.width=1;canvas.height=1;canvas.setAttribute('role','img');canvas.setAttribute('aria-label',m.title+'；关键数值和解释见下方文字。');canvas.textContent='图形不可用时请阅读下方公式与数值说明。';wrap.append(canvas);
 const controls=el('div','pv-controls'),actions=el('div','pv-actions'),status=el('p','pv-status','图示进入视野后加载；不会自动播放。');
 const state={host,canvas,params:{sectionId:item.sectionId},inputs:[],visible:false,playing:false,t:0,last:null,raf:0};
 const play=el('button','pv-play','播放'),reset=el('button','','重置'),step=el('button','','前进 0.1'),zoom=el('button','','放大图示');
 for(const b of [play,reset,step,zoom])b.type='button';play.setAttribute('aria-pressed','false');zoom.setAttribute('aria-pressed','false');
 const timeLabel=el('label','pv-time','时间'),time=el('input'),timeOut=el('output','','0.00');time.type='range';Object.assign(time,{min:0,max:20,step:.01,value:0});time.setAttribute('aria-label',item.sectionId+'：归一化时间');timeLabel.append(time,timeOut);
 function render(force=false){if(!state.visible&&!force)return;if(canvas.width!==760){canvas.width=760;canvas.height=340;}const c=canvas.getContext('2d');if(!c){status.textContent='浏览器画布不可用；公式与正文仍可阅读。';return;}c.clearRect(0,0,760,340);c.save();status.textContent=m.draw(c,760,340,state.t,state.params)||'';c.restore();time.value=state.t;timeOut.value=state.t.toFixed(2);}
 function stop(){state.playing=false;state.last=null;cancelAnimationFrame(state.raf);state.raf=0;play.textContent='播放';play.setAttribute('aria-pressed','false');}
 function tick(now){state.raf=0;if(!state.playing||!state.visible||document.hidden){state.last=null;return;}if(state.last!==null)state.t=Math.min(20,state.t+Math.min(.05,(now-state.last)/1000));state.last=now;render();if(state.t>=20)stop();else state.raf=requestAnimationFrame(tick);}
 state.wake=()=>{state.last=null;if(state.visible){render();if(state.playing&&!document.hidden&&!state.raf)state.raf=requestAnimationFrame(tick);}else{cancelAnimationFrame(state.raf);state.raf=0;canvas.width=1;canvas.height=1;}};
 state.print=()=>render(true);
 for(const def of m.controls||[]){state.params[def.key]=def.value;if((m.hiddenControls||[]).includes(def.key))continue;const label=el('label','pv-control',def.label),out=el('output','',String(def.value)),input=el('input');input.type='range';Object.assign(input,{min:def.min,max:def.max,step:def.step,value:def.value});input.setAttribute('aria-label',item.sectionId+'：'+def.label);state.params[def.key]=def.value;input.addEventListener('input',()=>{state.params[def.key]=Number(input.value);out.value=input.value;render();});state.inputs.push({input,out,def});label.append(out,input);controls.append(label);}
 play.addEventListener('click',()=>{if(state.playing)stop();else{if(state.t>=20)state.t=0;state.playing=true;play.textContent='暂停';play.setAttribute('aria-pressed','true');state.wake();}});
 reset.addEventListener('click',()=>{stop();state.t=0;for(const{input,out,def}of state.inputs){input.value=def.value;out.value=def.value;state.params[def.key]=def.value;}render();});
 step.addEventListener('click',()=>{stop();state.t=Math.min(20,state.t+.1);render();});time.addEventListener('input',()=>{stop();state.t=Number(time.value);render();});
 zoom.addEventListener('click',()=>{const on=wrap.classList.toggle('pv-zoom');zoom.textContent=on?'适合页面':'放大图示';zoom.setAttribute('aria-pressed',String(on));});
 if(animated)actions.append(play,step);actions.append(reset,zoom);if(animated)actions.append(timeLabel);
 host.append(wrap,controls,actions,el('p','pv-zoom-note','窄屏看不清标注时，选择“放大图示”并左右滑动。'),status,el('p','pv-question','观察问题：'+m.question),el('p','pv-limits','模型边界：'+m.limits));states.push(state);
}
const observer=new IntersectionObserver(entries=>{for(const e of entries){const s=states.find(x=>x.host===e.target);s.visible=e.isIntersecting;s.wake();}},{threshold:0});states.forEach(s=>observer.observe(s.host));
document.addEventListener('visibilitychange',()=>states.forEach(s=>s.wake()));
matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change',e=>{if(e.matches)for(const s of states)if(s.playing)s.host.querySelector('.pv-play').click();});
window.addEventListener('beforeprint',()=>states.forEach(s=>s.print()));window.addEventListener('afterprint',()=>states.forEach(s=>s.wake()));
})();
