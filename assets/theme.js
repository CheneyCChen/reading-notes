/* Keep one theme across the index, reports and the original course controls. */
(()=>{
  const key='reading-club-theme';
  const root=document.documentElement;
  let preference=null;
  try{preference=localStorage.getItem(key)}catch{}
  const system=window.matchMedia('(prefers-color-scheme: dark)');
  function apply(theme){
    root.dataset.theme=theme;
    if(!document.body)return;
    document.body.classList.toggle('night',theme==='dark');
    document.querySelectorAll('[data-theme-toggle]').forEach(button=>{
      button.setAttribute('aria-pressed',String(theme==='dark'));
      button.setAttribute('aria-label',theme==='dark'?'切换到浅色模式':'切换到深色模式');
      button.title=theme==='dark'?'切换到浅色模式':'切换到深色模式';
    });
    const course=document.querySelector('.reading-course #theme');
    if(course){course.textContent=theme==='dark'?'日间':'夜间';course.setAttribute('aria-pressed',String(theme==='dark'))}
  }
  function toggle(){preference=root.dataset.theme==='dark'?'light':'dark';try{localStorage.setItem(key,preference)}catch{}apply(preference)}
  apply(preference==='dark'||preference==='light'?preference:system.matches?'dark':'light');
  document.addEventListener('DOMContentLoaded',()=>{
    apply(root.dataset.theme);
    document.querySelectorAll('[data-theme-toggle]').forEach(button=>button.addEventListener('click',toggle));
    const course=document.querySelector('.reading-course #theme');
    if(course)course.onclick=toggle;
  });
  system.addEventListener('change',event=>{if(!preference)apply(event.matches?'dark':'light')});
  window.addEventListener('storage',event=>{if(event.key===key){preference=event.newValue;apply(preference==='dark'||preference==='light'?preference:system.matches?'dark':'light')}});
})();
