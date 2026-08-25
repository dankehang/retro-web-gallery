# 冰蝴蝶 Y2K-CN 主页 · 功能完善设计 spec（v2）

> 日期：2026-08-25
> 目标：把已经上线的"千禧年中国风"个人主页，升级为 **⭐⭐⭐ 高浓度黄钻感视觉 + 日记/友链/留言楼中楼/鼠标特效 4 大功能**，同时引入真实千禧年风格在线图库素材。

---

## 1. 本轮交付目标（与用户确认范围）

用户明确选择：
- ✅ **视觉浓度**：⭐⭐⭐ 高浓度（粉蓝紫撞色 + 动态GIF + 彩虹分割线 + QQ秀卡通人物 + 闪亮边框）
- ✅ **本轮范围**：视觉 + 功能全做
- ✅ **素材来源**：使用真实千禧年图库网站资源（不做 placeholder）

交付分成 **Part A 视觉升级** 和 **Part B 功能实现** 两部分，代码最终仍然只产出一个文件 `index.html`（保持单文件发布，用户最友好）。

---

## 2. Part A · 视觉升级方案

### 2.1 千禧年图库真实素材（使用在线 CDN，不本地存图）

所有图片都走"可公开直链"的 CDN，避免本地二进制文件带来的仓库膨胀、Pages 构建慢问题。

| 用途 | 尺寸 | 素材来源（可直链） | 说明 |
|---|---|---|---|
| 主页主背景（平铺） | 256×256 瓦片 | **WebArchive / GeoCities-Archive 项目** 的经典星尘背景 + 额外 `s3.amazonaws.com/ooomf.com/` 等早年平铺图 | 两种背景切换按钮：① 蝴蝶紫星点 ② 彩虹棉花云 |
| 左上角个人头像（QQ秀风格） | 120×120 正方形 | **Tumblr 千禧年 tag CDN 镜像**（PicRewrite/WordPress 博客外链）或 **Doll Divine / AzaleasDolls 像素娃娃**官方公开分享图 | 带金属边框 + 8 向闪光 |
| 日记头图（每篇一张） | 400×160 横幅 | **Unsplash 搜索 "y2k aesthetic" / "cyber y2k"** + **Picsum** seed 锁定 | 3 张不同：校园阶梯、CD 光盘、糖果色指甲 |
| 友链头像（8 位好友） | 48×48 | **Dicebear "pixel-art" / "thumbs"** + **RoboHash**（pixel seed） | 纯像素风，一致 16×16 放大 |
| 分割线（blingbling gif） | 600×16 | **Internet Archive / geocities.restructuration 集合**公开 gif URL | 3 款交替：彩虹星、粉蝶、小花链 |
| 播放器 CD 封面 | 64×64 | **Last.fm 专辑图**（七里香封面 CDN 直链）+ fallback 彩虹渐变 Canvas | 防止 Last.fm 过期，Canvas 兜底 |
| 鼠标尾迹 & 飘落粒子 | — | 纯 SVG/Canvas 生成，不引外部图 | 雪花/樱/星/蝶 4 种，Canvas 画 |

