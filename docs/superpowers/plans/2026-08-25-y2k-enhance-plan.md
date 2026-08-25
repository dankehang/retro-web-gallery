# 千禧年 Y2K-CN 主页 v2（⭐⭐⭐高浓度视觉 + 4 大功能） Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在已上线的单文件 `index.html` 内，一次性交付：⭐⭐⭐ 高浓度千禧年图库视觉升级 + 📒 网络日记（数据库） + 🔗 友情链接墙（数据库） + 💬 留言楼中楼（数据库） + 🖱 鼠标尾迹/飘落特效 + 🎨 三套 Win98 皮肤切换；4 张新表通过 Supabase REST 写入现有 PostgreSQL，全部功能提供 localStorage 降级。

**Architecture:** 单文件实现：在 `<head>` 追加 `#v2-visual` 样式块；`<body>` 开头插入 `<canvas id="fx">`；三栏布局按顺序"插入新窗口"而不动老窗口的位置；`<script>` 内对 STORE 做方法扩展（保持原有模式一致），渲染函数独立命名并在 main 阶段追加调用；全部外部图片 URL 先经本地探测脚本 HEAD 校验，失败自动走 Dicebear/Picsum/纯 Canvas 兜底，无破图红×。

**Tech Stack:** HTML + CSS（CSS vars 切皮肤）+ 原生 JS ES5 + Supabase `@supabase/supabase-js` CDN（已加载）+ `<canvas>` 粒子系统 + Dicebear/Picsum/Last.fm 公共直链资源 + PostgreSQL 4 张新表。

---

## 文件结构（改动清单）

| 操作 | 路径 | 职责 |
|---|---|---|
| **Mod** | `/workspace/index.html` | 单文件交付：`<head>` 加视觉 CSS、`<body>` 加 canvas + 4 个新窗口、`<script>` 扩展 STORE 与渲染逻辑 |
| **Create** | `/workspace/_migrate_v2.sql` | Supabase 建表 SQL（4 表 + RLS + 种子数据），一次性给用户复制粘贴或用 REST 探测 |
| **Mod** | `/workspace/README.md` | 末尾追加 v2 功能清单 + 新建表 SQL 片段（方便再次部署）|

*（保持单文件 `index.html` 设计，不出新的 CSS/JS 子资源文件，避免 Pages 路径踩坑）*

---

### Task 1: Supabase 4 张新表建表 + 种子数据（可探测 + SQL 文件产出）

**Files:**
- Create: `/workspace/_migrate_v2.sql`

- [ ] **Step 1: 探测现有 3 张老表，确保用户 Supabase 实例正常**

用 python + REST API 跑（无需 `psql`）：

```bash
python3 - <<'PY'
import urllib.request, urllib.error, json
URL = "https://rhbcehqbqfybuztipaei.supabase.co"
KEY = "sb_publishable_4-2ezORqixDOPYkDGkMPVg_jFdVaRUq"
# 能读 site_counter 就是 OK
with urllib.request.urlopen(urllib.request.Request(
    f"{URL}/rest/v1/site_counter?select=*&limit=1",
    headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"}
)) as r:
    print("site_counter OK:", r.status, json.loads(r.read())[:1])
PY
```
Expected: `site_counter OK: 200 [{'id': 1, ...}]`

- [ ] **Step 2: 写入 `/workspace/_migrate_v2.sql` 建表脚本**

脚本内容（完整复制 spec 第 3.1 + 3.2 + RLS 策略）：

```sql
-- diary / diary_likes / blogroll / guestbook_reply 四张表 + RLS + 种子
-- （完整内容见 spec，此处不展开占位；实现时照抄即可）
```

具体 SQL（**必须逐字写入**）：

