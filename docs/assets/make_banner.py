import base64, math, pathlib

W, H = 1600, 440
BG      = "#1d2733"
TEXT    = "#f4f6f8"
SUBTEXT = "#c9d1da"
LINE    = "#eef1f4"
FAINT   = "#56636f"
FORCE   = "#6fa3e0"
PHASE   = "#e0b350"
ION     = "#5cc19d"

TITLE    = "FP-DeErr"
SUBTITLE = "Application-Oriented Error Decomposition for Foundation Potentials"
FONT     = "Helvetica Neue, Helvetica, Arial, Liberation Sans, sans-serif"

MARGIN      = 56
LOGO_SIZE   = 150
TITLE_SIZE  = 72
SUB_SIZE    = 30
LABEL_SIZE  = 30
PANEL_X     = (56, 616, 1176)
PANEL_TOP   = 180
PANEL_SCALE = 1.35
LABEL_BASE  = 407
STROKE = 4.6
DASH   = "13 9"

def panel_force():
    ox, oy = 30, 125
    dft_tip, fp_tip = (235, 62), (190, 20)
    r = 112
    a_d = math.atan2(dft_tip[1]-oy, dft_tip[0]-ox)
    a_f = math.atan2(fp_tip[1]-oy, fp_tip[0]-ox)
    p1 = (ox + r*math.cos(a_d), oy + r*math.sin(a_d))
    p2 = (ox + r*math.cos(a_f), oy + r*math.sin(a_f))
    am = (a_d + a_f)/2
    lb = (ox + (r+24)*math.cos(am) + 2, oy + (r+24)*math.sin(am) + 9)
    return f"""<circle cx="{ox}" cy="{oy}" r="10" fill="none" stroke="{SUBTEXT}" stroke-width="3"/>
<line x1="{ox}" y1="{oy}" x2="{dft_tip[0]}" y2="{dft_tip[1]}" stroke="{LINE}" stroke-width="{STROKE+0.6}"/>
<polygon points="249,57 226,50 232,75" fill="{LINE}"/>
<line x1="{ox}" y1="{oy}" x2="{fp_tip[0]}" y2="{fp_tip[1]}" stroke="{FORCE}" stroke-width="{STROKE+0.6}" stroke-dasharray="{DASH}"/>
<polygon points="201,10 179,14 193,32" fill="{FORCE}"/>
<path d="M {p1[0]:.1f} {p1[1]:.1f} A {r} {r} 0 0 0 {p2[0]:.1f} {p2[1]:.1f}" fill="none" stroke="{SUBTEXT}" stroke-width="2.5"/>
<text x="{lb[0]:.1f}" y="{lb[1]:.1f}" font-size="24" fill="{SUBTEXT}" font-style="italic">&#916;&#952;</text>"""

def panel_hull():
    dft = [(20,22),(70,92),(135,122),(200,95),(255,18)]
    fp  = [(20,22),(70,106),(135,112),(200,106),(255,18)]
    above = [(105,70),(165,60),(232,48),(46,48)]
    pts = lambda P: " ".join(f"{a},{b}" for a,b in P)
    s  = f'<polyline points="{pts(dft)}" fill="none" stroke="{LINE}" stroke-width="{STROKE}"/>'
    s += f'<polyline points="{pts(fp)}" fill="none" stroke="{PHASE}" stroke-width="{STROKE}" stroke-dasharray="{DASH}"/>'
    for a,b in dft:     s += f'<circle cx="{a}" cy="{b}" r="8" fill="{LINE}"/>'
    for a,b in fp[1:-1]:s += f'<circle cx="{a}" cy="{b}" r="7.5" fill="{BG}" stroke="{PHASE}" stroke-width="3.5"/>'
    for a,b in above:   s += f'<circle cx="{a}" cy="{b}" r="6.5" fill="none" stroke="{SUBTEXT}" stroke-width="2.5"/>'
    return s

def panel_neb():
    dft = "M 15 120 C 80 120, 100 15, 140 15 S 200 105, 255 105"
    fp  = "M 15 120 C 80 120, 100 55, 140 55 S 200 118, 255 118"
    s  = f'<line x1="15" y1="138" x2="262" y2="138" stroke="{FAINT}" stroke-width="2.5"/>'
    s += f'<path d="{dft}" fill="none" stroke="{LINE}" stroke-width="{STROKE}"/>'
    s += f'<path d="{fp}" fill="none" stroke="{ION}" stroke-width="{STROKE}" stroke-dasharray="{DASH}"/>'
    for a,b in [(15,120),(140,15),(255,105)]: s += f'<circle cx="{a}" cy="{b}" r="8" fill="{LINE}"/>'
    for a,b in [(140,55),(255,118)]:          s += f'<circle cx="{a}" cy="{b}" r="7.5" fill="{BG}" stroke="{ION}" stroke-width="3.5"/>'
    return s

def build(logo_path):
    logo = base64.b64encode(pathlib.Path(logo_path).read_bytes()).decode()
    logo_w = round(LOGO_SIZE * 520 / 548)
    tx = MARGIN + logo_w + 26
    panels = "".join(
        f'<g transform="translate({x},{PANEL_TOP}) scale({PANEL_SCALE})">{d()}</g>'
        for x, d in zip(PANEL_X, (panel_force, panel_hull, panel_neb)))
    labels = [("Force Prediction", FORCE), ("Phase Stability &amp; Ordering", PHASE), ("Ion Migration (NEB)", ION)]
    lab = "".join(
        f'<rect x="{x}" y="{LABEL_BASE-23}" width="22" height="22" rx="4" fill="{c}"/>'
        f'<text x="{x+34}" y="{LABEL_BASE}" font-size="{LABEL_SIZE}" fill="{TEXT}">{t}</text>'
        for x,(t,c) in zip(PANEL_X, labels))
    third = W/3
    return f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}" role="img" aria-label="FP-DeErr: Application-Oriented Error Decomposition for Foundation Potentials">
<title>FP-DeErr: Application-Oriented Error Decomposition for Foundation Potentials</title>
<rect width="{W}" height="{H}" fill="{BG}"/>
<rect x="0" y="{H-8}" width="{third:.0f}" height="8" fill="{FORCE}"/>
<rect x="{third:.0f}" y="{H-8}" width="{third:.0f}" height="8" fill="{PHASE}"/>
<rect x="{2*third:.0f}" y="{H-8}" width="{third:.0f}" height="8" fill="{ION}"/>
<image x="{MARGIN}" y="34" width="{logo_w}" height="{LOGO_SIZE}" xlink:href="data:image/png;base64,{logo}"/>
<text x="{tx}" y="112" font-size="{TITLE_SIZE}" font-weight="700" fill="{TEXT}">{TITLE}</text>
<text x="{tx+2}" y="160" font-size="{SUB_SIZE}" fill="{SUBTEXT}">{SUBTITLE}</text>
<g font-size="26" fill="{SUBTEXT}">
  <line x1="1392" y1="62" x2="1436" y2="62" stroke="{LINE}" stroke-width="5"/><text x="1450" y="71">DFT</text>
  <line x1="1392" y1="102" x2="1436" y2="102" stroke="{SUBTEXT}" stroke-width="5" stroke-dasharray="10 7"/><text x="1450" y="111">FP</text>
</g>
{panels}
{lab}
</svg>"""

if __name__ == "__main__":
    import sys
    out = pathlib.Path(sys.argv[2])
    out.write_text(build(sys.argv[1]), encoding="utf-8")
    print("wrote", out, out.stat().st_size, "bytes")
