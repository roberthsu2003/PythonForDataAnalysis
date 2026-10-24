"""把根目錄與各章 README.md 轉成網頁版（docs/，由 GitHub Pages 發布），讓網頁和 repo 內容保持同步。

用法（在專案根目錄執行）：
    python tools/build_site.py

會產生：
    docs/index.html            課程首頁（茶語時光故事、3 步驟開始、各階段章節卡片）
    docs/chapters/chNN.html    每一章的網頁版（內容來自該章 README.md）
    docs/assets/site.css、site.js

章節清單、章節順序、「本章任務」連結都讀自根目錄 README.md 的「學習路徑」表格，
所以調整課程時只要改 README.md，再執行一次本程式即可。docs/chart-selection 是手寫的互動教材，不受影響。

需要套件：markdown-it-py、mdit-py-plugins
"""
import html
import re
from pathlib import Path
from urllib.parse import quote, unquote

from markdown_it import MarkdownIt
from mdit_py_plugins.tasklists import tasklists_plugin

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / 'docs'
REPO = 'https://github.com/roberthsu2003/PythonForDataAnalysis'
BLOB = f'{REPO}/blob/master/'
TREE = f'{REPO}/tree/master/'
RAW = f'{REPO}/raw/master/'
COLAB = 'https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/'
HLJS = 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0'
FONTS = ('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800'
         '&family=Noto+Sans+TC:wght@400;500;700;900&display=swap')

ALERTS = {'NOTE': ('note', 'ℹ️ 說明'), 'TIP': ('tip', '💡 提示'), 'IMPORTANT': ('important', '📌 重點'),
          'WARNING': ('warning', '⚠️ 注意'), 'CAUTION': ('caution', '🛑 小心')}

md = MarkdownIt('commonmark', {'html': True, 'linkify': False}).enable(['table', 'strikethrough'])
md.use(tasklists_plugin)


# ---------------------------------------------------------------- 讀取課程結構
def parse_course():
    """從根 README 的「學習路徑」表格讀出：階段 → 章節（編號、資料夾、標題、學到什麼、任務連結）。"""
    text = (ROOT / 'README.md').read_text(encoding='utf-8')
    stages = []
    for block in re.split(r'\n(?=### )', text):
        head = re.match(r'### (\S+) (階段.)｜(.+)', block)
        if not head:
            continue
        chapters = []
        for row in re.findall(r'^\| (\d+) \|(.+)\|$', block, re.M):
            no, rest = int(row[0]), [c.strip() for c in row[1].split(' | ')]
            topic, learn, mission = (rest + ['', ''])[:3]
            link = re.match(r'\[(.+?)\]\((.+?)\)', topic)
            title, href = link.groups()
            folder = re.match(r'\./(.+)/README\.md', href)
            m = re.match(r'\[(.+?)\]\((.+?)\)', mission)
            chapters.append({
                'no': no, 'title': title, 'learn': learn,
                'folder': folder.group(1) if folder else None,
                'external': None if folder else href,
                'mission': m.group(1) if m else None, 'mission_url': m.group(2) if m else None,
                'page': f'ch{no:02d}.html',
            })
        stages.append({'icon': head.group(1), 'label': head.group(2), 'name': head.group(3).strip(),
                       'chapters': chapters})
    intro = text.split('## 🧭 學習路徑')[0]
    return stages, intro


# ---------------------------------------------------------------- Markdown → HTML
def rewrite_link(url, base, pages):
    """把 README 裡的相對路徑換成網頁上點得到的網址。"""
    if re.match(r'^(https?:|mailto:|#|data:)', url):
        return url
    path, _, frag = url.partition('#')
    target = (base / unquote(path)).resolve()
    try:
        rel = target.relative_to(ROOT).as_posix()
    except ValueError:
        return url
    if rel in pages:                                          # 其他章節的 README → 網頁版章節
        return pages[rel] + (f'#{frag}' if frag else '')
    if rel == 'README.md':
        return '../index.html'
    if target.is_dir():
        return TREE + quote(rel)
    if target.suffix.lower() in ('.png', '.jpg', '.jpeg', '.gif', '.svg', '.zip', '.csv', '.xlsx', '.json', '.txt'):
        return RAW + quote(rel)
    return BLOB + quote(rel) + (f'#{frag}' if frag else '')


