"""极繁装饰 v2 重构：
- 删除坏掉的旧 #v2-deco CSS（url( + star_u + ) 非法）与 DOM
- 星/心/tint 纹理下沉到 body::before（z0，所有窗口之下，只露在缝隙）
- 飘浮动图/挂件 z3 但只摆页面边缘，不遮窗口内容
"""
import re, urllib.parse
path = "/workspace/index.html"
h = open(path, "r", encoding="utf-8").read()

# ---------- 0. 删除旧 #v2-deco CSS 块 ----------
pat_css = re.compile(r"/\* ===== 🌟 极繁堆叠装饰层.*?animation: none !important; \}\n\}\n", re.S)
h, n = pat_css.subn("", h, count=1)
assert n == 1, "旧 CSS 块删除失败"
print("✅ 0. 删除旧 #v2-deco CSS")

# ---------- 1. 删除旧 #v2-deco DOM 块 ----------
pat_dom = re.compile(r"<!-- 🌟 极繁堆叠装饰层：QQ 空间真实飘浮动图 \+ 挂件 -->\s*<div id=\"v2-deco\"[\s\S]*?</div>\n", re.S)
h, n = pat_dom.subn("", h, count=1)
assert n == 1, "旧 DOM 删除失败"
print("✅ 1. 删除旧 #v2-deco DOM")

# ---------- 2. body::before 纹理层（内容之下） ----------
STAR_SVG = "<svg xmlns='http://www.w3.org/2000/svg' width='40' height='40' viewBox='0 0 36 36'><path d='M18 3l4.4 10.1L33 14l-8 7.1 2.2 10.9L18 26 8.8 32 11 21.1 3 14l10.6-.9z' fill='white' fill-opacity='.55'/></svg>"
HEART_SVG= "<svg xmlns='http://www.w3.org/2000/svg' width='26' height='26' viewBox='0 0 24 24'><path d='M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54z' fill='white' fill-opacity='.4'/></svg>"
star_u  = "data:image/svg+xml," + urllib.parse.quote(STAR_SVG, safe="")
heart_u = "data:image/svg+xml," + urllib.parse.quote(HEART_SVG, safe="")

NEW_CSS = (
"/* ===== 🌟 极繁纹理（body::before，窗口之下仅露缝隙） ===== */\n"
"body::before {\n"
"  content: \"\"; position: fixed; inset: 0; z-index: 0;\n"
"  pointer-events: none;\n"
"  background-image:\n"
'    url("' + star_u + '"),\n'
'    url("' + heart_u + '"),\n'
"    radial-gradient(1100px 750px at 18% 12%, var(--deco-tint,#7cc4ff) 0%, rgba(255,255,255,0) 62%),\n"
"    radial-gradient(1000px 700px at 88% 88%, var(--deco-tint,#7cc4ff) 0%, rgba(255,255,255,0) 60%);\n"
"  background-size: 110px 110px, 88px 88px, 100% 100%, 100% 100%;\n"
"  background-repeat: repeat, repeat, no-repeat, no-repeat;\n"
"  background-position: 0 0, 0 0, 0 0, 0 0;\n"
"  mix-blend-mode: overlay;\n"
"  opacity: .5;\n"
"  animation: deco-pan 90s linear infinite;\n"
"}\n"
"@keyframes deco-pan {\n"
"  from { background-position: 0 0, 0 0, 0 0, 0 0; }\n"
"  to   { background-position: 110px 110px, 88px 88px, 0 0, 0 0; }\n"
"}\n"
"/* ===== 🌟 千禧年飘浮动图（叠页面边缘，不遮内容） ===== */\n"
"#v2-deco {\n"
"  position: fixed; inset: 0; z-index: 3; pointer-events: none; overflow: hidden;\n"
"}\n"
"#v2-deco .flt, #v2-deco .pend { position: absolute; will-change: transform; }\n"
"#v2-deco .flt { width: 40px; opacity: .92; filter: drop-shadow(0 0 4px rgba(255,255,255,.4)); }\n"
"#v2-deco .flt.f1 { left: 2.5%;  top: 7%;    width: 40px; animation: bobA 5.2s ease-in-out infinite; }\n"
"#v2-deco .flt.f2 { right: 2.5%; top: 8%;    width: 54px; animation: bobB 6.1s ease-in-out infinite; }\n"
"#v2-deco .flt.f3 { right: 4%;   bottom: 20%; width: 40px; animation: bobA 4.4s ease-in-out infinite reverse; }\n"
"#v2-deco .flt.f4 { left: 4%;    bottom: 22%; width: 42px; animation: bobC 5.8s ease-in-out infinite; }\n"
"#v2-deco .flt.f5 { right: 32%;  bottom: 3%;  width: 40px; animation: bobB 6.6s ease-in-out infinite reverse; }\n"
"#v2-deco .flt.f6 { left: 32%;   bottom: 3%;  width: 42px; animation: bobA 5.0s ease-in-out infinite; }\n"
"@keyframes bobA { 0%,100% { transform: translateY(0) rotate(0deg); } 50% { transform: translateY(-14px) rotate(9deg); } }\n"
"@keyframes bobB { 0%,100% { transform: translateY(0) rotate(0deg); } 50% { transform: translateY(12px) rotate(-10deg); } }\n"
"@keyframes bobC { 0%,100% { transform: translateY(0) scale(1); }       50% { transform: translateY(-10px) scale(1.14); } }\n"
"#v2-deco .pend { top: 0; width: 50px; transform-origin: top center; filter: drop-shadow(0 2px 6px rgba(0,0,0,.35)); opacity: .95; }\n"
"#v2-deco .pend.p1 { left: 10px;  animation: swayL 4.2s ease-in-out infinite; }\n"
"#v2-deco .pend.p2 { right: 10px; animation: swayR 4.8s ease-in-out infinite; }\n"
"@keyframes swayL { 0%,100% { transform: rotate(2.5deg); } 50% { transform: rotate(-2.5deg); } }\n"
"@keyframes swayR { 0%,100% { transform: rotate(-2.5deg); } 50% { transform: rotate(2.5deg); } }\n"
"@media (max-width: 780px) {\n"
"  #v2-deco .flt.f3, #v2-deco .flt.f4, #v2-deco .flt.f5, #v2-deco .flt.f6, #v2-deco .pend { display: none; }\n"
"  #v2-deco .flt { width: 30px !important; }\n"
"  body::before { opacity: .35; }\n"
"}\n"
"@media (prefers-reduced-motion: reduce) {\n"
"  #v2-deco .flt, #v2-deco .pend, body::before { animation: none !important; }\n"
"}\n"
)