> **直链可用性检查要求**：所有图片 URL 必须先通过脚本 HEAD 检测（200 且 Content-Type 为 image/*），失败的自动切换 Picsum/Dicebear 兜底，避免线上出现破图红×。

### 2.2 CSS 视觉增强清单

1. **页面 body 背景**：从目前的纯色/渐变，升级为
   - 低透明度 `linear-gradient(#fef,#eff,#ffe)` 叠加平铺图（`opacity:.18` + `mix-blend-mode: screen`）
   - 再叠一层 **CSS 点阵噪点**（`background-image: radial-gradient(#ffb 1px, transparent 1px) 0 0/4px 4px`），做"旧显示器颗粒"
2. **Win98 窗口皮肤**：新增 3 套窗口皮肤切换（右下角小按钮）：
   - 默认 **冰蓝主题**（现有的）
   - **薰衣草紫 WinMe 主题**（紫色渐变标题栏 + 粉色按钮）
   - **QQ2005 橙色主题**（橙红渐变标题栏 + 立体水晶按钮图标）
3. **文字特效升级**：
   - `<h2 class="win-title">` 默认加 1px 黑描边 + `text-shadow: 1px 1px 0 #fff, 2px 2px 4px #f9f`
   - 火星文签名栏加 彩虹渐变文字（现有的 `rainbow-text` 增强为双层：渐变 + 外描边）
4. **右下角浮窗**：新增两个 32×32 飘浮图标按钮：
   - 🎨：切换皮肤（冰蓝 / 紫 / QQ橙）
   - ✨：切换飘落特效（关 / ❄️雪 / 🌸樱 / ⭐星 / 🦋蝶）

---

## 3. Part B · 功能（平衡包 = 4 大功能）+ 鼠标特效

### 3.1 数据库新增表结构（Supabase PostgreSQL）

```sql
-- ================================================================
--  新增表 1：diary（网络日记/日志）
-- ================================================================
create table if not exists public.diary (
  id         bigserial primary key,
  title      text not null,
  category   text not null default '碎碎念',  -- 碎碎念 / 周记 / 音乐 / 校园 / 随便写写
  body       text not null,                    -- 允许 <br>, 其他标签自动转义
  mood       text default '😊',                -- 😊😢😍😴🤔😡🥳 7 种心情
  views      bigint not null default 0,
  created_at bigint not null default (extract(epoch from now())*1000)::bigint
);

-- ================================================================
--  新增表 2：diary_likes（每人每天 1 赞，防刷）
-- ================================================================
create table if not exists public.diary_likes (
  diary_id   bigint references public.diary(id) on delete cascade,
  visitor_id text not null,        -- 浏览器 fingerprint / 随机 id，匿名不对应真实用户
  day        text not null,        -- YYYY-MM-DD
  created_at bigint not null default (extract(epoch from now())*1000)::bigint,
  primary key (diary_id, visitor_id, day)
);

-- ================================================================
--  新增表 3：blogroll（友情链接墙）
-- ================================================================
create table if not exists public.blogroll (
  id         bigserial primary key,
  name       text not null,
  url        text not null,
  slogan     text not null default '',           -- 一句话标语
  avatar_url text not null default '',           -- 48x48 头像直链
  hits       bigint not null default 0,          -- 累计互踩次数
  approved   boolean not null default true,      -- true=显示；false=用户申请，等待审批
  sort_order int not null default 100,
  created_at bigint not null default (extract(epoch from now())*1000)::bigint
);

-- ================================================================
--  新增表 4：guestbook_reply（留言楼中楼回复）
-- ================================================================
create table if not exists public.guestbook_reply (
  id             bigserial primary key,
  guestbook_id   bigint references public.guestbook(floor) on delete cascade,
  reply_floor    int not null,       -- 每条留言内部的第几个回复，从 1 开始
  username       text not null,
  message        text not null,
  is_owner       boolean not null default false,   -- true = 站长/博主回复（🦋 徽标）
  created_at     bigint not null default (extract(epoch from now())*1000)::bigint,
  unique (guestbook_id, reply_floor)
);
```

RLS 策略（跟着现有表的风格一致）：
- `diary`、`diary_likes`、`blogroll`、`guestbook_reply` 全部启用 RLS
- 公开**读**（所有匿名用户可 SELECT approved=true 的行）
- 公开**写**仅限：INSERT `diary_likes` / INSERT `blogroll(approved=false)` / UPDATE `blogroll.hits`（+1 only）/ INSERT `guestbook_reply`
- 禁止匿名 DELETE / UPDATE 其他字段

### 3.2 种子数据

```sql
-- 日记 3 篇种子
insert into public.diary (title, category, body, mood) values
('开学第一天，好紧张呀~', '校园',
 '今天升初二啦！(>ω<) 换了新同桌叫小冉，她居然也喜欢周杰伦！我们约定明天一起去买《十一月的肖邦》磁带。<br>数学老师好像更凶了……作业有点多，呜呜。<br>对了，我的新笔袋是草莓味的！🍓',
 '🤔'),
('又到周末，终于可以上网了！', '碎碎念',
 '每个礼拜最期待的就是周六晚上爸妈允许上网 2 小时！(≧▽≦)/<br>先挂 QQ，再踩空间，再听一遍周杰伦《夜曲》的 MV……<br>今天收到了 32 条留言！！哇，谢谢大家支持我的小窝！+U +U！',
 '🥳'),
('单曲循环：七里香', '音乐',
 '窗外的麻雀 / 在电线杆上多嘴<br>你说这一句 / 很有夏天的感觉<br>———<br>CD 已经听到第 137 遍了还没厌。周杰伦为什么这么厉害啊？？？<br>下次想翻唱这首歌录给你们听 ♪(´▽`)',
 '😍');

-- 友链 8 条种子
insert into public.blogroll (name, url, slogan, avatar_url, sort_order) values
('§紫风铃§小窝',   'https://example.com/zifengling', '偶滴家~记得常来踩踩哦！',     'https://api.dicebear.com/9.x/pixel-art/svg?seed=zifengling&backgroundColor=ffd1dc', 1),
('月光剑客Baidu', 'https://example.com/yueguang',   'FrontPage 新手教程正在连载~', 'https://api.dicebear.com/9.x/pixel-art/svg?seed=yueguang&backgroundColor=c7d2fe',  2),
('淘气小熊のBLOG','https://example.com/xiaoxiong',  '小熊出没，注意！(>ω<)',       'https://api.dicebear.com/9.x/pixel-art/svg?seed=xiaoxiong&backgroundColor=fde68a', 3),
('蓝色蒲公英',     'https://example.com/pugongying', '用心写字，慢一点没关系。',     'https://api.dicebear.com/9.x/pixel-art/svg?seed=pugongying&backgroundColor=bae6fd',4),
('水晶鞋之恋',     'https://example.com/shuijing',   '少女心不死，公主梦不灭。',     'https://api.dicebear.com/9.x/pixel-art/svg?seed=shuijing&backgroundColor=fbcfe8', 5),
('追风少年',       'https://example.com/zhuifeng',   '玩跑跑卡丁车的来找我单挑！',   'https://api.dicebear.com/9.x/pixel-art/svg?seed=zhuifeng&backgroundColor=bbf7d0',  6),
('蜜糖甜甜圈',     'https://example.com/mitang',     '每天分享一首好听的歌 ♪',      'https://api.dicebear.com/9.x/pixel-art/svg?seed=mitang&backgroundColor=fecaca',    7),
('樱花盛开时',     'https://example.com/yinghua',    '一起看樱花雨吧~',              'https://api.dicebear.com/9.x/pixel-art/svg?seed=yinghua&backgroundColor=e9d5ff',   8);

-- 留言楼中楼回复种子：对应紫风铃(#1) / 月光剑客(#2) / 淘气小熊(#3)
insert into public.guestbook_reply (guestbook_id, reply_floor, username, message, is_owner) values
(1, 1, '冰蝴蝶🦋', '风铃妹妹你来啦～ 下次一定回访你的小窝！《隐形的翅膀》真的好好学，一起加油！♪(´▽`)', true),
(1, 2, '淘气小熊', '( っ´▽`)っ 我也想学这首歌！下次一起 K 歌哦～！', false),
(2, 1, '冰蝴蝶🦋', '收到剑客哥哥回访！百度空间链接一会儿就去加友情链接～握爪！(*´▽`*)', true),
(3, 1, '冰蝴蝶🦋', '小熊包在我身上！下周 FrontPage 教程开课，群里通知你～ (>ω<)ﾉ', true);
```

### 3.3 各功能交互流程

#### ① 📒 网络日记（中栏新窗口，放在留言板上面）
- **外观**：每篇日记一张横幅头图 + 标题 + 心情 emoji + 分类 tag + 浏览数 + 点赞按钮
- **点赞按钮**：点一下，调用 `STORE.likeDiary(id)` → Supabase 写 `diary_likes`（主键冲突 = 今日已赞，前端弹 Toast"今天已经赞过啦 ♡"）
- **阅读数**：渲染时 +1（`update diary set views = views + 1`），同一天同一访客只计 1 次（localStorage `diary_viewed_{id}_{date}`）
- **分类筛选**：顶部一排 tab 按钮（全部/碎碎念/校园/音乐/周记），点一下前端过滤
- **"写新日记"入口**：右下角浮动 📝 按钮 → 弹出密码框（默认密码 `binghudie2006`，localStorage 可改），过了密码才能写 → 提交 `STORE.addDiary(...)`

#### ② 🔗 友情链接墙（左栏新窗口，放在计数器下面）
- **外观**：Win98 窗口。每行 2 位好友（窄屏 1 位）。头像 48 + 名字（彩虹字）+ 标语灰字 + "踩一下 💗"按钮 + "已踩 N 次"徽章
- **踩一下**：点按钮 → 调用 `STORE.pressBlogroll(id)`（UPDATE `hits = hits + 1`）→ 按钮变成"今天已踩 ✓" 并禁用（localStorage 当天防刷）
- **"申请加入友情链接"**：窗口底部一个小输入组（站点名 + URL + 一句话标语 + 昵称）→ 提交 `blogroll(approved=false)` → 成功后显示"申请已发送，等蝴蝶姐姐审核 ♡"
- 站长审批用 SQL 面板（`update blogroll set approved=true, sort_order=... where id=...`），前端 UI 不做复杂后台

#### ③ 💬 留言板楼中楼（现有窗口升级）
- 原 `#guestbook` 每一条 `留言卡片 → 下面新增一个"回复区"`
  - 默认**折叠**，点"💬 查看回复 (N)"展开
  - 超过 5 条回复显示"展开更多 (N-5)"懒加载
  - 每条回复：楼层 N-M（如 1-1）+ 头像 + 昵称 + is_owner=true 时**前缀🦋 + 粉色高亮**
- **发表回复**：每条留言底部一个小表单（昵称 + 回复内容）→ 提交 `STORE.addReply(guestbook_floor, ...)`
  - 昵称如果等于"冰蝴蝶"或站长密码模式下，自动 `is_owner=true`
  - 回复内容同样走 HTML escape（`<>&"`）+ 允许 `<br>` 换行 + 表情 emoji
- **种子留言展示效果**：紫风铃那一条下面会出现🦋冰蝴蝶和淘气小熊的两次"1-1 / 1-2"楼中楼回复

#### ④ 🖱 鼠标尾迹 + 飘落粒子（纯前端 Canvas，零依赖）
- 右下"✨特效开关"按钮 5 档：关 / ❄️雪 / 🌸樱 / ⭐星 / 🦋蝶
- **鼠标尾迹**：mousemove 事件留下一串小粒子（每 20ms 1 颗，最多缓存 60 颗，半径 2-4px，opacity 衰减 0→1.5s 消失），默认开
- **飘落**：全屏 `<canvas id="fx">` `position:fixed; inset:0; pointer-events:none; z-index:1`
  - 雪 = 白圆 + 水平摇摆
  - 樱 = 粉椭圆 + 旋转 5°/帧
  - 星 = 黄菱形 + 随机闪烁
  - 蝶 = 紫心形 + 正弦曲线
- **性能保护**：`prefers-reduced-motion: reduce` 自动关闭 + 每 2 秒检查 FPS，低于 30 自动降级到只有尾迹

---

## 4. 代码组织结构

保持单文件 `index.html`，内部块结构：

```html
<head>
  <!-- 原内容不变 -->
  <!-- 新增 Part A：高浓度视觉升级 CSS -->
  <style id="v2-visual">
    /* 高浓度平铺背景、3 套窗口皮肤、彩虹标题字、浮动按钮、分隔线样式 */
  </style>