def render_markdown(text, base, pages):
    body = md.render(text)
    body = re.sub(r'(href|src)="([^"]+)"',
                  lambda m: f'{m.group(1)}="{html.escape(rewrite_link(html.unescape(m.group(2)), base, pages))}"', body)

    def alert(m):
        kind, label = ALERTS.get(m.group(1), ('note', m.group(1)))
        return f'<blockquote class="alert alert-{kind}">\n<p class="alert-title">{label}</p>\n<p>'
    body = re.sub(r'<blockquote>\s*<p>\[!(\w+)\]\s*', alert, body)
    body = body.replace('<table>', '<div class="table-wrap"><table>').replace('</table>', '</table></div>')
    body = re.sub(r'<a href="(https?://[^"]+)"', r'<a href="\1" target="_blank" rel="noopener"', body)
    # 標題加上錨點，方便目錄跳轉
    used = {}

    def anchor(m):
        level, inner = m.group(1), m.group(2)
        slug = re.sub(r'[^\w一-鿿-]+', '-', re.sub('<[^>]+>', '', inner)).strip('-').lower() or 'section'
        used[slug] = used.get(slug, 0) + 1
        if used[slug] > 1:
            slug += f'-{used[slug]}'
        return f'<h{level} id="{slug}">{inner}</h{level}>'
    body = re.sub(r'<h([23])>(.*?)</h\1>', anchor, body)
    toc = [(int(lv), sid, re.sub('<[^>]+>', '', t)) for lv, sid, t in re.findall(r'<h([23]) id="([^"]+)">(.*?)</h\1>', body)]
    return body, toc


# ---------------------------------------------------------------- 版型
def page(title, desc, body, depth, active=None):
    prefix = '../' * depth
    return f'''<!DOCTYPE html>
<html lang="zh-Hant-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="{HLJS}/styles/github.min.css" media="(prefers-color-scheme: light)">
<link rel="stylesheet" href="{HLJS}/styles/github-dark.min.css" media="(prefers-color-scheme: dark)">
<link rel="stylesheet" href="{prefix}assets/site.css">
</head>
<body>
<header class="topbar">
  <div class="topbar-inner">
    <a class="brand" href="{prefix}index.html"><span class="brand-icon">🧋</span><span>Python 資料分析</span></a>
    <nav class="topnav">
      <a href="{prefix}index.html"{' class="on"' if active == 'home' else ''}>課程首頁</a>
      <a href="{prefix}chart-selection/index.html">圖表思維實驗室</a>
      <a class="nav-gh" href="{REPO}" target="_blank" rel="noopener">GitHub ↗</a>
    </nav>
  </div>
</header>
{body}
<footer class="site-footer">
  <p>網頁版由 <code>tools/build_site.py</code> 從 GitHub 上的 README 自動產生，內容與 repo 同步。</p>
  <p><a href="{REPO}" target="_blank" rel="noopener">roberthsu2003 / PythonForDataAnalysis</a>｜「茶語時光」為課程虛構品牌，範例資料為模擬資料。</p>
</footer>
<script src="{HLJS}/highlight.min.js"></script>
<script src="{prefix}assets/site.js"></script>
</body>
</html>
'''


def zip_url(ch):
    z = ROOT / ch['folder'] / f"{ch['folder']}_學生素材.zip"
    return RAW + quote(z.relative_to(ROOT).as_posix()) if z.exists() else None


