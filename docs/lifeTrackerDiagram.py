#!/usr/bin/env python3
"""
lifeTrackerDiagram.py  →  generates lifeTrackerDiagram.svg

Edit the data constants below, then run:
    python3 docs/lifeTrackerDiagram.py
"""
from pathlib import Path

OUT = Path(__file__).with_suffix(".svg")

# ── titles ─────────────────────────────────────────────────────────────────────
TITLE    = "lifeTracker"
SUBTITLE = "My Personal Assistant Ecosystem, One Trusted Advisor/Advocate backed by Expert Agents"

# ── layout ─────────────────────────────────────────────────────────────────────
W, H   = 1100, 920          # viewBox width × height
CXS    = [108, 278, 448, 618, 788, 958]   # agent column centres
AW, AH = 152, 108           # agent box  width × height
AY     = 200                # agent box  top-y

PILL_H = 48                 # ingestion pill height
PILL_Y = AY + AH + 10      # = 318

RA_Y, RA_H = 398, 180      # RecordAgent outer container
DISK_CY    = 438            # disk top-cap cy  (inside RA)
DRX, DRY   = 64, 8         # disk  rx, ry
DISK_BH    = 40             # disk body height   (cy → cy + DISK_BH)
SVC_Y      = 498            # service-bar top    (Layer 2)

COMM_A_Y   = 600            # Communication Agent box top
COMM_A_H   = 58

CHAN_Y     = 684            # channel boxes top
CHAN_H     = 62

REPO_Y     = 794
FOOT_SEP   = 850

# ── per-agent data ─────────────────────────────────────────────────────────────
AGENTS = [
    dict(
        icon="🏠", name="houseAgent", ns="house.*",
        grad="houseGrad",
        title_fill="#f0f4f8", ns_fill="#c8d8ea", desc_fill="#b0c8e0",
        accent_bar="#a8c4e0",
        desc=["16 sub-agents", "systems · designs", "finance · life · core"],
        pill_bg="#2a3848", pill_label="#7898b0", pill_text="#a8c4e0",
        ingest=["Hays CAD · AVM comps", "County records · Photos"],
        disk_label="house data",
        disk_label_fill="#f0f4f8", disk_row_fill="#a8c4e0",
        disk_rows=["legal · ins · permits · basis", "hvac · plumb · floor_plan"],
        disk_top_cap="#7aaac8", disk_bot_cap="#2a4868",
    ),
    dict(
        icon="🏥", name="medicalAgent", ns="medical.*",
        grad="medGrad",
        title_fill="#f4f0f8", ns_fill="#d8c8ea", desc_fill="#d0b8e8",
        accent_bar="#c4a8d8",
        desc=["FHIR R4  ·  5M's", "Epic / ARC  ·  UHC", "CPAP  ·  BP  ·  Labs"],
        pill_bg="#2a2838", pill_label="#9888b0", pill_text="#d0b8e8",
        ingest=["Epic FHIR · ARC portal", "ResMed myAir · Apple Health"],
        disk_label="medical data",
        disk_label_fill="#f4f0f8", disk_row_fill="#c4a8d8",
        disk_rows=["conditions · medications", "labs · BP · CPAP"],
        disk_top_cap="#9878b8", disk_bot_cap="#402058",
    ),
    dict(
        icon="💰", name="moneyAgent", ns="money.*",
        grad="moneyGrad",
        title_fill="#f0f8f2", ns_fill="#c8e8d0", desc_fill="#b8e0c8",
        accent_bar="#a8d8b8",
        desc=["Beancount  ·  OFX", "RMDs  ·  IRMAA", "Owl runway model"],
        pill_bg="#283828", pill_label="#80a888", pill_text="#b8e0c8",
        ingest=["OFX/QFX · Plaid API", "Schwab · Vanguard feeds"],
        disk_label="money data",
        disk_label_fill="#f0f8f2", disk_row_fill="#a8d8b8",
        disk_rows=["accounts · transactions", "rmd · runway · beancount"],
        disk_top_cap="#68a880", disk_bot_cap="#1e4830",
    ),
    dict(
        icon="⚖",  name="estateAgent", ns="estate.*",
        grad="estateGrad",
        title_fill="#f8f4ee", ns_fill="#e8d0a8", desc_fill="#e0c890",
        accent_bar="#d8b888",
        desc=["7 legal pillars", "§121 · step-up basis", "RLT · DPOA · POLST"],
        pill_bg="#382a18", pill_label="#a08058", pill_text="#e0c890",
        ingest=["County deed · Brokerage", "Owl planner · Ghostfolio"],
        disk_label="estate data",
        disk_label_fill="#f8f4ee", disk_row_fill="#d8b888",
        disk_rows=["asset_registry · deeds", "trust · DPOA · beneficiaries"],
        disk_top_cap="#9a7a50", disk_bot_cap="#3e2a14",
    ),
    dict(
        icon="🕊️",  name="faithAgent", ns="faith.*",
        grad="faithGrad",
        title_fill="#f8f0f0", ns_fill="#e8c8c8", desc_fill="#e0b8b8",
        accent_bar="#d8a8a8",
        desc=["Ignatian Examen", "consolation / desolation", "Catholic practice"],
        pill_bg="#381818", pill_label="#a07878", pill_text="#e0b8b8",
        ingest=["LiturgicalCalendar API", "Magisterium AI · Diocese"],
        disk_label="faith data",
        disk_label_fill="#f8f0f0", disk_row_fill="#d8a8a8",
        disk_rows=["practice · examen", "sacraments · ethical_will"],
        disk_top_cap="#a87888", disk_bot_cap="#4a2828",
    ),
    dict(
        icon="🤝", name="emotionalAgent", ns="emotional.*",
        grad="emotGrad",
        title_fill="#f0f8e8", ns_fill="#d0e0b0", desc_fill="#c8d8a0",
        accent_bar="#b0c890",
        desc=["Relationships · Connection", "PERMA · CBT · Grief", "Erikson · Wellbeing"],
        pill_bg="#283018", pill_label="#809858", pill_text="#c8d8a0",
        ingest=["Apple Health · Wearable", "Daily check-in · Journals"],
        disk_label="emotional data",
        disk_label_fill="#f0f8e8", disk_row_fill="#b0c890",
        disk_rows=["checkin · relationships", "grief · review · contacts"],
        disk_top_cap="#8aa068", disk_bot_cap="#2a3e1e",
    ),
]