</head>
<body>
  <!-- 新增：全屏特效 canvas（z-index:1，内容 z-index:10） -->
  <canvas id="fx" style="position:fixed;inset:0;z-index:1;pointer-events:none"></canvas>

  <!-- 原三栏布局不变，每栏按顺序插入 4 个新窗口 -->
  <!-- 左栏插入顺序：个人资料 → 【新】友情链接墙 → 计数器 → ... -->
  <!-- 中栏插入顺序：【新】网络日记簿 → 原留言板（升级楼中楼） -->
  <!-- 右栏保持原顺序：播放器/日历/天气/投票不变 -->

  <!-- 原 <script> 块内部按顺序插入新增逻辑 -->
  <script>
    /* --- 原 SUPABASE_CONFIG + STORE 基础 --- (保持不变) */
    /* --- 新增 Part B：STORE 扩展方法
           STORE.addDiary({...})
           STORE.listDiary(category)
           STORE.likeDiary(id)
           STORE.listBlogroll()
           STORE.pressBlogroll(id)
           STORE.applyBlogroll({...})
           STORE.listReplies(gb_floor)
           STORE.addReply({...})
    --- */
    /* --- 新增 Part A：视觉逻辑
           setTheme(ice|purple|qq)   // 切换皮肤 class="theme-xxx on body"
           setFx(off|snow|sakura|star|butterfly) // 切换 canvas 模式
    --- */
    /* --- 新增 Part B：渲染函数
           paintDiary()
           paintBlogroll()
           paintGuestbookReplies() // 配合现有 paintGuestbook() 调用
    --- */
    /* --- 原 main(): STORE.init → 所有 paint → 新增 paintDiary/paintBlogroll/setFx(sakura 默认) */
  </script>
