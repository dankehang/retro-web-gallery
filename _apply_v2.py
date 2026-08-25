#!/usr/bin/env python3
"""
Apply Y2K-CN v2 enhancements to index.html in 7 precise injections.
All positions are marked with unique "anchor strings" found by grep above.
"""
from pathlib import Path
FILE = Path('/workspace/index.html')
html = FILE.read_text(encoding='utf-8', errors='ignore')

# ==========================================================
# INJECTION 1: High-concentration visual CSS (#v2-visual)
#   Anchor:  <style id="skin-extra"> (or last </style> before </head>)
#   Insert BEFORE the very last </style> in <head> at line 737
# ==========================================================
INJECT_1_CSS = r'''
<style id="v2-visual">
/* ===== 🌟 Y2K v2 高浓度黄钻感视觉升级 ===== */

/* --- CSS Variables: 三套皮肤（冰蓝/薰衣草紫/QQ橙）--- */
:root, body.theme-ice {
  --title-g1:#0055bb; --title-g2:#002288; --title-fg:#ffff66;
  --accent:#0077ff; --btn-primary-1:#0088dd; --btn-primary-2:#0055aa;
  --body-bg1:#000080; --body-bg2:#0044aa;
}
body.theme-purple {
  --title-g1:#7a2bce; --title-g2:#4a0e8a; --title-fg:#ffe6ff;
  --accent:#c084fc; --btn-primary-1:#c084fc; --btn-primary-2:#7e22ce;
  --body-bg1:#1a0540; --body-bg2:#4c1d95;
}
body.theme-qq {
  --title-g1:#ff6600; --title-g2:#c03300; --title-fg:#fffacd;
  --accent:#ff8833; --btn-primary-1:#ff8833; --btn-primary-2:#c05213;
  --body-bg1:#2a0800; --body-bg2:#7a2200;
}

/* --- 全屏特效 canvas & 所有 win98 升 z-index --- */
#fx { position:fixed; inset:0; z-index:1; pointer-events:none; }
.win98, .site-banner, .site-nav, .site-footer, .floating-ad, .backend-badge, .main-grid, .page-shell, #fxToolbar { position:relative; z-index:2; }

/* --- body 高浓度背景：旧 Win98 蓝底 + 点阵噪点 + 渐变叠层 --- */
body {
  background:
    radial-gradient(circle at 10% 20%, #fff 1px, transparent 2px),
    radial-gradient(circle at 80% 40%, #ffc0e6 1px, transparent 2px),
    radial-gradient(circle at 50% 90%, #b3e0ff 1px, transparent 2px),
    radial-gradient(circle at 30% 60%, #fffacd 1px, transparent 2px),
    radial-gradient(rgba(255,255,200,0.08) 1px, transparent 1px) 0 0 / 4px 4px,
    linear-gradient(180deg, var(--body-bg1,#000080) 0%, var(--body-bg2,#0044aa) 60%, #001155 100%) !important;
  background-blend-mode: normal, normal, normal, normal, overlay, normal;
  background-attachment: fixed;
}
/* 粉紫色皮肤用更粉的点阵 */
body.theme-purple {
  background-image:
    radial-gradient(circle at 20% 30%, #ffd1ff 1px, transparent 2px),
    radial-gradient(circle at 70% 70%, #e9d5ff 1px, transparent 2px),
    radial-gradient(circle at 90% 20%, #fbbf24 1px, transparent 2px),
    radial-gradient(rgba(255,200,255,0.15) 1px, transparent 1px) 0 0 / 4px 4px,
    linear-gradient(180deg,#1a0540 0%,#4c1d95 50%,#701a75 100%) !important;
}
body.theme-qq {
  background-image:
    radial-gradient(circle at 15% 20%, #ffd9a8 1px, transparent 2px),
    radial-gradient(circle at 85% 40%, #fff 1px, transparent 2px),
    radial-gradient(circle at 50% 80%, #ffd166 1px, transparent 2px),
    radial-gradient(rgba(255,200,100,0.1) 1px, transparent 1px) 0 0 / 4px 4px,
    linear-gradient(180deg,#2a0800 0%,#7a2200 50%,#4c0519 100%) !important;
}

/* --- Win98 窗口标题用皮肤色（覆盖原蓝/深蓝硬编码）--- */
.win98 > .win-title, .site-banner {
  background: linear-gradient(180deg, var(--title-g1,#0055bb) 0%, var(--title-g2,#002288) 100%) !important;
  color: var(--title-fg,#ffff66) !important;
}
.site-title { color: var(--title-fg,#ffff66) !important; }

.old-btn.primary, .pl-btn.pl-play {
  background: linear-gradient(180deg, var(--btn-primary-1,#0088dd) 0%, var(--btn-primary-2,#0055aa) 100%) !important;
  color: #fff !important;
  border: 2px outset var(--accent,#0077ff) !important;
}

/* --- 个人头像升级：真图 + 金属边框 + 8 角闪光 --- */
.avatar-pixel {
  width: 100px; height: 100px;
  border: 4px double #ff66cc;
  box-shadow:
    0 0 0 2px #fff,
    0 0 12px rgba(255,102,204,0.7),
    inset 0 0 0 2px rgba(255,255,255,0.4);
  border-radius: 0;
  display: flex; align-items: center; justify-content: center;
  position: relative;
  overflow: hidden;
  padding: 0;
  background: #fff !important;
}
.avatar-pixel img { width: 100%; height: 100%; object-fit: cover; display: block; }
.avatar-pixel::before, .avatar-pixel::after {
  content: "✦"; position: absolute; color: #fff; font-size: 14px; line-height: 1;
  text-shadow: 0 0 3px #fff, 0 0 6px #ff66cc;
  animation: sparkle 1.6s ease-in-out infinite;
}
.avatar-pixel::before { top: 3px; left: 4px; }
.avatar-pixel::after { bottom: 4px; right: 3px; animation-delay: .8s; }
@keyframes sparkle { 0%,100% { opacity:.3; transform: scale(.8);} 50% { opacity:1; transform: scale(1.25); } }

/* --- bling 分割线 --- */
.bling-divider {
  height: 14px;
  margin: 10px 4px;
  background:
    linear-gradient(90deg, transparent, #fff 50%, transparent),
    linear-gradient(90deg,#ff3399,#ffcc00,#33ccff,#9966ff,#ff66cc);
  background-size: 100% 100%, 100% 100%;
  border-radius: 3px;
  box-shadow: 0 0 6px rgba(255,102,204,0.7), inset 0 1px 0 #fff;
  position: relative;
}
.bling-divider::after {
  content: "✦✦✦"; color:#fff; font-size: 10px;
  position: absolute; inset: 0; display:flex; align-items:center; justify-content:center;
  text-shadow: 0 0 3px #ff0066, 0 0 6px #fff;
  letter-spacing: 4px;
}

/* --- 右下特效/换肤工具栏 --- */
#fxToolbar {
  position: fixed; right: 18px; bottom: 150px;
  display: flex; flex-direction: column; gap: 8px; z-index: 99;
}
.fx-btn {
  width: 40px; height: 40px; font-size: 18px;
  border: 2px outset #f9f;
  background: linear-gradient(180deg,#ffd1ff,#ff99dd);
  cursor: pointer; box-shadow: 2px 2px 0 rgba(0,0,0,.35);
  animation: btn-pulse 2s ease-in-out infinite;
}
.fx-btn:hover { transform: scale(1.08) rotate(-4deg); }
.fx-btn:nth-child(2) { animation-delay: .6s; }
@keyframes btn-pulse { 0%,100% { box-shadow: 2px 2px 0 rgba(0,0,0,.35);} 50% { box-shadow: 0 0 10px 3px #ff99dd, 2px 2px 0 rgba(0,0,0,.35);} }

/* --- 日记窗口新样式 --- */
.diary-tabs { display:flex; gap:4px; flex-wrap:wrap; margin-bottom:6px; }
.diary-tabs .d-tab {
  padding: 2px 10px; cursor: pointer; font-size: 12px;
  border: 1px solid #888; background:#f7f7f7;
}
.diary-tabs .d-tab.active {
  background: linear-gradient(180deg,#ffddf0,#ff99cc);
  color:#a00060; border-color:#ff66aa; font-weight:bold;
}
.diary-card {
  margin-bottom: 10px;
  border: 2px solid #aaa;
  background: #fff;
  box-shadow: inset 1px 1px 0 #fff, inset -1px -1px 0 #808080;
}
.diary-hero {
  height: 110px; position: relative; overflow: hidden;
  border-bottom: 2px solid #666;
}
.diary-hero img { width:100%; height:100%; object-fit:cover; display:block; filter: saturate(1.2) contrast(1.05); }
.diary-hero::after {
  content: ""; position: absolute; inset: 0;
  background: linear-gradient(180deg, rgba(0,0,0,0) 50%, rgba(0,0,30,0.75) 100%);
}
.diary-hero .d-title {
  position: absolute; left: 10px; right: 10px; bottom: 6px; color:#fff; z-index: 2;
  font-family: "华文行楷","KaiTi",serif; font-size: 22px; font-weight: bold;
  text-shadow: 1px 1px 0 #000, -1px -1px 0 #000, 2px 2px 6px rgba(255,0,100,0.8);
}
.diary-body-wrap { padding: 6px 8px; }
.diary-meta {
  display: flex; justify-content: space-between; flex-wrap: wrap; gap:4px;
  font-size: 12px; color:#555; margin-bottom:4px;
}
.diary-meta .cat-tag { padding:1px 8px; border-radius:999px; color:#fff; font-size: 11px; }
.cat-tag-碎碎念 { background: linear-gradient(180deg,#fbbf24,#d97706); }
.cat-tag-校园   { background: linear-gradient(180deg,#38bdf8,#0284c7); }
.cat-tag-音乐   { background: linear-gradient(180deg,#f472b6,#be185d); }
.cat-tag-周记   { background: linear-gradient(180deg,#34d399,#047857); }
.cat-tag-随便写写{ background: linear-gradient(180deg,#a78bfa,#6d28d9); }
.diary-body-text {
  font-family: "SimSun","宋体",serif; font-size: 13.5px; line-height: 1.9; color:#222;
}
.diary-actions {
  margin-top: 6px; display:flex; justify-content: space-between; align-items: center;
  border-top: 1px dashed #bbb; padding-top: 4px;
}
.like-btn {
  padding: 3px 10px; cursor:pointer;
  background: linear-gradient(180deg,#ffcce5,#ff99cc);
  border: 2px outset #ff99cc; color:#8b0048; font-weight:bold;
}
.like-btn:active { transform: translateY(1px); border-style: inset; }

/* --- 友情链接卡片 --- */
.blogroll-grid {
  display: grid; grid-template-columns: 1fr 1fr; gap: 6px;
}
@media (max-width: 780px) { .blogroll-grid { grid-template-columns: 1fr; } }
.br-card {
  display: grid; grid-template-columns: 48px 1fr; gap: 6px;
  padding: 4px; border: 1px solid #bbb; background: #fff;
  align-items: center;
}
.br-card img {
  width: 48px; height: 48px; object-fit: cover; display:block;
  border: 2px solid #ddd; background: #fafafa;
}
.br-card .br-info { font-size: 12px; min-width: 0; overflow: hidden; }
.br-card .br-name {
  font-weight: bold; font-size: 13px;
  background: linear-gradient(90deg,#ff0066,#ff9900,#0099ff,#9900ff);
  -webkit-background-clip: text; background-clip: text; color: transparent;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.br-card .br-slogan { color:#666; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.br-card .br-actions {
  display:flex; justify-content:space-between; align-items:center;
  margin-top: 3px;
}
.press-btn {
  background: linear-gradient(180deg,#ffe4f1,#ff99cc);
  border: 1px outset #ff99cc; color:#a00060;
  cursor: pointer; padding: 1px 8px; font-size: 11px;
}
.press-btn.pressed { background: #eee; color:#666; border-style: inset; cursor: default; }
.br-hits { color:#006; font-size: 11px; }

/* --- 留言楼中楼 --- */
.gb-reply-wrap {
  margin-top: 6px; padding-left: 20px; padding-top: 4px;
  border-top: 1px dotted #ccc;
}
.gb-reply-toggle {
  background: none; border: none; color:#0066cc; text-decoration: underline;
  font-size: 12px; cursor: pointer; padding: 0;
}
.gb-reply-list {
  margin-top: 4px; display: flex; flex-direction: column; gap: 4px;
}
.gb-reply {
  display: grid; grid-template-columns: 24px 1fr; gap: 6px;
  padding: 3px 4px; border-left: 2px dotted #ccc;
  font-size: 12px;
}
.gb-reply.owner-true {
  border-left-color: #ff66aa;
  background: linear-gradient(90deg, rgba(255,200,230,0.45), transparent);
}
.gb-reply .re-avatar {
  width: 24px; height: 24px; display:flex; align-items:center; justify-content:center;
  background: linear-gradient(135deg,#cce,#eff); border:1px solid #bbb; font-size: 14px;
}
.gb-reply .re-head { color:#444; }
.gb-reply .re-user { color:#006; font-weight: bold; }
.gb-reply.owner-true .re-user::before { content: "🦋 "; }
.gb-reply .re-body { color:#111; padding: 2px 0; }
.gb-reply-form {
  margin-top: 6px; padding: 4px; background: #f7f7f7;
  border: 1px solid #ccc; display: flex; gap: 4px; flex-wrap: wrap;
}
.gb-reply-form input {
  border: 2px inset #999; padding: 2px 4px; font-size: 12px; min-width: 0;
}
.gb-reply-form .gb-re-name { width: 80px; flex: 0 0 80px; }
.gb-reply-form .gb-re-msg  { flex: 1 1 160px; }

/* --- 写日记模态框 --- */
.owner-modal {
  position: fixed; inset: 0; background: rgba(0,0,30,0.6);
  z-index: 9999; display: none; align-items: center; justify-content: center;
}
.owner-modal.show { display: flex; }
.owner-modal > .win98 { width: 560px; max-width: 95vw; }
.owner-modal input[type=password],
.owner-modal input[type=text],
.owner-modal textarea,
.owner-modal select {
  border: 2px inset #999; padding: 3px; font-family: SimSun,serif; font-size: 13px;
}

/* --- 高浓度：标题字体加粗阴影 --- */
.diary-entry .d-title,
.win98 > .win-title > span:first-child {
  text-shadow: 1px 1px 0 #fff, 2px 2px 4px rgba(255,0,150,0.6) !important;
}

/* --- 原有页面宽度优化（特效不影响布局）--- */
.page-shell { max-width: 100%; }
</style>
'''