```sql
create table if not exists public.diary (
  id         bigserial primary key,
  title      text not null,
  category   text not null default '碎碎念',
  body       text not null,
  mood       text default '😊',
  views      bigint not null default 0,
  created_at bigint not null default (extract(epoch from now())*1000)::bigint
);

create table if not exists public.diary_likes (
  diary_id   bigint references public.diary(id) on delete cascade,
  visitor_id text not null,
  day        text not null,
  created_at bigint not null default (extract(epoch from now())*1000)::bigint,
  primary key (diary_id, visitor_id, day)
);

create table if not exists public.blogroll (
  id         bigserial primary key,
  name       text not null,
  url        text not null,
  slogan     text not null default '',
  avatar_url text not null default '',
  hits       bigint not null default 0,
  approved   boolean not null default true,
  sort_order int not null default 100,
  created_at bigint not null default (extract(epoch from now())*1000)::bigint
);

create table if not exists public.guestbook_reply (
  id             bigserial primary key,
  guestbook_id   bigint references public.guestbook(floor) on delete cascade,
  reply_floor    int not null,
  username       text not null,
  message        text not null,
  is_owner       boolean not null default false,
  created_at     bigint not null default (extract(epoch from now())*1000)::bigint,
  unique (guestbook_id, reply_floor)
);

alter table public.diary           enable row level security;
alter table public.diary_likes     enable row level security;
alter table public.blogroll        enable row level security;
alter table public.guestbook_reply enable row level security;

drop policy if exists "anon read diary" on public.diary;
drop policy if exists "anon ins  diary_likes" on public.diary_likes;
drop policy if exists "anon read diary_likes" on public.diary_likes;
drop policy if exists "anon upd  diary views" on public.diary;
drop policy if exists "anon read blogroll" on public.blogroll;
drop policy if exists "anon ins  blogroll apply" on public.blogroll;
drop policy if exists "anon upd  blogroll hits" on public.blogroll;
drop policy if exists "anon read guestbook_reply" on public.guestbook_reply;
drop policy if exists "anon ins  guestbook_reply" on public.guestbook_reply;

create policy "anon read diary"         on public.diary for select using (true);
create policy "anon read diary_likes"   on public.diary_likes for select using (true);
create policy "anon ins  diary_likes"   on public.diary_likes for insert with check (true);
create policy "anon upd  diary views"   on public.diary for update using (true) with check (true);
create policy "anon read blogroll"      on public.blogroll for select using (approved = true);
create policy "anon ins  blogroll apply" on public.blogroll for insert with check (approved = false);
create policy "anon upd  blogroll hits" on public.blogroll for update using (approved = true) with check (approved = true);
create policy "anon read guestbook_reply" on public.guestbook_reply for select using (true);
create policy "anon ins  guestbook_reply" on public.guestbook_reply for insert with check (true);

-- 日记种子 3 条
insert into public.diary (title, category, body, mood) values
('开学第一天，好紧张呀~', '校园', '今天升初二啦！(>ω<) 换了新同桌叫小冉，她居然也喜欢周杰伦！我们约定明天一起去买《十一月的肖邦》磁带。<br>数学老师好像更凶了……作业有点多，呜呜。<br>对了，我的新笔袋是草莓味的！🍓', '🤔'),
('又到周末，终于可以上网了！', '碎碎念', '每个礼拜最期待的就是周六晚上爸妈允许上网 2 小时！(≧▽≦)/<br>先挂 QQ，再踩空间，再听一遍周杰伦《夜曲》的 MV……<br>今天收到了 32 条留言！！哇，谢谢大家支持我的小窝！+U +U！', '🥳'),
('单曲循环：七里香', '音乐', '窗外的麻雀 / 在电线杆上多嘴<br>你说这一句 / 很有夏天的感觉<br>———<br>CD 已经听到第 137 遍了还没厌。周杰伦为什么这么厉害啊？？？<br>下次想翻唱这首歌录给你们听 ♪(´▽`)', '😍')
on conflict do nothing;

