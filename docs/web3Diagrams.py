#!/usr/bin/env python3
"""
web3Diagrams.py  →  generates web3-arch-web20.svg  and  web3-arch-web30.svg

Run:
    python3 docs/web3Diagrams.py
"""
import base64
from pathlib import Path

OUT_DIR = Path(__file__).parent

def _png_data_uri(filename):
    data = base64.b64encode((OUT_DIR / filename).read_bytes()).decode()
    return f"data:image/png;base64,{data}"

_THINKER_URI = _png_data_uri("iconThinker.png")


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

def arrow_marker_rev(mid, color):
    poly = tag("polygon", {"points": "9 0,0 3,9 6", "fill": color})
    return (f'<marker id="{mid}" markerWidth="9" markerHeight="6" '
            f'refX="1" refY="3" orient="auto">{poly}</marker>')

def bidir_line(x1, y1, x2, y2, stroke="#64748b", sw=1.8):
    a = {"x1": x1, "y1": y1, "x2": x2, "y2": y2,
         "stroke": stroke, "stroke-width": sw,
         "marker-start": "url(#arr-rev)", "marker-end": "url(#arr)"}
    return tag("line", a)

def drop_shadow(fid, dx=0, dy=2, std=3, color="#0f172a", opacity="0.08",
                px="-5%", py="-5%", pw="115%", ph="130%"):
    inner = (f'<feDropShadow dx="{dx}" dy="{dy}" stdDeviation="{std}" '
             f'flood-color="{color}" flood-opacity="{opacity}"/>')
    return (f'<filter id="{fid}" x="{px}" y="{py}" width="{pw}" height="{ph}">'
            f'{inner}</filter>')

def svg_wrap(w, h, content):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%"\n'
            f'     font-family="system-ui,-apple-system,sans-serif">\n'
            f'{content}\n</svg>')


# ══════════════════════════════════════════════════════════════════════════════
# WEB 2.0 DIAGRAM  —  upside-down triangle: Principal · World → [interface|Javier]
# ══════════════════════════════════════════════════════════════════════════════

def thinker_icon(x, y, h):
    """PNG thinker icon with top-left at (x,y), height h; width auto-scaled (208:316).
    multiply blend: white bg disappears into parent fill; dark silhouette stays."""
    w = round(h * 208 / 316)
    return f'<image href="{_THINKER_URI}" x="{x}" y="{y}" width="{w}" height="{h}" style="mix-blend-mode:multiply"/>'


W20, H20 = 500, 428

# two top-tier actors (closer together)
PRINC_CX, PRINC_CY, PRINC_R = 175, 94, 23
WORLD_CX, WORLD_CY, WORLD_R = 325, 94, 23

# Javier box: chips (top) · identity+thinker (mid) · AI/KB (mid) · agents (bottom)
JAV_X, JAV_Y, JAV_W, JAV_H = 48, 158, 404, 140
JAV_CX  = JAV_X + JAV_W // 2   # 250
JAV_BOT = JAV_Y + JAV_H        # 298

# Principal Data box
DATA_X, DATA_Y, DATA_W, DATA_H = 28, 316, 444, 62
DATA_CX = DATA_X + DATA_W // 2  # 250
DATA_BOT = DATA_Y + DATA_H      # 378

# interface channel chips  (icon, label, bg, border)
_CHANNELS = [
    ("📞", "Twilio",  "#fff7ed", "#ea580c"),
    ("📱", "iPhone",  "#eff6ff", "#3b82f6"),
    ("💻", "Web UI",  "#f0fdf4", "#16a34a"),
]

# discipline agent boxes (inside Javier bottom)
_AGENTS = [
    ("🏠", "houseAgent",   "#f0fdf4", "#16a34a"),
    ("🏥", "medicalAgent", "#eff6ff", "#3b82f6"),
    ("💰", "moneyAgent",   "#fefce8", "#ca8a04"),
    ("📄", "estateAgent",  "#fdf4ff", "#9333ea"),
]


