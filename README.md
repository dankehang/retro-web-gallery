# ❄ 冰蝴蝶的温馨小窝（千禧年 Y2K-CN 复古个人主页）

> 一个完整还原 2003-2006 年中国互联网个人主页风格的纯静态站点，
> 配备 **免费 PostgreSQL 后端**（Supabase 免费层）持久化存储：
> 访客计数器、今日访问、在线人数、留言板、周杰伦歌曲调查投票。
> 无需配置即可使用（浏览器 localStorage 本地存储），
> 填入两项配置即可升级为**全网同步云端数据库**。

🌐 **在线访问**：https://dankehang.github.io/retro-web-gallery/

---

## 📁 文件

| 文件 | 说明 |
|---|---|
| `index.html` | 千禧年中国风主页（主页面，含全部前端 + 后端 SDK） |

> 原 Blingee Pixel 闪亮风页面 `index.html` 已根据需求**删除**，
> 现在根路径直接打开就是千禧年中国风。

---

## ✨ 功能一览

- 🏠 经典 **Windows 98 风格蓝色立体窗口**（标题栏最小化/最大化/关闭）
- 💎 **QQ空间风** 三栏布局：左栏个人资料+计数器+友情链接，中栏日记+留言板，右栏播放器+日历+天气+投票
- 🖍 宋体 / 华文行楷 / 楷体 复古字体组合 + **火星文签名**
- 📺 **滚动跑马灯**（四色公告条）
- 💻 **DOS/BBS 绿字打字效果** 启动欢迎
- 🔴 **7位 LED 访客计数器 + 今日访问 + 在线人数**（真实持久化）
- 🎵 **千千静听风格音乐播放器**（10条频谱条 + 滚动歌名 + 播放/暂停/停止）
- 📅 **2006年8月迷你日历**（今天红色闪烁）
- 🌤 天气预报卡片
- ✍ **留言板**（沙发/板凳/地板 楼层标 + 表情 + 时间戳 + XSS 转义）
- 📊 **投票调查**（百分比进度条 + 每日防重复）
- 📱 响应式：窄屏自动两栏/单栏

---

## 🗄 后端数据库（免费 PostgreSQL！）

本页内置 **双存储引擎**，无需配置即可使用：

| 模式 | 需要配置？ | 刷新后保存？ | 跨设备同步？ | 写入位置 |
|---|---|---|---|---|
| 💾 **localStorage（默认）** | ❌ 不用配置 | ✅ 本机保留 | ❌ 只在当前浏览器 | 你自己的浏览器 |
| ☁️ **Supabase PostgreSQL** | ✅ 填 2 项 | ✅ 云端保留 | ✅ 全网同步 | 云端 PostgreSQL |

### 👉 启用云端 PostgreSQL（5 分钟，完全免费）

#### 第 1 步：创建 Supabase 项目
1. 打开 https://supabase.com/dashboard 注册/登录（GitHub 账号可直接登录）
2. **New Project** → 填项目名（例如 `retro-web-gallery`）→ 选就近区域（**Singapore/Tokyo** 延迟低）→ 设密码 → **Create new project**
3. 等初始化完成（约 1 分钟）

#### 第 2 步：进入项目 → 左边 **SQL Editor** → **New query** → 粘贴并执行以下 SQL：

