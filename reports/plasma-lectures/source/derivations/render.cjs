'use strict';
// Run normalize.py first. This script writes only in its own artifact directory.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');
const ROOT = __dirname;
const COURSE = process.env.COURSE_HTML || path.resolve(ROOT, '../../index.html');
const KATEX = process.env.KATEX_PATH || 'katex';
const katex = require(KATEX);
const modules = JSON.parse(fs.readFileSync(path.join(ROOT, 'modules.json'), 'utf8'));
const course = fs.readFileSync(COURSE, 'utf8');
const escape = text => text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const summaries = {
  'L4-B': '展开推导：超水平集体积匹配、广义逆与动量约束',
  'L5-C': '展开计算：Maxwell 背景的 Rosenbluth 势、慢化与扩散系数、两端极限和平衡检验',
  'L6-A': '展开推导：因果 Vlasov 响应、高相速度展开与低相速度 Boltzmann 极限',
};
const expressions = [];
let activeModule;
function math(tex, displayMode) {
  expressions.push({id: activeModule, display: displayMode, tex});
  const rendered = katex.renderToString(tex, {displayMode, throwOnError: true, trust: false, output: 'htmlAndMathml', strict: 'error'});
  return displayMode ? `<div class="derivation-equation">${rendered}</div>` : `<span class="derivation-inline-math">${rendered}</span>`;
}
function inline(text) {
  const held = [];
  text = text.replace(/\\\(([\s\S]*?)\\\)/g, (_, tex) => {
    held.push(math(tex, false)); return `\u0000${held.length - 1}\u0000`;
  });
  text = escape(text).replace(/\*\*([\s\S]*?)\*\*/g, '<strong>$1</strong>');
  return text.replace(/\u0000(\d+)\u0000/g, (_, i) => held[+i]);
}
function body(text) {
  return text.trim().split(/\n\s*\n/).map(block => {
    const display = block.match(/^\\\[([\s\S]*)\\\]$/);
    return display ? math(display[1].trim(), true) : `<p>${inline(block.replace(/\n/g, ' '))}</p>`;
  }).join('\n');
}
const index = [];
const all = [];
for (const module of modules) {
  activeModule = module.id;
  assert(course.includes(`id="${module.target_section}"`), `Missing target ${module.target_section}`);
  // Re-rendering source fragments is safe even after website integration.
  const countBefore = expressions.length;
  const renderedTitle = inline(module.title);
  const sourceRef = module.source_insertion_note.match(/原讲义[\s\S]*/)?.[0] || '';
  let content = body(module.body);
  if (module.collapsed) content = `<details class="derivation-details">\n<summary>${escape(summaries[module.source_id])}</summary>\n${content}\n</details>`;
  const html = `<div class="derivation-supplement" id="${module.id}" aria-labelledby="${module.id}-title" data-source-module="${module.source_id}">\n<h4 id="${module.id}-title"><span class="derivation-label">推导补充</span> · ${renderedTitle}</h4>\n<p class="derivation-source">教学补充 · ${escape(sourceRef)}</p>\n${content}\n</div>\n`;
  assert(!/<section\b/.test(html));
  assert(!/<details>/.test(html));
  assert(!html.includes('katex-error'));
  const filename = `${module.id}.html`;
  fs.writeFileSync(path.join(ROOT, filename), html);
  const formulae = expressions.slice(countBefore);
  index.push({
    id: module.id, lecture: module.lecture, target_section: module.target_section,
    title: module.title_plain,
    rendered_math_expressions: formulae.length,
    inline_math_expressions: formulae.filter(x => !x.display).length,
    display_math_expressions: formulae.filter(x => x.display).length,
    html_file: filename, collapsed: module.collapsed,
    insertion: module.insertion, preserve_existing_content: true,
    source_reference: sourceRef,
  });
  all.push(html);
}
assert.equal(index.length, 17);
fs.writeFileSync(path.join(ROOT, 'index.json'), JSON.stringify(index, null, 2) + '\n');
fs.writeFileSync(path.join(ROOT, 'math-expressions.json'), JSON.stringify(expressions, null, 2) + '\n');
// Optional standalone preview artifacts are not part of the published sources.
if (process.argv.includes('--preview')) {
  fs.writeFileSync(path.join(ROOT, 'all-fragments.html'), all.join('\n'));
  const styles = [...course.matchAll(/<style\b[^>]*>[\s\S]*?<\/style>/g)].map(m => m[0]).join('\n');
  const extraCSS = fs.readFileSync(path.join(ROOT, 'supplements.css'), 'utf8');
  fs.writeFileSync(path.join(ROOT, 'preview.html'), `<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>推导补充校验预览</title>${styles}<style>${extraCSS}\n.preview-main{max-width:850px;margin:0 auto;padding:28px 22px 80px}</style></head><body class="reading-course"><main class="preview-main"><h1>17 项推导补充</h1><p>Gaussian-cgs 制；温度以能量计；速度积分的边界项为零。此页仅预览新增片段，不含课程原正文。</p><div class="prose">${all.join('\n')}</div></main></body></html>`);
}
const source = fs.readFileSync(path.join(ROOT, 'derivation-supplements.original.md'));
const stats = {
  modules: index.length, rendered_math_expressions: expressions.length,
  display_math_expressions: expressions.filter(x => x.display).length,
  inline_math_expressions: expressions.filter(x => !x.display).length,
  collapsed_modules: index.filter(x => x.collapsed).map(x => x.id),
  katex_version: katex.version, throwOnError: true, strict: 'error',
  source_sha256: crypto.createHash('sha256').update(source).digest('hex'),
};
console.log(JSON.stringify(stats, null, 2));
