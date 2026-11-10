/* Add Lecture 7 without rebuilding or changing the first six lecture articles.
 * Requires KaTeX 0.16.x: set KATEX_PATH if it is not locally installed.
 * Run prepare-plasma-l7.py first only when changing the supplied source text.
 */
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');
const katex = require(process.env.KATEX_PATH || 'katex');
const root = path.resolve(__dirname, '..');
const course = path.join(root, 'reports/plasma-lectures');
const source = path.join(course, 'source');
const content = JSON.parse(fs.readFileSync(path.join(source, 'lecture07-content.json'), 'utf8'));
const target = path.join(course, 'index.html');
let text = fs.readFileSync(target, 'utf8');
const old = text;
const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const decode = s => s.replace(/&amp;/g,'&').replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&quot;/g,'"').replace(/&#39;/g,"'");
let mathCount = 0;
const tags = [];
function render(html) {
  return html.replace(/<span\s+class="math (display|inline)">([\s\S]*?)<\/span>/g, (_, mode, source) => {
    let tex = decode(source).trim().slice(2,-2).replace(/\\label\{[^}]+\}/g,'');
    const tag = /\\tag\{([^}]+)\}/.exec(tex)?.[1];
    if (tag) tags.push(tag);
    const rendered = katex.renderToString(tex,{displayMode:mode==='display',throwOnError:true,strict:'ignore',trust:false});
    mathCount++;
    return tag ? `<span id="eq-${tag}" data-equation="${tag}">${rendered}</span>` : mode==='inline' ? `<span class="l7-inline-math">${rendered}</span>` : rendered;
  });
}
const sourceLink = pages => `<a href="#" class="source" data-pdf="6" data-page="${pages.match(/\d+/)[0]}">原讲义 p.${pages} ↗</a>`;
const nav = '<div class="nav-group" data-lecture7-nav><a class="nav-major" href="#lecture7"><span>07</span>'+esc(content.title)+'</a>'+content.sections.map((s,i)=>`<a href="#lecture7-s${i+1}" class="nav-sub">${esc(s.title)}</a>`).join('')+'</div>';
const sectionHTML = content.sections.map((s,i)=>`<section class="study-section searchable" id="lecture7-s${i+1}" data-lecture="7"><div class="section-meta"><span>讲次 7 · ${i+1}</span>${sourceLink(s.pages)}</div><h3>${esc(s.title)}</h3><div class="prose">${render(s.html)}</div><label class="done"><input type="checkbox" data-done="lecture7-s${i+1}"> 我能不看答案复现本节推导</label></section>`).join('\n');
const cleanQuestion = s => s.trim().replace(/^<p>/,'').replace(/<\/p>$/,'');
const article = `<article id="lecture7" class="lecture" data-lecture="7"><header class="chapter-header"><div class="eyebrow">LECTURE 07 · 12 页原文</div><h2>${esc(content.title)}</h2><p>${esc(content.summary)}</p><div class="objectives">${content.objectives.map(o=>'<span>'+esc(o)+'</span>').join('')}</div><button class="pdf-button" data-pdf="6" data-page="1">打开本讲原件 ↗</button></header>${sectionHTML}<section class="study-section searchable quiz" data-lecture="7" id="lecture7-quiz"><div class="eyebrow">ACTIVE RECALL</div><h3>自测与回忆</h3><p>以下 14 题完整保留原讲义自测。先在纸上作答，再展开作为学习补充的参考答案，核对假设、符号和适用范围。</p>${content.questions.map((q,i)=>`<details><summary>${i+1}. ${cleanQuestion(render(q.q))}</summary><div class="answer prose">${render(q.a)}</div></details>`).join('')}</section><section class="study-section searchable cautions" data-lecture="7" id="lecture7-cautions"><div class="eyebrow">READ CRITICALLY</div><h3>条件、易错点与原稿核对</h3><div class="prose">${render(content.cautions)}</div></section><section class="study-section searchable" data-lecture="7" id="lecture7-references"><div class="section-meta"><span>原始文献</span>${sourceLink('12')}</div><h3>参考文献</h3><div class="prose">${render(content.references)}</div><p class="source-key">原讲义更新于 2026-11-03；使用用户提供的中文全译版及 LaTeX 源码核查，原 PDF 以原始字节内嵌。</p></section></article>`;
assert.equal(tags.length,73);
assert.equal(new Set(tags).size,73);
assert.equal(content.sections.length,19);
const block = (name, value) => `<!-- PLASMA-L7:${name}:start -->${value}<!-- PLASMA-L7:${name}:end -->`;
const install = (name, value, anchor) => {
  const pattern = new RegExp(`<!-- PLASMA-L7:${name}:start -->[\\s\\S]*?<!-- PLASMA-L7:${name}:end -->`);
  if (pattern.test(text)) text = text.replace(pattern, () => block(name,value));
  else { assert(text.includes(anchor), `Missing ${name} anchor`); text=text.replace(anchor,()=>block(name,value)+anchor); }
};
install('nav',nav,'</nav>');
install('article',article,'<footer class="foot">');
install('style','<style>.reading-course #lecture7 .correction,.reading-course #lecture7 .learning-note{border-top:1px solid var(--line);margin-top:1.6em;padding-top:.75em}.reading-course #lecture7 .correction>p:first-child>span:first-child{font-weight:600}.reading-course #lecture7 .footnotes{font-size:.85em;overflow-wrap:anywhere}.reading-course #lecture7 .learning-note h4{font-size:1em;margin:.4em 0}.reading-course #lecture7 [data-equation]{display:block;max-width:100%;position:relative}.reading-course #lecture7 .l7-inline-math{display:inline-block;max-width:100%;overflow-x:auto;overflow-y:hidden;vertical-align:middle;position:relative}.reading-course #lecture7 .katex-display{position:relative;max-width:100%}.reading-course #lecture7 .katex-mathml{contain:strict;clip-path:inset(50%)}</style>','</head>');
text=text.replace(/等离子体物理讲义自学手册 Lecture 1[—–-][567]/,'等离子体物理讲义自学手册 Lecture 1—7');
text=text.replace('LECTURES 01–06','LECTURES 01–07').replace('<strong>6</strong><span>讲原始材料','<strong>7</strong><span>讲原始材料').replace('<strong>69</strong><span>页原文','<strong>81</strong><span>页原文').replace('<strong>89</strong><span>个学习单元','<strong>108</strong><span>个学习单元').replace('六份讲义整理','七份讲义整理');
text=text.replace('Lecture 6 的流体矩、波与无碰撞闭合。','Lecture 6 的流体矩、波与无碰撞闭合 → Lecture 7 的输运与有碰撞闭合。');
if (!text.includes('data-filter="7"')) text=text.replace('<button data-filter="6">06 无碰撞流体</button>','<button data-filter="6">06 无碰撞流体</button><button data-filter="7">07 输运与闭合</button>');
text=text.replace(/更新日期 2026-10-28 · 本地自学版。六份 PDF/,'更新日期 2026-11-09 · 本地自学版。七份 PDF');
const pdfPattern=/<script id="pdf-data" type="application\/json">([\s\S]*?)<\/script>/;
const originalPDFs=JSON.parse(old.match(pdfPattern)[1]);
const pdfs=JSON.parse(text.match(pdfPattern)[1]);
assert([6,7].includes(pdfs.length));
const bytes=fs.readFileSync(path.join(source,'Lecture07.pdf'));
pdfs[6]={name:'Lecture07.pdf',pages:12,sha256:crypto.createHash('sha256').update(bytes).digest('hex'),base64:bytes.toString('base64')};
text=text.replace(pdfPattern,()=>`<script id="pdf-data" type="application/json">${JSON.stringify(pdfs)}</script>`);
for(let i=1;i<=6;i++) {
  const rx=new RegExp(`<article id="lecture${i}"[\\s\\S]*?<\\/article>`);
  assert.equal(text.match(rx)[0],old.match(rx)[0],`Lecture ${i} changed`);
}
assert.deepEqual(pdfs.slice(0,6),originalPDFs.slice(0,6));
fs.writeFileSync(target,text);
// Preserve the reviewed website prose while retaining the unabridged TeX source.
require("node:child_process").execFileSync("python3", [path.join(root,"scripts/plasma_prose.py")]);
// Metadata edits deliberately target only the existing Plasma entry.
const libraryPath=path.join(root,'assets/library.js');
let library=fs.readFileSync(libraryPath,'utf8');
library=library.replace(/\{"id":\s*"plasma-lectures"[^\n]+/, line => {
  const comma=line.endsWith(','); const report=JSON.parse(comma?line.slice(0,-1):line);
  report.title='等离子体物理 Lectures 1–7：从基本概念到输运与闭合';
  report.authors='课程讲义 / 2026 · 81 页原文逐页对应';
  report.description='108 个学习单元、63 道带答案自测：逐步推导尺度、漂移、动理学、碰撞、无碰撞流体与有碰撞输运，完整保留第七讲公式、脚注和勘误核对；七份原 PDF 与公式内嵌，可离线阅读。';
  for(const tag of ['Lecture 7','Braginskii','Chapman–Enskog','双极扩散','输运与闭合']) if(!report.tags.includes(tag))report.tags.push(tag);
  return JSON.stringify(report)+(comma?',':'');
});
fs.writeFileSync(libraryPath,library);
const readmePath=path.join(root,'README.md');
let readme=fs.readFileSync(readmePath,'utf8');
readme=readme.replace(/^- \[等离子体物理 Lectures 1[–—-][67] 自学手册\].*$/m,'- [等离子体物理 Lectures 1–7 自学手册](reports/plasma-lectures/index.html)：81 页原讲义、108 个学习单元、63 道带答案自测；新增第七讲迁移率、双极扩散、Chapman–Enskog 展开和 Braginskii 输运，保留 73 个编号公式标签、5 条脚注及原稿校注；七份原 PDF 与离线公式完整内嵌（2026-11-09）。');
fs.writeFileSync(readmePath,readme);
const audit={lecture:7,originalPages:12,studySections:19,originalQuizQuestions:14,originalEquationTags:tags,renderedMathExpressions:mathCount,originalFootnotes:5,originalFigures:0,sourceSHA256:pdfs[6].sha256,originalSixLecturesUnchanged:true,originalSixPDFsUnchanged:true};
fs.writeFileSync(path.join(source,'lecture07-integration.json'),JSON.stringify(audit,null,2)+'\n');
console.log(JSON.stringify(audit,null,2));
