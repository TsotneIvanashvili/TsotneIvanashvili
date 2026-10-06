#!/usr/bin/env python3
"""Generate the animated SVGs used by README.md.

Everything is self-hosted: no external fonts, scripts or images, so GitHub
renders them through <img> without rate limits or broken links.

Edit the CONFIG block, then run:  python3 scripts/build_assets.py
"""
from html import escape
from pathlib import Path

# ----------------------------------------------------------------------------
# CONFIG: change these, then re-run the script.
# ----------------------------------------------------------------------------
NAME = "Tsotne Ivanashvili"
TAGLINE = "builder  ·  learner  ·  shipping every day"

TYPING_LINES = [
    "Hi, I'm Tsotne.",
    "I build things for the web.",
    "I learn in public.",
    "Shipping > perfect.",
]

TERMINAL = [
    ("whoami", "tsotne_ivanashvili"),
    ("cat mission.txt", "build things that matter. ship. learn. repeat."),
    ("git log --oneline | wc -l", "always +1"),
    ("./ascend --level=next", "[##########----] loading the next version of me..."),
]
# ----------------------------------------------------------------------------

OUT = Path(__file__).resolve().parent.parent / "assets"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'DejaVu Sans Mono', 'Courier New', monospace"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
BG = "#0d1117"
C1, C2, C3 = "#22d3ee", "#a78bfa", "#f472b6"


def write(name: str, svg: str) -> None:
    (OUT / name).write_text(svg.strip() + "\n", encoding="utf-8")
    print(f"wrote assets/{name}")


