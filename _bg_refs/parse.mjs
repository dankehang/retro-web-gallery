import fs from 'fs';
// catalog 截断成无效 JS 的概率高，先做括号裁剪：找到最后一个 '];'
let src = fs.readFileSync('/workspace/_bg_refs/qzone-catalog.js','utf8');
const idx = src.lastIndexOf('];');
if (idx > 0) src = src.slice(0, idx+2);
let META = [];
try {
  sandbox = new Function(src + '\n;return window.META;');
  META = sandbox();
} catch(e) { console.log("eval fail:", e.message.slice(0,200)); process.exit(1); }
console.log(`META total=${META.length}`);
const skins = META.filter(m => m.type === 'skin');
console.log(`skins=${skins.length}`);
// 按色调去重，每组挑 3 个 2005-2007 的
const picks = [];
for (const hue of ['blue','purple','orange','pink','red']) {
  const group = skins.filter(m => (m.hue||'').toLowerCase() === hue || (m.hues||[]).includes(hue));
  group.sort((a,b)=> (a.date||'').localeCompare(b.date||''));
  const top = group.slice(0, 3);
  if (top.length) picks.push(...top);
}
// 纯列表（不能跑 node 的话，直接输出候选）
const seen = new Set();
for (const m of picks) {
  const key = m.id;
  if (seen.has(key)) continue; seen.add(key);
  console.log(fig(m));
}
function fig(m){
  return `${m.id}\t${m.name}\t${m.date}\t${m.hue}\t${m.tone||''}\t${m.ext}\tanim=${m.animated}\t${m.w}x${m.h}`;
}
