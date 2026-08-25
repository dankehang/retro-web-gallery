"""极繁堆叠装饰层：真实 QQ 空间 floaty 飘浮动图 + pendant 挂件 + 星光纹理
叠加在现有 8 套皮肤图之上，形成千禧年极繁效果
"""
import re, urllib.parse
path = "/workspace/index.html"
h = open(path, "r", encoding="utf-8").read()

# ---------- 1. 8 个主题变量块加 --deco-tint ----------
TINTS = {
 "ice":    "#7cc4ff",
 "purple": "#d8a9ff",
 "qq":     "#ffb35c",
 "pink":   "#ff9ad5",
 "green":  "#7de3b0",
 "black":  "#ff7ad9",
 "yellow": "#ffdf6b",
 "red":    "#ff8fa0",
}
for tname, c in TINTS.items():
    if tname == "ice":
        blocks = re.findall(r":root, body\.theme-ice \{[\s\S]*?\n\}", h)
        for b in blocks:
            h = h.replace(b, b[:-1] + f"  --deco-tint:{c};\n}}", 1)
    else:
        pat = re.compile(r"body\.theme-" + tname + r" \{[\s\S]*?\n\}", re.M)
        def repl(m):
            return m.group(0)[:-1] + f"  --deco-tint:{c};\n"
        h, n = pat.subn(repl, h, count=1)
        assert n == 1, tname
print("✅ 1. 8 主题 + --deco-tint")

# ---------- 2. CSS：极繁堆叠大块（btn-pulse 之后插入） ----------
STAR_SVG = "<svg xmlns='http://www.w3.org/2000/svg' width='40' height='40' viewBox='0 0 36 36'><path d='M18 3l4.4 10.1L33 14l-8 7.1 2.2 10.9L18 26 8.8 32 11 21.1 3 14l10.6-.9z' fill='white' fill-opacity='.5'/></svg>"
HEART_SVG= "<svg xmlns='http://www.w3.org/2000/svg' width='26' height='26' viewBox='0 0 24 24'><path d='M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54z' fill='white' fill-opacity='.4'/></svg>"
star_u  = "data:image/svg+xml," + urllib.parse.quote(STAR_SVG, safe="")
heart_u = "data:image/svg+xml," + urllib.parse.quote(HEART_SVG, safe="")

