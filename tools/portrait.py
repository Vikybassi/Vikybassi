# Ritratto ASCII: la persona (scontornata con rembg) in caratteri pieni e colorati, il paesaggio in caratteri leggeri e spenti.
import os
import numpy as np
from PIL import Image, ImageEnhance
COLS, ROWS = int(os.environ.get('COLS', 66)), int(os.environ.get('ROWS', 50))
W, H = 370, 470
X0, Y0, X1, Y1 = 540, 905, 1000, 1490
im = Image.open(os.path.expanduser('~/Desktop/portfolio-next/assets-source/hero-vetta.jpg')).convert('RGB').crop((X0, Y0, X1, Y1))
if not os.path.exists('mask-full.png'):  # la maschera è già qui: rembg serve solo per rifarla
    from rembg import remove, new_session
    remove(im, session=new_session('u2net_human_seg')).split()[-1].save('mask-full.png')
mask = np.asarray(Image.open('mask-full.png').resize((COLS, ROWS), Image.BOX)).astype(float) / 255
pic = ImageEnhance.Color(ImageEnhance.Contrast(im).enhance(1.2)).enhance(1.5)
a = np.asarray(pic.resize((COLS, ROWS), Image.LANCZOS)).astype(float)
lum = (0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]) / 255
lo, hi = np.percentile(lum, 2), np.percentile(lum, 98)
lum = np.clip((lum - lo) / (hi - lo), 0, 1)
rng = np.random.default_rng(7)
sat = (a.max(-1) - a.min(-1)) / np.maximum(1, a.max(-1))
sky = (a[..., 2] >= a[..., 0] - 12) & (lum > 0.22) & (mask <= 0.45)  # cielo e foschia: azzurrini
# il cielo è solo la parte alta, fino alla cresta: sotto la prima riga "non cielo" di ogni colonna non è più cielo
for c in range(COLS):
    stop = False
    for r in range(ROWS):
        if not stop and not sky[r, c] and mask[r, c] <= 0.45 and r > 3: stop = True
        if stop: sky[r, c] = False
horizon = max(1, max(r for r in range(ROWS) if sky[r].any()))
FG = "*csx%#&@"      # la persona: sempre "piena"
BG = " .`'-:;=+"     # lo sfondo: leggero
hexc = lambda c: '#%02x%02x%02x' % tuple(int(max(0, min(255, v))) for v in c)
esc = lambda s: s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
cw, rh = (W - 24) / COLS, (H - 24) / ROWS
lines = []
for r in range(ROWS):
    runs, cur, buf = [], None, ''
    for c in range(COLS):
        col = a[r, c]
        if mask[r, c] > 0.45:
            ch = FG[min(len(FG) - 1, int((0.35 + 0.65 * lum[r, c]) * (len(FG) - 1) + 0.5))]
            m = max(1, col.max()); col = col * (max(185, m) / m)
        elif sky[r, c]:
            # cielo: puntini radi con la sfumatura del tramonto (viola in alto, rosa-arancio verso l'orizzonte)
            k = r / max(1, horizon)
            ch = '.' if rng.random() < 0.10 + 0.25 * k else ("'" if rng.random() < 0.04 else ' ')
            if rng.random() < 0.012 and k < 0.6: ch = '+'
            col = np.array([120, 96, 168]) * (1 - k) + np.array([240, 150, 128]) * k
        else:
            v = lum[r, c]
            ch = BG[min(len(BG) - 1, int(v * (len(BG) - 1) + 0.5))]
            col = col * 0.5 + np.array([40, 30, 52]) * 0.5  # spento, verso il viola del fondo
        col = np.round(col / 20) * 20
        hc = hexc(col)
        if hc != cur and buf:
            runs.append((cur, buf)); buf = ''
        cur = hc; buf += ch
    runs.append((cur, buf))
    y = 12 + rh * (r + 0.8)
    ts = ''.join(f'<tspan fill="{c}">{esc(b)}</tspan>' for c, b in runs)
    lines.append(f'<text x="12" y="{y:.1f}" textLength="{W-24}" lengthAdjust="spacingAndGlyphs" style="animation-delay:{0.2 + r*0.04:.2f}s">{ts}</text>')
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="ASCII portrait of Vittoria on a mountain top, arms wide open">
<style>
text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace; font-size: {rh*1.05:.1f}px; font-weight: 700; white-space: pre; opacity: 0; animation: in .6s ease-out forwards; }}
@keyframes in {{ from {{ opacity: 0; transform: translateX(-8px); }} to {{ opacity: 1; transform: none; }} }}
@media (prefers-reduced-motion: reduce) {{ text {{ animation: none; opacity: 1; }} }}
</style>
<rect width="{W}" height="{H}" rx="14" fill="#17111f"/>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="13.5" fill="none" stroke="#3a2a48"/>
{chr(10).join(lines)}
</svg>'''
open(os.environ.get('OUT', '../portrait.svg'), 'w').write(svg)
print(len(svg) // 1024, 'KB')