ANCHOR = "@keyframes btn-pulse { 0%,100% { box-shadow: 2px 2px 0 rgba(0,0,0,.35);} 50% { box-shadow: 0 0 10px 3px #ff99dd, 2px 2px 0 rgba(0,0,0,.35);} }"
assert ANCHOR in h, "btn-pulse 锚失败"
h = h.replace(ANCHOR, ANCHOR + "\n" + NEW_CSS, 1)
print("✅ 2. 新 CSS 注入（body::before 纹理 + 边缘动图）")

# ---------- 3. 新 DOM：fxToolbar 之前 ----------
DECO_DOM = (
"<!-- 🌟 千禧年飘浮装饰：QQ 空间原版动图（叠页面边缘） -->\n"
'<div id="v2-deco" aria-hidden="true">\n'
'  <img class="flt f1" src="assets/float_145.gif" alt=""><!-- 七彩音符 -->\n'
'  <img class="flt f2" src="assets/float_222.gif" alt=""><!-- 紫蝴蝶 -->\n'
'  <img class="flt f3" src="assets/float_613.gif" alt=""><!-- 星星雨 -->\n'
'  <img class="flt f4" src="assets/float_604.gif" alt=""><!-- 草莓 -->\n'
'  <img class="flt f5" src="assets/float_601.gif" alt=""><!-- 冰块 -->\n'
'  <img class="flt f6" src="assets/float_602.gif" alt=""><!-- 冰柠檬 -->\n'
'  <img class="pend p1" src="assets/pend_552.gif" alt=""><!-- 粉红的心 -->\n'
'  <img class="pend p2" src="assets/pend_639.gif" alt=""><!-- 城堡 -->\n'
"</div>\n"
)
ANCHOR2 = '<div id="fxToolbar" title="点击切换皮肤 / 飘落特效">'
assert ANCHOR2 in h, "fxToolbar 锚失败"
h = h.replace(ANCHOR2, DECO_DOM + ANCHOR2, 1)
print("⚠️ canvas 唯一性检查:", h.count('<canvas id="fx"'))
assert h.count('<canvas id="fx"') == 1, "canvas 数量异常"
open(path, "w", encoding="utf-8").write(h)
print(f"✅ 3. 新 DOM 注入完成 {len(h):,}B")