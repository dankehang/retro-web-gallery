"""只改背景这一层：CSS + 装饰 div（可逆）"""
path = "/workspace/index.html"
html = open(path, "r", encoding="utf-8").read()

# ========== INJECT 1: 在 </style> (v2-visual 的闭合, 1016行) 之前追加背景升级版 CSS ==========
BG_CSS = r"""

/* ===== 🌟 背景超升级：光晕+斜纹+棋盘+扫光+装饰层（黄钻感拉满） ===== */

/* 6 层叠加：斜纹 ＋ 棋盘 ＋ 3 色大光晕 ＋ 扫光条 ＋ 主渐变 */
body {
  background:
    /* L6: 扫光条（白霓光，25s 循环左→右） */
    linear-gradient(105deg,
      transparent 0%, transparent 38%,
      rgba(255,255,255,0.28) 44%,
      rgba(255,255,255,0.55) 49%,
      rgba(255,255,200,0.45) 52%,
      rgba(255,255,255,0.28) 56%,
      transparent 62%, transparent 100%) center/220% 100% no-repeat,
    /* L5: 3 层大面积彩色光晕 */
    radial-gradient(680px 420px at 12% 18%, rgba(255,140,220,0.55), rgba(255,140,220,0) 60%),
    radial-gradient(820px 520px at 92% 32%, rgba(120,210,255,0.55), rgba(120,210,255,0) 62%),
    radial-gradient(760px 620px at 55% 110%, rgba(255,230,130,0.55), rgba(255,230,130,0) 60%),
    /* L4: 棋盘格（半透明） */
    conic-gradient(from 0deg at 0 0, rgba(255,255,255,0.08) 0 25%, rgba(0,0,0,0) 0 50%,
      rgba(255,255,255,0.08) 0 75%, rgba(0,0,0,0) 0) 0 0 / 14px 14px,
    /* L3: 对角斜纹 */
    repeating-linear-gradient(45deg,
      rgba(255,255,255,0.05) 0 2px,
      rgba(255,0,200,0.05) 2px 4px,
      rgba(0,180,255,0.05) 4px 6px,
      rgba(255,200,0,0.05) 6px 8px),
    /* L2: 之前的 4 个 1px 星点保留（小细节） */
    radial-gradient(circle at 10% 20%, #fff 1px, transparent 2px),
    radial-gradient(circle at 80% 40%, #ffc0e6 1px, transparent 2px),
    radial-gradient(circle at 50% 90%, #b3e0ff 1px, transparent 2px),
    radial-gradient(circle at 30% 60%, #fffacd 1px, transparent 2px),
    radial-gradient(rgba(255,255,200,0.08) 1px, transparent 1px) 0 0 / 4px 4px,
    /* L1: 主渐变（保留原皮肤色） */
    linear-gradient(180deg, var(--body-bg1,#000080) 0%, var(--body-bg2,#0044aa) 60%, #001155 100%) !important;
  animation: sweep 25s linear infinite;
  background-attachment: fixed;
}
@keyframes sweep {
  0%   { background-position: 100% 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0; }
  100% { background-position: -120% 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0; }
}

/* 薰衣草紫：换光晕配色 + 紫色星空星点 */
body.theme-purple {
  background:
    linear-gradient(105deg,
      transparent 0%, transparent 38%,
      rgba(220,180,255,0.32) 44%,
      rgba(255,220,255,0.55) 49%,
      rgba(180,130,255,0.45) 52%,
      rgba(220,180,255,0.32) 56%,
      transparent 62%, transparent 100%) center/220% 100% no-repeat,
    radial-gradient(720px 520px at 15% 12%, rgba(255,120,220,0.55), rgba(255,120,220,0) 62%),
    radial-gradient(900px 620px at 88% 40%, rgba(180,140,255,0.60), rgba(180,140,255,0) 62%),
    radial-gradient(780px 640px at 55% 110%, rgba(255,200,230,0.45), rgba(255,200,230,0) 60%),
    conic-gradient(from 0deg at 0 0, rgba(255,200,255,0.10) 0 25%, rgba(0,0,0,0) 0 50%,
      rgba(255,200,255,0.10) 0 75%, rgba(0,0,0,0) 0) 0 0 / 14px 14px,
    repeating-linear-gradient(45deg,
      rgba(255,150,230,0.06) 0 2px,
      rgba(200,140,255,0.06) 2px 4px,
      rgba(120,80,220,0.06) 4px 6px,
      rgba(255,80,180,0.06) 6px 8px),
    radial-gradient(circle at 20% 30%, #ffd1ff 1px, transparent 2px),
    radial-gradient(circle at 70% 70%, #e9d5ff 1px, transparent 2px),
    radial-gradient(circle at 90% 20%, #fbbf24 1px, transparent 2px),
    radial-gradient(rgba(255,200,255,0.15) 1px, transparent 1px) 0 0 / 4px 4px,
    linear-gradient(180deg,#1a0540 0%,#4c1d95 50%,#701a75 100%) !important;
  animation: sweep 28s linear infinite;
  background-attachment: fixed;
}

/* QQ橙：暖光晕 + 橙色斜纹 */
body.theme-qq {
  background:
    linear-gradient(105deg,
      transparent 0%, transparent 38%,
      rgba(255,240,180,0.30) 44%,
      rgba(255,240,150,0.55) 49%,
      rgba(255,180,90,0.45) 52%,
      rgba(255,240,180,0.30) 56%,
      transparent 62%, transparent 100%) center/220% 100% no-repeat,
    radial-gradient(720px 480px at 15% 18%, rgba(255,170,80,0.60), rgba(255,170,80,0) 62%),
    radial-gradient(860px 580px at 88% 28%, rgba(255,220,120,0.55), rgba(255,220,120,0) 62%),
    radial-gradient(800px 620px at 55% 110%, rgba(255,120,60,0.45), rgba(255,120,60,0) 60%),
    conic-gradient(from 0deg at 0 0, rgba(255,230,170,0.10) 0 25%, rgba(0,0,0,0) 0 50%,
      rgba(255,230,170,0.10) 0 75%, rgba(0,0,0,0) 0) 0 0 / 14px 14px,
    repeating-linear-gradient(45deg,
      rgba(255,180,60,0.06) 0 2px,
      rgba(255,100,30,0.06) 2px 4px,
      rgba(255,220,100,0.06) 4px 6px,
      rgba(200,60,0,0.06) 6px 8px),
    radial-gradient(circle at 15% 20%, #ffd9a8 1px, transparent 2px),
    radial-gradient(circle at 85% 40%, #fff 1px, transparent 2px),
    radial-gradient(circle at 50% 80%, #ffd166 1px, transparent 2px),
    radial-gradient(rgba(255,200,100,0.1) 1px, transparent 1px) 0 0 / 4px 4px,
    linear-gradient(180deg,#2a0800 0%,#7a2200 50%,#4c0519 100%) !important;
  animation: sweep 22s linear infinite;
  background-attachment: fixed;
}

/* 全屏装饰层：💿🦋✦💗 随时间漂移旋转（fixed, z=1 在 canvas 之下） */
#bg-deco {
  position: fixed; inset: 0; z-index: 1; pointer-events: none; overflow: hidden;
}
#bg-deco .deco {
  position: absolute;
  filter: drop-shadow(0 0 10px rgba(255,200,255,0.75)) drop-shadow(0 0 22px rgba(120,200,255,0.55));
  opacity: .82;
  will-change: transform;
}
#bg-deco .deco.d1 { /* 💿 左上 */
  left: 4%; top: 6%;
  width: 130px; height: 130px;
  background:
    repeating-conic-gradient(from 0deg,
      #ff00aa 0deg 10deg, #ffcc00 10deg 20deg, #00ccff 20deg 30deg,
      #aa66ff 30deg 40deg, #ff6699 40deg 50deg, #66ffcc 50deg 60deg,
      #ffffff 60deg 70deg, #ff00aa 70deg 80deg, #000 80deg 90deg);
  border-radius: 50%;
  box-shadow:
    inset 0 0 0 10px rgba(0,0,0,0.55),
    inset 0 0 0 26px rgba(255,255,255,0.08),
    inset 0 0 0 46px rgba(0,0,0,0.35),
    inset 0 0 0 56px rgba(255,255,255,0.05);
  animation: spin 22s linear infinite, floatY 9s ease-in-out infinite;
}
#bg-deco .deco.d1::after {
  content:""; position:absolute; left:50%; top:50%; width:18px; height:18px;
  margin:-9px 0 0 -9px; border-radius:50%;
  background: radial-gradient(circle, #fff 0 40%, #000 45% 100%);
}
#bg-deco .deco.d2 { /* 🦋 右上 */
  right: 6%; top: 14%; font-size: 120px; line-height: 1;
  color: #ffd1ff;
  animation: floatX 12s ease-in-out infinite, rot3d 14s linear infinite;
}
#bg-deco .deco.d3 { /* ✦ 大星 左下 */
  left: 8%; bottom: 14%; font-size: 110px; line-height: 1;
  color: #fff8a0;
  animation: sparkle 2s ease-in-out infinite, floatY 10s ease-in-out infinite reverse;
}
#bg-deco .deco.d4 { /* 💗 右下 */
  right: 10%; bottom: 12%; font-size: 100px; line-height: 1;
  color: #ff99cc;
  animation: beat 1.3s ease-in-out infinite, floatX 13s ease-in-out infinite reverse;
}
#bg-deco .deco.d5 { /* 🌈 彩虹圆环 中右 */
  right: 18%; top: 55%;
  width: 160px; height: 160px;
  border-radius: 50%;
  background: conic-gradient(from 0deg, #ff0066, #ff9900, #ffee00, #00ee66, #00aaff, #9900ff, #ff0066);
  -webkit-mask: radial-gradient(circle, transparent 58%, #000 60%, #000 74%, transparent 76%);
          mask: radial-gradient(circle, transparent 58%, #000 60%, #000 74%, transparent 76%);
  filter: drop-shadow(0 0 16px rgba(255,120,220,0.55));
  opacity: .65;
  animation: spin 30s linear infinite reverse, floatY 14s ease-in-out infinite;
}
#bg-deco .deco.d6 { /* 小星群 中上 */
  left: 52%; top: 3%;
  width: 180px; height: 70px;
  background:
    radial-gradient(circle at 10% 50%, #fff 2px, transparent 4px),
    radial-gradient(circle at 30% 30%, #ffe8a0 1.5px, transparent 3px),
    radial-gradient(circle at 55% 60%, #ffc0e6 2.5px, transparent 5px),
    radial-gradient(circle at 78% 20%, #b3e0ff 1.5px, transparent 3px),
    radial-gradient(circle at 92% 70%, #fff 2px, transparent 4px);
  animation: twinkle 3.2s ease-in-out infinite, floatY 11s ease-in-out infinite;
  opacity: .85;
  filter: drop-shadow(0 0 4px #fff);
}

@keyframes spin    { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
@keyframes floatY  { 0%,100% { translate: 0 -8px;} 50% { translate: 0 16px;} }
@keyframes floatX  { 0%,100% { translate: -10px 0;} 50% { translate: 14px 0;} }
@keyframes rot3d   { 0% { transform: rotateY(0)   rotate(-6deg);}
                     50%{ transform: rotateY(180deg) rotate(8deg);}
                    100%{ transform: rotateY(360deg) rotate(-6deg);} }
@keyframes beat    { 0%,100%{ transform: scale(1);}
                     20%   { transform: scale(1.18);}
                     40%   { transform: scale(1);}
                     60%   { transform: scale(1.12);}
                     80%   { transform: scale(.98);} }
@keyframes twinkle { 0%,100%{ opacity:.35;} 50%{ opacity:1;} }

/* 手机端：关闭大装饰（挡内容） + 降低扫光强度 */
@media (max-width: 780px) {
  #bg-deco .deco.d1 { width: 70px; height: 70px; }
  #bg-deco .deco.d2 { font-size: 68px; right: -6px; }
  #bg-deco .deco.d3 { font-size: 62px; left: -4px; }
  #bg-deco .deco.d4 { font-size: 58px; right: 2px; }
  #bg-deco .deco.d5 { width: 90px; height: 90px; opacity:.35; }
  #bg-deco .deco.d6 { width: 110px; height: 44px; }
}

/* 尊重 reduced-motion 用户：关所有动画，但保留光晕/斜纹静态视觉 */
@media (prefers-reduced-motion: reduce) {
  body, body.theme-purple, body.theme-qq { animation: none !important; }
  #bg-deco .deco { animation: none !important; }
}
"""