DECO_CSS = (
"""
/* ===== 🌟 极繁堆叠装饰层（真实 QQ 空间 floaty/pendant 动图 × 星光纹理） ===== */
#v2-deco {
  position: fixed; inset: 0; z-index: 3; pointer-events: none; overflow: hidden;
}
#v2-deco .pat {
  position: absolute; inset: -20%;
  background-image:
    linear-gradient(135deg, var(--deco-tint,#7cc4ff) 0%, rgba(255,255,255,0.08) 45%, var(--deco-tint,#7cc4ff) 100%),
    url("""" + star_u + """"),
    url("""" + heart_u + """");
  background-size: 200% 200%, 120px 120px, 96px 96px;
  background-position: 0 0, 0 0, 0 0;
  mix-blend-mode: screen;
  opacity: .38;
  animation: deco-pan 80s linear infinite, deco-hue 24s ease-in-out infinite;
}
@keyframes deco-pan {
  from { background-position: 0 0, 0 0, 0 0; }
  to   { background-position: 100% 100%, 120px 120px, 96px 96px; }
}
@keyframes deco-hue {
  0%,100% { filter: hue-rotate(0deg); }
  50%     { filter: hue-rotate(40deg); }
}
#v2-deco .flt {
  position: absolute; display: block; image-rendering: auto;
  will-change: transform; opacity: .92;
  filter: drop-shadow(0 0 4px rgba(255,255,255,.45));
}
#v2-deco .flt.f1  { left: 5%;   top: 16%;  width: 40px; animation: bobA 5.2s ease-in-out infinite; }
#v2-deco .flt.f2  { right: 8%;  top: 24%;  width: 60px; animation: bobB 6.1s ease-in-out infinite; }
#v2-deco .flt.f3  { left: 47%;  top: 6%;   width: 46px; animation: bobA 4.4s ease-in-out infinite reverse; }
#v2-deco .flt.f4  { right: 20%; bottom: 18%; width: 36px; animation: bobB 5.8s ease-in-out infinite; }
#v2-deco .flt.f5  { left: 11%;  bottom: 24%; width: 44px; animation: bobC 6.6s ease-in-out infinite reverse; }
#v2-deco .flt.f6  { right: 38%; top: 10%;  width: 42px; animation: bobA 3.9s ease-in-out infinite; }
#v2-deco .flt.f7  { left: 28%;  bottom: 10%; width: 46px; animation: bobC 5.0s ease-in-out infinite; }
#v2-deco .flt.f8  { right: 4%;  bottom: 28%; width: 44px; animation: bobB 4.8s ease-in-out infinite reverse; }
#v2-deco .flt.f9  { left: 21%;  top: 40%;  width: 42px; animation: bobA 7.0s ease-in-out infinite; }
@keyframes bobA { 0%,100% { transform: translateY(0)    rotate(0deg); }  50% { transform: translateY(-16px) rotate(10deg);  } }
@keyframes bobB { 0%,100% { transform: translateY(0)    rotate(0deg); }  50% { transform: translateY(14px)  rotate(-12deg); } }
@keyframes bobC { 0%,100% { transform: translateY(0) scale(1); }       50% { transform: translateY(-12px) scale(1.15); } }
#v2-deco .pend {
  position: absolute; top: 0; width: 55px;
  transform-origin: top center;
  filter: drop-shadow(0 2px 6px rgba(0,0,0,.35));
  opacity: .95;
}
#v2-deco .pend.p1 { left: 6px;  animation: swayL 4.2s ease-in-out infinite; }
#v2-deco .pend.p2 { right: 6px; animation: swayR 4.8s ease-in-out infinite; }
@keyframes swayL { 0%,100% { transform: rotate(2.5deg); } 50% { transform: rotate(-2.5deg); } }
@keyframes swayR { 0%,100% { transform: rotate(-2.5deg); } 50% { transform: rotate(2.5deg); } }
@media (max-width: 780px) {
  #v2-deco .flt.f2, #v2-deco .flt.f4, #v2-deco .flt.f5,
  #v2-deco .flt.f6, #v2-deco .flt.f7, #v2-deco .flt.f9 { display: none; }
  #v2-deco .flt { width: 30px !important; }
  #v2-deco .pend { width: 34px; }
  #v2-deco .pat { opacity: .3; }
}
@media (prefers-reduced-motion: reduce) {
  #v2-deco .flt, #v2-deco .pend, #v2-deco .pat { animation: none !important; }
}
"""
)

ANCHOR = "@keyframes btn-pulse { 0%,100% { box-shadow: 2px 2px 0 rgba(0,0,0,.35);} 50% { box-shadow: 0 0 10px 3px #ff99dd, 2px 2px 0 rgba(0,0,0,.35);} }"
assert ANCHOR in h, "btn-pulse 锚失败"
h = h.replace(ANCHOR, ANCHOR + "\n" + DECO_CSS, 1)
print("✅ 2. 极繁 CSS 注入")

# ---------- 3. DOM：#v2-deco（fxToolbar 之后） ----------
FXT = '</div>\n\n<div class="page-shell">'
DECO_HTML = (
"""
</div>

<!-- 🌟 极繁堆叠装饰层：QQ 空间真实飘浮动图 + 挂件 -->
<div id="v2-deco" aria-hidden="true">
  <span class="pat"></span>
  <img class="flt f1" src="assets/float_145.gif" alt="">
  <img class="flt f2" src="assets/float_222.gif" alt="">
  <img class="flt f3" src="assets/float_613.gif" alt="">
  <img class="flt f4" src="assets/float_219.gif" alt="">
  <img class="flt f5" src="assets/float_601.gif" alt="">
  <img class="flt f6" src="assets/float_604.gif" alt="">
  <img class="flt f7" src="assets/float_602.gif" alt="">
  <img class="flt f8" src="assets/float_610.gif" alt="">
  <img class="flt f9" src="assets/float_215.gif" alt="">
  <img class="pend p1" src="assets/pend_552.gif" alt="">
  <img class="pend p2" src="assets/pend_639.gif" alt="">
</div>

<div class="page-shell">"""
)
assert FXT in h, "fxToolbar 结束锚失败"
h = h.replace(FXT, DECO_HTML, 1)
print("✅ 3. 装饰 DOM 注入")

open(path, "w", encoding="utf-8").write(h)
print(f"✅ 写入完成 {len(h):,}B")