# ── gradient stops ─────────────────────────────────────────────────────────────
GRADS = {
    "bgGrad":     [("#f5f0e8", "0%"), ("#faf8f5", "100%")],
    "paGrad":     [("#2c3e50", "0%"), ("#1a252f", "100%")],
    "houseGrad":  [("#5b7fa6", "0%"), ("#3d5c7a", "100%")],
    "medGrad":    [("#7a5b8a", "0%"), ("#5a3d6a", "100%")],
    "moneyGrad":  [("#4a7a5b", "0%"), ("#2d5c3d", "100%")],
    "estateGrad": [("#7a6040", "0%"), ("#5a4428", "100%")],
    "faithGrad":  [("#8a6060", "0%"), ("#6a4040", "100%")],
    "emotGrad":   [("#6a7a50", "0%"), ("#4a5a38", "100%")],
    "commGrad":   [("#607050", "0%"), ("#404e30", "100%")],
}


# ── helpers ────────────────────────────────────────────────────────────────────
def line(x1, y1, x2, y2, stroke="#8e7b5e", sw=1.5, dash=None, opacity=1.0):
    da = f' stroke-dasharray="{dash}"' if dash else ""
    op = f' opacity="{opacity}"' if opacity != 1.0 else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{stroke}" stroke-width="{sw}"{da}{op}/>')


def rect(x, y, w, h, fill, rx=0, stroke=None, sw=1, filt=None, opacity=None):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    f_ = f' filter="url(#{filt})"' if filt else ""
    op = f' opacity="{opacity}"' if opacity else ""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" '
            f'rx="{rx}" fill="{fill}"{s}{f_}{op}/>')


def text(x, y, msg, size, fill, anchor="middle", bold=False, italic=False,
         spacing=None):
    fw = ' font-weight="bold"' if bold else ""
    fi = ' font-style="italic"' if italic else ""
    ls = f' letter-spacing="{spacing}"' if spacing else ""
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" '
            f'font-size="{size}"{fw}{fi}{ls} fill="{fill}">')


def tline(x, y, msg, size, fill, **kw):
    return text(x, y, msg, size, fill, **kw) + msg + "</text>"


def hline(y, x1=80, x2=1020, stroke="#c8b89a", sw=1, dash=None):
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{stroke}" stroke-width="{sw}"{da}/>'


