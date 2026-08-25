"""背景换真：QQ 空间千禧年皮肤（qzone2000.com 归档原图）
删除：上轮『背景超升级』整块（10层渐变+装饰层+keyframes）+ bg-deco DOM
替换：旧 body 升级块 → 3 套皮肤各一张真实 1260-1280 宽皮肤原图
"""
import re

path = "/workspace/index.html"
html = open(path, "r", encoding="utf-8").read()
orig_len = len(html)

# ========== 1. 删除『背景超升级』整块（1017 行 → .page-shell 之前）==========
START = "/* ===== 🌟 背景超升级：光晕+斜纹+棋盘+扫光+装饰层（黄钻感拉满） ===== */"
END   = ".page-shell { max-width: 100%; }"
i0 = html.find(START)
i1 = html.find(END)
if i0 < 0 or i1 < 0 or i1 < i0:
    raise SystemExit(f"❌ 背景超升级块定位失败 i0={i0} i1={i1}")
html = html[:i0] + html[i1:]
print("✅ 已删除『背景超升级』CSS 块")

# ========== 2. 删除 bg-deco 装饰层 DOM ==========
DECO_START = '<div id="bg-deco" aria-hidden="true">'
i2 = html.find(DECO_START)
if i2 < 0:
    raise SystemExit("❌ 找不到 bg-deco DOM")
# 找到配对的 </div>（计数：<div 与 </div> 配对）
depth = 0; j = i2
while j < len(html):
    o = html.find("<div", j, j+80)
    c = html.find("</div>", j, j+80)
    if o < 0 and c < 0: break
    if c < 0 or (0 <= o < c):
        depth += 1; j = o + 4
    else:
        depth -= 1; j = c + 6
        if depth == 0: break
html = html[:i2] + html[j:]
print("✅ 已删除 bg-deco DOM")

# ========== 3. 替换旧 body 升级块 → 真实皮肤 ==========
OLD_BODY = """/* --- body 高浓度背景：旧 Win98 蓝底 + 点阵噪点 + 渐变叠层 --- */
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
"""
NEW_BODY = """/* --- body 真实千禧年 QQ 空间皮肤背景（qzone2000.com 归档原图，cover 铺满）--- */
body {
  background:
    radial-gradient(circle at 50% 40%, rgba(255,255,255,0.10) 1px, transparent 2px) 0 0 / 4px 4px,
    linear-gradient(180deg, var(--body-bg1,#000080) 0%, var(--body-bg2,#0044aa) 60%, #001155 100%),
    url("https://qzone2000.com/library/skin/43766_top.jpg") center top / cover no-repeat fixed !important;
}
body.theme-purple {
  background:
    radial-gradient(rgba(255,200,255,0.12) 1px, transparent 1px) 0 0 / 4px 4px,
    linear-gradient(180deg,#1a0540 0%,#4c1d95 50%,#701a75 100%),
    url("https://qzone2000.com/library/skin/43080_top.jpg") center top / cover no-repeat fixed !important;
}
body.theme-qq {
  background:
    radial-gradient(rgba(255,200,100,0.10) 1px, transparent 1px) 0 0 / 4px 4px,
    linear-gradient(180deg,#2a0800 0%,#7a2200 50%,#4c0519 100%),
    url("https://qzone2000.com/library/skin/43730_top.jpg") center top / cover no-repeat fixed !important;
}
/* 手机端：scroll 避免 iOS fixed 抖动 */
@media (max-width: 780px) {
  body, body.theme-purple, body.theme-qq { background-attachment: scroll !important; }
}
"""
# 容错：若旧块文本不精确匹配，退化为用行号重建区间
if OLD_BODY not in html:
    print("⚠️ 旧 body 块精确文本不匹配，改用正则按特征切除")
    pat = re.compile(r'/\* --- body 高浓度背景.*?body\.theme-qq \{[^}]*\}\n', re.S)
    html, n = pat.subn(NEW_BODY, html, count=1)
    if n != 1:
        raise SystemExit("❌ 旧 body 块替换失败")
    print("✅ 旧 body 块已替换（正则）")
else:
    html = html.replace(OLD_BODY, NEW_BODY, 1)
    print("✅ 旧 body 块已替换")

open(path, "w", encoding="utf-8").write(html)
print(f"✅ 写入完成 {len(html):,}B（原 {orig_len:,}B，净减 {orig_len-len(html):,}B）")