def build_index(stages, intro):
    pages = {f"{c['folder']}/README.md": f"chapters/{c['page']}" for s in stages for c in s['chapters'] if c['folder']}
    intro = re.sub(r'^!\[.*\n+# .*\n+.*\n', '', intro)          # 圖片、標題與第一段（已放在網頁上方的大標題區）
    intro = re.sub(r'^> 🌐.*\n', '', intro, flags=re.M)                  # 「網頁版」連結在網頁上不需要
    intro_html, _ = render_markdown(intro, ROOT, pages)
    intro_html = intro_html.replace('點下方表格「🧋 本章任務」的連結', '點下方章節卡片的「▶ 在 Colab 開始任務」')
    total = sum(1 for s in stages for c in s['chapters'] if c['mission_url'])
    sections = []
    for s in stages:
        cards = []
        for c in s['chapters']:
            read = (f'<a class="btn btn-ghost" href="{c["external"]}" target="_blank" rel="noopener">前往 Python 基礎 ↗</a>'
                    if c['external'] else f'<a class="btn btn-ghost" href="chapters/{c["page"]}">📖 閱讀章節</a>')
            run = (f'<a class="btn btn-primary" href="{c["mission_url"]}" target="_blank" rel="noopener">▶ 在 Colab 開始任務</a>'
                   if c['mission_url'] else '')
            mission = (f'<p class="card-mission">{html.escape(c["mission"])}</p>' if c['mission'] else '')
            cards.append(f'''
      <article class="card">
        <div class="card-no">第 {c["no"]} 章</div>
        <h3 class="card-title">{html.escape(c["title"])}</h3>
        <p class="card-learn">{html.escape(c["learn"])}</p>
        {mission}
        <div class="card-actions">{read}{run}</div>
      </article>''')
        sections.append(f'''
  <section class="stage">
    <h2 class="stage-title"><span class="stage-icon">{s["icon"]}</span>{s["label"]}<span class="stage-sep">｜</span>{html.escape(s["name"])}</h2>
    <div class="cards">{"".join(cards)}
    </div>
  </section>''')
    body = f'''
<section class="hero">
  <div class="hero-inner">
    <p class="hero-badge">🧋 跟著「茶語時光」一起學資料分析</p>
    <h1>Python 資料分析</h1>
    <p class="hero-sub">用 NumPy、pandas、Matplotlib 把原始資料變成能做決策的報表與圖表。<br>{total} 個情境任務、每章都有自動批改的練習，打開 Colab 就能開始。</p>
    <div class="hero-actions">
      <a class="btn btn-primary btn-lg" href="#start">🚀 第一次上課從這裡開始</a>
      <a class="btn btn-ghost btn-lg" href="#path">🧭 看完整學習路徑</a>
    </div>
  </div>
</section>
<main class="home">
  <section class="intro md" id="start">{intro_html}
  </section>
  <h2 class="path-title" id="path">🧭 學習路徑</h2>
  {"".join(sections)}
  <section class="stage">
    <h2 class="stage-title"><span class="stage-icon">🧪</span>互動補充教材</h2>
    <div class="cards">
      <article class="card card-feature">
        <div class="card-no">搭配第 3、13 章</div>
        <h3 class="card-title">📊 圖表思維互動實驗室</h3>
        <p class="card-learn">拿到一份資料，該畫哪一種圖？用五大問題類型、選圖矩陣與欄位組合速查，練習「先想清楚問題，再選圖」。</p>
        <div class="card-actions"><a class="btn btn-primary" href="chart-selection/index.html">進入互動實驗室 →</a></div>
      </article>
    </div>
  </section>
</main>'''
    (DOCS / 'index.html').write_text(page('Python 資料分析｜茶語時光互動教材',
                                          'Python 資料分析課程網頁版：跟著虛構手搖飲品牌「茶語時光」學 NumPy、pandas 與 Matplotlib。',
                                          body, 0, 'home'), encoding='utf-8')