def header() -> str:
    w, h = 1200, 320
    stars = []
    # Deterministic pseudo-random star field so rebuilds are diff-stable.
    seed = 7
    for i in range(46):
        seed = (seed * 1103515245 + 12345) % 2**31
        x = seed % w
        seed = (seed * 1103515245 + 12345) % 2**31
        y = seed % h
        r = 0.6 + (i % 3) * 0.5
        delay = (i * 0.37) % 4
        stars.append(
            f'<circle class="star" cx="{x}" cy="{y}" r="{r}" style="animation-delay:-{delay:.2f}s"/>'
        )
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{escape(NAME)}: {escape(TAGLINE)}">
  <title>{escape(NAME)}</title>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0b1020"/>
      <stop offset="1" stop-color="#140b24"/>
    </linearGradient>
    <linearGradient id="txt" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{w}" y2="0" spreadMethod="reflect">
      <stop offset="0" stop-color="{C1}"/>
      <stop offset="0.5" stop-color="{C2}"/>
      <stop offset="1" stop-color="{C3}"/>
      <animateTransform attributeName="gradientTransform" type="translate" values="0 0;{2 * w} 0" dur="10s" repeatCount="indefinite"/>
    </linearGradient>
    <linearGradient id="txt2" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{w}" y2="0" spreadMethod="reflect">
      <stop offset="0" stop-color="{C3}"/>
      <stop offset="0.5" stop-color="{C1}"/>
      <stop offset="1" stop-color="{C2}"/>
      <animateTransform attributeName="gradientTransform" type="translate" values="0 0;{2 * w} 0" dur="10s" repeatCount="indefinite"/>
    </linearGradient>
    <filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="40"/></filter>
    <filter id="glow" x="-20%" y="-50%" width="140%" height="200%">
      <feGaussianBlur stdDeviation="6" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M40 0H0V40" fill="none" stroke="#ffffff" stroke-opacity="0.04"/>
    </pattern>
    <clipPath id="card"><rect width="{w}" height="{h}" rx="18"/></clipPath>
  </defs>
  <style>
    .blob {{ animation: drift 14s ease-in-out infinite alternate; transform-box: fill-box; transform-origin: center; }}
    .b2 {{ animation-duration: 18s; animation-direction: alternate-reverse; }}
    .b3 {{ animation-duration: 11s; }}
    @keyframes drift {{
      0%   {{ transform: translate(0, 0) scale(1); }}
      50%  {{ transform: translate(120px, 40px) scale(1.25); }}
      100% {{ transform: translate(-80px, -30px) scale(0.9); }}
    }}
    .star {{ fill: #fff; animation: twinkle 4s ease-in-out infinite; }}
    @keyframes twinkle {{ 0%, 100% {{ opacity: .15; }} 50% {{ opacity: .9; }} }}
    .name {{ font: 800 76px {SANS}; letter-spacing: 1px; opacity: 0; animation: rise 1.2s cubic-bezier(.2,.8,.2,1) .2s forwards; }}
    .tag {{ font: 500 24px {MONO}; letter-spacing: 3px; fill: #c9d1d9; opacity: 0; animation: rise 1.2s cubic-bezier(.2,.8,.2,1) .8s forwards; }}
    @keyframes rise {{ from {{ opacity: 0; transform: translateY(24px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    .scan {{ animation: scan 6s linear infinite; }}
    @keyframes scan {{ from {{ transform: translateY(-40px); }} to {{ transform: translateY({h + 40}px); }} }}
    .line {{ stroke-dasharray: 520; stroke-dashoffset: 520; animation: draw 1.4s ease-out 1.2s forwards; }}
    @keyframes draw {{ to {{ stroke-dashoffset: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{
      * {{ animation: none !important; }}
      .name, .tag {{ opacity: 1; }}
      .line {{ stroke-dashoffset: 0; }}
      .scan {{ display: none; }}
    }}
  </style>
  <g clip-path="url(#card)">
    <rect width="{w}" height="{h}" fill="url(#bg)"/>
    <rect width="{w}" height="{h}" fill="url(#grid)"/>
    <g filter="url(#blur)" opacity="0.55">
      <circle class="blob" cx="220" cy="90" r="130" fill="{C1}"/>
      <circle class="blob b2" cx="980" cy="230" r="150" fill="{C3}"/>
      <circle class="blob b3" cx="620" cy="300" r="120" fill="{C2}"/>
    </g>
    {''.join(stars)}
    <rect class="scan" x="0" y="0" width="{w}" height="40" fill="#ffffff" opacity="0.025"/>
    <g filter="url(#glow)">
      <text class="name" x="50%" y="165" text-anchor="middle" fill="url(#txt)">{escape(NAME)}</text>
    </g>
    <path class="line" d="M{w/2 - 260} 195 H{w/2 + 260}" stroke="url(#txt2)" stroke-width="3" stroke-linecap="round"/>
    <text class="tag" x="50%" y="240" text-anchor="middle">{escape(TAGLINE)}</text>
  </g>
  <rect x="1" y="1" width="{w-2}" height="{h-2}" rx="17" fill="none" stroke="url(#txt)" stroke-opacity="0.5" stroke-width="2"/>
</svg>"""


def typing() -> str:
    w, h = 900, 70
    fs = 30
    cw = fs * 0.6  # monospace advance; textLength pins it so every font matches
    slot = 4.0     # seconds per line
    total = slot * len(TYPING_LINES)
    css, groups = [], []
    for i, line in enumerate(TYPING_LINES):
        n = len(line)
        tw = n * cw
        x0 = (w - tw) / 2
        p = lambda s: f"{(i * slot + s) / total * 100:.3f}%"  # noqa: E731
        start, typed, hold, gone = p(0), p(1.6), p(3.2), p(3.7)
        # Visibility window [i*slot, (i+1)*slot) with hard edges: step-end holds
        # each keyframe's value until the next one, so no cross-fades.
        on, off = p(0), p(slot)
        show = f"0% {{ opacity: 1; }} {off} {{ opacity: 0; }}" if i == 0 else \
            f"0% {{ opacity: 0; }} {on} {{ opacity: 1; }} {off} {{ opacity: 0; }}"
        css.append(f"""
    @keyframes show{i} {{ {show} }}
    @keyframes type{i} {{
      0%, {start} {{ transform: translateX(0); animation-timing-function: steps({n}, end); }}
      {typed}, {hold} {{ transform: translateX({tw:.1f}px); animation-timing-function: steps({n}, end); }}
      {gone}, 100% {{ transform: translateX(0); }}
    }}
    .l{i} {{ animation: show{i} {total}s step-end infinite; }}
    .m{i} {{ animation: type{i} {total}s linear infinite; }}""")
        groups.append(f"""
  <g class="l{i}" opacity="0">
    <text x="{x0:.1f}" y="{h/2 + fs*0.35:.1f}" textLength="{tw:.1f}" lengthAdjust="spacingAndGlyphs" class="t">{escape(line)}</text>
    <g class="m{i}">
      <rect x="{x0:.1f}" y="0" width="{w}" height="{h}" fill="{BG}"/>
      <rect class="cursor" x="{x0 + 2:.1f}" y="{h/2 - fs*0.55:.1f}" width="3" height="{fs*1.1:.1f}" fill="{C1}"/>
    </g>
  </g>""")
    alt = " / ".join(TYPING_LINES)
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{escape(alt)}">
  <title>{escape(alt)}</title>
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{C1}"/><stop offset="0.5" stop-color="{C2}"/><stop offset="1" stop-color="{C3}"/>
    </linearGradient>
    <clipPath id="c"><rect width="{w}" height="{h}" rx="12"/></clipPath>
  </defs>
  <style>
    .t {{ font: 600 {fs}px {MONO}; fill: url(#g); }}
    .cursor {{ animation: blink 1s step-end infinite; }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}{''.join(css)}
    @media (prefers-reduced-motion: reduce) {{
      * {{ animation: none !important; }}
      .l0 {{ opacity: 1; }}
      .m0 {{ display: none; }}
    }}
  </style>
  <g clip-path="url(#c)">
    <rect width="{w}" height="{h}" fill="{BG}"/>{''.join(groups)}
  </g>
  <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="12" fill="none" stroke="#30363d"/>
</svg>"""


def terminal() -> str:
    w = 900
    lh = 30
    top = 70
    h = top + lh * (len(TERMINAL) * 2) + 30
    step = 1.6  # seconds between commands
    rows, css = [], []
    y = top
    for i, (cmd, out) in enumerate(TERMINAL):
        n = len(cmd) + 2  # "$ " prefix
        tw = n * 9.6      # 16px mono advance (0.6em)
        d = i * step + 0.4
        rows.append(f"""
    <g class="row" style="animation-delay:{d:.2f}s">
      <text x="28" y="{y}" class="mono"><tspan fill="{C1}">$</tspan> <tspan fill="#e6edf3">{escape(cmd)}</tspan></text>
      <rect class="cover" x="28" y="{y - 20}" width="{tw + 14:.1f}" height="28" fill="#161b22" style="animation: wipe{i} .6s steps({n}, end) {d:.2f}s forwards"/>
    </g>
    <text x="28" y="{y + lh}" class="mono out" style="animation-delay:{d + 0.7:.2f}s">{escape(out)}</text>""")
        css.append(f"    @keyframes wipe{i} {{ to {{ transform: translateX({tw + 14:.1f}px); }} }}")
        y += lh * 2
    last = len(TERMINAL) * step + 0.6
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Terminal: {escape('; '.join(f'{c} -> {o}' for c, o in TERMINAL))}">
  <title>whoami</title>
  <style>
    .mono {{ font: 16px {MONO}; }}
    .out {{ fill: #8b949e; opacity: 0; animation: fade .4s ease-out forwards; }}
    .row {{ opacity: 0; animation: fade .01s linear forwards; }}
    .caret {{ animation: blink 1s step-end infinite; opacity: 0; animation-delay: {last:.2f}s; }}
    @keyframes fade {{ to {{ opacity: 1; }} }}
    @keyframes blink {{ 0% {{ opacity: 1; }} 50% {{ opacity: 0; }} 100% {{ opacity: 1; }} }}
{chr(10).join(css)}
    @media (prefers-reduced-motion: reduce) {{
      * {{ animation: none !important; }}
      .row, .out, .caret {{ opacity: 1; }}
      .cover {{ display: none; }}
    }}
  </style>
  <rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="12" fill="#161b22" stroke="#30363d"/>
  <path d="M0.5 12.5a12 12 0 0 1 12-12h{w-25}a12 12 0 0 1 12 12V40H0.5z" fill="#21262d"/>
  <circle cx="24" cy="20" r="6" fill="#ff5f56"/><circle cx="44" cy="20" r="6" fill="#ffbd2e"/><circle cx="64" cy="20" r="6" fill="#27c93f"/>
  <text x="{w/2}" y="25" text-anchor="middle" class="mono" fill="#8b949e" font-size="13">tsotne@github: ~</text>
  <g>{''.join(rows)}
  </g>
  <text x="28" y="{y}" class="mono"><tspan fill="{C1}">$</tspan> <tspan class="caret" fill="#e6edf3">▍</tspan></text>
</svg>"""


def divider() -> str:
    w, h = 1200, 12
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="presentation" aria-hidden="true">
  <defs>
    <linearGradient id="d" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{w}" y2="0" spreadMethod="repeat">
      <stop offset="0" stop-color="{C1}" stop-opacity="0"/>
      <stop offset="0.25" stop-color="{C1}"/>
      <stop offset="0.5" stop-color="{C2}"/>
      <stop offset="0.75" stop-color="{C3}"/>
      <stop offset="1" stop-color="{C3}" stop-opacity="0"/>
      <animateTransform attributeName="gradientTransform" type="translate" values="0 0;{w} 0" dur="5s" repeatCount="indefinite"/>
    </linearGradient>
  </defs>
  <rect y="{h/2 - 1.5}" width="{w}" height="3" rx="1.5" fill="url(#d)"/>
</svg>"""


def footer() -> str:
    w, h = 1200, 120

    def wave(amp: float, y0: float) -> str:
        # Period P = w/2; the path spans w + P so translating by -P loops seamlessly.
        period = w / 2
        d = f"M0 {y0}"
        for k in range(6):
            x = k * period / 2
            sign = -1 if k % 2 == 0 else 1
            d += f" Q{x + period / 4:g} {y0 + sign * amp:g} {x + period / 2:g} {y0}"
        return d + f" V{h} H0Z"

    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="presentation" aria-hidden="true">
  <defs>
    <linearGradient id="f" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{C1}"/><stop offset="0.5" stop-color="{C2}"/><stop offset="1" stop-color="{C3}"/>
    </linearGradient>
  </defs>
  <style>
    .w {{ animation: flow 8s linear infinite; }}
    .w2 {{ animation-duration: 12s; animation-direction: reverse; }}
    .w3 {{ animation-duration: 6s; }}
    @keyframes flow {{ from {{ transform: translateX(0); }} to {{ transform: translateX(-{w // 2}px); }} }}
    @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
  </style>
  <path class="w w2" d="{wave(14, 50)}" fill="url(#f)" opacity="0.25"/>
  <path class="w" d="{wave(18, 65)}" fill="url(#f)" opacity="0.45"/>
  <path class="w w3" d="{wave(10, 85)}" fill="url(#f)" opacity="0.9"/>
</svg>"""


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    write("header.svg", header())
    write("typing.svg", typing())
    write("terminal.svg", terminal())
    write("divider.svg", divider())
    write("footer.svg", footer())
