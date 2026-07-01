#!/usr/bin/env python3
"""
web3Diagrams.py  →  generates web3-arch-web20.svg  and  web3-arch-web30.svg

Run:
    python3 docs/web3Diagrams.py
"""
from pathlib import Path

OUT_DIR = Path(__file__).parent


# ── shared helpers (same style as lifeTrackerDiagram.py) ──────────────────────

def _attrs(d):
    return "".join(f' {k}="{v}"' for k, v in d.items())

def tag(name, attrs, content=None):
    a = _attrs(attrs)
    if content is None:
        return f"<{name}{a}/>"
    return f"<{name}{a}>{content}</{name}>"

def rect(x, y, w, h, fill, rx=0, stroke=None, sw=1.5, filt=None, opacity=None):
    a = {"x": x, "y": y, "width": w, "height": h, "fill": fill, "rx": rx}
    if stroke:   a["stroke"] = stroke; a["stroke-width"] = sw
    if filt:     a["filter"]  = f"url(#{filt})"
    if opacity is not None: a["opacity"] = opacity
    return tag("rect", a)

def line(x1, y1, x2, y2, stroke="#64748b", sw=1.8, dash=None, marker=None):
    a = {"x1": x1, "y1": y1, "x2": x2, "y2": y2,
         "stroke": stroke, "stroke-width": sw}
    if dash:   a["stroke-dasharray"] = dash
    if marker: a["marker-end"] = f"url(#{marker})"
    return tag("line", a)

def circle(cx, cy, r, fill, stroke=None, sw=2, filt=None):
    a = {"cx": cx, "cy": cy, "r": r, "fill": fill}
    if stroke: a["stroke"] = stroke; a["stroke-width"] = sw
    if filt:   a["filter"] = f"url(#{filt})"
    return tag("circle", a)

def text(x, y, msg, size, fill, anchor="middle", bold=False, italic=False, spacing=None):
    a = {"x": x, "y": y, "text-anchor": anchor, "font-size": size, "fill": fill}
    if bold:    a["font-weight"]  = "700"
    if italic:  a["font-style"]   = "italic"
    if spacing: a["letter-spacing"] = spacing
    return tag("text", a, content=msg)

def sep_line(x1, y, x2, stroke="#a7f3d0", sw=1):
    return tag("line", {"x1": x1, "y1": y, "x2": x2, "y2": y,
                        "stroke": stroke, "stroke-width": sw})

def arrow_marker(mid, color):
    poly = tag("polygon", {"points": "0 0,9 3,0 6", "fill": color})
    return (f'<marker id="{mid}" markerWidth="9" markerHeight="6" '
            f'refX="8" refY="3" orient="auto">{poly}</marker>')

def drop_shadow(fid, dx=0, dy=2, std=3, color="#0f172a", opacity="0.08",
                px="-5%", py="-5%", pw="115%", ph="130%"):
    inner = (f'<feDropShadow dx="{dx}" dy="{dy}" stdDeviation="{std}" '
             f'flood-color="{color}" flood-opacity="{opacity}"/>')
    return (f'<filter id="{fid}" x="{px}" y="{py}" width="{pw}" height="{ph}">'
            f'{inner}</filter>')

def svg_wrap(w, h, content):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"\n'
            f'     font-family="system-ui,-apple-system,sans-serif">\n'
            f'{content}\n</svg>')


# ══════════════════════════════════════════════════════════════════════════════
# WEB 2.0 DIAGRAM  —  "Javier as an App in Others' Platforms"
# ══════════════════════════════════════════════════════════════════════════════
W20, H20 = 740, 358

# layout
FLOW_Y    = 105   # main flow row center-y
JAV20_CX  = 388   # Javier center-x
RAIL_Y    = 178   # dashed dependency rail y
PLAT_Y    = 198   # platform boxes top-y
WARN_Y    = 284   # warning banner top-y

PLATFORMS = [
    dict(bx=112, cx=200, bw=176, icon="☁",  title="Google Drive", sub="data store · Google owns · can read"),
    dict(bx=305, cx=388, bw=166, icon="✉",  title="Gmail",        sub="email channel · Google reads"),
    dict(bx=508, cx=590, bw=164, icon="☎",  title="Twilio",       sub="SMS channel · Twilio-owned"),
]


