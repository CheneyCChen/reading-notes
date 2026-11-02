/* Isolate diagrams from report styles; pause computation outside the viewport. */
(() => {
  'use strict';
  const frames = [...document.querySelectorAll('iframe.reading-lab-frame')];
  const visible = new Map();
  const send = frame => frame.contentWindow?.postMessage({type:'reading-lab-visible',visible:!!visible.get(frame) && !document.hidden},'*');
  const observer = new IntersectionObserver(entries=>entries.forEach(entry=>{visible.set(entry.target,entry.isIntersecting);send(entry.target);}),{threshold:0});
  frames.forEach(frame=>{observer.observe(frame);frame.addEventListener('load',()=>send(frame));});
  document.addEventListener('visibilitychange',()=>frames.forEach(send));
  window.addEventListener('message',event=>{
    const frame=frames.find(f=>f.contentWindow===event.source);if(!frame)return;
    if(event.data?.type==='reading-lab-ready')send(frame);
    if(event.data?.type==='reading-lab-height' && Number.isFinite(event.data.height))frame.style.height=`${Math.max(400,Math.min(2200,event.data.height+4))}px`;
  });
})();
