"""Generate the profile's deterministic, portfolio-themed SVG artwork.

No external dependencies. Run from the root of the README package:
    python3 scripts/build_artwork.py
"""

from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
INK = "#161616"
CREAM = "#F7F5EE"
YELLOW = "#FACC00"
MUTED = "#66645E"
FONT = "Space Grotesk, Arial, DejaVu Sans, sans-serif"


def text(x, y, value, size=28, weight=600, color=INK, extra=""):
    return (f'<text x="{x}" y="{y}" fill="{color}" font-family="{FONT}" '
            f'font-size="{size}" font-weight="{weight}" {extra}>{escape(value)}</text>')


def svg_header(width, height, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" role="img" aria-label="{escape(title)}">'
            f'<title>{escape(title)}</title>')


def frame(width, height, fill=CREAM):
    return (f'<rect width="{width}" height="{height}" fill="{fill}"/>'
            f'<rect x="2" y="2" width="{width-4}" height="{height-4}" fill="none" '
            f'stroke="{INK}" stroke-width="3"/>')


def project_motif(slug):
    # All coordinates are local to the 255x210 right-hand panel.
    if slug == "foreman":
        return f'''
        <rect x="48" y="28" width="148" height="112" fill="{CREAM}" stroke="{INK}" stroke-width="3"/>
        <path d="M48 28L122 89L196 28" fill="none" stroke="{INK}" stroke-width="3"/>
        <rect x="66" y="68" width="148" height="112" fill="{CREAM}" stroke="{INK}" stroke-width="3"/>
        <path d="M66 68L140 129L214 68" fill="none" stroke="{INK}" stroke-width="3"/>
        <rect x="158" y="11" width="60" height="60" fill="{YELLOW}" stroke="{INK}" stroke-width="3"/>
        <path d="M187 24V56M171 40H203" stroke="{INK}" stroke-width="3"/>
        '''
    if slug == "ridley":
        return f'''
        <rect x="35" y="15" width="177" height="150" fill="{CREAM}" stroke="{INK}" stroke-width="3"/>
        <path d="M65 53H182M65 80H168M65 107H151" stroke="{INK}" stroke-width="4"/>
        <path d="M68 165L57 184L106 165" fill="{CREAM}" stroke="{INK}" stroke-width="3"/>
        <rect x="151" y="122" width="79" height="67" fill="{YELLOW}" stroke="{INK}" stroke-width="3"/>
        <path d="M167 150H214M167 165H200" stroke="{INK}" stroke-width="3"/>
        '''
    if slug == "sentrax":
        return f'''
        <path d="M130 10L213 44V111C213 159 180 191 130 207C80 191 47 159 47 111V44Z" fill="{CREAM}" stroke="{INK}" stroke-width="3"/>
        <path d="M130 38L184 60V111C184 141 164 163 130 178C96 163 76 141 76 111V60Z" fill="none" stroke="{INK}" stroke-width="2"/>
        <circle cx="130" cy="109" r="36" fill="{YELLOW}" stroke="{INK}" stroke-width="3"/>
        <path d="M130 88V130M109 109H151" stroke="{INK}" stroke-width="3"/>
        <circle cx="130" cy="38" r="5" fill="{INK}"/><circle cx="184" cy="111" r="5" fill="{INK}"/>
        <circle cx="130" cy="178" r="5" fill="{INK}"/><circle cx="76" cy="111" r="5" fill="{INK}"/>
        '''
    return f'''
        <path d="M47 155L104 91L173 135L210 44" stroke="{INK}" stroke-width="3" fill="none"/>
        <path d="M104 91L133 36L210 44" stroke="{INK}" stroke-width="2" fill="none" stroke-dasharray="7 8"/>
        <rect x="24" y="132" width="47" height="47" fill="{CREAM}" stroke="{INK}" stroke-width="3"/>
        <rect x="81" y="68" width="47" height="47" fill="{YELLOW}" stroke="{INK}" stroke-width="3"/>
        <rect x="152" y="113" width="43" height="43" fill="{CREAM}" stroke="{INK}" stroke-width="3"/>
        <circle cx="210" cy="44" r="24" fill="{CREAM}" stroke="{INK}" stroke-width="3"/>
        <circle cx="210" cy="44" r="6" fill="{INK}"/>
        '''


PROJECTS = [
    ("foreman", "01", "CLIENT PROTOTYPE", "FOREMAN", 85,
     "Inbox triage with human approval.", "NEXT.JS / N8N / SUPABASE"),
    ("ridley", "02", "CLIENT WORK", "RIDLEY ACADEMY", 65,
     "Support emails with a human fallback.", "N8N / RAG / PINECONE"),
    ("sentrax", "03", "SECURITY TOOL", "SENTRAX AI", 83,
     "Security findings backed by proof.", "PYTHON / PYDANTIC / PYTEST"),
    ("pratyaksh", "04", "HACKATHON PROJECT", "PRATYAKSH", 76,
     "Trace a leak through incomplete logs.", "FASTAPI / REACT / TYPESCRIPT"),
]


