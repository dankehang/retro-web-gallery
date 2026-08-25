import fs from 'fs';
let src = fs.readFileSync('/workspace/_bg_refs/qzone-catalog.js','utf8');
const m = src.match(/window\.META\s*=\s*/);
const start = src.indexOf('[', m.index);
let depth=0, inStr=null, esc=false, end=-1, lastObj=-1;
for (let i=start;i<src.length;i++){
  const c=src[i];
  if (inStr){ if(esc) esc=false; else if(c==='\\') esc=true; else if(c===inStr) inStr=null; continue; }
  if (c==='"'||c==="'"||c==='`'){ inStr=c; continue; }
  if (c==='[') depth++;
  else if (c===']'){ depth--; if(depth===0){ end=i; break; } }
  else if (c==='{') depth++;
  else if (c==='}'){ depth--; if(depth===0) lastObj=i; }
}
let raw = src.slice(start, (end>0?end+1:lastObj+1)).replace(/,\s*$/, '') + (end<0?']':'');
let META;
try { META = eval('(' + raw + ')'); }
catch(e){ console.log("eval fail:", e.message.slice(0,200)); process.exit(2); }
console.log(`META total=${META.length}`);
const skins = META.filter(x=>x && x.type==='skin');
console.log(`skins=${skins.length}`);
const cnt={}, ext={};
for (const s of skins){ const h=(s.hue||'?'); cnt[h]=(cnt[h]||0)+1; ext[s.ext]=(ext[s.ext]||0)+1; }
console.log("by hue:", JSON.stringify(cnt));
console.log("by ext:", JSON.stringify(ext));
const seen = new Set();
console.log("id\tname\tdate\thue\ttone\text\tanim\twh\tkeyUrls");
for (const hue of ['blue','purple','orange','red','pink','green','white','black']) {
  const g = skins.filter(s=> (s.hue||'').toLowerCase()===hue || (s.hues||[]).includes(hue));
  g.sort((a,b)=>String(a.date||'').localeCompare(String(b.date||'')));
  for (const s of g.slice(0,4)) {
    const urls = Object.entries(s).filter(([k,v])=> typeof v==='string' && v.includes('gtimg')).map(([k,v])=>k+'='+v.slice(-40));
    const key = s.id;
    if (seen.has(key)) continue; seen.add(key);
    console.log([s.id, s.name, (s.date||'').slice(0,10), s.hue, s.tone||'', s.ext, s.animated?1:0, (s.w||'')+'x'+(s.h||''), urls.join(' | ')].join('\t'));
  }
  console.log('---');
}