# Find 2nd-to-last </style> before </head> (the one that closes skin-extra, line ~737).
# We inject right BEFORE the LAST </style> in file.
assert html.count('</style>') >= 2, "Expected multiple </style> tags"
last_style_end = html.rfind('</style>')
# Inject BEFORE the very last </style>  (which closes #skin-extra @ line 737 in original)
html = html[:last_style_end] + INJECT_1_CSS + "\n" + html[last_style_end:]
print("✅ INJECT 1: v2 visual CSS")
# ==========================================================


# ==========================================================
# INJECTION 2: <canvas id="fx"> + fxToolbar
#   Anchor:  <div class="page-shell">
#   Insert BEFORE that line (right after <body>)
# ==========================================================
INJECT_2_BODY = r'''
<canvas id="fx" aria-hidden="true"></canvas>
<div id="fxToolbar" title="点击切换皮肤 / 飘落特效">
  <button class="fx-btn" onclick="cycleTheme()" title="换肤：冰蓝 / 薰衣草紫 / QQ橙">🎨</button>
  <button class="fx-btn" onclick="cycleFx()"    title="飘落：关 / ❄️雪 / 🌸樱 / ⭐星 / 🦋蝶">✨</button>
</div>
'''
anchor = '<div class="page-shell">'
assert anchor in html
html = html.replace(anchor, INJECT_2_BODY + '\n' + anchor, 1)
print("✅ INJECT 2: canvas + fxToolbar")
# ==========================================================