def build_chapters(stages):
    chapters = [c for s in stages for c in s['chapters'] if c['folder']]
    pages = {f"{c['folder']}/README.md": c['page'] for c in chapters}
    out = DOCS / 'chapters'
    out.mkdir(exist_ok=True)
    for old in out.glob('*.html'):
        old.unlink()
    side = []
    for s in stages:
        items = ''.join(f'<li><a href="{c["page"]}" data-page="{c["page"]}"><span class="side-no">{c["no"]}</span>{html.escape(c["title"])}</a></li>'
                        for c in s['chapters'] if c['folder'])
        side.append(f'<p class="side-stage">{s["icon"]} {s["label"]}｜{html.escape(s["name"])}</p><ul>{items}</ul>')
    side_html = ''.join(side)
    for i, c in enumerate(chapters):
        folder = ROOT / c['folder']
        text = (folder / 'README.md').read_text(encoding='utf-8')
        h1 = re.search(r'^# (.+)$', text, re.M)
        title = h1.group(1).strip() if h1 else c['title']
        text = text.replace(h1.group(0), '', 1) if h1 else text
        content, toc = render_markdown(text, folder, pages)
        actions = []
        if c['mission_url']:
            actions.append(f'<a class="btn btn-primary" href="{c["mission_url"]}" target="_blank" rel="noopener">▶ 在 Colab 開始任務：{html.escape(c["mission"])}</a>')
        if zip_url(c):
            actions.append(f'<a class="btn btn-ghost" href="{zip_url(c)}">⬇️ 下載本章素材</a>')
        actions.append(f'<a class="btn btn-ghost" href="{TREE + quote(c["folder"])}" target="_blank" rel="noopener">📂 在 GitHub 看原始檔</a>')
        toc_html = ''.join(f'<li class="toc-l{lv}"><a href="#{sid}">{html.escape(t)}</a></li>' for lv, sid, t in toc if lv == 2)
        prev_c = chapters[i - 1] if i > 0 else None
        next_c = chapters[i + 1] if i + 1 < len(chapters) else None
        pager = '<nav class="pager">'
        pager += (f'<a class="pager-prev" href="{prev_c["page"]}"><small>← 上一章</small>第 {prev_c["no"]} 章　{html.escape(prev_c["title"])}</a>'
                  if prev_c else '<span></span>')
        pager += (f'<a class="pager-next" href="{next_c["page"]}"><small>下一章 →</small>第 {next_c["no"]} 章　{html.escape(next_c["title"])}</a>'
                  if next_c else '<a class="pager-next" href="../index.html"><small>完成！</small>回到課程首頁</a>')
        pager += '</nav>'
        body = f'''
<div class="layout">
  <aside class="sidebar" id="sidebar">
    <button class="side-toggle" type="button" aria-expanded="false" aria-controls="side-list">📚 全部章節</button>
    <div class="side-list" id="side-list">{side_html}</div>
  </aside>
  <main class="chapter">
    <p class="crumb"><a href="../index.html">課程首頁</a> › 第 {c["no"]} 章</p>
    <h1 class="chapter-title">{html.escape(title)}</h1>
    <div class="chapter-actions">{"".join(actions)}</div>
    <details class="toc" open><summary>📑 本章目錄</summary><ul>{toc_html}</ul></details>
    <article class="md">{content}</article>
    {pager}
  </main>
</div>'''
        (out / c['page']).write_text(
            page(f'第 {c["no"]} 章 {c["title"]}｜Python 資料分析', c['learn'], body, 1).replace(
                f'data-page="{c["page"]}"', f'data-page="{c["page"]}" class="on" aria-current="page"'),
            encoding='utf-8')
    return chapters