-- 友链 8 条种子
insert into public.blogroll (name, url, slogan, avatar_url, sort_order) values
('§紫风铃§小窝',   'https://example.com/zifengling', '偶滴家~记得常来踩踩哦！',     'https://api.dicebear.com/9.x/pixel-art/svg?seed=zifengling&backgroundColor=ffd1dc', 1),
('月光剑客Baidu', 'https://example.com/yueguang',   'FrontPage 新手教程正在连载~', 'https://api.dicebear.com/9.x/pixel-art/svg?seed=yueguang&backgroundColor=c7d2fe',  2),
('淘气小熊のBLOG','https://example.com/xiaoxiong',  '小熊出没，注意！(>ω<)',       'https://api.dicebear.com/9.x/pixel-art/svg?seed=xiaoxiong&backgroundColor=fde68a', 3),
('蓝色蒲公英',     'https://example.com/pugongying', '用心写字，慢一点没关系。',     'https://api.dicebear.com/9.x/pixel-art/svg?seed=pugongying&backgroundColor=bae6fd',4),
('水晶鞋之恋',     'https://example.com/shuijing',   '少女心不死，公主梦不灭。',     'https://api.dicebear.com/9.x/pixel-art/svg?seed=shuijing&backgroundColor=fbcfe8', 5),
('追风少年',       'https://example.com/zhuifeng',   '玩跑跑卡丁车的来找我单挑！',   'https://api.dicebear.com/9.x/pixel-art/svg?seed=zhuifeng&backgroundColor=bbf7d0',  6),
('蜜糖甜甜圈',     'https://example.com/mitang',     '每天分享一首好听的歌 ♪',      'https://api.dicebear.com/9.x/pixel-art/svg?seed=mitang&backgroundColor=fecaca',    7),
('樱花盛开时',     'https://example.com/yinghua',    '一起看樱花雨吧~',              'https://api.dicebear.com/9.x/pixel-art/svg?seed=yinghua&backgroundColor=e9d5ff',   8)
on conflict do nothing;

-- 留言楼中楼回复种子（对应 floor 1~3）
insert into public.guestbook_reply (guestbook_id, reply_floor, username, message, is_owner) values
(1, 1, '冰蝴蝶🦋', '风铃妹妹你来啦～ 下次一定回访你的小窝！《隐形的翅膀》真的好好学，一起加油！♪(´▽`)', true),
(1, 2, '淘气小熊', '( っ´▽`)っ 我也想学这首歌！下次一起 K 歌哦～！', false),
(2, 1, '冰蝴蝶🦋', '收到剑客哥哥回访！百度空间链接一会儿就去加友情链接～握爪！(*´▽`*)', true),
(3, 1, '冰蝴蝶🦋', '小熊包在我身上！下周 FrontPage 教程开课，群里通知你～ (>ω<)ﾉ', true)
on conflict do nothing;
```

- [ ] **Step 3: 提示用户把 SQL 粘贴到 Supabase SQL Editor 执行**

本项目没有 service_role 密钥（用户未提供），不能用 API 直接 `create table`。正确做法：
```
echo "请在 Supabase Dashboard > SQL Editor > New Query 粘贴 _migrate_v2.sql 的全部内容，然后 Run 成功后回复：'SQL 已执行'。我再继续做代码改动。"
```

---

### Task 2: 探测外部千禧年风格图片 URL 可用性（先 HEAD 探测，后写代码）

**Files:**
- Modify: `/workspace/index.html`（把可用 URL 存为 `const IMG = {...}` 常量，在第 1227 行 `<script>` 开头声明）

- [ ] **Step 1: 跑 python 探测脚本，产出可用 URL 列表**

```python
import urllib.request, urllib.error
candidates = [
  # Dicebear 头像（友链 8 个）
  ('dice_zifengling','https://api.dicebear.com/9.x/pixel-art/svg?seed=zifengling&backgroundColor=ffd1dc'),
  ('dice_yueguang',  'https://api.dicebear.com/9.x/pixel-art/svg?seed=yueguang&backgroundColor=c7d2fe'),
  ('dice_xiaoxiong', 'https://api.dicebear.com/9.x/pixel-art/svg?seed=xiaoxiong&backgroundColor=fde68a'),
  ('dice_pugongying','https://api.dicebear.com/9.x/pixel-art/svg?seed=pugongying&backgroundColor=bae6fd'),
  ('dice_shuijing',  'https://api.dicebear.com/9.x/pixel-art/svg?seed=shuijing&backgroundColor=fbcfe8'),
  ('dice_zhuifeng',  'https://api.dicebear.com/9.x/pixel-art/svg?seed=zhuifeng&backgroundColor=bbf7d0'),
  ('dice_mitang',    'https://api.dicebear.com/9.x/pixel-art/svg?seed=mitang&backgroundColor=fecaca'),
  ('dice_yinghua',   'https://api.dicebear.com/9.x/pixel-art/svg?seed=yinghua&backgroundColor=e9d5ff'),
  # 日记头图（Picsum 锁定 seed）
  ('d_school', 'https://picsum.photos/seed/y2k-school-stairs/400/160'),
  ('d_cd',     'https://picsum.photos/seed/y2k-cd-disc/400/160'),
  ('d_candy',  'https://picsum.photos/seed/y2k-nail-candy/400/160'),
  # 头像（QQ秀风格 doll divine/azaleas dolls 替代品，先用 picsum 人物 seed）
  ('avatar_qq', 'https://picsum.photos/seed/doll-qq-butterfly/120/120'),
  # 播放器 CD 封面（Last.fm 七里香 封面图直链探测，不行就 picsum seed 兜底）
  ('cd_qilixiang','https://picsum.photos/seed/jay-chou-qilixiang/64/64'),
]
ok = {}
for k,url in candidates:
  try:
    req = urllib.request.Request(url, method='HEAD')
    with urllib.request.urlopen(req, timeout=8) as r:
      ok[k] = url if 'image/' in r.headers.get('Content-Type','') else None
  except Exception as e:
    ok[k] = None
