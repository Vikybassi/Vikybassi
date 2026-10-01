# Scheda "whoami" in stile terminale: le righe compaiono una alla volta, dopo il ritratto.
from html import escape
W, H = 490, 470
PROMPT = 'vittoria@valtellina ~ $'
L = [
    ('cmd', 'whoami'),
    ('txt', 'Vittoria Bassi'),
    ('dim', 'web & mobile development, data, communication'),
    ('gap', ''),
    ('kv', 'studying', 'BSc Computer Science for Digital'),
    ('kv', '', 'Communication · Social & Mobile Computing'),
    ('kv', '', 'University of Milan · graduating Jan 2027'),
    ('kv', 'thesis', 'internship at Koinè, 2025 – Jul 2026'),
    ('kv', '', '→ built PiccoliPassi, for preschools'),
    ('kv', 'building', 'Back before dark · Fotogram'),
    ('kv', 'stack', 'JavaScript · TypeScript · React'),
    ('kv', '', 'Kotlin · Go · SQL'),
    ('kv', 'also', 'UX/UI · network analysis · SEO'),
    ('kv', 'speaks', 'Italian · English B2 · German, French A2'),
    ('kv', 'offline', 'painting · DJing · running · climbing'),
    ('kv', 'site', 'vikybassi.github.io'),
    ('gap', ''),
    ('end', ''),
]
x0, y, lh = 24, 76, 22
out = []
delay = 1.0
for item in L:
    kind = item[0]
    if kind == 'gap':
        y += lh * 0.55; continue
    st = f'style="animation-delay:{delay:.2f}s"'
    if kind == 'cmd':
        out.append(f'<text x="{x0}" y="{y:.0f}" class="ln" {st}><tspan class="p">{escape(PROMPT)}</tspan> <tspan class="c">{escape(item[1])}</tspan></text>')
    elif kind == 'txt':
        out.append(f'<text x="{x0}" y="{y:.0f}" class="ln big" {st}>{escape(item[1])}</text>')
    elif kind == 'dim':
        out.append(f'<text x="{x0}" y="{y:.0f}" class="ln d" {st}>{escape(item[1])}</text>')
    elif kind == 'kv':
        out.append(f'<text x="{x0}" y="{y:.0f}" class="ln" {st}><tspan class="k">{escape(item[1])}</tspan><tspan x="{x0+92}" class="v">{escape(item[2])}</tspan></text>')
    elif kind == 'end':
        out.append(f'<text x="{x0}" y="{y:.0f}" class="ln" {st}><tspan class="p">{escape(PROMPT)}</tspan> <tspan class="cur">▌</tspan></text>')
    y += lh + (12 if kind == 'cmd' else 4 if kind == 'txt' else 0)
    delay += 0.18
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="whoami: Vittoria Bassi, web and mobile development, data and communication">
<style>
text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace; font-size: 13px; white-space: pre; }}
.ln {{ opacity: 0; animation: in .45s ease-out forwards; }}
.p {{ fill: #f07a9a; }}
.c {{ fill: #f6e9ef; }}
.big {{ font: 800 22px "Segoe UI", "Helvetica Neue", Helvetica, Arial, sans-serif; fill: #f6e9ef; letter-spacing: -.4px; }}
.d {{ fill: #b9a6c6; }}
.k {{ fill: #f0a77e; }}
.v {{ fill: #e9dfee; }}
.t {{ font-size: 12px; fill: #8f7d9c; }}
.cur {{ fill: #f07a9a; animation: blink 1s steps(1) infinite; }}
@keyframes in {{ from {{ opacity: 0; transform: translateX(-6px); }} to {{ opacity: 1; transform: none; }} }}
@keyframes blink {{ 50% {{ opacity: 0; }} }}
@media (prefers-reduced-motion: reduce) {{ .ln {{ animation: none; opacity: 1; }} .cur {{ animation: none; }} }}
</style>
<rect width="{W}" height="{H}" rx="14" fill="#17111f"/>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="13.5" fill="none" stroke="#3a2a48"/>
<circle cx="22" cy="22" r="5.5" fill="#f07a7a"/><circle cx="40" cy="22" r="5.5" fill="#f0b07e"/><circle cx="58" cy="22" r="5.5" fill="#9fc79a"/>
<text x="{W/2}" y="26" text-anchor="middle" class="t">vittoria@valtellina: ~</text>
<line x1="0" y1="44" x2="{W}" y2="44" stroke="#3a2a48"/>
{chr(10).join(out)}
</svg>'''
open('../card.svg', 'w').write(svg)
print('ultima riga y', y)
