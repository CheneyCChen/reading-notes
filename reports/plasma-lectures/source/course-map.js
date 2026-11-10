/* Keep native fragment links usable when a lecture/search filter is active. */
(()=>{
  document.addEventListener('click',event=>{
    const link=event.target.closest('a[href^="#lecture"],a[href^="#supplement"]');
    if(!link||!link.closest('#course-map,.supplement-crosslinks')||event.defaultPrevented||event.button!==0||event.metaKey||event.ctrlKey||event.shiftKey||event.altKey)return;
    const search=document.getElementById('search');
    if(search)search.value='';
    const all=document.querySelector('[data-filter="all"]');
    if(all)all.click();
    else if(search)search.dispatchEvent(new Event('input',{bubbles:true}));
    document.body.classList.remove('nav-open');
    // Do not preventDefault: browser history, URLs and no-JS navigation stay native.
  });
})();