# ── SVG sections ───────────────────────────────────────────────────────────────
def defs_block():
    lines = ['<defs>']
    for gid, stops in GRADS.items():
        lines.append(f'  <linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">')
        for color, offset in stops:
            lines.append(f'    <stop offset="{offset}" stop-color="{color}"/>')
        lines.append('  </linearGradient>')
    lines += [
        '  <filter id="shadow">',
        '    <feDropShadow dx="2" dy="3" stdDeviation="4" flood-color="#00000028"/>',
        '  </filter>',
        '  <filter id="softShadow">',
        '    <feDropShadow dx="1" dy="2" stdDeviation="3" flood-color="#0000001a"/>',
        '  </filter>',
        '</defs>',
    ]
    return "\n".join(lines)


def title_block():
    return "\n".join([
        f'  {tline(W//2, 36, TITLE, 22, "#2c3e50", bold=True, spacing="1")}',
        f'  {tline(W//2, 55, SUBTITLE, 12, "#6b5a3e", italic=True)}',
        f'  {hline(64)}',
    ])


def pa_block():
    cx = W // 2
    return "\n".join([
        f'  {rect(330, 76, 440, 76, "url(#paGrad)", rx=10, filt="shadow")}',
        f'  {rect(330, 76, 440, 4,  "#c8a96e", rx=2)}',
        f'  {tline(cx, 105, "🧭 Personal Assistant  (PA)", 15, "#f5f0e8", bold=True, spacing="0.5")}',
        f'  {tline(cx, 123, "life.pa.*  ·  Chief of Staff + Wise Counsel", 11, "#c8b89a")}',
        f'  {tline(cx, 141, "Routes all cross-domain queries  ·  Knows your whole life, not just one domain", 10, "#a09080", italic=True)}',
    ])


def pa_connectors():
    cx = W // 2
    return "\n".join([
        f'  {line(cx, 152, cx, 192, dash="4,3")}',
        f'  {line(CXS[0], 192, CXS[-1], 192)}',
    ])


def agent_block(a, cx):
    bx = cx - AW // 2
    sep_y = AY + 50
    lines = [
        f'  {line(cx, 192, cx, AY)}',
        f'  {rect(bx, AY, AW, AH, f"url(#{a["grad"]})", rx=8, filt="softShadow")}',
        f'  {rect(bx, AY, AW, 4, a["accent_bar"], rx=2)}',
        f'  {tline(cx, AY+24, a["icon"]+" "+a["name"], 13, a["title_fill"], bold=True)}',
        f'  {tline(cx, AY+41, a["ns"], 10, a["ns_fill"])}',
        f'  <line x1="{bx+16}" y1="{sep_y}" x2="{bx+AW-16}" y2="{sep_y}" stroke="{a["ns_fill"]}" stroke-width="0.5" opacity="0.5"/>',
    ]
    for i, d in enumerate(a["desc"]):
        lines.append(f'  {tline(cx, AY+63+13*i, d, 9, a["desc_fill"])}')
    return "\n".join(lines)


def pill_block(a, cx):
    bx = cx - AW // 2
    bot = AY + AH
    return "\n".join([
        f'  {line(cx, bot, cx, PILL_Y, stroke="#7090a0", sw=1, dash="3,2", opacity=0.8)}',
        f'  {rect(bx, PILL_Y, AW, PILL_H, a["pill_bg"], rx=6, filt="softShadow", opacity="0.92")}',
        f'  {tline(cx, PILL_Y+14, "ingests from", 7.5, a["pill_label"], italic=True)}',
        f'  {tline(cx, PILL_Y+27, a["ingest"][0], 8.5, a["pill_text"])}',
        f'  {tline(cx, PILL_Y+39, a["ingest"][1], 8.5, a["pill_text"])}',
    ])


def cross_agent_block():
    msg = ("↔  cross-agent signals  "
           "(consolation/desolation · wellness · financial runway · "
           "home accessibility · relationship health)")
    return "\n".join([
        f'  {tline(W//2, 380, msg, 10, "#8e7b5e", italic=True)}',
        f'  {hline(387, sw=0.5, dash="6,4")}',
    ])


