"""產生 README 圖解用的極簡 SVG 工具：表格、箭頭、標籤、程式碼標籤，統一配色與字型。"""
from html import escape

FONT = "'Noto Sans TC','PingFang TC','Microsoft JhengHei','Heiti TC',sans-serif"
MONO = "'SFMono-Regular','Consolas','Menlo','Noto Sans Mono CJK TC',monospace"

C = {
    'ink': '#1E293B', 'muted': '#64748B', 'line': '#CBD5E1', 'head': '#F1F5F9', 'bg': '#FFFFFF', 'frame': '#E2E8F0',
    'blue': '#2563EB', 'blue_l': '#DBEAFE', 'red': '#DC2626', 'red_l': '#FEE2E2', 'green': '#15803D', 'green_l': '#DCFCE7',
    'amber': '#B45309', 'amber_l': '#FEF3C7', 'brown': '#8B5E3C', 'brown_l': '#F5EBDD', 'navy': '#1E3A8A',
}
TONE = {  # 儲存格強調樣式：(底色, 字色, 粗體)
    'blue': (C['blue_l'], C['navy'], True), 'red': (C['red_l'], C['red'], True), 'green': (C['green_l'], C['green'], True),
    'amber': (C['amber_l'], C['amber'], True), 'muted': (None, C['muted'], False), 'strong': (C['navy'], '#FFFFFF', True),
    'redtext': (None, C['red'], True),
}


def tw(s, size, mono=False):
    """估算文字寬度（中文約 1 個字高，英數約 0.58）。"""
    w = 0
    for ch in str(s):
        if ord(ch) > 0x2E80:
            w += 1.0
        elif mono:
            w += 0.61
        else:
            w += 0.58 if ch not in 'il.,:;|!' else 0.3
    return w * size


