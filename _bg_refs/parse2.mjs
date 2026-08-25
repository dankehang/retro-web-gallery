import fs from 'fs';
let src = fs.readFileSync('/workspace/_bg_refs/qzone-catalog.js','utf8');
// 定位数组起点 window.META= 或 window.META =
const m = src.match(/window\.META\s*=\s*/);
if (!m) { console.log("no META marker"); process.exit(1); }
let i = src.indexOf('[', m.index);
// 字符级扫描找匹配的数组结束（容忍被截断 → 停在最后一个完整对象）
let depth = 0, inStr = null, esc = false, end = -1, lastObj = -1;
for (; i < src.length; i++) {
  const c = src[i];
  if (inStr) {
    if (esc) esc = false;
    else if (c === '\\') esc = true;
    else if (c === inStr) inStr = null;
    continue;
  }
  if (c === '"' || c === "'" || c === '`') { inStr = c; continue; }
  if (c === '[') depth++;
  else if (c === ']') { depth--; if (depth === 0) { end = i; break; } }
  else if (c === '{' ) depth++;
  else if (c === '}' ) { depth--; if (depth === 0) lastObj = i; }
}
if (end < 0 && lastObj > 0) {
  // 截断：取到最后一个完整对象，然后手动闭合数组
  const json = src.slice(src.indexOf('[', m.index), lastObj + 2); // +2 -> "},]"? no
  console.log("truncated - lastObj at", lastObj);
}
let raw = src.slice(src.indexOf('[', m.index), (end > 0 ? end + 1 : lastObj + 1));
// 若截断，补一个 close
if (end < 0) raw += ']';
let META;
try { META = JSON.parse(raw); }
catch(e) { console.log("JSON fail:", e.message.slice(0,150)); process.exit(2); }
console.log(`META total=${META.length}`);
const skins = META.filter(m => m && m.type === 'skin');
console.log(`skins=${skins.length}`);
const out = [];
for (const hue of ['blue','purple','orange','pink','green','red','black','white','yellow']) {
  const group = skins.filter(s => (s.hue||'').toLowerCase() === hue || (s.hues||[]).includes(hue));
  group.sort((a,b)=>String(a.date||'').localeCompare(String(b.date||'')));
  const list = group.slice(0, 5);
  for (const s of list) {
    out.push([s.id, s.name, s.date, s.hue, s.tone||'', s.ext, s.animated?1:0, s.w+'x'+s.h, s.price||'']);
  }
}
console.log("id\tname\tdate\thue\ttone\text\tanim\twh\tprice");
for (const r of out) console.log(r.join('\t'));
// 统计每个 hue 数量
const cnt = {};
for (const s of skins) { const h=(s.hue||'?'); cnt[h]=(cnt[h]||0)+1; }
console.log("\nskins by hue:", JSON.stringify(cnt));
// 统计 ext 分布
const ext = {};
for (const s of skins) ext[s.ext]=(ext[s.ext]||0)+1;
console.log("skins by ext:", JSON.stringify(ext));