def project_card(data):
    slug, num, category, name, name_size, tagline, stack = data
    parts = [svg_header(1040, 255, f"{name}: {tagline}"), frame(1040, 255)]
    parts += [f'<rect x="2" y="2" width="12" height="251" fill="{YELLOW}"/>',
              f'<line x1="748" y1="19" x2="748" y2="236" stroke="{INK}" stroke-width="2"/>',
              text(42, 48, f"{num} / {category}", 20, 700, MUTED, 'letter-spacing="2"'),
              text(40, 137, name, name_size, 800, INK, 'letter-spacing="-2"'),
              text(42, 185, tagline, 31, 500),
              f'<line x1="42" y1="205" x2="704" y2="205" stroke="{INK}" stroke-width="2"/>',
              text(42, 234, stack, 17, 700, MUTED, 'letter-spacing="1"'),
              '<g transform="translate(770,18)">', project_motif(slug), '</g>',
              '</svg>']
    (ASSETS / "projects" / f"{slug}.svg").write_text("\n".join(parts), encoding="utf-8")


def toolbox():
    groups = [
        ("LANGUAGES", ["Python", "JavaScript", "TypeScript"]),
        ("AI & AUTOMATION", ["n8n", "OpenAI API", "RAG", "LangChain"]),
        ("FRONTEND", ["React", "Next.js", "Tailwind CSS"]),
        ("BACKEND / DATA", ["FastAPI", "Node.js", "PostgreSQL", "Supabase", "SQLite"]),
        ("TOOLS / CREATIVE", ["Git", "Linux", "Unity", "Blender"]),
    ]
    w, h = 1040, 497
    parts = [svg_header(w, h, "The tools Tanish builds with"), frame(w, h)]
    parts += [text(34, 46, "WHAT I BUILD WITH", 30, 800, INK, 'letter-spacing="1"'),
              f'<rect x="944" y="17" width="70" height="35" fill="{YELLOW}" stroke="{INK}" stroke-width="2"/>',
              text(962, 42, "TM", 20, 800)]
    for index, (label, names) in enumerate(groups):
        y = 72 + index * 81
        parts.append(f'<line x1="26" y1="{y}" x2="1015" y2="{y}" stroke="{INK}" stroke-width="2"/>')
        parts.append(text(34, y + 48, label, 23, 800))
        x = 331
        for name in names:
            width = max(89, int(26 + len(name) * 12.3))
            parts.append(f'<rect x="{x}" y="{y+14}" width="{width}" height="48" fill="{CREAM}" stroke="{INK}" stroke-width="2"/>')
            parts.append(text(x + 14, y + 45, name, 21, 650))
            x += width + 11
    parts.append('</svg>')
    (ASSETS / "toolbox.svg").write_text("\n".join(parts), encoding="utf-8")


def in_the_works():
    blocks = [
        ("NOW", "AI SERVICES AGENCY", "Starting small. Building useful tools."),
        ("NEXT", "BUILD IN PUBLIC", "Sharing what I learn and ship."),
        ("SOMEDAY", "STORY-DRIVEN GAMES", "I want to build my own worlds."),
    ]
    parts = [svg_header(1040, 221, "What Tanish is working on now and next"), frame(1040, 221)]
    for i, (stamp, title, note) in enumerate(blocks):
        x = 22 + i * 342
        if i:
            parts.append(f'<line x1="{x-11}" y1="18" x2="{x-11}" y2="202" stroke="{INK}" stroke-width="2"/>')
        parts += [f'<rect x="{x+5}" y="29" width="14" height="14" fill="{YELLOW}" stroke="{INK}" stroke-width="2"/>',
                  text(x+31, 43, stamp, 18, 800, MUTED, 'letter-spacing="2"'),
                  text(x+5, 105, title, 25 if i != 2 else 24, 800),
                  f'<path d="M{x+5} 128H{x+301}" stroke="{INK}" stroke-width="2"/>',
                  text(x+5, 165, note, 18, 500)]
    parts.append('</svg>')
    (ASSETS / "now.svg").write_text("\n".join(parts), encoding="utf-8")


def contact():
    parts = [svg_header(1040, 207, "Have something you want to build? Get in touch with Tanish"), frame(1040, 207, YELLOW),
             text(38, 58, "SOMETHING ON YOUR MIND?", 22, 800, INK, 'letter-spacing="2"'),
             text(34, 139, "LET'S BUILD IT.", 90, 800, INK, 'letter-spacing="-3"'),
             f'<circle cx="944" cy="101" r="57" fill="{CREAM}" stroke="{INK}" stroke-width="3"/>',
             f'<path d="M917 128L971 74M937 74H971V108" stroke="{INK}" stroke-width="5" fill="none"/>',
             '</svg>']
    (ASSETS / "contact.svg").write_text("\n".join(parts), encoding="utf-8")


def activity_placeholder():
    parts = [svg_header(1040, 320, "Contribution activity graph awaiting its first refresh"), frame(1040, 320),
             text(33, 46, "05 / GITHUB ACTIVITY", 28, 800),
             text(1007, 45, "UPDATES WEEKLY", 17, 750, MUTED, 'text-anchor="end" letter-spacing="1"')]
    for x in range(52):
        for y in range(7):
            px, py = 38 + x * 18, 77 + y * 23
            parts.append(f'<rect x="{px}" y="{py}" width="13" height="13" rx="2" fill="#E1DDD2"/>')
    parts += [text(36, 271, "The graph will fill with real contributions after the first GitHub Action run.", 19, 550, MUTED),
              text(36, 302, "VISIBLE GITHUB CONTRIBUTIONS", 15, 700, INK, 'letter-spacing="2"'), '</svg>']
    (ASSETS / "activity.svg").write_text("\n".join(parts), encoding="utf-8")


def main():
    (ASSETS / "projects").mkdir(parents=True, exist_ok=True)
    for project in PROJECTS:
        project_card(project)
    toolbox()
    in_the_works()
    contact()
    if not (ASSETS / "activity.svg").exists():
        activity_placeholder()


if __name__ == "__main__":
    main()