CSS = r'''
:root {
  --bg: #f8fafc; --surface: #ffffff; --surface-2: #f1f5f9; --border: #e2e8f0;
  --text: #1e293b; --muted: #475569; --faint: #64748b;
  --brand: #8b5e3c; --brand-2: #c8a27c; --brand-soft: #f7efe6;
  --accent: #2563eb; --accent-soft: #eff6ff;
  --code-bg: #f6f8fa;
  --tip: #16a34a; --tip-soft: #f0fdf4; --imp: #7c3aed; --imp-soft: #f5f3ff;
  --warn: #d97706; --warn-soft: #fffbeb; --note: #2563eb; --note-soft: #eff6ff; --caution: #dc2626; --caution-soft: #fef2f2;
  --shadow: 0 1px 2px rgba(15,23,42,.06), 0 4px 12px rgba(15,23,42,.06);
  --radius: 14px;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #0f172a; --surface: #111c33; --surface-2: #1b2742; --border: #26334f;
    --text: #e2e8f0; --muted: #cbd5e1; --faint: #94a3b8;
    --brand: #e0b48a; --brand-2: #c8a27c; --brand-soft: #2a2118;
    --accent: #60a5fa; --accent-soft: #172554; --code-bg: #0d1526;
    --tip-soft: #0f2a1b; --imp-soft: #231a3d; --warn-soft: #2d2210; --note-soft: #13213f; --caution-soft: #3a1515;
    --shadow: 0 1px 2px rgba(0,0,0,.3), 0 4px 12px rgba(0,0,0,.25);
  }
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; scroll-padding-top: 76px; }
body { margin: 0; background: var(--bg); color: var(--text); font-family: 'Inter', 'Noto Sans TC', system-ui, sans-serif;
       font-size: 16.5px; line-height: 1.8; -webkit-text-size-adjust: 100%; }
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }
img { max-width: 100%; height: auto; }

.topbar { position: sticky; top: 0; z-index: 50; background: color-mix(in srgb, var(--surface) 92%, transparent);
          backdrop-filter: blur(10px); border-bottom: 1px solid var(--border); }
.topbar-inner { max-width: 1280px; margin: 0 auto; padding: 10px 16px; display: flex; align-items: center; justify-content: space-between; gap: 12px; }
.brand { display: flex; align-items: center; gap: 8px; font-weight: 800; color: var(--text); font-size: 1.05rem; white-space: nowrap; }
.brand:hover { text-decoration: none; }
.brand-icon { font-size: 1.4rem; }
.topnav { display: flex; gap: 2px; }
.topnav a { white-space: nowrap; }
.topnav a { color: var(--muted); padding: 6px 10px; border-radius: 8px; font-size: .92rem; font-weight: 600; }
.topnav a:hover, .topnav a.on { background: var(--surface-2); color: var(--text); text-decoration: none; }

.btn { display: inline-flex; align-items: center; gap: 6px; padding: 9px 16px; border-radius: 10px; font-weight: 700;
       font-size: .94rem; line-height: 1.3; border: 1px solid transparent; transition: transform .12s, box-shadow .12s; }
.btn:hover { text-decoration: none; transform: translateY(-1px); box-shadow: var(--shadow); }
.btn-primary { background: var(--brand); color: #fff; }
@media (prefers-color-scheme: dark) { .btn-primary { color: #1b1209; } }
.btn-ghost { background: var(--surface); color: var(--text); border-color: var(--border); }
.btn-lg { padding: 12px 22px; font-size: 1rem; }

/* 首頁 */
.hero { background: linear-gradient(135deg, var(--brand-soft), var(--accent-soft)); border-bottom: 1px solid var(--border); }
.hero-inner { max-width: 960px; margin: 0 auto; padding: 56px 16px 48px; text-align: center; }
.hero-badge { display: inline-block; margin: 0 0 14px; padding: 4px 14px; border-radius: 999px; background: var(--surface);
              border: 1px solid var(--border); font-weight: 700; font-size: .9rem; color: var(--brand); }
.hero h1 { margin: 0 0 12px; font-size: clamp(2rem, 5vw, 3rem); font-weight: 900; letter-spacing: -.02em; }
.hero-sub { margin: 0 auto 26px; max-width: 640px; color: var(--muted); font-size: 1.08rem; }
.hero-actions { display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; }
.home { max-width: 1120px; margin: 0 auto; padding: 32px 16px 64px; }
.intro { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 8px 28px 20px; box-shadow: var(--shadow); }
.path-title { font-size: 1.7rem; margin: 48px 0 8px; }
.stage { margin-top: 28px; }
.stage-title { display: flex; align-items: center; gap: 8px; font-size: 1.2rem; margin: 0 0 14px; }
.stage-icon { font-size: 1.4rem; }
.stage-sep { color: var(--faint); }
.cards { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 16px; }
.card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 18px 20px;
        display: flex; flex-direction: column; box-shadow: var(--shadow); }
.card-feature { border-color: var(--brand-2); }
.card-no { font-size: .8rem; font-weight: 800; color: var(--brand); letter-spacing: .04em; }
.card-title { margin: 4px 0 6px; font-size: 1.15rem; }
.card-learn { margin: 0 0 10px; color: var(--muted); font-size: .95rem; line-height: 1.65; }
.card-mission { margin: 0 0 14px; padding: 8px 12px; background: var(--brand-soft); border-radius: 10px; font-weight: 600; font-size: .93rem; line-height: 1.5; }
.card-actions { margin-top: auto; display: flex; gap: 8px; flex-wrap: wrap; }
.card-actions .btn { padding: 7px 12px; font-size: .88rem; }

/* 章節頁 */
.layout { max-width: 1280px; margin: 0 auto; display: grid; grid-template-columns: 270px minmax(0, 1fr); gap: 32px; padding: 0 16px; }
.sidebar { position: sticky; top: 60px; align-self: start; max-height: calc(100vh - 60px); overflow-y: auto; padding: 20px 0 40px; }
.side-toggle { display: none; }
.side-stage { margin: 16px 0 4px; font-size: .8rem; font-weight: 800; color: var(--faint); }
.sidebar ul { list-style: none; margin: 0; padding: 0; }
.sidebar li a { display: flex; gap: 8px; padding: 5px 10px; border-radius: 8px; color: var(--muted); font-size: .92rem; line-height: 1.45; }
.sidebar li a:hover { background: var(--surface-2); text-decoration: none; }
.sidebar li a.on { background: var(--brand-soft); color: var(--text); font-weight: 700; }
.side-no { flex: 0 0 22px; color: var(--faint); font-variant-numeric: tabular-nums; }
.chapter { padding: 24px 0 64px; min-width: 0; max-width: 880px; }
.crumb { margin: 0 0 6px; color: var(--faint); font-size: .9rem; }
.chapter-title { font-size: clamp(1.5rem, 3.6vw, 2.1rem); line-height: 1.35; margin: 0 0 16px; font-weight: 900; }
.chapter-actions { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 20px; }
.toc { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 10px 18px; margin-bottom: 24px; }
.toc summary { cursor: pointer; font-weight: 700; }
.toc ul { list-style: none; margin: 8px 0 4px; padding-left: .2em; columns: 2; column-gap: 28px; }
.toc li { break-inside: avoid; font-size: .93rem; line-height: 1.7; }
.pager { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 48px; }
.pager a { display: block; padding: 14px 18px; border: 1px solid var(--border); border-radius: var(--radius); background: var(--surface); color: var(--text); font-weight: 700; }
.pager a:hover { border-color: var(--brand-2); text-decoration: none; }
.pager small { display: block; color: var(--faint); font-weight: 600; }
.pager-next { text-align: right; }

/* Markdown 內容 */
.md h2 { font-size: 1.45rem; margin: 2.2em 0 .7em; padding-bottom: .3em; border-bottom: 1px solid var(--border); line-height: 1.4; }
.md h3 { font-size: 1.17rem; margin: 1.8em 0 .6em; line-height: 1.45; }
.md p, .md li { overflow-wrap: anywhere; }
.md hr { border: 0; border-top: 1px solid var(--border); margin: 2em 0; }
.md blockquote { margin: 1.2em 0; padding: 10px 18px; border-left: 4px solid var(--border); background: var(--surface); border-radius: 0 10px 10px 0; color: var(--muted); }
.md blockquote p { margin: .4em 0; }
.md .alert { color: var(--text); }
.md .alert-title { font-weight: 800; margin-bottom: .2em; }
.alert-tip { border-left-color: var(--tip) !important; background: var(--tip-soft) !important; }
.alert-important { border-left-color: var(--imp) !important; background: var(--imp-soft) !important; }
.alert-warning { border-left-color: var(--warn) !important; background: var(--warn-soft) !important; }
.alert-note { border-left-color: var(--note) !important; background: var(--note-soft) !important; }
.alert-caution { border-left-color: var(--caution) !important; background: var(--caution-soft) !important; }
.table-wrap { overflow-x: auto; margin: 1.2em 0; border: 1px solid var(--border); border-radius: 10px; background: var(--surface); }
.md table { border-collapse: collapse; width: 100%; font-size: .93rem; line-height: 1.6; }
.md th, .md td { padding: 9px 12px; border-bottom: 1px solid var(--border); text-align: left; vertical-align: top; }
.md th { background: var(--surface-2); font-weight: 700; white-space: nowrap; }
.md tr:last-child td { border-bottom: 0; }
.md code { font-family: 'SFMono-Regular', Menlo, Consolas, monospace; font-size: .88em; background: var(--surface-2); padding: .12em .38em; border-radius: 5px; }
.md pre { position: relative; background: var(--code-bg); border: 1px solid var(--border); border-radius: 12px; padding: 14px 16px; overflow-x: auto; line-height: 1.6; }
.md pre code { background: none; padding: 0; font-size: .86rem; }
.md pre code.hljs { background: none; padding: 0; }
.copy-btn { position: absolute; top: 8px; right: 8px; padding: 3px 10px; font-size: .78rem; font-weight: 700; border-radius: 7px;
            border: 1px solid var(--border); background: var(--surface); color: var(--muted); cursor: pointer; opacity: .85; font-family: inherit; }
.copy-btn:hover { opacity: 1; }
.md details { border: 1px solid var(--border); border-radius: 10px; padding: 8px 14px; background: var(--surface); margin: 1em 0; }
.md summary { cursor: pointer; font-weight: 700; }
.md ul.contains-task-list { list-style: none; padding-left: .4em; }
.md .task-list-item input { margin-right: .5em; transform: scale(1.15); accent-color: var(--brand); }
.md img[src*="colab-badge"] { vertical-align: middle; }

.site-footer { border-top: 1px solid var(--border); padding: 24px 16px 40px; text-align: center; color: var(--faint); font-size: .88rem; }
.site-footer p { margin: 4px 0; }

@media (max-width: 900px) {
  .layout { grid-template-columns: minmax(0, 1fr); gap: 0; }
  .sidebar { position: static; max-height: none; padding: 12px 0 0; }
  .side-toggle { display: block; width: 100%; padding: 10px 14px; border-radius: 10px; border: 1px solid var(--border);
                 background: var(--surface); color: var(--text); font: inherit; font-weight: 700; text-align: left; cursor: pointer; }
  .side-list { display: none; padding: 4px 4px 8px; }
  .sidebar.open .side-list { display: block; }
  .toc ul { columns: 1; }
  .intro { padding: 4px 16px 14px; }
  .pager { grid-template-columns: 1fr; }
  .pager-next { text-align: left; }
}
@media (max-width: 560px) {
  .topnav a { padding: 6px 7px; font-size: .84rem; }
  .topnav .nav-gh { display: none; }
  .brand { font-size: .98rem; }
  .chapter-actions .btn { width: 100%; justify-content: center; }
}
'''

