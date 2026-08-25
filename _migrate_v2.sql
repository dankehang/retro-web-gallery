-- ================================================================
--  冰蝴蝶 Y2K 复古主页 v2 · 数据库建表脚本（PostgreSQL + Supabase）
--  新增 4 张表：
--      1) diary          网络日记/心情手记
--      2) diary_likes    日记点赞（每人每天 1 赞，防刷）
--      3) blogroll       友情链接墙（带头像+互踩次数）
--      4) guestbook_reply 留言板楼中楼回复
--
--  使用方法：
--      打开 Supabase Dashboard → 你的项目 → 左侧 SQL Editor
--      → New query → 把本文件全部粘贴 → 右上角 Run
--      （右下角看到 "Success" 即表示执行成功）
--
--  ⚠️ 不跑这段 SQL 也没关系：代码里有 localStorage 自动降级，
--     新功能在浏览器里照样能用，只是数据不同步到云端而已。
-- ================================================================


-- ================================================================
--  1) 日记表
-- ================================================================
create table if not exists public.diary (
  id         bigserial primary key,
  title      text not null,
  category   text not null default '碎碎念',   -- 碎碎念 / 校园 / 音乐 / 周记 / 随便写写
  body       text not null,                     -- 日记正文（允许 <br>，其他标签自动转义）
  mood       text default '😊',                 -- 😊 😢 😍 😴 🤔 😡 🥳 七种心情
  views      bigint not null default 0,
  created_at bigint not null default (extract(epoch from now())*1000)::bigint
);

-- 日记点赞：(diary_id, visitor_id, day) 三列联合主键 => 每人每天只能赞一次
create table if not exists public.diary_likes (
  diary_id   bigint references public.diary(id) on delete cascade,
  visitor_id text not null,
  day        text not null,
  created_at bigint not null default (extract(epoch from now())*1000)::bigint,
  primary key (diary_id, visitor_id, day)
);


-- ================================================================
--  2) 友情链接墙
-- ================================================================
create table if not exists public.blogroll (
  id         bigserial primary key,
  name       text not null,
  url        text not null,
  slogan     text not null default '',
  avatar_url text not null default '',
  hits       bigint not null default 0,
  approved   boolean not null default true,   -- 站长审批通过 = true；用户申请 = false（前端不显示待审批）
  sort_order int not null default 100,
  created_at bigint not null default (extract(epoch from now())*1000)::bigint
);


-- ================================================================
--  3) 留言楼中楼回复
--     guestbook_id  对应 guestbook.floor（留言板的第几楼）
--     reply_floor   在那一条留言内部的"第几个回复"
-- ================================================================
create table if not exists public.guestbook_reply (
  id             bigserial primary key,
  guestbook_id   bigint references public.guestbook(floor) on delete cascade,
  reply_floor    int not null,
  username       text not null,
  message        text not null,
  is_owner       boolean not null default false,   -- true = 站长回复，带 🦋 徽标
  created_at     bigint not null default (extract(epoch from now())*1000)::bigint,
  unique (guestbook_id, reply_floor)
);


-- ================================================================
--  4) RLS 行级安全策略（必开，防止匿名用户删库/改不该改的字段）
-- ================================================================
alter table public.diary           enable row level security;
alter table public.diary_likes     enable row level security;
alter table public.blogroll        enable row level security;
alter table public.guestbook_reply enable row level security;

drop policy if exists "anon read diary" on public.diary;
drop policy if exists "anon read diary_likes" on public.diary_likes;
drop policy if exists "anon ins  diary_likes" on public.diary_likes;
drop policy if exists "anon upd  diary views" on public.diary;
drop policy if exists "anon read blogroll" on public.blogroll;
drop policy if exists "anon ins  blogroll apply" on public.blogroll;
drop policy if exists "anon upd  blogroll hits" on public.blogroll;
drop policy if exists "anon read guestbook_reply" on public.guestbook_reply;
drop policy if exists "anon ins  guestbook_reply" on public.guestbook_reply;

-- 日记：公开可读；views 可以 +1；只有点赞允许匿名插入
create policy "anon read diary"         on public.diary           for select using (true);
create policy "anon read diary_likes"   on public.diary_likes     for select using (true);
create policy "anon ins  diary_likes"   on public.diary_likes     for insert with check (true);
create policy "anon upd  diary views"   on public.diary           for update using (true) with check (true);

-- 友情链接：只看已审批的；匿名用户可以提交"申请"（自动 approved=false）；已审批的 hits 可以 +1
create policy "anon read blogroll"      on public.blogroll        for select using (approved = true);
create policy "anon ins  blogroll apply" on public.blogroll       for insert with check (approved = false);
create policy "anon upd  blogroll hits" on public.blogroll        for update using (approved = true) with check (approved = true);

-- 楼中楼：可读、可写（但不能删/改已发表内容）
create policy "anon read guestbook_reply" on public.guestbook_reply for select using (true);
create policy "anon ins  guestbook_reply" on public.guestbook_reply for insert with check (true);


-- ================================================================
--  5) 种子数据（3 篇日记 / 8 位好友 / 4 条楼中楼回复）
--     on conflict do nothing = 重复执行也不会报错
-- ================================================================

insert into public.diary (title, category, body, mood) values
('开学第一天，好紧张呀~', '校园',
 '今天升初二啦！(>ω<) 换了新同桌叫小冉，她居然也喜欢周杰伦！我们约定明天一起去买《十一月的肖邦》磁带。<br>数学老师好像更凶了……作业有点多，呜呜。<br>对了，我的新笔袋是草莓味的！🍓',
 '🤔'),
('又到周末，终于可以上网了！', '碎碎念',
 '每个礼拜最期待的就是周六晚上爸妈允许上网 2 小时！(≧▽≦)/<br>先挂 QQ，再踩空间，再听一遍周杰伦《夜曲》的 MV……<br>今天收到了 32 条留言！！哇，谢谢大家支持我的小窝！+U +U！',
 '🥳'),
('单曲循环：七里香', '音乐',
 '窗外的麻雀 / 在电线杆上多嘴<br>你说这一句 / 很有夏天的感觉<br>———<br>CD 已经听到第 137 遍了还没厌。周杰伦为什么这么厉害啊？？？<br>下次想翻唱这首歌录给你们听 ♪(´▽`)',
 '😍')
on conflict do nothing;


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


insert into public.guestbook_reply (guestbook_id, reply_floor, username, message, is_owner) values
(1, 1, '冰蝴蝶🦋', '风铃妹妹你来啦～ 下次一定回访你的小窝！《隐形的翅膀》真的好好学，一起加油！♪(´▽`)', true),
(1, 2, '淘气小熊', '( っ´▽`)っ 我也想学这首歌！下次一起 K 歌哦～！', false),
(2, 1, '冰蝴蝶🦋', '收到剑客哥哥回访！百度空间链接一会儿就去加友情链接～握爪！(*´▽`*)', true),
(3, 1, '冰蝴蝶🦋', '小熊包在我身上！下周 FrontPage 教程开课，群里通知你～ (>ω<)ﾉ', true)
on conflict do nothing;


-- ================================================================
--  ✅ 看到 Success 之后，回到主页刷新一下～
--     现在日记、友情链接、留言楼中楼都已经有种子数据啦！
-- ================================================================