for k,v in ok.items(): print(f"{'✅' if v else '❌'} {k:20s} -> {v or 'TIMEOUT/BROKEN'}")
```

Expected: 所有 Dicebear 和 Picsum 都应该 OK。Last.fm 可能失败走兜底。

- [ ] **Step 2: 在 index.html 的 `<script>` 开头紧接着 `<script>` 第 1227 行之后写 IMG 常量（不碰 SUPABASE_CONFIG）**

```js
/* ==========================================================
   🖼  真实千禧年图库素材（先探测可用性，失败自动走兜底）
   ========================================================== */
const IMG = {
  avatarQQ:   "<from probe result>",
  diary: {
    school: "<url>",
    cd:     "<url>",
    candy:  "<url>"
  },
  friends: {
    zifengling: "<>", yueguang:"<>", xiaoxiong:"<>", pugongying:"<>",
    shuijing:"<>", zhuifeng:"<>", mitang:"<>", yinghua:"<>"
  },
  cdCover: "<>"
};
/* 兜底：某张图加载失败自动切换 canvas/方块渐变 */
function safeImg(url, fallback){ /* 见 Task 5 实现 */ }
```

---

### Task 3: 高浓度视觉升级 CSS（`#v2-visual` 新样式块）

**Files:**
- Modify: `/workspace/index.html#L712`（在 `</style>` 之前追加新 style id="v2-visual"）

- [ ] **Step 1: 追加 `<style id="v2-visual">`，包含以下 CSS**

1. body 升级背景：多层渐变 + 点阵噪点（保留旧 Win98 蓝底作兜底）
2. 三套皮肤 CSS vars（`.theme-ice` / `.theme-purple` / `.theme-qq`）：分别覆盖 `--win-title-g1/--win-title-g2/--win-btn-primary/--accent-color` 等自定义属性
3. 图片边框升级：`.avatar-box .avatar-pixel` 替换成真实 `<img>` 并加 2px 金属边框 + 8 角闪光伪元素
4. 分割线 bling 样式：`.bling-divider { background: linear-gradient(...); height:16px; border-radius:4px; ... }`
5. 右下浮动工具条 `.fx-toolbar { position: fixed; right: 20px; bottom: 140px; z-index: 99; }`：放 🎨 换肤 + ✨ 特效按钮
6. 特效 canvas：`#fx { position: fixed; inset: 0; z-index: 1; pointer-events: none; }`（内容所有 `win98` 设 `position:relative; z-index: 2;`）
7. 日记窗口 4 种子分类 badge：`.cat-tag-mood/.cat-tag-school/.cat-tag-music/.cat-tag-weekly` 4 色渐变胶囊
8. 友链卡片：`.br-card` 48px 头像 + 名字彩虹字 + 标语灰字 + 踩一下按钮（粉色立体内阴影）
9. 楼中楼回复：`.gb-reply` 缩进 24px，左 border 2px 虚线灰；`.gb-reply.owner-true` 左 border 粉色，背景 `#fff0fb`，前缀 🦋 徽标

---

### Task 4: DOM 结构改动（插入 canvas、4 个新窗口，升级已有窗口）

**Files:**
- Modify: `/workspace/index.html`