</body>
```

---

## 5. 上线 & 验证清单

实现完成后，必须逐一验证以下项：

1. ✅ GitHub 推送后 Pages 构建成功（HTTP 200 + 文件大小合理）
2. ✅ 新增 4 张 Supabase 表通过脚本检测存在且有种子数据
3. ✅ `STORE.listDiary()`、`listBlogroll()`、`listReplies()` 能正确读到种子
4. ✅ 点赞日记：赞 1 次成功，赞 2 次弹"今日已赞"Toast（主键冲突捕获）
5. ✅ 踩友链：点 1 次，数字 +1；当天刷新后按钮显示"已踩 ✓"
6. ✅ 留言回复：紫风铃那条有 2 条楼中楼；发一条新回复，楼号自动 +1
7. ✅ 所有外部图片：至少 1 个 HEAD 检测通过，不存在红×（失败则回退 Dicebear/Picsum）
8. ✅ 特效切换：雪/樱/星/蝶 4 模式均不报错，FPS 不低于 30（弱机自动降级）
9. ✅ 皮肤切换：冰蓝/薰衣草紫/QQ橙 3 套均正常覆盖颜色变量
10. ✅ localStorage 降级：清空 Supabase URL 后 4 个新功能仍能工作（种子 + 写入本地，刷新不丢）

---

## 6. 不做 / 推迟项（scope 控制）

- ❌ 不做用户注册/登录系统（留言/日记/友链都用"昵称 + 匿名"，当年个人主页就是这个气质）
- ❌ 不做图片上传后端；相册功能推迟到用户确认做方案 C 时再做
- ❌ 不写独立 CSS/JS 文件（保持单文件 index.html，避免 Pages 资源路径踩坑）
- ❌ 不做复杂的"管理后台 UI"，日记发文和友链审批用密码框 + Supabase SQL Editor 足够
