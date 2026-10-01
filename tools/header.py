# Intestazione del profilo: le creste vere del Monte Disgrazia (DEM Copernicus, dal portfolio) che si disegnano una dopo l'altra,
# il sole che tramonta dietro, le stelle che si accendono e il saluto.
import base64, json, os, random
import numpy as np
d = json.load(open(os.path.expanduser('~/Desktop/portfolio-next/src/data/ridges/disgrazia.json')))
cols, rows = d['cols'], d['rows']
g = np.frombuffer(base64.b64decode(d['data']), dtype=np.uint8).reshape(rows, cols).astype(float) / 255
# ammorbidisce un po' lungo le colonne
k = np.array([1, 2, 3, 2, 1], float); k /= k.sum()
g = np.array([np.convolve(np.pad(r, 2, mode='edge'), k, 'valid') for r in g])
W, H = 860, 260
N = 6                                  # quante creste
FLIP = os.environ.get('FLIP') == '1'
pick = [int(i * (rows - 1) / (N - 1)) for i in range(N)]
if FLIP: pick = pick[::-1]
paths = []
for i, r in enumerate(pick):           # i = 0 è la più lontana
    t = i / (N - 1)
    base = H * (0.76 + 0.30 * t)       # le vicine più in basso
    amp = H * (0.30 - 0.12 * t)
    xs = np.linspace(-10, W + 10, cols)
    ys = base - g[r] * amp
    pts = ' '.join(f'{x:.1f},{y:.1f}' for x, y in zip(xs, ys))
    paths.append((t, pts))
random.seed(3)
stars = ''.join(
    f'<circle cx="{random.uniform(8, W-8):.0f}" cy="{random.uniform(6, H*0.5):.0f}" r="{random.choice([0.8,1,1.2,1.5]):.1f}" class="s" style="animation-delay:{random.uniform(1.5, 5):.2f}s,{random.uniform(0, 3):.2f}s"/>'
    for _ in range(46))
ridges = []
for i, (t, pts) in enumerate(paths):
    stroke = f'rgb({int(240 - 90*t)},{int(150 - 70*t)},{int(170 - 40*t)})'
    op = 0.35 + 0.65 * t
    ridges.append(
        f'<polygon points="-10,{H+10} {pts} {W+10},{H+10}" fill="#17111f" class="f" style="animation-delay:{0.25 + i*0.22 + 0.8:.2f}s"/>'
        f'<polyline points="{pts}" fill="none" stroke="{stroke}" stroke-opacity="{op:.2f}" stroke-width="{1 + 0.6*t:.1f}" pathLength="1" class="l" style="animation-delay:{0.25 + i*0.22:.2f}s"/>')
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Hi, I'm Vittoria: sunset over the ridges of Monte Disgrazia">
<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#17111f"/><stop offset=".35" stop-color="#32203f"/><stop offset=".6" stop-color="#8e3f63"/><stop offset=".78" stop-color="#e98a7c"/><stop offset="1" stop-color="#f6b48f"/>
  </linearGradient>
  <radialGradient id="sun"><stop offset="0" stop-color="#ffe2b8"/><stop offset=".6" stop-color="#ffb08a"/><stop offset="1" stop-color="#f07a7a"/></radialGradient>
  <radialGradient id="glow"><stop offset="0" stop-color="#ffb08a" stop-opacity=".55"/><stop offset="1" stop-color="#ffb08a" stop-opacity="0"/></radialGradient>
  <clipPath id="card"><rect width="{W}" height="{H}" rx="14"/></clipPath>
  <clipPath id="type"><rect x="40" y="30" width="0" height="70"><animate attributeName="width" from="0" to="520" dur="1.6s" begin=".6s" fill="freeze" calcMode="discrete" values="0;52;104;156;208;260;312;364;416;468;520" keyTimes="0;.1;.2;.3;.4;.5;.6;.7;.8;.9;1"/></rect></clipPath>
</defs>
<style>
.l {{ stroke-dasharray: 1; stroke-dashoffset: 1; animation: draw 2.4s cubic-bezier(.3,.6,.3,1) forwards; }}
.f {{ opacity: 0; animation: fade 1.2s ease-out forwards; }}
.s {{ fill: #f6e9ef; opacity: 0; animation: fade 1.5s ease-out forwards, tw 3.2s ease-in-out infinite alternate; }}
.sun {{ animation: set 9s cubic-bezier(.4,0,.3,1) forwards; }}
.t1 {{ font: 800 46px "Segoe UI", "Helvetica Neue", Helvetica, Arial, sans-serif; letter-spacing: -1.5px; fill: #f6e9ef; }}
.t2 {{ font: 500 14px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; fill: #f0b8c8; opacity: 0; animation: fade 1s ease-out 2.4s forwards; }}
.t3 {{ font: 500 14px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; fill: #c9b3d6; opacity: 0; animation: fade 1s ease-out 2.9s forwards; }}
.cur {{ fill: #f07a9a; animation: blink 1s steps(1) infinite; }}
@keyframes draw {{ to {{ stroke-dashoffset: 0; }} }}
@keyframes fade {{ to {{ opacity: 1; }} }}
@keyframes tw {{ from {{ fill-opacity: 1; }} to {{ fill-opacity: .25; }} }}
@keyframes set {{ from {{ transform: translateY(-40px); }} to {{ transform: translateY(6px); }} }}
@keyframes blink {{ 50% {{ opacity: 0; }} }}
@media (prefers-reduced-motion: reduce) {{ .l, .f, .s, .sun, .t2, .t3 {{ animation: none; opacity: 1; stroke-dashoffset: 0; }} }}
</style>
<g clip-path="url(#card)">
  <rect width="{W}" height="{H}" fill="url(#sky)"/>
  {stars}
  <g class="sun"><circle cx="650" cy="150" r="120" fill="url(#glow)"/><circle cx="650" cy="150" r="30" fill="url(#sun)"/></g>
  {''.join(ridges)}
</g>
<g clip-path="url(#type)"><text x="40" y="80" class="t1">Hi, I&#8217;m Vittoria</text></g>
<text x="42" y="110" class="t2">web &amp; mobile development · data · digital communication</text>
<text x="42" y="132" class="t3">from the Valtellina mountains, based in Milan</text>
</svg>'''
open('../header.svg', 'w').write(svg)
print(len(svg) // 1024, 'KB')
