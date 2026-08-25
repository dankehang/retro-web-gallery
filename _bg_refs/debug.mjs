import fs from 'fs';
let src = fs.readFileSync('/workspace/_bg_refs/qzone-catalog.js','utf8');
console.log("total len:", src.length);
const m = src.match(/window\.META\s*=\s*/);
const start = src.indexOf('[', m.index);
console.log("start idx:", start);
let depth=0, inStr=null, esc=false, end=-1, lastObj=-1, chars=[];
for (let i=start;i<src.length;i++){
  const c=src[i];
  chars.push(c);
  if (inStr){ if(esc) esc=false; else if(c==='\\') esc=true; else if(c===inStr) inStr=null; continue; }
  if (c==='"'||c==="'"||c==='`'){ inStr=c; continue; }
  if (c==='[') depth++;
  else if (c===']'){ depth--; if(depth===0){ end=i; break; } }
  else if (c==='{') depth++;
  else if (c==='}'){ depth--; if(depth===0) lastObj=i; }
}
console.log("end:", end, "lastObj:", lastObj, "depth:", depth);
let raw = src.slice(start, (end>0?end+1:lastObj+1));
console.log("raw head 300:\n", raw.slice(0,300));
console.log("raw tail 300:\n", raw.slice(-300));
// 统计引号类型
console.log("double quotes:", (raw.match(/"/g)||[]).length, "single:", (raw.match(/'/g)||[]).length, "tick:", (raw.match(/`/g)||[]).length);