class Canvas:
    def __init__(self):
        self.el = []
        self.max_x = self.max_y = 0

    def _ext(self, x, y):
        self.max_x, self.max_y = max(self.max_x, x), max(self.max_y, y)

    def text(self, x, y, s, size=15, color=C['ink'], weight='normal', anchor='start', mono=False, italic=False):
        fam = MONO if mono else FONT
        style = ' font-style="italic"' if italic else ''
        self.el.append(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{fam}" font-size="{size}" fill="{color}" '
                       f'font-weight="{weight}" text-anchor="{anchor}" xml:space="preserve"{style}>{escape(str(s))}</text>')
        w = tw(s, size, mono)
        self._ext(x + (w if anchor == 'start' else w / 2 if anchor == 'middle' else 0), y + size * 0.3)
        return w

    def rect(self, x, y, w, h, fill='none', stroke=C['line'], rx=6, sw=1.2, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        self.el.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" '
                       f'stroke="{stroke}" stroke-width="{sw}"{d}/>')
        self._ext(x + w, y + h)

    def line(self, x1, y1, x2, y2, color=C['line'], sw=1.2, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        self.el.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{sw}"{d}/>')
        self._ext(max(x1, x2), max(y1, y2))

    def arrow(self, x1, y1, x2, y2, color=C['blue'], sw=2.2, label=None, label_size=13, label_color=None, mono=False):
        mid = {'#2563EB': 'ab', '#DC2626': 'ar', '#15803D': 'ag', '#64748B': 'am', '#8B5E3C': 'an'}.get(color, 'ab')
        self.el.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" '
                       f'stroke-width="{sw}" marker-end="url(#{mid})"/>')
        self._ext(max(x1, x2), max(y1, y2))
        if label:
            if abs(y2 - y1) < 2:    # 水平箭頭：標籤放上方
                self.text((x1 + x2) / 2, y1 - 9, label, label_size, label_color or color, 'bold', 'middle', mono)
            else:                   # 垂直箭頭：標籤放右側
                self.text(x1 + 12, (y1 + y2) / 2 + 5, label, label_size, label_color or color, 'bold', 'start', mono)

    def path(self, d, color=C['blue'], sw=2, fill='none', marker=True):
        m = ' marker-end="url(#ab)"' if marker else ''
        self.el.append(f'<path d="{d}" stroke="{color}" stroke-width="{sw}" fill="{fill}"{m}/>')

    def circle(self, cx, cy, r, fill=C['blue'], stroke='none'):
        self.el.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}" stroke="{stroke}"/>')
        self._ext(cx + r, cy + r)

    def badge(self, x, y, n, color=C['red']):
        """編號圓點（用來標註圖中元素）。"""
        self.circle(x, y, 11, color)
        self.text(x, y + 4.5, n, 13, '#FFFFFF', 'bold', 'middle')

    def tag(self, x, y, s, tone='blue', size=13):
        """圓角小標籤，例如「處理前」、「處理後」。回傳寬度。"""
        bg, fg = {'blue': (C['blue_l'], C['navy']), 'grey': (C['head'], C['muted']), 'green': (C['green_l'], C['green']),
                  'red': (C['red_l'], C['red']), 'amber': (C['amber_l'], C['amber']), 'brown': (C['brown_l'], C['brown'])}[tone]
        w = tw(s, size) + 20
        self.rect(x, y, w, size + 12, fill=bg, stroke='none', rx=(size + 12) / 2)
        self.text(x + w / 2, y + size + 3, s, size, fg, 'bold', 'middle')
        return w

    def code(self, x, y, s, size=13.5, tone='ink'):
        """程式碼標籤（深色底、等寬字）。回傳寬度。"""
        w = tw(s, size, mono=True) + 22
        self.rect(x, y, w, size + 14, fill='#0F172A' if tone == 'ink' else C['brown'], stroke='none', rx=7)
        self.text(x + 11, y + size + 4, s, size, '#E2E8F0', 'normal', 'start', mono=True)
        return w

    def note(self, x, y, s, color=C['red'], size=13, icon='●'):
        self.text(x, y, icon, size - 3, color)
        return self.text(x + size, y, s, size, color, 'bold')

    def table(self, x, y, cols, rows, index=None, index_name='', widths=None, row_h=32, size=14, mono_cols=(),
              styles=None, header_tone='head', min_w=46, ellipsis_row=None, index_tone='muted'):
        """畫表格；styles = {(列, 欄): tone}，欄 -1 代表索引欄。回傳 (寬, 高, 每欄 x 中心, 每列 y 中心)。"""
        styles = styles or {}
        has_idx = index is not None
        all_cols = ([index_name] if has_idx else []) + list(cols)
        body = [([index[i]] if has_idx else []) + list(r) for i, r in enumerate(rows)]
        if widths is None:
            widths = []
            for j, h in enumerate(all_cols):
                cells = [h] + [r[j] for r in body]
                mono = (j - (1 if has_idx else 0)) in mono_cols
                widths.append(max(min_w, max(tw(c, size, mono) for c in cells) + 22))
        tw_total, th = sum(widths), row_h * (len(body) + 1)
        self.rect(x, y, tw_total, th, fill=C['bg'], stroke=C['line'], rx=8)
        self.rect(x, y, tw_total, row_h, fill=C['head'] if header_tone == 'head' else C['blue_l'], stroke='none', rx=8)
        self.line(x, y + row_h, x + tw_total, y + row_h, C['line'])
        xs, cx = [], x
        for w in widths:
            xs.append(cx + w / 2)
            cx += w
        if has_idx:
            self.line(x + widths[0], y, x + widths[0], y + th, C['line'])
        for j, h in enumerate(all_cols):
            self.text(xs[j], y + row_h / 2 + size * 0.36, h, size, C['ink'] if j or not has_idx else C['muted'], 'bold', 'middle')
        ys = []
        for i, r in enumerate(body):
            ry = y + row_h * (i + 1)
            ys.append(ry + row_h / 2)
            if i:
                self.line(x + 6, ry, x + tw_total - 6, ry, '#EEF2F7', 1)
            for j, v in enumerate(r):
                key = (i, j - (1 if has_idx else 0))
                tone = styles.get(key)
                is_idx = has_idx and j == 0
                if tone:
                    bg, fg, bold = TONE[tone]
                    if bg:
                        self.rect(xs[j] - widths[j] / 2 + 3, ry + 3, widths[j] - 6, row_h - 6, fill=bg, stroke='none', rx=5)
                else:
                    fg, bold = (C['muted'] if is_idx and index_tone == 'muted' else C['ink']), is_idx and index_tone != 'muted'
                mono = (j - (1 if has_idx else 0)) in mono_cols
                if ellipsis_row is not None and i == ellipsis_row:
                    fg = C['muted']
                self.text(xs[j], ry + row_h / 2 + size * 0.36, v, size, fg, 'bold' if bold else 'normal', 'middle', mono)
        return tw_total, th, xs, ys

    def svg(self, title, pad=24):
        w, h = self.max_x + pad, self.max_y + pad
        defs = ''.join(
            f'<marker id="{i}" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>'
            for i, c in [('ab', C['blue']), ('ar', C['red']), ('ag', C['green']), ('am', C['muted']), ('an', C['brown'])])
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h:.0f}" viewBox="0 0 {w:.0f} {h:.0f}" '
                f'role="img" aria-label="{escape(title)}">\n<title>{escape(title)}</title>\n<defs>{defs}</defs>\n'
                f'<rect x="1" y="1" width="{w - 2:.0f}" height="{h - 2:.0f}" rx="16" fill="{C["bg"]}" stroke="{C["frame"]}" stroke-width="1.5"/>\n'
                + '\n'.join(self.el) + '\n</svg>\n')