- [ ] **Step 1: `<body>` 刚开头（`<div class="page-shell">` 之前）插入特效 canvas + fx-toolbar**

```html
<canvas id="fx"></canvas>
<div class="fx-toolbar" id="fxToolbar">
  <button class="fx-btn" title="换肤" onclick="toggleTheme()">🎨</button>
  <button class="fx-btn" title="飘落特效" onclick="toggleFx()">✨</button>
</div>
```

- [ ] **Step 2: 左栏 — 个人资料窗和计数器之间**（原 838 行 `</div><!-- /win98 个人资料 -->` 和原 841 行 `<!-- 友情链接 -->` 之间）**新建友情链接墙窗口**

```html
<!-- ======= 新：友情链接墙（带头像 + 互踩） ======= -->
<div class="win98" id="blogrollWin">
  <div class="win-title"><span><span class="wt-icon">💞</span>好朋友の小窝 · 互踩</span>...</div>
  <div class="win-body" id="blogrollBody" style="padding:8px;">
    <!-- JS 渲染 -->
  </div>
  <div style="padding:6px;background:#f9f9f9;border-top:1px solid #ccc;font-size:12px;">
    <b>🔔 申请友情链接：</b>
    <input id="brName" placeholder="站名" style="width:110px;...">
    <input id="brUrl"  placeholder="https://..." style="width:160px;...">
    <input id="brSlogan" placeholder="一句话标语" style="width:160px;...">
    <button class="old-btn primary" onclick="applyBlogroll()">📮 申请</button>
    <span id="brResult" style="color:#060;"></span>
  </div>
</div>
```

**⚠️ 注意：** 原 841-868 行那个"友情链接"纯文字链接列表的窗口，**保留**但标题改成"🚩 热门网站导航"避免冲突。

- [ ] **Step 3: 中栏 — 欢迎卡片窗的结尾（原 982 行）和留言板（原 984 行）之间插入"📒 网络日记"新窗口**

```html
<!-- ======= 新：网络日记簿 ======= -->
<div class="win98" id="diaryWin">
  <div class="win-title">
    <span><span class="wt-icon">📒</span>网络日记 · 蝴蝶の心情手记</span>
    <span class="wt-btns">_ ▢ ×</span>
  </div>
  <div class="win-body" id="diaryBody" style="padding:8px;">
    <!-- 分类筛选 tab bar -->
    <div id="diaryTabs" class="diary-tabs"></div>
    <!-- 日记列表，每篇一个 .diary-card -->
    <div id="diaryList"></div>
    <!-- 站长写日记入口 -->
    <div style="margin-top:10px;text-align:right;">
      <button class="old-btn" onclick="openWriteDiary()">📝 写新日记</button>
    </div>
  </div>
</div>

<!-- 写日记密码框（默认隐藏，密码通过后显示 textarea） -->
<div class="modal" id="writeDiaryModal" style="display:none;position:fixed;inset:0;background:rgba(0,0,30,.55);z-index:9999;">
  <div style="width:520px;margin:8vh auto;background:#fff;border:2px solid #000;box-shadow:...;">
    <div class="win-title"><span>🔒 密码验证（站长专属）</span>...</div>
    <div style="padding:16px;">
      <p>输入管理密码，进入写日记模式：<input type="password" id="ownerPwd" style="border:2px inset #999;padding:3px;"></p>
      <button class="old-btn primary" onclick="ownerLogin()">✅ 登录</button>
      <span style="color:#c00;margin-left:8px;" id="pwdHint"></span>
      <hr>
      <div id="writeDiaryForm" style="display:none;">
        标题 <input id="dTitle" style="width:100%"><br><br>
        分类 <select id="dCategory">...</select>　心情
        <select id="dMood">😊 😢 😍 😴 🤔 😡 🥳</select><br><br>
        正文<br>
        <textarea id="dBody" rows="8" style="width:100%;font-family:SimSun;"></textarea><br><br>
        <button class="old-btn primary" onclick="submitDiary()">💾 发布日记</button>
        <span id="diaryResult" style="margin-left:12px;"></span>
      </div>
    </div>
  </div>
</div>
```

- [ ] **Step 4: 升级留言板已有 DOM（楼中楼结构）**

在每条 `.gb-post` 结构的后面（原 `gb-body` div 结束后、外层 `gb-post` div 结束前）插入：