def web20_defs():
    return "\n".join([
        "<defs>",
        f"  {arrow_marker('arr', '#64748b')}",
        f"  {arrow_marker('arr-dash', '#94a3b8')}",
        f"  {drop_shadow('shadow')}",
        "</defs>",
    ])


def web20_header():
    return "\n".join([
        rect(0, 0, W20, 56, "#1e293b", rx=12),
        rect(0, 44, W20, 12, "#1e293b"),           # fill rounded-corner notch
        text(W20//2, 26, "Web 2.0  —  Javier as an App in Others' Platforms",
             14, "#f1f5f9", bold=True, spacing="0.3"),
        text(W20//2, 44, "BirthPlan · current state", 10, "#94a3b8"),
    ])


def web20_flow():
    return "\n".join([
        # Frank
        circle(68, FLOW_Y, 26, "#dbeafe", stroke="#3b82f6", filt="shadow"),
        text(68, FLOW_Y+8, "🧑", 24, "#000"),
        text(68, FLOW_Y+34, "Frank", 11, "#1d4ed8", bold=True),
        line(95, FLOW_Y, 150, FLOW_Y, marker="arr"),
        # Browser / iPhone
        rect(150, 82, 118, 46, "#e0f2fe", rx=7, stroke="#0284c7", filt="shadow"),
        text(209, 100, "Browser", 11, "#0c4a6e", bold=True),
        text(209, 116, "/ iPhone", 10, "#0369a1"),
        line(268, FLOW_Y, 318, FLOW_Y, marker="arr"),
        # Javier
        rect(318, 68, 140, 74, "#ccfbf1", rx=9, stroke="#0f766e", sw=2.5, filt="shadow"),
        text(JAV20_CX, 94, "Javier", 15, "#064e3b", bold=True),
        text(JAV20_CX, 112, "Personal Assistant", 9.5, "#065f46"),
        text(JAV20_CX, 127, "(Flask app)", 9.5, "#065f46"),
        line(458, FLOW_Y, 510, FLOW_Y, marker="arr"),
        # Anthropic
        rect(510, 76, 205, 58, "#ede9fe", rx=7, stroke="#7c3aed", filt="shadow"),
        text(612, 99, "Anthropic API", 11, "#4c1d95", bold=True),
        text(612, 115, "Claude — sees all context", 10, "#6d28d9"),
        text(612, 128, "Anthropic-owned infra", 9, "#7c3aed"),
    ])


def web20_rails():
    parts = [
        line(JAV20_CX, 142, JAV20_CX, RAIL_Y, stroke="#cbd5e1", sw=1.5, dash="5,3"),
        line(200, RAIL_Y, 590, RAIL_Y,         stroke="#cbd5e1", sw=1.5, dash="5,3"),
        text(JAV20_CX, RAIL_Y-4, "Javier depends on ↓", 8.5, "#94a3b8", italic=True),
    ]
    for cx in [p["cx"] for p in PLATFORMS]:
        parts.append(line(cx, RAIL_Y, cx, PLAT_Y-2, stroke="#cbd5e1",
                          sw=1.5, dash="5,3", marker="arr-dash"))
    return "\n".join(parts)


def web20_platforms():
    parts = []
    for p in PLATFORMS:
        parts += [
            rect(p["bx"], PLAT_Y, p["bw"], 68, "#fff7ed",
                 rx=7, stroke="#f97316", sw=2, filt="shadow"),
            text(p["cx"], PLAT_Y+22, p["icon"], 20, "#7a7a7a"),
            text(p["cx"], PLAT_Y+42, p["title"], 11, "#c2410c", bold=True),
            text(p["cx"], PLAT_Y+57, p["sub"], 9, "#ea580c"),
        ]
    return "\n".join(parts)


def web20_warning():
    return "\n".join([
        rect(28, WARN_Y, 684, 58, "#fef2f2", rx=8, stroke="#fca5a5"),
        text(W20//2, WARN_Y+22, "⚠  Frank is a user of platforms — not an owner",
             12, "#dc2626", bold=True),
        text(W20//2, WARN_Y+40,
             "Any platform can read his data · change terms · go dark · sell to a competitor",
             10, "#b91c1c"),
    ])


def build_web20():
    sections = [
        web20_defs(),
        rect(0, 0, W20, H20, "#f8fafc", rx=12),
        "<!-- header -->", web20_header(),
        "<!-- main flow -->", web20_flow(),
        "<!-- dependency rails -->", web20_rails(),
        "<!-- platform boxes -->", web20_platforms(),
        "<!-- warning banner -->", web20_warning(),
    ]
    return svg_wrap(W20, H20, "\n".join(sections))


# ══════════════════════════════════════════════════════════════════════════════
# WEB 3.0 DIAGRAM  —  "Javier as a Sovereign Agent"
# ══════════════════════════════════════════════════════════════════════════════
W30, H30 = 740, 390

# Frank DID box
FK_X, FK_Y, FK_W, FK_H = 18, 156, 158, 100
FK_CX = FK_X + FK_W // 2     # 97

# Javier box
JV_X, JV_Y, JV_W, JV_H = 238, 112, 162, 190
JV_CX = JV_X + JV_W // 2     # 319
JV_RX = JV_X + JV_W          # 400 — right edge

# Branch boxes (right side)
BR_X, BR_W = 480, 234
BR_CX = BR_X + BR_W // 2     # 597

# Each branch: box geometry, colors, arrow source y on Javier, lines of text
BRANCHES = [
    dict(
        y=58, h=100, icon="🗄", label="SOLID Pod",
        bg="#dcfce7", border="#16a34a", title_c="#15803d",
        arr_id="arr-green", arr_color="#059669",
        from_y=JV_Y+46, to_y=108,
        lines=[
            ("Frank's personal data store",           "#166534", 10),
            ("Encrypted · Self-hosted",                "#15803d",  9),
            ("Apps request access · Frank revokes",    "#15803d",  9),
            ("RecordAgent API unchanged — swap store", "#16a34a", 8.5),
        ],
    ),
    dict(
        y=173, h=84, icon="🤝", label="Agent Mesh  (A2A)",
        bg="#e0f2fe", border="#0284c7", title_c="#0369a1",
        arr_id="arr-sky", arr_color="#0284c7",
        from_y=JV_Y+JV_H//2, to_y=215,
        lines=[
            ("Doctor · Attorney · Contractor agents",  "#075985", 10),
            ("Agent2Agent protocol · DID-auth",         "#0284c7",  9),
            ("Javier books, negotiates, delegates",     "#0284c7",  9),
        ],
    ),
    dict(
        y=271, h=88, icon="🔒", label="ZK Proofs",
        bg="#f3e8ff", border="#7c3aed", title_c="#6b21a8",
        arr_id="arr-purple", arr_color="#7c3aed",
        from_y=JV_Y+JV_H-46, to_y=315,
        lines=[
            ("Share proof, not raw data",                   "#581c87", 10),
            ('"A1C &lt; 7.5" — insurer sees proof only',    "#7c3aed",  9),
            ("HIPAA-compatible · privacy by design",         "#7c3aed",  9),
        ],
    ),
]


def web30_defs():
    parts = ["<defs>",
             f"  {arrow_marker('arr-blue', '#1d4ed8')}"]
    for b in BRANCHES:
        parts.append(f"  {arrow_marker(b['arr_id'], b['arr_color'])}")
    parts += [
        f"  {drop_shadow('shadow')}",
        f"  {drop_shadow('glow', dx=0, dy=0, std=6, color='#059669', opacity='0.35', px='-12%', py='-12%', pw='128%', ph='134%')}",
        "</defs>",
    ]
    return "\n".join(parts)


def web30_header():
    return "\n".join([
        rect(0, 0, W30, 56, "#064e3b", rx=12),
        rect(0, 44, W30, 12, "#064e3b"),
        text(W30//2, 26, "Web 3.0  —  Javier as a Sovereign Agent",
             14, "#d1fae5", bold=True, spacing="0.3"),
        text(W30//2, 44, "TrustedPlan+ · target state", 10, "#6ee7b7"),
    ])


def web30_frank():
    cx, mid_y = FK_CX, FK_Y + FK_H // 2
    auth_label_x = (FK_X + FK_W + JV_X) // 2
    return "\n".join([
        rect(FK_X, FK_Y, FK_W, FK_H, "#dbeafe", rx=9, stroke="#1d4ed8", sw=2, filt="shadow"),
        text(cx, FK_Y+28, "🔑", 24, "#000"),
        text(cx, FK_Y+52, "Frank", 13, "#1e40af", bold=True),
        text(cx, FK_Y+68, "did:key:z6MkFrank…", 8.5, "#1d4ed8"),
        text(cx, FK_Y+82, "self-sovereign identity", 8.5, "#3b82f6"),
        text(cx, FK_Y+94, "cryptographic · no middleman", 8, "#60a5fa"),
        # arrow Frank → Javier
        line(FK_X+FK_W, mid_y, JV_X, JV_Y+JV_H//2, stroke="#1d4ed8", sw=2.2, marker="arr-blue"),
        text(auth_label_x, mid_y-8, "authorizes", 8.5, "#1d4ed8", italic=True),
    ])


def web30_javier():
    cx, sep_y = JV_CX, JV_Y+98
    return "\n".join([
        rect(JV_X, JV_Y, JV_W, JV_H, "#d1fae5", rx=11, stroke="#059669", sw=3, filt="glow"),
        text(cx, JV_Y+38, "🛡", 30, "#000"),
        text(cx, JV_Y+70, "Javier", 16, "#064e3b", bold=True),
        text(cx, JV_Y+88, "Sovereign Agent", 10, "#047857", bold=True),
        sep_line(JV_X+18, sep_y, JV_X+JV_W-18),
        text(cx, JV_Y+112, "did:key:z6MkJavier…", 8.5, "#065f46"),
        text(cx, JV_Y+127, "Frank's authorized actor", 8.5, "#065f46"),
        text(cx, JV_Y+142, "holds keys · acts on Frank's", 8.5, "#065f46"),
        text(cx, JV_Y+157, "behalf in the world", 8.5, "#065f46"),
        text(cx, JV_Y+173, "A2A endpoint · VC authority", 8, "#6ee7b7"),
        text(cx, JV_Y+185, "pod ACL manager", 8, "#6ee7b7"),
    ])


def web30_branches():
    parts = []
    for b in BRANCHES:
        title_y = b["y"] + 24
        # arrow from Javier right edge
        parts.append(line(JV_RX, b["from_y"], BR_X, b["to_y"],
                          stroke=b["arr_color"], sw=2.2, marker=b["arr_id"]))
        # box
        parts.append(rect(BR_X, b["y"], BR_W, b["h"],
                          b["bg"], rx=8, stroke=b["border"], sw=2, filt="shadow"))
        # title with icon
        parts.append(text(BR_CX, title_y, f'{b["icon"]}  {b["label"]}',
                          12, b["title_c"], bold=True))
        # detail lines
        line_y = title_y + 20
        for msg, fill, sz in b["lines"]:
            parts.append(text(BR_CX, line_y, msg, sz, fill))
            line_y += int(sz) + 5
    return "\n".join(parts)


def web30_success():
    return "\n".join([
        rect(28, H30-22, 684, 14, "#86efac", rx=6, opacity=0.5),
        text(W30//2, H30-11,
             "✓  Frank owns every layer — identity · data · communication · privacy",
             9.5, "#15803d", bold=True),
    ])


def build_web30():
    sections = [
        web30_defs(),
        rect(0, 0, W30, H30, "#f0fdf4", rx=12),
        "<!-- header -->", web30_header(),
        "<!-- Frank DID -->", web30_frank(),
        "<!-- Javier sovereign agent -->", web30_javier(),
        "<!-- branch arrows + boxes -->", web30_branches(),
        "<!-- success banner -->", web30_success(),
    ]
    return svg_wrap(W30, H30, "\n".join(sections))


# ── main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    for name, build_fn in [
        ("web3-arch-web20.svg", build_web20),
        ("web3-arch-web30.svg", build_web30),
    ]:
        out = OUT_DIR / name
        svg = build_fn()
        out.write_text(svg, encoding="utf-8")
        print(f"wrote {out}  ({len(svg):,} bytes)")