def build_web20():
    # ── Javier internals ──
    CH_Y   = JAV_Y + 4         # 162
    CH_H   = 22
    SEP1_Y = CH_Y + CH_H + 3  # 187
    ID_ICN = SEP1_Y + 15      # thinker center-y: 202
    SEP2_Y = SEP1_Y + 42      # 229
    AI_Y   = SEP2_Y + 3       # 232
    AI_H   = 26
    SEP3_Y = AI_Y + AI_H + 2  # 260
    AG_Y   = SEP3_Y + 3       # 263
    AG_H   = 30

    ag_w = (JAV_W - 5 * 4) // 4   # 96px each
    ag_x_starts = [JAV_X + 4 + i*(ag_w + 4) for i in range(4)]
    ag_centers  = [x + ag_w // 2 for x in ag_x_starts]  # [100, 200, 300, 400]

    parts = [
        "\n".join([
            "<defs>",
            f"  {arrow_marker('arr', '#64748b')}",
            f"  {arrow_marker_rev('arr-rev', '#64748b')}",
            f"  {drop_shadow('shadow')}",
            "</defs>",
        ]),
        rect(0, 0, W20, H20, "#f8fafc", rx=12),
        rect(0, 0, W20, 48, "#1e293b", rx=12),
        rect(0, 36, W20, 12, "#1e293b"),
        text(W20//2, 22, "Web 2.0  —  Javier in Others' Platforms",
             13, "#f1f5f9", bold=True, spacing="0.3"),
        text(W20//2, 39, "BirthPlan · current state", 9, "#94a3b8"),
        # ── triangle skeleton ──
        line(PRINC_CX+PRINC_R, PRINC_CY, WORLD_CX-WORLD_R, WORLD_CY,
             stroke="#cbd5e1", sw=1.2, dash="5,4"),
        bidir_line(PRINC_CX, PRINC_CY+PRINC_R, 210, JAV_Y),
        # 📱 label at midpoint of Principal→Javier diagonal
        rect(183, 129, 18, 16, "#f8fafc", rx=3),
        text(192, 141, "📱", 11, "#000"),
        bidir_line(WORLD_CX, WORLD_CY+WORLD_R, 290, JAV_Y),
        # ── actors ──
        circle(PRINC_CX, PRINC_CY, PRINC_R, "#dbeafe", stroke="#3b82f6", sw=2, filt="shadow"),
        text(PRINC_CX, PRINC_CY+7,           "🧑", 20, "#000"),
        text(PRINC_CX-20, PRINC_CY+PRINC_R+14, "Principal", 10, "#1e40af", bold=True),
        circle(WORLD_CX, WORLD_CY, WORLD_R, "#dcfce7", stroke="#16a34a", sw=2, filt="shadow"),
        text(WORLD_CX, WORLD_CY+7,           "🌐", 20, "#000"),
        text(WORLD_CX+26, WORLD_CY+WORLD_R+14, "The World", 10, "#15803d", bold=True),
        # ── Javier outer box ──
        rect(JAV_X, JAV_Y, JAV_W, JAV_H, "#ccfbf1", rx=9,
             stroke="#0f766e", sw=2.5, filt="shadow"),
    ]

    # interface chips (slim, inside Javier top)
    ch_x = JAV_X + 6
    for icon, label, bg, border in _CHANNELS:
        cw = 126
        ccx = ch_x + cw // 2
        parts += [
            rect(ch_x, CH_Y, cw, CH_H, bg, rx=3, stroke=border, sw=0.8),
            text(ccx, CH_Y+9,  icon,  8, "#000"),
            text(ccx, CH_Y+18, label, 6.5, border, bold=True),
        ]
        ch_x += cw + 5

    parts += [
        sep_line(JAV_X+10, SEP1_Y, JAV_X+JAV_W-10, "#a7f3d0"),
        # thinker PNG icon + Javier identity — group centered in J box
        # icon h=24 matches two-line text block; w≈16 (208:316 ratio)
        thinker_icon(x=JAV_CX - 56, y=ID_ICN - 10, h=24),
        text(JAV_CX - 34, ID_ICN + 2,  "Javier", 12, "#064e3b", bold=True, anchor="start"),
        text(JAV_CX - 34, ID_ICN + 16, "Personal Assistant", 8, "#065f46", anchor="start"),
        sep_line(JAV_X+10, SEP2_Y, JAV_X+JAV_W-10, "#a7f3d0"),
        # AI/KB strip
        rect(JAV_X+3, AI_Y, JAV_W-6, AI_H, "#0d9488", rx=5),
        text(JAV_CX, AI_Y + AI_H//2 + 5, "🧠  AI · Knowledge Base", 9, "#ccfbf1", bold=True),
        sep_line(JAV_X+10, SEP3_Y, JAV_X+JAV_W-10, "#a7f3d0"),
    ]

    # agent boxes inside Javier
    for i, (icon, label, bg, border) in enumerate(_AGENTS):
        ax = ag_x_starts[i]
        acx = ag_centers[i]
        parts += [
            rect(ax, AG_Y, ag_w, AG_H, bg, rx=4, stroke=border, sw=1),
            text(acx, AG_Y+10, icon,  10, "#000"),
            text(acx, AG_Y+21, label,  6.5, border, bold=True),
        ]

    # 1 line per agent piercing through Javier bottom → data box top
    for acx in ag_centers:
        parts.append(
            line(acx, AG_Y+AG_H, acx, DATA_Y, stroke="#94a3b8", sw=1.2, marker="arr")
        )

    parts += [
        # Principal Data box (no label above)
        rect(DATA_X, DATA_Y, DATA_W, DATA_H, "#fffbeb", rx=8,
             stroke="#d97706", sw=1.5, filt="shadow"),
        # Google Drive sub-section
        rect(DATA_X+4, DATA_Y+4, 294, DATA_H-8, "#fff7ed", rx=5, stroke="#fbbf24", sw=1),
        text(DATA_X+151, DATA_Y+20, "📁  Google Drive", 10, "#92400e", bold=True),
        text(DATA_X+151, DATA_Y+36, "🏠 house  ·  🏥 medical  ·  💰 finance  ·  …", 8.5, "#b45309"),
        text(DATA_X+151, DATA_Y+50, "Google owns · can read · can go down", 7.5, "#d97706"),
        # Gmail sub-section
        rect(DATA_X+302, DATA_Y+4, 138, DATA_H-8, "#fff7ed", rx=5, stroke="#fbbf24", sw=1),
        text(DATA_X+371, DATA_Y+20, "✉  Gmail", 10, "#92400e", bold=True),
        text(DATA_X+371, DATA_Y+36, "email · comm", 8.5, "#b45309"),
        text(DATA_X+371, DATA_Y+50, "Google reads", 7.5, "#d97706"),
        # label + warning BELOW data box
        text(DATA_CX, DATA_BOT+13,
             "principal data  (platforms own it ⚠)", 8, "#b45309", italic=True),
        text(DATA_CX, DATA_BOT+27,
             "⚠  Principal is a user of these platforms — not an owner",
             8, "#dc2626", bold=True),
        text(DATA_CX, DATA_BOT+39,
             "any platform can read the data · go dark · sell to a competitor",
             7.5, "#dc2626"),
    ]

    return svg_wrap(W20, H20, "\n".join(parts))


# ══════════════════════════════════════════════════════════════════════════════
# WEB 3.0 DIAGRAM  —  same logical flow as Web 2.0; Principal owns the data
# Same canvas, same triangle, same Javier internals — only the data layer changes
# ══════════════════════════════════════════════════════════════════════════════
W30, H30 = W20, H20   # identical canvas — parallelism is intentional

# Web 3.0 replaces the 3 platform interface chips with 2 AI-native interfaces
_CHANNELS_30 = [
    ("Agent Mesh",  "AI talks to AI — negotiate, book, delegate",  "#e0f2fe", "#0284c7"),
    ("ZK Proof",    "prove facts without sharing your raw data",    "#f3e8ff", "#7c3aed"),
]


def build_web30():
    # Interface chips are taller (CH_H=30 vs 22) to fit name+statement;
    # agent boxes shrink by same amount (AG_H=22 vs 30) — J box height unchanged.
    CH_Y   = JAV_Y + 4
    CH_H   = 30                 # taller: name + 1-line statement
    SEP1_Y = CH_Y + CH_H + 3   # 195
    ID_ICN = SEP1_Y + 15       # 210
    SEP2_Y = SEP1_Y + 42       # 237
    AI_Y   = SEP2_Y + 3        # 240
    AI_H   = 26
    SEP3_Y = AI_Y + AI_H + 2   # 268
    AG_Y   = SEP3_Y + 3        # 271
    AG_H   = 22                 # compressed to compensate for taller chips

    ag_w        = (JAV_W - 5 * 4) // 4
    ag_x_starts = [JAV_X + 4 + i*(ag_w + 4) for i in range(4)]
    ag_centers  = [x + ag_w // 2 for x in ag_x_starts]

    parts = [
        "\n".join([
            "<defs>",
            f"  {arrow_marker('arr', '#64748b')}",      # needed by bidir_line
            f"  {arrow_marker('arr-g', '#059669')}",    # green — owned connection
            f"  {arrow_marker_rev('arr-rev', '#64748b')}",
            f"  {drop_shadow('shadow')}",
            "</defs>",
        ]),
        # ── background + header (deep green — signals ownership era) ──
        rect(0, 0, W30, H30, "#f0fdf4", rx=12),
        rect(0, 0, W30, 48, "#064e3b", rx=12),
        rect(0, 36, W30, 12, "#064e3b"),
        text(W30//2, 22, "Web 3.0  —  Javier as Your Sovereign Agent",
             13, "#d1fae5", bold=True, spacing="0.3"),
        text(W30//2, 39, "TrustedPlan+ · target state", 9, "#6ee7b7"),
        # ── same triangle skeleton ──
        line(PRINC_CX+PRINC_R, PRINC_CY, WORLD_CX-WORLD_R, WORLD_CY,
             stroke="#bbf7d0", sw=1.2, dash="5,4"),
        bidir_line(PRINC_CX, PRINC_CY+PRINC_R, 210, JAV_Y),
        # 📱 label at midpoint of Principal→Javier diagonal
        rect(183, 129, 18, 16, "#f0fdf4", rx=3),
        text(192, 141, "📱", 11, "#000"),
        bidir_line(WORLD_CX, WORLD_CY+WORLD_R, 290, JAV_Y),
        # ── same actors ──
        circle(PRINC_CX, PRINC_CY, PRINC_R, "#dbeafe", stroke="#3b82f6", sw=2, filt="shadow"),
        text(PRINC_CX, PRINC_CY+7,           "🧑", 20, "#000"),
        text(PRINC_CX, PRINC_CY+PRINC_R+16, "Principal", 10, "#1e40af", bold=True),
        circle(WORLD_CX, WORLD_CY, WORLD_R, "#dcfce7", stroke="#16a34a", sw=2, filt="shadow"),
        text(WORLD_CX, WORLD_CY+7,           "🌐", 20, "#000"),
        text(WORLD_CX, WORLD_CY+WORLD_R+16, "The World", 10, "#15803d", bold=True),
        # ── Javier outer box (greener than Web 2.0) ──
        rect(JAV_X, JAV_Y, JAV_W, JAV_H, "#d1fae5", rx=9,
             stroke="#059669", sw=2.5, filt="shadow"),
    ]

    # 2 wide interface chips — Agent Mesh + ZK Proof; each shows name + 1-line statement
    cw30 = 193
    ch_x = JAV_X + 6
    for label, stmt, bg, border in _CHANNELS_30:
        ccx = ch_x + cw30 // 2
        parts += [
            rect(ch_x, CH_Y, cw30, CH_H, bg, rx=3, stroke=border, sw=0.8),
            text(ccx, CH_Y+12, label, 8.5, border, bold=True),
            text(ccx, CH_Y+23, stmt,  7,   border, italic=True),
        ]
        ch_x += cw30 + 6

    parts += [
        sep_line(JAV_X+10, SEP1_Y, JAV_X+JAV_W-10, "#86efac"),
        # thinker + identity ("Sovereign Agent" vs "Personal Assistant" in Web 2.0)
        thinker_icon(x=JAV_CX - 56, y=ID_ICN - 10, h=24),
        text(JAV_CX - 34, ID_ICN + 2,  "Javier", 12, "#064e3b", bold=True, anchor="start"),
        text(JAV_CX - 34, ID_ICN + 16, "Sovereign Agent", 8, "#065f46", anchor="start"),
        sep_line(JAV_X+10, SEP2_Y, JAV_X+JAV_W-10, "#86efac"),
        # AI/KB strip (same)
        rect(JAV_X+3, AI_Y, JAV_W-6, AI_H, "#065f46", rx=5),
        text(JAV_CX, AI_Y + AI_H//2 + 5, "🧠  AI · Knowledge Base", 9, "#d1fae5", bold=True),
        sep_line(JAV_X+10, SEP3_Y, JAV_X+JAV_W-10, "#86efac"),
    ]

    # same agent boxes inside Javier
    for i, (icon, label, bg, border) in enumerate(_AGENTS):
        ax = ag_x_starts[i]
        acx = ag_centers[i]
        parts += [
            rect(ax, AG_Y, ag_w, AG_H, bg, rx=4, stroke=border, sw=1),
            text(acx, AG_Y+9,  icon,  9,   "#000"),
            text(acx, AG_Y+19, label, 6.5, border, bold=True),
        ]

    # green agent lines → YOUR vault (contrast: gray → foreign platform in Web 2.0)
    for acx in ag_centers:
        parts.append(
            line(acx, AG_Y+AG_H, acx, DATA_Y, stroke="#059669", sw=1.4, marker="arr-g")
        )

    parts += [
        # ── Your Vault — the one thing that changed ──
        rect(DATA_X, DATA_Y, DATA_W, DATA_H, "#dcfce7", rx=8,
             stroke="#16a34a", sw=2, filt="shadow"),
        # Left sub-box: your data (mirrors Google Drive box position in Web 2.0)
        rect(DATA_X+4, DATA_Y+4, 294, DATA_H-8, "#f0fdf4", rx=5, stroke="#4ade80", sw=1),
        text(DATA_X+151, DATA_Y+20, "🔒  Your SOLID Pod", 10, "#14532d", bold=True),
        text(DATA_X+151, DATA_Y+36, "🏠 house  ·  🏥 medical  ·  💰 finances  ·  📄 estate", 8.5, "#15803d"),
        text(DATA_X+151, DATA_Y+50, "self-hosted · encrypted · your keys", 7.5, "#16a34a"),
        # Right sub-box: access control (mirrors Gmail box position in Web 2.0)
        rect(DATA_X+302, DATA_Y+4, 138, DATA_H-8, "#f0fdf4", rx=5, stroke="#4ade80", sw=1),
        text(DATA_X+371, DATA_Y+18, "🔑  You Control", 9.5, "#14532d", bold=True),
        text(DATA_X+371, DATA_Y+33, "grant · revoke", 8.5, "#15803d"),
        text(DATA_X+371, DATA_Y+47, "no platform reads", 7.5, "#16a34a"),
        # label + celebration BELOW data box (contrast to Web 2.0's warning)
        text(DATA_CX, DATA_BOT+13,
             "your data  (you own it ✓)", 8, "#15803d", italic=True),
        text(DATA_CX, DATA_BOT+27,
             "✓  same Javier · same agents · same interfaces  —  different ownership",
             8, "#059669", bold=True),
        text(DATA_CX, DATA_BOT+39,
             "swap any platform · revoke any access · no vendor can go dark",
             7.5, "#16a34a"),
    ]

    return svg_wrap(W30, H30, "\n".join(parts))


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