# ==========================================================
# INJECTION 3: 左栏 个人资料窗 & 计数器 之后，插入"💞好朋友の小窝"新窗口
#             同时把原来的"友情链接"重命名为 "🚩 热门网站导航"
#   Anchor:      <!-- 友情链接 -->
# ==========================================================
INJECT_3_NEW_WINDOW = r'''
      <!-- ===== 新：好朋友の小窝 · 互踩（带头像 + 标语 + 踩一下） ===== -->
      <div class="win98" id="blogrollWin">
        <div class="win-title">
          <span><span class="wt-icon">💞</span>好朋友の小窝 · 互踩</span>
          <span class="wt-btns">
            <span class="wt-btn">_</span><span class="wt-btn">▢</span><span class="wt-btn x">×</span>
          </span>
        </div>
        <div class="win-body" style="padding:6px;">
          <div class="blogroll-grid" id="blogrollGrid">
            <!-- JS 渲染 -->
          </div>
          <div id="brResult" style="color:#060;margin-top:4px;font-size:12px;min-height:14px;"></div>
          <div style="margin-top:8px;padding:6px;background:#fff7fb;border:1px dashed #ff99cc;font-size:12px;">
            <b>🔔 申请友情链接</b>（蝴蝶姐姐审批通过后显示）
            <div style="margin-top:4px;display:grid;grid-template-columns:1fr 1fr;gap:4px;">
              <input id="brName"   type="text" placeholder="站名(必填)" style="border:2px inset #999;padding:2px;">
              <input id="brUrl"    type="text" placeholder="网址 https://…" style="border:2px inset #999;padding:2px;">
              <input id="brSlogan" type="text" placeholder="一句话标语(必填)" style="grid-column:span 2;border:2px inset #999;padding:2px;">
            </div>
            <div style="margin-top:4px;text-align:right;">
              <button class="old-btn primary" onclick="applyBlogroll()">📮 提交申请</button>
            </div>
          </div>
        </div>
      </div>
      <!-- ========================================= -->

      <!-- 🚩 热门网站导航（原 友情链接 列表，改名避免冲突） -->
'''
anchor = '      <!-- 友情链接 -->'
assert anchor in html
html = html.replace(anchor, INJECT_3_NEW_WINDOW + '\n' + anchor, 1)
# Also rename old <span>友情链接</span> title text in the same block
# Only replace the FIRST occurrence (the old links window title) after the anchor.
html = html.replace(
  '<span><span class="wt-icon">🔗</span>友情链接</span>',
  '<span><span class="wt-icon">🚩</span>热门网站导航</span>',
  1
)
print("✅ INJECT 3: blogroll window + 旧友情链接改名")
# ==========================================================


# ==========================================================
# INJECTION 4: 中栏 欢迎卡片之后、留言板之前，插入"📒网络日记"新窗口 + 写日记模态框
#   Anchor:      <!-- 留言板 -->
# ==========================================================
INJECT_4_DIARY = r'''
      <!-- ===== 新：网络日记簿 ===== -->
      <div class="win98" id="diaryWin">
        <div class="win-title">
          <span><span class="wt-icon">📒</span>网络日记 · 蝴蝶の心情手记</span>
          <span class="wt-btns">
            <span class="wt-btn">_</span><span class="wt-btn">▢</span><span class="wt-btn x">×</span>
          </span>
        </div>
        <div class="win-body" style="padding:6px;">
          <div id="diaryTabs" class="diary-tabs"></div>
          <div id="diaryList"></div>
          <div style="margin-top:10px;text-align:right;">
            <button class="old-btn" onclick="openWriteDiary()">📝 写新日记</button>
          </div>
        </div>
      </div>

      <div class="bling-divider"></div>

      <!-- 留言板 -->
'''
anchor = '      <!-- 留言板 -->'
assert anchor in html
html = html.replace(anchor, INJECT_4_DIARY, 1)
print("✅ INJECT 4: diary window + bling divider")


# INJECT 4b: 写日记模态框，放在 </body> 前的 </div><!-- /page-shell --> 后面
INJECT_4_MODAL = r'''
<!-- 写日记模态框（密码保护，站长专属） -->
<div class="owner-modal" id="ownerModal">
  <div class="win98" style="margin:auto;">
    <div class="win-title">
      <span><span class="wt-icon">🔒</span>站长工具 · 写新日记</span>
      <span class="wt-btns">
        <span class="wt-btn" onclick="closeOwnerModal()">_</span>
        <span class="wt-btn">▢</span>
        <span class="wt-btn x" onclick="closeOwnerModal()">×</span>
      </span>
    </div>
    <div style="padding:10px;font-size:13px;">
      <div>
        🔐 站长密码：
        <input id="ownerPwd" type="password" style="border:2px inset #999;padding:2px;width:180px;" value="">
        <button class="old-btn primary" onclick="ownerLogin()">✅ 登录</button>
        <span id="pwdHint" style="color:#c00;margin-left:6px;"></span>
        <button class="old-btn" style="float:right;" onclick="closeOwnerModal()">关闭</button>
      </div>
      <hr>
      <div id="writeDiaryForm" style="display:none;">
        <table style="width:100%;font-size:13px;">
          <tr><td style="width:56px;">标题</td><td><input id="dTitle" style="width:100%;"></td></tr>
          <tr>
            <td>分类</td>
            <td>
              <select id="dCategory">
                <option>碎碎念</option><option>校园</option><option>音乐</option>
                <option>周记</option><option>随便写写</option>
              </select>
              &nbsp;&nbsp;心情
              <select id="dMood">
                <option>😊</option><option>🥳</option><option>😍</option>
                <option>🤔</option><option>😢</option><option>😡</option><option>😴</option>
              </select>
            </td>
          </tr>
          <tr>
            <td>正文</td>
            <td style="padding-top:4px;">
              <textarea id="dBody" rows="8" style="width:100%;font-family:SimSun;" placeholder="今天的心情是…（支持换行，自动转 br）"></textarea>
            </td>
          </tr>
          <tr>
            <td></td>
            <td style="padding-top:6px;text-align:right;">
              <button class="old-btn primary" onclick="submitDiary()">💾 发布日记</button>
              <span id="diaryResult" style="color:#060;margin-left:10px;"></span>
            </td>
          </tr>
        </table>
      </div>
    </div>
  </div>
</div>
'''
anchor = '</div><!-- /page-shell -->'
assert anchor in html
html = html.replace(anchor, '</div><!-- /page-shell -->\n' + INJECT_4_MODAL, 1)
print("✅ INJECT 4b: 写日记 owner-modal")
# ==========================================================


# ==========================================================
# INJECTION 5: 留言板种子结构升级 —— 每条 .gb-post 包裹里加楼中楼结构
#   策略：给已有 3 条种子留言的 div 加 id 便于 JS 定位，
#         每条在 <div class="gb-body">…</div> 之后、外层 </div> 之前插入 reply-wrap
#   用唯一字符串定位三条留言
# ==========================================================
def upgrade_seed_post(floor, unique_text, gb_post_unique_open):
    """在每条已知种子留言的 <div class="gb-body">…</div> 之后插入楼中楼模板。
    因为三条 gb-post HTML 长得很像，分别用它们唯一的 span.user 文本做锚点：
    §紫风铃§ / 月光剑客 / 淘气小熊
    """
    return None  # placeholder - 实现用下面的字符串替换
# 三条种子留言，分别用唯一字符串定位并插入 reply-wrap
UPGRADES = [
  # floor 1 紫风铃
  (
    '            <div class="gb-body">\n                哇~~新主页好漂亮哦！蝴蝶的设计越来越棒了！+U +U！<br>\n                对了，你推荐的《隐形的翅膀》我已经开始学了~ ♪(´▽`)\n              </div>\n            </div>\n          </div>',
    '            <div class="gb-body" data-gb-floor="1">\n                哇~~新主页好漂亮哦！蝴蝶的设计越来越棒了！+U +U！<br>\n                对了，你推荐的《隐形的翅膀》我已经开始学了~ ♪(´▽`)\n              </div>\n              <div class="gb-reply-wrap" data-gb-floor="1">\n                <button class="gb-reply-toggle" onclick="toggleReplies(this)">💬 查看回复 (<span class="gb-reply-cnt">0</span>)</button>\n                <div class="gb-reply-list" style="display:none;"></div>\n                <div class="gb-reply-form">\n                  <input type="text" class="gb-re-name" placeholder="昵称" value="匿名网友">\n                  <input type="text" class="gb-re-msg"  placeholder="回复这条留言（最多120字）">\n                  <button class="old-btn" onclick="submitReply(this)">📨 回复</button>\n                  <span class="gb-re-result"></span>\n                </div>\n              </div>\n            </div>\n          </div>'
  ),
  # floor 2 月光剑客
  (
    '            <div class="gb-body">\n                偶来踩踩~~~记得回访哦！我在百度空间也开新主页了~<br>\n                周杰伦那首《七里香》真的百听不厌，握个爪！o(≧v≦)o\n              </div>\n            </div>\n          </div>',
    '            <div class="gb-body" data-gb-floor="2">\n                偶来踩踩~~~记得回访哦！我在百度空间也开新主页了~<br>\n                周杰伦那首《七里香》真的百听不厌，握个爪！o(≧v≦)o\n              </div>\n              <div class="gb-reply-wrap" data-gb-floor="2">\n                <button class="gb-reply-toggle" onclick="toggleReplies(this)">💬 查看回复 (<span class="gb-reply-cnt">0</span>)</button>\n                <div class="gb-reply-list" style="display:none;"></div>\n                <div class="gb-reply-form">\n                  <input type="text" class="gb-re-name" placeholder="昵称" value="匿名网友">\n                  <input type="text" class="gb-re-msg"  placeholder="回复这条留言（最多120字）">\n                  <button class="old-btn" onclick="submitReply(this)">📨 回复</button>\n                  <span class="gb-re-result"></span>\n                </div>\n              </div>\n            </div>\n          </div>'
  ),
  # floor 3 淘气小熊
  (
    '            <div class="gb-body">\n                今天来的有点晚~ <span class="rainbow-text">不过留言还是要留的！</span><br>\n                蝴蝶姐姐！！我也要学做 FrontPage 教程，下次开课叫我！(>ω<)\n              </div>\n            </div>\n          </div>',
    '            <div class="gb-body" data-gb-floor="3">\n                今天来的有点晚~ <span class="rainbow-text">不过留言还是要留的！</span><br>\n                蝴蝶姐姐！！我也要学做 FrontPage 教程，下次开课叫我！(>ω<)\n              </div>\n              <div class="gb-reply-wrap" data-gb-floor="3">\n                <button class="gb-reply-toggle" onclick="toggleReplies(this)">💬 查看回复 (<span class="gb-reply-cnt">0</span>)</button>\n                <div class="gb-reply-list" style="display:none;"></div>\n                <div class="gb-reply-form">\n                  <input type="text" class="gb-re-name" placeholder="昵称" value="匿名网友">\n                  <input type="text" class="gb-re-msg"  placeholder="回复这条留言（最多120字）">\n                  <button class="old-btn" onclick="submitReply(this)">📨 回复</button>\n                  <span class="gb-re-result"></span>\n                </div>\n              </div>\n            </div>\n          </div>'
  )
]
for i,(old,new) in enumerate(UPGRADES):
    if old in html:
        html = html.replace(old, new, 1)
        print(f"✅ INJECT 5{i+1}: floor {i+1} 楼中楼结构已插入")
    else:
        print(f"⚠️  INJECT 5{i+1}: 找不到锚点（可能 HTML 已被修改），跳过 - 依赖 JS 在 paintGuestbook() 时统一重写结构")
