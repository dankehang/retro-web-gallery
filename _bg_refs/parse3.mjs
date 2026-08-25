import fs from 'fs';
let src = fs.readFileSync('/workspace/_bg_refs/qzone-catalog.js','utf8');
const m = src.match(/window\.META\s*=\s*/);
const start = src.indexOf('[', m.index);
let depth = 0, inStr = null, esc = false, end = -1, lastObj = -1, i;
for (i = start; i < src.length; i++) {
  const c = src[i];
  if (inStr) { if (esc) esc=false; else if (c==='\\') esc=true; else if (c===inStr) inStr=null; continue; }
  if (c==='"'||c==="'") { inStr=c; continue; }
  if (c==='[') depth++;
  else if (c===']') { depth--; if (depth===0){ end=i; break; } }
  else if (c==='{') depth++;
  else if (c==='}') { depth--; if (depth===0) lastObj=i; }
}
let raw = start > 0 ? src.slice(start, (end>0? end+1 : lastObj+1)) : '';
if (end<0) raw += ']';
while (/,\s*\]?$/.test(raw)) raw = raw.replace(/,\s*$/, '');
let META;
try { META = JSON.parse(raw); }
catch(e){ console.log("JSON fail:", e.message.slice(0,150)); process.exit(2); }
console.log(`META total=${META.length}`);
const skins = META.filter(x => x && x.type==='skin');
console.log(`skins=${skins.length}`);
const cnt={}, ext={};
for (const s of skins){ const h=(s.hue||'?'); cnt[h]=(cnt[h]||0)+1; ext[s.ext]=(ext[s.ext]||0)+1; }
console.log("by hue:", JSON.stringify(cnt));
console.log("by ext:", JSON.stringify(ext));
console.log("id\tname\tdate\thue\ttone\text\tanim\twh\tprice\tfirst-url-field");
for (const hue of ['blue','purple','orange','red','pink','green']) {
  const g = skins.filter(s=> (s.hue||'').toLowerCase()===hue || (s.hues||[]).includes(hue));
  g.sort((a,b)=>String(a.date||'').localeCompare(String(b.date||'')));
  for (const s of g.slice(0,5)) {
    const u = s[Object.keys(s).find(k=>typeof s[k]==='string' && s[k].includes('gtimg')) ] || '';
    console.log([s.id, s.name, (s.date||'').slice(0,10), s.hue, s.tone||'', s.ext, s.animated?1:0, (s.w||'')+'x'+(s.h||''), s.price||'', u.slice(0,60)].join('\t'));
  }
  console.log('--');
}