JS = r'''
// 程式碼上色＋「複製」按鈕
document.querySelectorAll('.md pre > code').forEach((code) => {
  if (code.classList.contains('language-text')) return;   // 示意圖不需要上色與複製
  if (window.hljs) hljs.highlightElement(code);
  const btn = document.createElement('button');
  btn.className = 'copy-btn';
  btn.type = 'button';
  btn.textContent = '複製';
  btn.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(code.innerText);
      btn.textContent = '已複製 ✓';
    } catch (e) {
      btn.textContent = '請手動選取';
    }
    setTimeout(() => { btn.textContent = '複製'; }, 1600);
  });
  code.parentElement.appendChild(btn);
});

// 手機版：展開／收合章節清單
const side = document.getElementById('sidebar');
const toggle = side && side.querySelector('.side-toggle');
if (toggle) {
  toggle.addEventListener('click', () => {
    const open = side.classList.toggle('open');
    toggle.setAttribute('aria-expanded', String(open));
  });
}

// 自我檢查清單：勾選狀態記在這台瀏覽器
document.querySelectorAll('.task-list-item input[type=checkbox]').forEach((box, i) => {
  const key = 'pfda:' + location.pathname + ':' + i;
  box.disabled = false;
  try { box.checked = localStorage.getItem(key) === '1'; } catch (e) { /* 無法使用儲存空間時就不記錄 */ }
  box.addEventListener('change', () => {
    try { localStorage.setItem(key, box.checked ? '1' : '0'); } catch (e) { /* 同上 */ }
  });
});
'''


if __name__ == '__main__':
    stages, intro = parse_course()
    (DOCS / 'assets').mkdir(parents=True, exist_ok=True)
    (DOCS / 'assets' / 'site.css').write_text(CSS.lstrip(), encoding='utf-8')
    (DOCS / 'assets' / 'site.js').write_text(JS.lstrip(), encoding='utf-8')
    build_index(stages, intro)
    chapters = build_chapters(stages)
    (DOCS / '.nojekyll').write_text('', encoding='utf-8')
    print(f'✅ 網頁版已產生：首頁 + {len(chapters)} 個章節頁（docs/）')