def record_agent_block():
    # outer container + Layer 1 (disks) + Layer 2 (service bar)
    bot_y    = RA_Y + RA_H          # 578
    svc_bot  = bot_y                 # same bottom
    disk_bot = DISK_CY + DISK_BH    # 478
    cap_bot  = disk_bot + DRY       # 486

    parts = [
        # outer box
        f'  {rect(20, RA_Y, 1026, RA_H, "#c8d6e2", rx=10, stroke="#7890a4", sw=1.2, filt="shadow")}',
        # Layer 1 bg
        f'  {rect(20, RA_Y, 1026, 100, "#c8d6e2", rx=10)}',
        f'  {rect(20, RA_Y+50, 1026, 50, "#c8d6e2")}',
        # accent bar
        f'  {rect(20, RA_Y, 1026, 4, "#5878a0", rx=2)}',
        # header label
        f'  {tline(W//2, RA_Y+20, "🗄 RecordAgent", 12, "#1c3048", bold=True, spacing="0.5")}',
        # layer divider
        f'  {hline(SVC_Y, x1=20, x2=1046, stroke="#5878a0", sw=1.2)}',
        # Layer 2 dark service bar (rounded bottom corners via path)
        f'  <path d="M 20,{SVC_Y} H 1046 V {bot_y-10} a 10,10 0 0 1 -10,10 H 30 a 10,10 0 0 1 -10,-10 Z" fill="#12202c"/>',
    ]

    # 6 data disks
    for a, cx in zip(AGENTS, CXS):
        bx = cx - DRX
        parts += [
            f'  <!-- disk: {a["name"]} -->',
            f'  {rect(bx, DISK_CY, DRX*2, DISK_BH, f"url(#{a["grad"]})")}',
            f'  <ellipse cx="{cx}" cy="{disk_bot}" rx="{DRX}" ry="{DRY}" fill="{a["disk_bot_cap"]}"/>',
            f'  <ellipse cx="{cx}" cy="{DISK_CY}" rx="{DRX}" ry="{DRY}" fill="{a["disk_top_cap"]}"/>',
            f'  {tline(cx, DISK_CY+5,  a["disk_label"],    8,   a["disk_label_fill"], bold=True)}',
            f'  {tline(cx, DISK_CY+18, a["disk_rows"][0],  7.5, a["disk_row_fill"])}',
            f'  {tline(cx, DISK_CY+30, a["disk_rows"][1],  7.5, a["disk_row_fill"])}',
        ]

    # service-bar text
    parts += [
        f'  {tline(W//2, SVC_Y+21, "Common Records Service", 13, "#b8d0e0", bold=True)}',
        f'  {tline(W//2, SVC_Y+38, "life.core.records  ·  git-as-master  ·  auto_push=true  ·  lifeTracker-data (private repo)", 10.5, "#8ab0c8")}',
        f'  {tline(W//2, SVC_Y+54, "Read · Write · Append · Register Document · Get Action Items  —  no agent touches the filesystem directly", 9.5, "#6890a8", italic=True)}',
    ]
    return "\n".join(parts)


def comm_agent_block():
    cx = W // 2
    return "\n".join([
        f'  {line(cx, RA_Y+RA_H, cx, COMM_A_Y, dash="4,3")}',
        f'  {rect(200, COMM_A_Y, 700, COMM_A_H, "url(#commGrad)", rx=8, filt="softShadow")}',
        f'  {rect(200, COMM_A_Y, 700, 4, "#a0c088", rx=2)}',
        f'  {tline(cx, COMM_A_Y+24, "📡 Communication Agent", 13, "#f0f8ee", bold=True)}',
        f'  {tline(cx, COMM_A_Y+42, "Twilio  ·  Flask  ·  CrewAI  ·  LangGraph  ·  auth  ·  LLM routing", 10.5, "#c8e0b8")}',
    ])


CHANNELS = [
    dict(cx=200, fill="#4a4030", accent="#c8a870", icon="📱",
         title="Voice  ·  iPhone/laptop",  title_fill="#f5e8c8",
         sub=["speech-to-speech", "on-device LLM"], sub_fill="#c0a870"),
    dict(cx=550, fill="#303a4a", accent="#90a8c8", icon="🌐",
         title="Web  ·  Mobile",            title_fill="#d8e8f8",
         sub=["Flask UI (pyTrackers)", "Jinja2 blueprints"], sub_fill="#a8c8e0"),
    dict(cx=900, fill="#2a3a2a", accent="#88b888", icon="🔔",
         title="Notifications",             title_fill="#d8f0d8",
         sub=["Twilio SMS  ·  alerts", "monthly check-in cadence"], sub_fill="#a8d8a8"),
]