# 精准定位：在 1016 行的 </style>（v2-visual 的闭合标签）之前插入
# 做法：找到 ".page-shell { max-width: 100%; }\n</style>" 这个特征块
needle = ".page-shell { max-width: 100%; }\n</style>"
if needle not in html:
    raise SystemExit("❌ 找不到注入点 needle CSS")
html = html.replace(needle, BG_CSS + "\n" + needle, 1)
print("✅ BG-CSS 注入成功")

# ========== INJECT 2: canvas#fx 之后插入 bg-deco 装饰层 ==========
CANVAS = '<canvas id="fx" aria-hidden="true"></canvas>'
if CANVAS not in html:
    raise SystemExit("❌ 找不到 canvas 注入点")
DECO_HTML = r"""
<div id="bg-deco" aria-hidden="true">
  <div class="deco d1" title=""></div>
  <div class="deco d2">🦋</div>
  <div class="deco d3">✦</div>
  <div class="deco d4">💗</div>
  <div class="deco d5" title=""></div>
  <div class="deco d6" title=""></div>
</div>
"""
html = html.replace(CANVAS, CANVAS + "\n" + DECO_HTML, 1)
print("✅ bg-deco DOM 注入成功")

open(path, "w", encoding="utf-8").write(html)
print(f"✅ 写入完毕，最终文件 {len(html):,} 字节")