# ==========================================================


# ==========================================================
# INJECTION 6: 脚本 —— 在 bootstrap() 调用之前插入一整块 V2 JS
#   Anchor:  /* ============ 启动：数据加载 + 定时器 ============ */
# ==========================================================
INJECT_6_JS = r'''
/* ============================================================
   🌼 V2 高浓度视觉 + 4 大功能（日记 / 友链 / 楼中楼 / 特效）
   ============================================================ */

/* -------- 图片资源常量（真实千禧年图库，已探测全部可直链）-------- */
const IMG = {
  avatarQQ:   "https://picsum.photos/seed/doll-qq-butterfly/120/120",
  diary: {
    school:  "https://picsum.photos/seed/y2k-school-stairs/400/160",
    cd:      "https://picsum.photos/seed/y2k-cd-disc/400/160",
    candy:   "https://picsum.photos/seed/y2k-nail-candy/400/160",
  },
  friends: {
    zifengling:"https://api.dicebear.com/9.x/pixel-art/svg?seed=zifengling&backgroundColor=ffd1dc",
    yueguang:  "https://api.dicebear.com/9.x/pixel-art/svg?seed=yueguang&backgroundColor=c7d2fe",
    xiaoxiong: "https://api.dicebear.com/9.x/pixel-art/svg?seed=xiaoxiong&backgroundColor=fde68a",
    pugongying:"https://api.dicebear.com/9.x/pixel-art/svg?seed=pugongying&backgroundColor=bae6fd",
    shuijing:  "https://api.dicebear.com/9.x/pixel-art/svg?seed=shuijing&backgroundColor=fbcfe8",
    zhuifeng:  "https://api.dicebear.com/9.x/pixel-art/svg?seed=zhuifeng&backgroundColor=bbf7d0",
    mitang:    "https://api.dicebear.com/9.x/pixel-art/svg?seed=mitang&backgroundColor=fecaca",
    yinghua:   "https://api.dicebear.com/9.x/pixel-art/svg?seed=yinghua&backgroundColor=e9d5ff",
  },
  cdCover:   "https://picsum.photos/seed/jay-chou-qilixiang/64/64",
};
// 图片加载失败的兜底：小 SVG data URL（避免红×）
function fallbackAvatar(seed, color) {
  const svg = `<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 48 48'><rect width='48' height='48' rx='0' fill='${color||'#ffd1dc}'/><text x='50%' y='58%' font-size='28' text-anchor='middle' dominant-baseline='middle'>🦋</text></svg>`;
  return "data:image/svg+xml;charset=utf-8," + encodeURIComponent(svg);
}
function safeImgEl(url, seed, color){
  // 生成一个带 onerror 兜底的 <img> 标签（在 HTML 里）
  const fb = fallbackAvatar(seed || 'x', color || '#fde68a');
  return `<img src="${escapeAttr(url)}" onerror="this.onerror=null;this.src='${fb}';">`;
}
function escapeAttr(s){ return String(s||'').replace(/"/g,'&quot;').replace(/'/g,'&#39;'); }

/* -------- 升级个人资料头像：替换 emoji 为真实图片 + 闪光边框 -------- */
(function swapAvatar(){
  const box = document.querySelector('.avatar-pixel');
  if (!box) return;
  const oldText = box.innerHTML;  // 可能还是🦋
  if (oldText && oldText.indexOf('<img') === -1) {
    box.innerHTML = `<img src="${IMG.avatarQQ}" onerror="this.onerror=null;this.src='${fallbackAvatar('qq','#fbcfe8')}';">`;
  }
})();
/* -------- 音乐播放器 CD 封面：插在播放器 title 左侧 -------- */
(function addPlayerCover(){
  const title = document.querySelector('.pl-title');
  if (!title) return;
  title.style.display = 'flex'; title.style.alignItems = 'center'; title.style.gap = '6px';
  title.insertAdjacentHTML('afterbegin',
    `<img src="${IMG.cdCover}" style="width:20px;height:20px;border-radius:50%;border:1px solid #999;" onerror="this.remove();">`
  );
})();

/* -------- STORE 扩展：日记 / 友链 / 楼中楼 -------- */
(function extendStore(){
  // 访客 ID：浏览器唯一（不关联真实身份，纯用于防刷）
  let vid = localStorage.getItem('v2.visitor_id');
  if (!vid) {
    vid = 'v_' + Math.random().toString(36).slice(2) + Date.now().toString(36);
    localStorage.setItem('v2.visitor_id', vid);
  }
  STORE.visitorId = () => vid;
  const todayStr = () => {
    const d = new Date();
    return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');
  };

  /* 本地 storage helpers */
  const LS = {
    get(key, def){ try { return JSON.parse(localStorage.getItem(key)) ?? def; } catch(_){ return def; } },
    set(key, val){ localStorage.setItem(key, JSON.stringify(val)); }
  };
  /* 默认种子（localStorage 模式 & 新 Supabase 返回空时都能用） */
  const SEED_DIARY = [
    {id:1, title:'开学第一天，好紧张呀~', category:'校园', mood:'🤔', views:238,
     body:'今天升初二啦！(>ω<) 换了新同桌叫小冉，她居然也喜欢周杰伦！我们约定明天一起去买《十一月的肖邦》磁带。<br>数学老师好像更凶了……作业有点多，呜呜。<br>对了，我的新笔袋是草莓味的！🍓',
     created_at: Date.now() - 86400000*2},
    {id:2, title:'又到周末，终于可以上网了！', category:'碎碎念', mood:'🥳', views:891,
     body:'每个礼拜最期待的就是周六晚上爸妈允许上网 2 小时！(≧▽≦)/<br>先挂 QQ，再踩空间，再听一遍周杰伦《夜曲》的 MV……<br>今天收到了 32 条留言！！哇，谢谢大家支持我的小窝！+U +U！',
     created_at: Date.now() - 86400000*1},
    {id:3, title:'单曲循环：七里香', category:'音乐', mood:'😍', views:1204,
     body:'窗外的麻雀 / 在电线杆上多嘴<br>你说这一句 / 很有夏天的感觉<br>———<br>CD 已经听到第 137 遍了还没厌。周杰伦为什么这么厉害啊？？？<br>下次想翻唱这首歌录给你们听 ♪(´▽`)',
     created_at: Date.now() - 86400000*0},
  ];
  const SEED_BR = [
    {id:1,name:'§紫风铃§小窝',  url:'#', slogan:'偶滴家~记得常来踩踩哦！',    avatar_url:IMG.friends.zifengling, hits:127,approved:true,sort_order:1},
    {id:2,name:'月光剑客Baidu', url:'#', slogan:'FrontPage 新手教程正在连载~',avatar_url:IMG.friends.yueguang,  hits:89, approved:true,sort_order:2},
    {id:3,name:'淘气小熊のBLOG',url:'#', slogan:'小熊出没，注意！(>ω<)',      avatar_url:IMG.friends.xiaoxiong, hits:356,approved:true,sort_order:3},
    {id:4,name:'蓝色蒲公英',    url:'#', slogan:'用心写字，慢一点没关系。',    avatar_url:IMG.friends.pugongying,hits:58, approved:true,sort_order:4},
    {id:5,name:'水晶鞋之恋',    url:'#', slogan:'少女心不死，公主梦不灭。',    avatar_url:IMG.friends.shuijing,  hits:201,approved:true,sort_order:5},
    {id:6,name:'追风少年',      url:'#', slogan:'玩跑跑卡丁车的来找我单挑！',  avatar_url:IMG.friends.zhuifeng,  hits:143,approved:true,sort_order:6},
    {id:7,name:'蜜糖甜甜圈',    url:'#', slogan:'每天分享一首好听的歌 ♪',     avatar_url:IMG.friends.mitang,    hits:76, approved:true,sort_order:7},
    {id:8,name:'樱花盛开时',    url:'#', slogan:'一起看樱花雨吧~',             avatar_url:IMG.friends.yinghua,   hits:188,approved:true,sort_order:8},
  ];
  const SEED_REPLIES = [
    {id:1,guestbook_id:1,reply_floor:1,username:'冰蝴蝶🦋',is_owner:true,message:'风铃妹妹你来啦～ 下次一定回访你的小窝！《隐形的翅膀》真的好好学，一起加油！♪(´▽`)',created_at:Date.now()-1000*60*60*6},
    {id:2,guestbook_id:1,reply_floor:2,username:'淘气小熊',is_owner:false,message:'( っ´▽`)っ 我也想学这首歌！下次一起 K 歌哦～！',created_at:Date.now()-1000*60*60*5},
    {id:3,guestbook_id:2,reply_floor:1,username:'冰蝴蝶🦋',is_owner:true,message:'收到剑客哥哥回访！百度空间链接一会儿就去加友情链接～握爪！(*´▽`*)',created_at:Date.now()-1000*60*60*4},
    {id:4,guestbook_id:3,reply_floor:1,username:'冰蝴蝶🦋',is_owner:true,message:'小熊包在我身上！下周 FrontPage 教程开课，群里通知你～ (>ω<)ﾉ',created_at:Date.now()-1000*60*60*3},
  ];
  /* ---- ensure default seed on localStorage --- */
  if (!localStorage.getItem('v2.diary'))       LS.set('v2.diary', SEED_DIARY);
  if (!localStorage.getItem('v2.blogroll'))    LS.set('v2.blogroll', SEED_BR);
  if (!localStorage.getItem('v2.gb_replies'))  LS.set('v2.gb_replies', SEED_REPLIES);
  if (!localStorage.getItem('v2.diary_likes')) LS.set('v2.diary_likes', []);

  STORE.listDiary = async function(category){
    let list = [];
    if (useSupa && supabase) {
      const { data, error } = await supabase.from('diary').select('*').order('id', {ascending:false});
      if (error && error.code !== 'PGRST205') console.warn('listDiary supa fail', error);
      if (Array.isArray(data) && data.length) list = data.slice();
    }
    if (!list.length) list = LS.get('v2.diary', SEED_DIARY).slice();
    if (category && category !== '全部') list = list.filter(d => d.category === category);
    return list.sort((a,b)=> (b.created_at||0)-(a.created_at||0));
  };
  STORE.viewDiary = async function(id){
    // 同访客同日只计 1 次
    const key = `diary_viewed_${id}_${todayStr()}`;
    if (localStorage.getItem(key)) return;
    localStorage.setItem(key, '1');
    if (useSupa && supabase) {
      try {
        await supabase.rpc('view_diary', {id_arg: id}).catch(()=>null);
        // fallback rpc：直接 update views = views + 1
        await supabase.from('diary').update({views: STORE.__noop}).eq('id',id).catch(()=>null);
        // use plain UPDATE:
        const {error} = await supabase.from('diary').update({views: (await STORE.getDiaryRaw(id) || {views:0}).views + 1}).eq('id',id);
        if (!error) return;
      } catch(_) {}
    }
    // fallback
    const arr = LS.get('v2.diary', SEED_DIARY);
    const d = arr.find(x => x.id === id);
    if (d) { d.views = (d.views||0) + 1; LS.set('v2.diary', arr); }
  };
  STORE.getDiaryRaw = async function(id){
    if (useSupa && supabase) {
      const {data} = await supabase.from('diary').select('*').eq('id',id).limit(1);
      if (Array.isArray(data) && data[0]) return data[0];
    }
    return LS.get('v2.diary', []).find(x => x.id===id);
  };
  STORE.likeDiary = async function(id){
    const today = todayStr();
    const v = STORE.visitorId();
    if (useSupa && supabase) {
      const { error } = await supabase.from('diary_likes').insert([{diary_id:id, visitor_id:v, day:today}]);
      if (!error) return 'OK';
      if (error && error.code === '23505') return '今日已赞';
      console.warn('likeDiary supa err', error);
    }
    // fallback
    const arr = LS.get('v2.diary_likes', []);
    if (arr.some(x => x.diary_id===id && x.visitor_id===v && x.day===today)) return '今日已赞';
    arr.push({diary_id:id, visitor_id:v, day:today, created_at:Date.now()});
    LS.set('v2.diary_likes', arr);
    return 'OK';
  };
  STORE.addDiary = async function({title, category, body, mood}){
    const row = {
      title, category: category || '碎碎念',
      body: escapeHtml(body||'').replace(/\n/g,'<br>'),
      mood: mood || '😊',
      views: 0,
      created_at: Date.now(),
    };
    if (useSupa && supabase) {
      const {data, error} = await supabase.from('diary').insert([row]).select();
      if (!error && data && data[0]) return data[0];
    }
    // fallback
    const arr = LS.get('v2.diary', []);
    row.id = (arr[0]?.id || 0) + 1;
    arr.unshift(row);
    LS.set('v2.diary', arr);
    return row;
  };

  STORE.listBlogroll = async function(){
    if (useSupa && supabase) {
      const {data, error} = await supabase.from('blogroll').select('*').eq('approved',true).order('sort_order');
      if (!error && Array.isArray(data) && data.length) return data;
    }
    return LS.get('v2.blogroll', SEED_BR).slice().sort((a,b)=>(a.sort_order||100)-(b.sort_order||100));
  };
  STORE.pressBlogroll = async function(id){
    const today = todayStr();
    const k = `br_pressed_${id}_${today}`;
    if (localStorage.getItem(k)) return { pressed: false, msg: '今天已经踩过啦 ♡' };
    localStorage.setItem(k, '1');
    if (useSupa && supabase) {
      // 需要先拿到当前 hits，再 +1 UPDATE（RLS 允许 approved=true 行 UPDATE）
      try {
        const {data:cur} = await supabase.from('blogroll').select('hits').eq('id',id).limit(1);
        const currentHits = (Array.isArray(cur) && cur[0]?.hits) || 0;
        await supabase.from('blogroll').update({hits: currentHits + 1}).eq('id', id);
        return { pressed: true, hits: currentHits + 1 };
      } catch(e) { /* fall to local */ }
    }
    // fallback
    const arr = LS.get('v2.blogroll', SEED_BR);
    const x = arr.find(b => b.id === id);
    if (!x) return {pressed:false, msg:'找不到该友链'};
    x.hits = (x.hits || 0) + 1;
    LS.set('v2.blogroll', arr);
    return { pressed: true, hits: x.hits };
  };
  STORE.applyBlogroll = async function({name, url, slogan}){
    const row = {
      name, url: url || '#', slogan: slogan || '',
      avatar_url: '', hits: 0, approved: false, sort_order: 200, created_at: Date.now()
    };
    if (useSupa && supabase) {
      const { error } = await supabase.from('blogroll').insert([row]);
      if (!error) return 'OK';
      if (error) console.warn('applyBlogroll supa err', error); // 继续本地写
    }
    // local fallback（approved=false，但我们在本地也给它存下来，方便演示）
    const arr = LS.get('v2.blogroll', SEED_BR);
    row.id = Math.max(0, ...arr.map(b=>b.id||0)) + 1;
    row.approved = true; // 本地模式直接通过
    arr.push(row);
    LS.set('v2.blogroll', arr);
    return 'OK';
  };

  STORE.listReplies = async function(floor){
    if (useSupa && supabase) {
      const {data, error} = await supabase.from('guestbook_reply').select('*').eq('guestbook_id', floor).order('reply_floor');
      if (!error && Array.isArray(data)) return data;
    }
    return LS.get('v2.gb_replies', []).filter(r => r.guestbook_id === floor).sort((a,b)=>(a.reply_floor||0)-(b.reply_floor||0));
  };
  STORE.addReply = async function({floor, username, message, is_owner}){
    const clean = escapeHtml(message||'').replace(/\n/g,'<br>');
    const exist = await STORE.listReplies(floor);
    const nextFloor = (exist[exist.length - 1]?.reply_floor || 0) + 1;
    const row = {
      guestbook_id: floor, reply_floor: nextFloor,
      username: username || '匿名网友', message: clean,
      is_owner: !!is_owner, created_at: Date.now()
    };
    if (useSupa && supabase) {
      try {
        const {data, error} = await supabase.from('guestbook_reply').insert([row]).select();
        if (!error && data && data[0]) return data[0];
      } catch(e) { /* fall to local */ }
    }
    // local fallback
    const arr = LS.get('v2.gb_replies', []);
    row.id = Math.max(0, ...arr.map(r=>r.id||0)) + 1;
    arr.push(row);
    LS.set('v2.gb_replies', arr);
    return row;
  };

  /* -------- 分类 + 头图映射 -------- */
  STORE.diaryCategories = () => ['全部','碎碎念','校园','音乐','周记','随便写写'];
  STORE.diaryHero = function(category){
    if (category === '校园') return IMG.diary.school;
    if (category === '音乐') return IMG.diary.cd;
    return IMG.diary.candy;
  };
  STORE.ownerPwd = 'binghudie2006'; // 别改，公开页面前端密码本来就是图个乐，防路人乱发
})();

/* -------- 渲染：日记 -------- */
let DIARY_CATEGORY = '全部';
async function paintDiary(){
  const tabs = document.getElementById('diaryTabs');
  const list = document.getElementById('diaryList');
  if (!tabs || !list) return;
  tabs.innerHTML = STORE.diaryCategories().map(c =>
    `<span class="d-tab ${c===DIARY_CATEGORY?'active':''}" onclick="setDiaryCat('${c}')">${c}</span>`
  ).join('');
  const arr = await STORE.listDiary(DIARY_CATEGORY);
  list.innerHTML = arr.map(d => `
    <div class="diary-card" data-id="${d.id}">
      <div class="diary-hero">
        <img src="${escapeAttr(STORE.diaryHero(d.category))}"
             onerror="this.onerror=null;this.style.background='linear-gradient(135deg,#f472b6,#60a5fa,#fde68a)';this.removeAttribute('src');">
        <div class="d-title">${escapeHtml(d.title||'(无题)')} <span style="font-size:14px;vertical-align:middle;">${escapeHtml(d.mood||'😊')}</span></div>
      </div>
      <div class="diary-body-wrap">
        <div class="diary-meta">
          <div><span class="cat-tag cat-tag-${d.category||'随便写写'}">${escapeHtml(d.category||'随便写写')}</span>
          &nbsp;📅 ${fmtDate(d.created_at)}
          </div>
          <div>👁 阅读 ${(d.views||0).toLocaleString()} &nbsp; 💗 <span class="d-likecnt-${d.id}">0</span> 赞</div>
        </div>
        <div class="diary-body-text">${d.body||''}</div>
        <div class="diary-actions">
          <div style="color:#999;font-size:11px;">♡ 欢迎在下面留言板一起聊~</div>
          <button class="like-btn" onclick="likeDiary(${d.id})">💗 点个赞</button>
        </div>
      </div>
    </div>
  `).join('');
  // 异步加载每个帖子的点赞数
  arr.forEach(async d => {
    try {
      const cnt = await countLikes(d.id);
      const el = document.querySelector(`.d-likecnt-${d.id}`);
      if (el) el.textContent = cnt;
      // 顺便记录 views
      await STORE.viewDiary(d.id);
    } catch(_) {}
  });
}
async function countLikes(id){
  // 本地 + 远程各读一次
  if (useSupa && supabase) {
    try {
      const {data,error} = await supabase.from('diary_likes').select('*').eq('diary_id',id);
      if (!error && Array.isArray(data)) return data.length;
    } catch(_) {}
  }
  const arr = JSON.parse(localStorage.getItem('v2.diary_likes') || '[]');
  return arr.filter(x => x.diary_id===id).length;
}
async function setDiaryCat(c){
  DIARY_CATEGORY = c;
  await paintDiary();
}
async function likeDiary(id){
  const res = await STORE.likeDiary(id);
  if (res === '今日已赞') {
    toast('♡ 今天已经赞过这篇啦！明天再来~');
    return;
  }
  const el = document.querySelector(`.d-likecnt-${id}`);
  if (el) el.textContent = (parseInt(el.textContent,10)||0) + 1;
  toast('💗 点赞成功 ♡ 谢谢你！');
}

/* -------- 渲染：友情链接 -------- */
async function paintBlogroll(){
  const grid = document.getElementById('blogrollGrid');
  if (!grid) return;
  const arr = await STORE.listBlogroll();
  const today = (() => {
    const d = new Date();
    return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');
  })();
  grid.innerHTML = arr.map(b => {
    const pressed = !!localStorage.getItem(`br_pressed_${b.id}_${today}`);
    return `
    <div class="br-card">
      <a href="${escapeAttr(b.url || '#')}" target="_blank" rel="noopener noreferrer">
        ${safeImgEl(b.avatar_url || fallbackAvatar(b.name || 'br','#ffd1dc'), b.name || 'br','#ffd1dc')}
      </a>
      <div class="br-info">
        <div class="br-name">
          <a href="${escapeAttr(b.url || '#')}" target="_blank" rel="noopener noreferrer" style="color:inherit;text-decoration:none;">${escapeHtml(b.name||'新小窝')}</a>
        </div>
        <div class="br-slogan">${escapeHtml(b.slogan||'欢迎来访~')}</div>
        <div class="br-actions">
          <button class="press-btn ${pressed?'pressed':''}" ${pressed?'disabled':''} onclick="pressBlogroll(${b.id}, this)">${pressed?'今日已踩 ✓':'💗 踩一下'}</button>
          <span class="br-hits">总踩 <b class="br-hits-${b.id}">${(b.hits||0).toLocaleString()}</b> 次</span>
        </div>
      </div>
    </div>`;
  }).join('');
}
async function pressBlogroll(id, btn){
  const res = await STORE.pressBlogroll(id);
  const hitsEl = document.querySelector(`.br-hits-${id}`);
  if (res.pressed) {
    if (hitsEl) hitsEl.textContent = res.hits.toLocaleString();
    if (btn) { btn.classList.add('pressed'); btn.disabled = true; btn.textContent = '今日已踩 ✓'; }
    toast('💗 踩一下成功！回访感谢~');
  } else {
    if (btn) { btn.classList.add('pressed'); btn.disabled = true; btn.textContent = '今日已踩 ✓'; }
    toast('♡ ' + (res.msg || '今天已经踩过啦'));
  }
}
async function applyBlogroll(){
  const name = document.getElementById('brName')?.value.trim();
  const url  = document.getElementById('brUrl')?.value.trim();
  const slogan = document.getElementById('brSlogan')?.value.trim();
  const result = document.getElementById('brResult');
  if (!name || !slogan) { if (result) { result.style.color='#c00'; result.textContent='❌ 站名和标语必填~'; } return; }
  if (result) { result.style.color='#006'; result.textContent='⏳ 正在提交申请...'; }
  try {
    await STORE.applyBlogroll({name, url, slogan});
    if (result) { result.style.color='#060'; result.textContent='✅ 申请已发送！蝴蝶姐姐审批通过就会显示 ♡'; }
    document.getElementById('brName').value='';
    document.getElementById('brUrl').value='';
    document.getElementById('brSlogan').value='';
    // 本地模式会直接通过，刷新一下
    setTimeout(() => paintBlogroll(), 300);
  } catch(e) {
    if (result) { result.style.color='#c00'; result.textContent='❌ 失败：' + (e.message||e); }
  }
}

/* -------- 渲染：留言楼中楼 -------- */
async function paintGuestbookReplies(){
  // 给所有留言（不管种子还是新写的）查找/插入 reply-wrap
  const gbPosts = document.querySelectorAll('#gbList .gb-post');
  for (let i = 0; i < gbPosts.length; i++) {
    const p = gbPosts[i];
    // 每条留言楼号：尝试从 gb-floor span 获取；没有就从 DOM 中的 data-gb-floor 找
    const floorEl = p.querySelector('.gb-floor');
    const bodyEl  = p.querySelector('.gb-body');
    let floor = bodyEl && bodyEl.getAttribute('data-gb-floor');
    if (!floor && floorEl && floorEl.textContent) {
      const m = floorEl.textContent.match(/(\d+)F/);
      if (m) floor = m[1];
    }
    if (!floor) {
      // 最后兜底：用 gb-body 顺序编号（种子1-3 + 新写 N），直接按写入序给个自增
      floor = i + 1;
      if (bodyEl) bodyEl.setAttribute('data-gb-floor', floor);
    }
    // 如果没有 reply-wrap，给加一个
    let wrap = p.querySelector('.gb-reply-wrap');
    if (!wrap && bodyEl) {
      const html = `
        <div class="gb-reply-wrap" data-gb-floor="${floor}">
          <button class="gb-reply-toggle" onclick="toggleReplies(this)">💬 查看回复 (<span class="gb-reply-cnt">0</span>)</button>
          <div class="gb-reply-list" style="display:none;"></div>
          <div class="gb-reply-form">
            <input type="text" class="gb-re-name" placeholder="昵称" value="匿名网友">
            <input type="text" class="gb-re-msg"  placeholder="回复这条留言（最多120字）">
            <button class="old-btn" onclick="submitReply(this)">📨 回复</button>
            <span class="gb-re-result"></span>
          </div>
        </div>`;
      bodyEl.insertAdjacentHTML('afterend', html);
      wrap = bodyEl.nextElementSibling;
    }
    if (wrap) {
      const replies = await STORE.listReplies(parseInt(floor,10));
      const cnt = wrap.querySelector('.gb-reply-cnt');
      if (cnt) cnt.textContent = replies.length;
      const list = wrap.querySelector('.gb-reply-list');
      if (list) {
        list.innerHTML = replies.map(r => {
          const em = String(r.username||'?').slice(-1).match(/[\u{1F300}-\u{1FAFF}]/u) ? '' : (r.is_owner ? '🦋' : '💬');
          return `
            <div class="gb-reply ${r.is_owner?'owner-true':''}">
              <div class="re-avatar">${em || '💬'}</div>
              <div>
                <div class="re-head">
                  <span class="re-user">${escapeHtml(r.username)}</span>
                  <span style="color:#888;"> 回复 ${floor}-${r.reply_floor} · ${fmtDate(r.created_at)}</span>
                </div>
                <div class="re-body">${r.message||''}</div>
              </div>
            </div>`;
        }).join('');
      }
    }
  }
}
function toggleReplies(btn){
  const list = btn.parentNode.querySelector('.gb-reply-list');
  if (!list) return;
  const open = list.style.display !== 'none';
  list.style.display = open ? 'none' : 'flex';
  const cnt = btn.querySelector('.gb-reply-cnt');
  btn.textContent = `${open?'💬 查看回复':'🔽 收起回复'} (${cnt?cnt.textContent:0})`;
}
async function submitReply(btn){
  const wrap = btn.closest('.gb-reply-wrap');
  if (!wrap) return;
  const floor = parseInt(wrap.getAttribute('data-gb-floor') || '0', 10);
  const nameEl = wrap.querySelector('.gb-re-name');
  const msgEl  = wrap.querySelector('.gb-re-msg');
  const resEl  = wrap.querySelector('.gb-re-result');
  const name = nameEl.value.trim() || '匿名网友';
  const msg  = msgEl.value.trim();
  if (!msg) { if (resEl) { resEl.style.color='#c00'; resEl.textContent='❌ 内容必填~';} return; }
  if (msg.length > 120) { if (resEl) { resEl.style.color='#c00'; resEl.textContent='❌ 最多120字~';} return; }
  // 站长回复：昵称=冰蝴蝶 + owner 密码已登录时，is_owner=true
  const owner = (name === '冰蝴蝶🦋' || name === '冰蝴蝶') && !!window.__ownerLoggedIn;
  if (resEl) { resEl.style.color='#006'; resEl.textContent='⏳ 发表中...'; }
  try {
    await STORE.addReply({floor, username: name, message: msg, is_owner: owner});
    msgEl.value = '';
    if (resEl) { resEl.style.color='#060'; resEl.textContent='✅ 回复发表成功 ♡'; }
    await paintGuestbookReplies();
  } catch(e) {
    if (resEl) { resEl.style.color='#c00'; resEl.textContent='❌ 失败：' + (e.message||e); }
  }
  setTimeout(()=>{ if (resEl) resEl.textContent=''; }, 5000);
}

/* -------- 站长写日记模式（简易密码）-------- */
let __ownerLoggedIn = false;
function openWriteDiary(){
  const m = document.getElementById('ownerModal');
  if (m) m.classList.add('show');
}
function closeOwnerModal(){
  const m = document.getElementById('ownerModal');
  if (m) m.classList.remove('show');
}
function ownerLogin(){
  const pwd = document.getElementById('ownerPwd').value;
  const hint = document.getElementById('pwdHint');
  if (pwd === STORE.ownerPwd) {
    __ownerLoggedIn = true; window.__ownerLoggedIn = true;
    document.getElementById('writeDiaryForm').style.display = '';
    hint.textContent = '';
    toast('🦋 站长你好，欢迎回来~ 记得发完日记把密码换个安全的（前端密码别当真哈）');
  } else {
    hint.textContent = '❌ 密码不对哦~';
  }
}
async function submitDiary(){
  if (!__ownerLoggedIn) { alert('请先输入正确的站长密码！'); return; }
  const title = document.getElementById('dTitle').value.trim();
  const category = document.getElementById('dCategory').value;
  const mood = document.getElementById('dMood').value;
  const body = document.getElementById('dBody').value.trim();
  const result = document.getElementById('diaryResult');
  if (!title || !body) { result.style.color='#c00'; result.textContent='❌ 标题和正文必填~'; return; }
  result.style.color='#006'; result.textContent='⏳ 发表中...';
  try {
    await STORE.addDiary({title, category, mood, body});
    result.style.color='#060'; result.textContent='✅ 日记发表成功 ♡ 去首页看看吧！';
    document.getElementById('dTitle').value='';
    document.getElementById('dBody').value='';
    await paintDiary();
  } catch(e) {
    result.style.color='#c00'; result.textContent='❌ 失败：' + (e.message||e);
  }
}

/* -------- 皮肤切换（3 套）-------- */
const THEMES = ['ice','purple','qq'];
function setTheme(name){
  document.body.classList.remove('theme-ice','theme-purple','theme-qq');
  if (THEMES.indexOf(name) === -1) name = 'ice';
  document.body.classList.add('theme-' + name);
  localStorage.setItem('theme', name);
}
function cycleTheme(){
  const cur = localStorage.getItem('theme') || 'purple';
  const next = THEMES[(THEMES.indexOf(cur)+1) % THEMES.length];
  setTheme(next);
  toast(`🎨 皮肤已切换：${next==='ice'?'冰蓝 💎':next==='purple'?'薰衣草紫 💜':'QQ2005 橙 🧡'}`);
}

/* -------- 飘落 + 尾迹特效 -------- */
const FX_MODES = ['off','snow','sakura','star','butterfly'];
let FX = { mode:'off', canvas:null, ctx:null, w:0, h:0, parts:[], lastT:0, fps:60, fpsLast:0, fpsCount:0, reduced: false, initialized:false };
function setFx(mode){
  FX.mode = FX_MODES.indexOf(mode) >= 0 ? mode : 'off';
  localStorage.setItem('fx', FX.mode);
  if (!FX.initialized) initFx();
  updateParticleGravityByMode();
}
function cycleFx(){
  const cur = localStorage.getItem('fx') || 'sakura';
  const next = FX_MODES[(FX_MODES.indexOf(cur)+1) % FX_MODES.length];
  setFx(next);
  const label = {off:'关闭 ✅', snow:'❄️ 雪花', sakura:'🌸 樱花', star:'⭐ 星星', butterfly:'🦋 蝴蝶'};
  toast(`✨ 飘落特效：${label[next]}`);
}
function initFx(){
  FX.canvas = document.getElementById('fx');
  if (!FX.canvas) return;
  FX.ctx    = FX.canvas.getContext('2d');
  FX.reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  resizeFx();
  window.addEventListener('resize', resizeFx);
  window.addEventListener('mousemove', onFxMouse, {passive:true});
  FX.initialized = true;
  FX.lastT = performance.now();
  requestAnimationFrame(rafFx);
}
function resizeFx(){
  FX.canvas.width  = window.innerWidth;
  FX.canvas.height = window.innerHeight;
  FX.w = FX.canvas.width; FX.h = FX.canvas.height;
}
function onFxMouse(e){
  if (FX.reduced || FX.fps < 25) return;  // 弱机降级
  if (Math.random() > 0.5) return;  // 每 20ms 1 颗（节流）
  FX.parts.push({
    type:'trail', x: e.clientX, y: e.clientY,
    vx: (Math.random()-0.5)*0.2, vy: (Math.random()-0.5)*0.2,
    life: 900, age: 0, r: 2 + Math.random()*2,
    color: pick(['#fef08a','#fda4af','#a5f3fc','#ddd6fe','#fcd34d'])
  });
  if (FX.parts.length > 120) FX.parts.splice(0, FX.parts.length - 120);
}
function pick(a){ return a[Math.floor(Math.random()*a.length)]; }
function updateParticleGravityByMode(){
  // 模式切换时，初始丢一批粒子
  const cap = FX.mode === 'off' ? 0 : (FX.reduced ? 24 : 60);
  while (FX.parts.length > cap) FX.parts.splice(0,1);
}
function spawnRain(){
  if (FX.mode === 'off' || FX.reduced) return;
  const count = (FX.fps<30) ? 1 : 2;
  for (let i = 0; i < count; i++){
    const base = {
      x: Math.random()*FX.w, y: -12,
      life: 12000, age: 0, type: FX.mode
    };
    if (FX.mode === 'snow') {
      Object.assign(base, { r: 2+Math.random()*3, vx:(Math.random()-.5)*.3, vy:.4+Math.random()*.5, color:'#ffffff' });
    } else if (FX.mode === 'sakura') {
      Object.assign(base, { r: 3+Math.random()*2, vx:(Math.random()-.5)*.7, vy:.3+Math.random()*.3, rot: Math.random()*6.28, vr:(Math.random()-.5)*.08, color: pick(['#fbcfe8','#f9a8d4','#fecaca']) });
    } else if (FX.mode === 'star') {
      Object.assign(base, { r: 2+Math.random()*2, vx:0, vy:.3+Math.random()*.4, twinkle: Math.random()*6.28, color: pick(['#fde68a','#fbbf24','#fff7d6']) });
    } else if (FX.mode === 'butterfly') {
      Object.assign(base, { r: 5+Math.random()*2, vx:(Math.random()-.5)*1.2, vy:.1+Math.random()*.2, t: Math.random()*6.28, color: pick(['#c084fc','#f472b6','#60a5fa']) });
    }
    FX.parts.push(base);
    if (FX.parts.length > 180) FX.parts.splice(0,1);
  }
}
function rafFx(t){
  const dt = Math.min(64, t - FX.lastT); FX.lastT = t;
  // FPS 测量
  FX.fpsCount++;
  if (t - FX.fpsLast >= 1000) { FX.fps = FX.fpsCount; FX.fpsCount = 0; FX.fpsLast = t; }
  requestAnimationFrame(rafFx);
  if (!FX.ctx) return;
  const ctx = FX.ctx;
  ctx.clearRect(0,0,FX.w,FX.h);
  // 每隔 N ms 喷 1~2 颗雨
  spawnRain();
  // 更新 + 画
  const alive = [];
  for (let i = 0; i < FX.parts.length; i++){
    const p = FX.parts[i];
    p.age += dt;
    if (p.age > p.life) continue;
    if (p.y > FX.h + 20) continue;
    if (p.x < -20 || p.x > FX.w + 20) continue;
    if (p.type === 'trail'){
      p.x += p.vx; p.y += p.vy;
    } else {
      p.x += p.vx * (dt/16);
      p.y += p.vy * (dt/16);
      if (FX.mode === 'sakura') { p.rot = (p.rot||0) + (p.vr||0)*dt; }
      if (FX.mode === 'star')   { p.twinkle = (p.twinkle||0) + dt*0.008; }
      if (FX.mode === 'butterfly') { p.t = (p.t||0) + dt*0.01; p.vx += Math.sin(p.t)*0.02; }
    }
    drawParticle(ctx, p);
    alive.push(p);
  }
  FX.parts = alive;
}
function drawParticle(ctx, p){
  ctx.save();
  if (p.type === 'trail'){
    const alpha = 1 - p.age / p.life;
    ctx.globalAlpha = Math.max(0, alpha);
    ctx.fillStyle = p.color;
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.r, 0, Math.PI*2);
    ctx.fill();
  } else if (p.type === 'snow') {
    ctx.globalAlpha = 0.9;
    ctx.fillStyle = p.color;
    ctx.beginPath(); ctx.arc(p.x,p.y,p.r,0,Math.PI*2); ctx.fill();
  } else if (p.type === 'sakura') {
    ctx.translate(p.x,p.y); ctx.rotate(p.rot||0);
    ctx.fillStyle = p.color;
    ctx.beginPath();
    for (let k = 0; k < 5; k++){
      const a = k/5*Math.PI*2 - Math.PI/2;
      ctx.ellipse(Math.cos(a)*p.r, Math.sin(a)*p.r, p.r*0.9, p.r*0.5, a, 0, Math.PI*2);
    }
    ctx.fill();
  } else if (p.type === 'star') {
    const sp = 0.7 + 0.3*Math.sin(p.twinkle||0);
    ctx.globalAlpha = sp;
    ctx.fillStyle = p.color;
    ctx.translate(p.x,p.y); ctx.rotate(p.twinkle||0);
    drawStar(ctx, 0, 0, 4, p.r*2, p.r);
    ctx.fill();
  } else if (p.type === 'butterfly') {
    const w = Math.abs(Math.sin(p.t||0))*p.r + p.r*0.2;
    ctx.fillStyle = p.color;
    ctx.translate(p.x,p.y);
    ctx.beginPath();
    ctx.ellipse(-w*.6, 0, w, p.r*0.8, -0.3, 0, Math.PI*2); ctx.fill();
    ctx.beginPath();
    ctx.ellipse( w*.6, 0, w, p.r*0.8,  0.3, 0, Math.PI*2); ctx.fill();
  }
  ctx.restore();
}
function drawStar(ctx, cx, cy, spikes, outer, inner){
  let rot = -Math.PI/2;
  const step = Math.PI / spikes;
  ctx.beginPath();
  ctx.moveTo(cx, cy - outer);
  for (let i = 0; i < spikes; i++){
    ctx.lineTo(cx + Math.cos(rot)*outer, cy + Math.sin(rot)*outer);
    rot += step;
    ctx.lineTo(cx + Math.cos(rot)*inner, cy + Math.sin(rot)*inner);
    rot += step;
  }
  ctx.closePath();
}

/* -------- Toast 提示 -------- */
function toast(msg){
  let t = document.getElementById('y2kToast');
  if (!t) {
    t = document.createElement('div');
    t.id = 'y2kToast';
    t.style.cssText = 'position:fixed;left:50%;top:16%;transform:translateX(-50%);padding:6px 14px;background:#fff5fd;color:#a00060;border:2px outset #ff99cc;box-shadow:3px 3px 0 rgba(0,0,0,.35);font-size:13px;font-family:SimSun;z-index:9999;opacity:0;transition:opacity .25s;pointer-events:none;';
    document.body.appendChild(t);
  }
  t.textContent = msg; t.style.opacity = '1';
  clearTimeout(t.__timer);
  t.__timer = setTimeout(()=>{ t.style.opacity = '0'; }, 2400);
}

// 覆写原来的 paintGuestbook：画完之后立刻顺便把楼中楼也画了
const _origPaintGB = paintGuestbook;
paintGuestbook = function(list){
  _origPaintGB(list);
  // 小等一下 DOM 插入
  setTimeout(()=>paintGuestbookReplies().catch(()=>null), 20);
};

// 提交留言后，把楼号也写到 data-gb-floor 方便 reply 定位
const _origSubmitGB = submitGB;
submitGB = async function(){
  await _origSubmitGB();
  setTimeout(()=>paintGuestbookReplies().catch(()=>null), 80);
};
'''