```sql
-- ================================================================
--  冰蝴蝶复古主页 · 数据库建表脚本（PostgreSQL + Supabase）
-- ================================================================

-- 1) 站点计数器 / 今日访问 / 在线人数
create table if not exists public.site_counter (
  id          int primary key default 1,
  counter_val bigint not null default 52018,
  today_val   int not null default 1,
  today_date  text not null default to_char(current_date,'YYYY-MM-DD'),
  online      int not null default 37,
  updated_at  timestamptz not null default now(),
  constraint site_counter_id_1 check (id = 1)
);
insert into public.site_counter (id) values (1) on conflict do nothing;

-- 自增函数（可选，没建的话代码会自动降级为 update）
create or replace function public.increment_counter()
returns public.site_counter language plpgsql as $$
declare
  today_ text := to_char(current_date,'YYYY-MM-DD');
  out_ public.site_counter;
begin
  update public.site_counter
   set counter_val = counter_val + 1,
       today_val   = case when today_date = today_ then today_val + 1 else 1 end,
       today_date  = today_,
       online      = greatest(10, least(60, online + (random()*5-2)::int)),
       updated_at  = now()
   where id = 1
   returning * into out_;
  return out_;
end; $$;

-- 2) 周杰伦调查投票
create table if not exists public.site_poll (
  id    int primary key default 1,
  v0    bigint not null default 380, -- 七里香
  v1    bigint not null default 260, -- 青花瓷
  v2    bigint not null default 180, -- 双截棍
  v3    bigint not null default 120, -- 晴天
  v4    bigint not null default 60,  -- 其他
  constraint site_poll_id_1 check (id = 1)
);
insert into public.site_poll (id) values (1) on conflict do nothing;

-- 3) 留言板
create table if not exists public.guestbook (
  id         bigserial primary key,
  floor      int not null unique,
  username   text not null,
  message    text not null,
  face       text default '😊',
  ip         text,
  created_at bigint not null default (extract(epoch from now())*1000)::bigint
);
-- 初始 3 条种子留言
insert into public.guestbook (floor, username, message, face, ip) values
(1, '§紫风铃§', '哇~~新主页好漂亮哦！蝴蝶的设计越来越棒了！+U +U！<br>对了，你推荐的《隐形的翅膀》我已经开始学了~ ♪(´▽`)', '🐱', '123.45.67.89'),
(2, '月光剑客', '偶来踩踩~~~记得回访哦！我在百度空间也开新主页了~<br>周杰伦那首《七里香》真的百听不厌，握个爪！o(≧v≦)o', '🌙', '202.108.xx.xx'),
(3, '淘气小熊',  '今天来的有点晚~ <span class="rainbow-text">不过留言还是要留的！</span><br>蝴蝶姐姐！！我也要学做 FrontPage 教程，下次开课叫我！(>ω<)', '🐻', '61.50.xx.xx')
on conflict do nothing;

-- 4) RLS（行级安全）：只允许匿名查询 / 插入 / 更新计数器与投票（可选，推荐开启）
alter table public.site_counter enable row level security;
alter table public.site_poll    enable row level security;
alter table public.guestbook    enable row level security;

drop policy if exists "anon read site_counter" on public.site_counter;
drop policy if exists "anon upd  site_counter" on public.site_counter;
drop policy if exists "anon read site_poll"    on public.site_poll;
drop policy if exists "anon upd  site_poll"    on public.site_poll;
drop policy if exists "anon read guestbook"    on public.guestbook;
drop policy if exists "anon ins  guestbook"    on public.guestbook;

create policy "anon read site_counter" on public.site_counter for select using (true);
create policy "anon upd  site_counter" on public.site_counter for update using (id = 1) with check (id = 1);
create policy "anon read site_poll"    on public.site_poll    for select using (true);
create policy "anon upd  site_poll"    on public.site_poll    for update using (id = 1) with check (id = 1);
create policy "anon read guestbook"    on public.guestbook    for select using (true);
create policy "anon ins  guestbook"    on public.guestbook    for insert with check (true);
```

> 点 **Run** 执行 SQL，右下角提示"Success"即完成。

#### 第 3 步：获取两项配置，填入页面

1. 项目左侧 **Settings** → **API**
2. 复制：
   - **Project URL**（例如 `https://abcdefghijklmnop.supabase.co`）
   - **Project API keys → anon public**（以 `eyJhbGciOiJIUzI1...` 开头的一长串）
3. 打开 [index.html](file:///workspace/index.html)，在 `<head>` 后面脚本里找到：

```js
const SUPABASE_CONFIG = {
  url: "",          // ← 粘贴 Project URL
  anonKey: ""       // ← 粘贴 anon public key
};
```

把两个字符串填进去 → **保存** → **继续下面推送 GitHub**。

---

## 🚀 推送到 GitHub Pages（本仓库已启用）

```bash
cd retro-web-gallery
git add index.html README.md
git commit -m "feat: 千禧年主页作为首页 + Supabase 免费后端双引擎"
git push origin main
git push origin gh-pages  # 或 git checkout gh-pages && merge main 后推送
```

本仓库已经自动推送完成 ✅，构建成功后直接访问：

👉 **https://dankehang.github.io/retro-web-gallery/**

页面右上角会显示：
- `✅ 云端模式 Supabase (PostgreSQL)`（填了 URL/Key）
- 或 `💾 本地模式 (localStorage)`（未填但照样可用）

---

## 📜 License

本项目为复古网页演示，代码仅供学习参考。
Blingee 闪亮风页面已按用户要求删除。