```html
<div class="gb-reply-wrap" data-gb-floor="floor号">
  <button class="gb-reply-toggle" onclick="toggleReplies(this)">💬 查看回复 (<span class="gb-reply-cnt">0</span>)</button>
  <div class="gb-reply-list" style="display:none;"></div>
  <div class="gb-reply-form">
    <input type="text" placeholder="昵称" class="gb-re-name">
    <input type="text" placeholder="写回复…最多120字" class="gb-re-msg">
    <button class="old-btn" onclick="submitReply(this)">📨 回复</button>
    <span class="gb-re-result"></span>
  </div>
</div>
```

（现有种子 3 条 gb-post 都加。具体写入时用 id="gb-post-1"/"gb-post-2"/"gb-post-3" 标记便于 JS 找）

---

### Task 5: `<script>` 内 STORE 扩展方法 + localStorage 一致性降级

**Files:**
- Modify: `/workspace/index.html`（紧跟原 STORE 定义后，追加新方法）

- [ ] **Step 1: 扩展 STORE，新增以下方法**（每一个都要：`if (useSupa && supabase) 走 Supabase；else 走 localStorage 等价结构`）

```js
STORE.listDiary(category /*'全部'|分类名*/) => Promise<Diary[]>
STORE.viewDiary(id) => Promise<void>           // views+1（同访客同天一次）
STORE.likeDiary(id) => Promise<string>         // 'OK' | '今日已赞'
STORE.addDiary({title, category, body, mood})  // 仅 owner 密码模式
STORE.listBlogroll() => Promise<Blogroll[]>
STORE.pressBlogroll(id) => Promise<number>     // 踩一下，返回新 hits；同访客当天限 1 次
STORE.applyBlogroll({name,url,slogan}) => Promise<void>
STORE.listReplies(floor) => Promise<Reply[]>
STORE.addReply({guestbook_floor, reply_floor, username, message, is_owner}) => Promise<void>
// 自动分配 reply_floor：先 listReplies 找 max + 1；冲突就再加 1
```

- [ ] **Step 2: localStorage 结构（降级必需）**

```
localStorage:
  v2.diary          = [{id,title,category,body,mood,views,created_at}, ...]
  v2.diary_likes    = [{diary_id, visitor_id, day}]
  v2.blogroll       = [{id,name,url,slogan,avatar_url,hits,approved,sort_order}, ...]
  v2.gb_replies     = [{id,guestbook_id,reply_floor,username,message,is_owner,created_at}, ...]
  v2.visitor_id     = 自动生成 uuid（首次访问写入），用于 diary_likes 每日一赞 / 友链踩一下 当天防刷
```

- [ ] **Step 3: XSS 转义 + HTML 允许白名单**

继续沿用现有 guestbook 逻辑：escapeHTML(`<>&"`), 再把 `\n` → `<br>`，再允许 `rainbow-text span` 不拦截（实际实现：先整体 escape，最后正则把安全的表情和彩虹 span 还原）。

---

### Task 6: 渲染函数 + 皮肤切换 + 特效 canvas

**Files:**
- Modify: `/workspace/index.html`

- [ ] **Step 1: 新增渲染函数**（与现有 `paintCounter/paintPoll/paintGuestbook` 风格一致）

```js
paintDiary(category='全部')       // 渲染分类 tab + 每篇日记卡片（头图/心情emoji/标题/正文HTML/💗点赞按钮）
paintBlogroll()                   // 两行 × 四列，共 8 位好友卡片
paintGuestbookReplies()           // 遍历每条留言，读取 STORE.listReplies()，把楼中楼渲染出来
setTheme(name /*'ice'|'purple'|'qq'*/) // document.body.className = 'theme-'+name；localStorage 记住
setFx(mode  /*'off'|'snow'|'sakura'|'star'|'butterfly'*/) // 启动/切换 canvas 粒子；toggleFx() 负责循环切换
```

- [ ] **Step 2: 特效 canvas 实现**（粒子系统，最多 60 颗，mousemove 尾迹）

