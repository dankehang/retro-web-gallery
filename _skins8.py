"""扩皮肤：3 套 → 8 套（全部真实 qzone2000 归档皮肤图）"""
import re
path = "/workspace/index.html"
h = open(path, "r", encoding="utf-8").read()

# ---------- 1. CSS 变量块追加 5 个主题 ----------
VARS_OLD = """body.theme-qq {
  --title-g1:#ff6600; --title-g2:#c03300; --title-fg:#fffacd;
  --accent:#ff8833; --btn-primary-1:#ff8833; --btn-primary-2:#c05213;
  --body-bg1:#2a0800; --body-bg2:#7a2200;
}
"""
VARS_NEW = VARS_OLD + """body.theme-pink { /* 🌸 樱之恋 */
  --title-g1:#d63384; --title-g2:#9c1f63; --title-fg:#fff0f6;
  --accent:#f06595; --btn-primary-1:#f06595; --btn-primary-2:#c2255c;
  --body-bg1:#3d0e26; --body-bg2:#7a1f4d;
}
body.theme-green { /* 🍃 碧水莲天 */
  --title-g1:#0d9f74; --title-g2:#04694c; --title-fg:#eafff6;
  --accent:#10b981; --btn-primary-1:#0d9f74; --btn-primary-2:#04694c;
  --body-bg1:#02150e; --body-bg2:#0b4a38;
}
body.theme-black { /* 🖤 暗夜黑 */
  --title-g1:#6d28d9; --title-g2:#2e1065; --title-fg:#ff9be0;
  --accent:#a855f7; --btn-primary-1:#8b5cf6; --btn-primary-2:#4c1d95;
  --body-bg1:#12000f; --body-bg2:#24142e;
}
body.theme-yellow { /* 💛 古典旋律 */
  --title-g1:#d9a400; --title-g2:#8a6200; --title-fg:#fff0b3;
  --accent:#fbbf24; --btn-primary-1:#d9a400; --btn-primary-2:#996d00;
  --body-bg1:#2a1e00; --body-bg2:#6b4a00;
}
body.theme-red { /* ❤️ 校园的甜蜜 */
  --title-g1:#e11d48; --title-g2:#9f1239; --title-fg:#ffe6ea;
  --accent:#f43f5e; --btn-primary-1:#e11d48; --btn-primary-2:#9f1239;
  --body-bg1:#2b0008; --body-bg2:#7a0923;
}
"""
assert VARS_OLD in h, "变量块定位失败"
h = h.replace(VARS_OLD, VARS_NEW, 1)
print("✅ 1. CSS 变量 +5 主题")

# ---------- 2. body 背景块追加 5 个主题 ----------
BG_OLD = """body.theme-qq {
  background:
    radial-gradient(rgba(255,200,100,0.10) 1px, transparent 1px) 0 0 / 4px 4px,
    linear-gradient(180deg,#2a0800 0%,#7a2200 50%,#4c0519 100%),
    url("https://qzone2000.com/library/skin/43730_top.jpg") center top / cover no-repeat fixed !important;
}
"""
BG_NEW = BG_OLD + """body.theme-pink { /* 🌸 樱之恋 42595 */
  background:
    radial-gradient(rgba(255,150,220,0.14) 1px, transparent 1px) 0 0 / 4px 4px,
    linear-gradient(180deg,#3d0e26 0%,#7a1f4d 50%,#5b0e3a 100%),
    url("https://qzone2000.com/library/skin/42595_top.jpg") center top / cover no-repeat fixed !important;
}
body.theme-green { /* 🍃 碧水莲天 43564 */
  background:
    radial-gradient(rgba(150,255,200,0.12) 1px, transparent 1px) 0 0 / 4px 4px,
    linear-gradient(180deg,#02150e 0%,#0b4a38 50%,#03231a 100%),
    url("https://qzone2000.com/library/skin/43564_top.jpg") center top / cover no-repeat fixed !important;
}
body.theme-black { /* 🖤 暗夜黑 42876 */
  background:
    radial-gradient(rgba(255,150,230,0.12) 1px, transparent 1px) 0 0 / 4px 4px,
    linear-gradient(180deg,#12000f 0%,#24142e 50%,#16061f 100%),
    url("https://qzone2000.com/library/skin/42876_top.jpg") center top / cover no-repeat fixed !important;
}
body.theme-yellow { /* 💛 古典旋律 43778 */
  background:
    radial-gradient(rgba(255,230,150,0.14) 1px, transparent 1px) 0 0 / 4px 4px,
    linear-gradient(180deg,#2a1e00 0%,#6b4a00 50%,#3d2b00 100%),
    url("https://qzone2000.com/library/skin/43778_top.jpg") center top / cover no-repeat fixed !important;
}
body.theme-red { /* ❤️ 校园的甜蜜 43397 */
  background:
    radial-gradient(rgba(255,150,150,0.14) 1px, transparent 1px) 0 0 / 4px 4px,
    linear-gradient(180deg,#2b0008 0%,#7a0923 50%,#3d0411 100%),
    url("https://qzone2000.com/library/skin/43397_top.jpg") center top / cover no-repeat fixed !important;
}
/* 手机端：scroll 避免 iOS fixed 抖动 */
@media (max-width: 780px) {
  body { background-attachment: scroll !important; }
}
"""
assert BG_OLD in h, "背景块定位失败"
h = h.replace(BG_OLD, BG_NEW, 1)
print("✅ 2. body 背景 +5 主题")

# ---------- 3. THEMES 数组 + 标签映射 + cycleTheme ----------
OLD_JS = """const THEMES = ['ice','purple','qq'];
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
"""
NEW_JS = """const THEMES = ['ice','purple','qq','pink','green','black','yellow','red'];
const THEME_LABEL = {
  ice:'冰蓝 💎', purple:'薰衣草紫 💜', qq:'QQ2005 橙 🧡',
  pink:'樱之恋 🌸', green:'碧水莲天 🍃', black:'暗夜黑 🖤',
  yellow:'古典旋律 💛', red:'校园的甜蜜 ❤️'
};
function setTheme(name){
  document.body.classList.remove('theme-ice','theme-purple','theme-qq','theme-pink','theme-green','theme-black','theme-yellow','theme-red');
  if (THEMES.indexOf(name) === -1) name = 'ice';
  document.body.classList.add('theme-' + name);
  localStorage.setItem('theme', name);
}
function cycleTheme(){
  const cur = localStorage.getItem('theme') || 'purple';
  const next = THEMES[(THEMES.indexOf(cur)+1) % THEMES.length];
  setTheme(next);
  toast(`🎨 皮肤已切换：${THEME_LABEL[next]}`);
}
"""
assert OLD_JS in h, "JS 块定位失败"
h = h.replace(OLD_JS, NEW_JS, 1)
print("✅ 3. JS THEMES/标签/cycleTheme")

# ---------- 4. 按钮 title 更新 ----------
OLD_TITLE = '<button class="fx-btn" onclick="cycleTheme()" title="换肤：冰蓝 / 薰衣草紫 / QQ橙"'
assert OLD_TITLE in h, "按钮定位失败"
h = h.replace(OLD_TITLE, '<button class="fx-btn" onclick="cycleTheme()" title="换肤：冰蓝💎 / 薰衣草紫💜 / 2005橙🧡 / 樱粉🌸 / 碧绿🍃 / 暗夜🖤 / 金辉💛 / 中国红❤️"', 1)
print("✅ 4. 按钮 title")

open(path, "w", encoding="utf-8").write(h)
print(f"✅ 写入完成 {len(h):,}B")