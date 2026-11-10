/* Exercise the map/cross-link reset handler without a browser dependency. */
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),path=require('node:path');
const code=fs.readFileSync(path.join(__dirname,'../reports/plasma-lectures/source/course-map.js'),'utf8');
let listener,search,clicks,closed;
const document={addEventListener:(name,handler)=>{assert.equal(name,'click');listener=handler},getElementById:id=>{assert.equal(id,'search');return search},querySelector:selector=>{assert.equal(selector,'[data-filter="all"]');return{click:()=>clicks++}},body:{classList:{remove:name=>{assert.equal(name,'nav-open');closed++}}}};
vm.runInNewContext(code,{document});
for(const within of ['map','crosslink',null])for(const modified of [false,true]){
 search={value:'Rosenbluth'};clicks=0;closed=0;
 const link={closest:()=>within};
 const event={target:{closest:()=>link},defaultPrevented:false,button:0,metaKey:modified,ctrlKey:false,shiftKey:false,altKey:false,preventDefault:()=>{throw Error('Must preserve native navigation')}};
 listener(event);
 const active=!!within&&!modified;
 assert.equal(clicks,active?1:0);assert.equal(closed,active?1:0);assert.equal(search.value,active?'':'Rosenbluth');
}
console.log('PASS: map and supplementary links reset search/filter/mobile drawer only for ordinary clicks; native hash history and modified-click behavior preserved.');