anchor = '/* ============ 启动：数据加载 + 定时器 ============ */'
assert anchor in html
html = html.replace(anchor, INJECT_6_JS + '\n\n' + anchor, 1)

# Also update bootstrap(): call paintDiary/paintBlogroll + theme/fx after gb
old_bootstrap_tail = r'''  // 3) 留言板
  try {
    const gb = await STORE.listGuestbook(50);
    paintGuestbook(gb);
  } catch(_) {}
})();'''
new_bootstrap_tail = r'''  // 3) 留言板
  try {
    const gb = await STORE.listGuestbook(50);
    paintGuestbook(gb);
  } catch(_) {}

  // 4) V2：日记 + 友情链接
  try { await Promise.all([paintDiary(), paintBlogroll()]); } catch(e){ console.warn('V2 paint fail', e); }
  try {
    setTheme(localStorage.getItem('theme') || 'purple');
    setFx(localStorage.getItem('fx') || 'sakura');
  } catch(_) {}
})();'''
assert old_bootstrap_tail in html, "Could not find old bootstrap tail for replacement"
html = html.replace(old_bootstrap_tail, new_bootstrap_tail, 1)
print("✅ INJECT 6: V2 JS（图片常量 / STORE 扩展 / 渲染 / 特效 / 皮肤） 已插入并改写 bootstrap")
# ==========================================================


FILE.write_text(html, encoding='utf-8')
print("\n🆗 全部 6 段注入完成。最终文件尺寸：", len(html), "字节，行数约：", html.count('\n')+1)