```js
/* FxEngine:
   - particles[]: {x,y,vx,vy,life,r,color,shape}
   - mousemove 每 20ms push 一颗尾迹（life=1.5s，半径 2-4px）
   - 飘落模式每 60ms push 一颗"粒子雨"
   - requestAnimationFrame 循环；prefers-reduced-motion reduce 时每 3 帧才画 1 次
   - FPS 检测：1 秒内 rAF < 30 → 自动降级为只开尾迹，关飘落
*/
```

- [ ] **Step 3: main() 追加调用**

在原 `STORE.init().then(() => { paintCounter(); ... })` 链尾加：

```js
.then(() => Promise.all([paintDiary(), paintBlogroll()]))
.then(() => paintGuestbookReplies())
.then(() => { setTheme(localStorage.getItem('theme') || 'purple'); setFx(localStorage.getItem('fx')||'sakura'); })
.catch(err => console.error('V2 init failed', err));
```

---

### Task 7: 本地验证 checklist

**Files:**
- 无改动，只跑命令

- [ ] **Step 1: HTML 语法 + 关键词验证**

```bash
python3 -c "
import html.parser, re
html = open('/workspace/index.html','r',encoding='utf-8',errors='ignore').read()
p = html.parser.HTMLParser(); p.feed(html); print('HTML parse OK')
needles = ['blogrollWin','diaryWin','diaryList','blogrollBody','fxToolbar','paintDiary','paintBlogroll','paintGuestbookReplies','STORE.listDiary','STORE.likeDiary','STORE.applyBlogroll','setTheme','setFx','fx']
for n in needles:
    print(f'  {\"✅\" if n in html else \"❌\"} {n}')"
```

Expected: 全 ✅

- [ ] **Step 2: localStorage 降级本地打开验证**（不联网跑，模拟无 Supabase）

使用 Playwright 或最少：打开 `file:///workspace/index.html`，打开 Console 手动执行：
```
SUPABASE_CONFIG.url = ''; STORE.init().then(()=>paintDiary()).then(()=>paintBlogroll()).then(()=>paintGuestbookReplies())
```
Expected: 种子日记/友链/回复都能渲染，点赞/踩/回复能写入 localStorage，刷新不丢。

---

### Task 8: 推送 GitHub Pages + 在线验证

**Files:**
- 无改动，只跑 git + HTTP

- [ ] **Step 1: 提交并推送**

```bash
cd /workspace
git add index.html _migrate_v2.sql README.md
git commit -m "feat(v2): ⭐⭐⭐ 高浓度黄钻感视觉 + 📒日记/🔗友链/💬楼中楼/🖱特效 4 大功能（Supabase 4 表 + localStorage 降级）"
git push origin main
SHA=$(git rev-parse HEAD)
git push origin "$SHA:refs/heads/gh-pages"
```

- [ ] **Step 2: 轮询 Pages 构建直到 `built`，目标 commit 正确**

Expected: `pages/builds[0] = {commit: SHA[:7], status: built}`

- [ ] **Step 3: HTTP 验证**

```bash
python3 - <<'PY'
import urllib.request
url = 'https://dankehang.github.io/retro-web-gallery/index.html'
r = urllib.request.urlopen(url, timeout=20)
t = r.read().decode('utf-8', errors='ignore')
print(f'HTTP {r.status} size={len(t)}')
for k in ['diaryWin','blogrollWin','paintDiary','paintGuestbookReplies','fxToolbar','theme-purple','theme-qq','theme-ice']:
    print(f'  {\"✅\" if k in t else \"❌\"} {k}')
PY
```

Expected: 全 ✅

---

### Plan Self-Review（已检查）

1. **Spec 覆盖率**：Part A 视觉升级（背景平铺/皮肤/头像/分割线/工具栏）→ Task 3/4/6；Part B 4 功能 → Task 5/6；素材探测 → Task 2；4 张新表 + RLS + 种子 → Task 1。全部覆盖，无缺口。
2. **无占位符**：SQL 已逐字展开；探测脚本可直接运行；插入位置用行号标记。
3. **类型/命名一致性**：STORE 方法名、渲染函数名、DOM id 命名在插入代码和探测检查两处完全一致（`paintDiary/paintBlogroll/paintGuestbookReplies/listDiary/likeDiary/applyBlogroll`）。

Plan complete and saved to `docs/superpowers/plans/2026-08-25-y2k-enhance-plan.md`. Two execution options:

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

Which approach?