def channels_block():
    COMM_A_BOT = COMM_A_Y + COMM_A_H   # 658
    HORIZ_Y    = COMM_A_BOT + 18       # 676
    parts = [
        f'  {line(W//2, COMM_A_BOT, W//2, HORIZ_Y, dash="4,3")}',
        f'  {line(CHANNELS[0]["cx"], HORIZ_Y, CHANNELS[-1]["cx"], HORIZ_Y)}',
    ]
    for ch in CHANNELS:
        cx, bx = ch["cx"], ch["cx"] - 100
        parts += [
            f'  {line(cx, HORIZ_Y, cx, CHAN_Y)}',
            f'  {rect(bx, CHAN_Y, 200, CHAN_H, ch["fill"], rx=7, filt="softShadow")}',
            f'  {rect(bx, CHAN_Y, 200, 3, ch["accent"], rx=1.5)}',
            f'  {tline(cx, CHAN_Y+22, ch["icon"]+" "+ch["title"], 12, ch["title_fill"], bold=True)}',
            f'  {tline(cx, CHAN_Y+39, ch["sub"][0], 9.5, ch["sub_fill"])}',
            f'  {tline(cx, CHAN_Y+53, ch["sub"][1], 9.5, ch["sub_fill"])}',
        ]
    return "\n".join(parts)


REPOS = [
    # (label, x, width) — 5 pills, w=204, gap=10, margins=20 each side → right edge=1080
    ("lifeTracker-data  (JSON records)", 20,  204),
    ("lifeTracker  (code · docs)",       234, 204),
    ("userID@GitHub",                    448, 204),
    ("SSH alias: github.com-fxr",        662, 204),
    ("id_#######_abc",                   876, 204),
]


def repos_block():
    sep_y  = FOOT_SEP - 68   # 782
    lbl_y  = sep_y + 16      # 798
    pill_y = lbl_y + 9       # 807  (pill top)
    parts  = [
        f'  {hline(sep_y, sw=0.5, dash="6,4")}',
        f'  {tline(W//2, lbl_y+1, "Data Repositories  ·  Private Git  ·  All records local / on-premises", 10, "#8e7b5e", italic=True)}',
    ]
    for label, rx, rw in REPOS:
        cx = rx + rw // 2
        parts += [
            f'  {rect(rx, pill_y, rw, 30, "#2c3e50", rx=15, opacity="0.85")}',
            f'  {tline(cx, pill_y+19, label, 9.5, "#c8d8e8")}',
        ]
    return "\n".join(parts)


def footer_block():
    ver = "v1.6"
    return "\n".join([
        f'  {hline(FOOT_SEP, sw=0.5)}',
        f'  {tline(W//2, FOOT_SEP+18, f"lifeTracker  ·  lifeTrackers ecosystem  ·  My Name  ·  June 2026  ·  {ver}", 9, "#a09080")}',
        f'  {tline(W//2, FOOT_SEP+34, chr(34)+"Your wisest counselor, always available — chief of staff and trusted friend."+chr(34), 9, "#b8a888", italic=True)}',
    ])


# ── assemble ───────────────────────────────────────────────────────────────────
def build_svg():
    parts = [
        f'<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg"',
        f'     font-family="Georgia, \'Times New Roman\', serif">',
        "",
        defs_block(),
        "",
        f'  {rect(0, 0, W, H, "url(#bgGrad)")}',
        "",
        "  <!-- ══ TITLE ══════════════════════════════════════════════════ -->",
        title_block(),
        "",
        "  <!-- ══ PERSONAL ASSISTANT ════════════════════════════════════ -->",
        pa_block(),
        pa_connectors(),
        "",
        "  <!-- ══ 6 DISCIPLINE AGENTS ══════════════════════════════════ -->",
    ]

    for a, cx in zip(AGENTS, CXS):
        parts.append(f"  <!-- {a['name']} -->")
        parts.append(agent_block(a, cx))

    parts += [
        "",
        "  <!-- ══ INGESTION PILLS ═══════════════════════════════════════ -->",
    ]
    for a, cx in zip(AGENTS, CXS):
        parts.append(pill_block(a, cx))

    parts += [
        "",
        "  <!-- ══ CROSS-AGENT SIGNALS ══════════════════════════════════ -->",
        cross_agent_block(),
        "",
        "  <!-- ══ RECORD AGENT ════════════════════════════════════════ -->",
        record_agent_block(),
        "",
        "  <!-- ══ COMMUNICATION AGENT ══════════════════════════════════ -->",
        comm_agent_block(),
        "",
        "  <!-- ══ COMMUNICATION CHANNELS ═══════════════════════════════ -->",
        channels_block(),
        "",
        "  <!-- ══ REPOS + FOOTER ════════════════════════════════════════ -->",
        repos_block(),
        footer_block(),
        "",
        "</svg>",
    ]
    return "\n".join(parts)


if __name__ == "__main__":
    svg = build_svg()
    OUT.write_text(svg, encoding="utf-8")
    print(f"wrote {OUT}  ({len(svg):,} bytes)")
