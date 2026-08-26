#!/usr/bin/env python3
"""修复 v2-visual CSS 中 7 个缺失的闭合大括号"""
with open('/workspace/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

orig = '''body.theme-purple {
  --title-g1:#7a2bce; --title-g2:#4a0e8a; --title-fg:#ffe6ff;
  --accent:#c084fc; --btn-primary-1:#c084fc; --btn-primary-2:#7e22ce;
  --body-bg1:#1a0540; --body-bg2:#4c1d95;
  --deco-tint:#d8a9ff;

body.theme-qq {
  --title-g1:#ff6600; --title-g2:#c03300; --title-fg:#fffacd;
  --accent:#ff8833; --btn-primary-1:#ff8833; --btn-primary-2:#c05213;
  --body-bg1:#2a0800; --body-bg2:#7a2200;
  --deco-tint:#ffb35c;

body.theme-pink { /* 🌸 樱之恋 */
  --title-g1:#d63384; --title-g2:#9c1f63; --title-fg:#fff0f6;
  --accent:#f06595; --btn-primary-1:#f06595; --btn-primary-2:#c2255c;
  --body-bg1:#3d0e26; --body-bg2:#7a1f4d;
  --deco-tint:#ff9ad5;

body.theme-green { /* 🍃 碧水莲天 */
  --title-g1:#0d9f74; --title-g2:#04694c; --title-fg:#eafff6;
  --accent:#10b981; --btn-primary-1:#0d9f74; --btn-primary-2:#04694c;
  --body-bg1:#02150e; --body-bg2:#0b4a38;
  --deco-tint:#7de3b0;

body.theme-black { /* 🖤 暗夜黑 */
  --title-g1:#6d28d9; --title-g2:#2e1065; --title-fg:#ff9be0;
  --accent:#a855f7; --btn-primary-1:#8b5cf6; --btn-primary-2:#4c1d95;
  --body-bg1:#12000f; --body-bg2:#24142e;
  --deco-tint:#ff7ad9;

body.theme-yellow { /* 💛 古典旋律 */
  --title-g1:#d9a400; --title-g2:#8a6200; --title-fg:#fff0b3;
  --accent:#fbbf24; --btn-primary-1:#d9a400; --btn-primary-2:#996d00;
  --body-bg1:#2a1e00; --body-bg2:#6b4a00;
  --deco-tint:#ffdf6b;

body.theme-red { /* ❤️ 校园的甜蜜 */
  --title-g1:#e11d48; --title-g2:#9f1239; --title-fg:#ffe6ea;
  --accent:#f43f5e; --btn-primary-1:#e11d48; --btn-primary-2:#9f1239;
  --body-bg1:#2b0008; --body-bg2:#7a0923;
  --deco-tint:#ff8fa0;'''

fixed = '''body.theme-purple {
  --title-g1:#7a2bce; --title-g2:#4a0e8a; --title-fg:#ffe6ff;
  --accent:#c084fc; --btn-primary-1:#c084fc; --btn-primary-2:#7e22ce;
  --body-bg1:#1a0540; --body-bg2:#4c1d95;
  --deco-tint:#d8a9ff;
}
body.theme-qq {
  --title-g1:#ff6600; --title-g2:#c03300; --title-fg:#fffacd;
  --accent:#ff8833; --btn-primary-1:#ff8833; --btn-primary-2:#c05213;
  --body-bg1:#2a0800; --body-bg2:#7a2200;
  --deco-tint:#ffb35c;
}
body.theme-pink { /* 🌸 樱之恋 */
  --title-g1:#d63384; --title-g2:#9c1f63; --title-fg:#fff0f6;
  --accent:#f06595; --btn-primary-1:#f06595; --btn-primary-2:#c2255c;
  --body-bg1:#3d0e26; --body-bg2:#7a1f4d;
  --deco-tint:#ff9ad5;
}
body.theme-green { /* 🍃 碧水莲天 */
  --title-g1:#0d9f74; --title-g2:#04694c; --title-fg:#eafff6;
  --accent:#10b981; --btn-primary-1:#0d9f74; --btn-primary-2:#04694c;
  --body-bg1:#02150e; --body-bg2:#0b4a38;
  --deco-tint:#7de3b0;
}
body.theme-black { /* 🖤 暗夜黑 */
  --title-g1:#6d28d9; --title-g2:#2e1065; --title-fg:#ff9be0;
  --accent:#a855f7; --btn-primary-1:#8b5cf6; --btn-primary-2:#4c1d95;
  --body-bg1:#12000f; --body-bg2:#24142e;
  --deco-tint:#ff7ad9;
}
body.theme-yellow { /* 💛 古典旋律 */
  --title-g1:#d9a400; --title-g2:#8a6200; --title-fg:#fff0b3;
  --accent:#fbbf24; --btn-primary-1:#d9a400; --btn-primary-2:#996d00;
  --body-bg1:#2a1e00; --body-bg2:#6b4a00;
  --deco-tint:#ffdf6b;
}
body.theme-red { /* ❤️ 校园的甜蜜 */
  --title-g1:#e11d48; --title-g2:#9f1239; --title-fg:#ffe6ea;
  --accent:#f43f5e; --btn-primary-1:#e11d48; --btn-primary-2:#9f1239;
  --body-bg1:#2b0008; --body-bg2:#7a0923;
  --deco-tint:#ff8fa0;
}'''

assert orig in content, "原始片段未找到，请检查"
new_content = content.replace(orig, fixed)

start = new_content.find('<style id="v2-visual">')
end = new_content.find('</style>', start)
css = new_content[start:end]
opens = css.count('{')
closes = css.count('}')
print(f"修复后 CSS 块：Open={opens}, Close={closes}, 差={opens-closes}")

with open('/workspace/index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("已修复 /workspace/index.html")
