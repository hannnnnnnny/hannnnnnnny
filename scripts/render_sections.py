from __future__ import annotations

from pathlib import Path

if __package__:
    from .visual_tokens import (
        BORDER, CORAL, MINT, MUTED, SURFACE, TEXT, VIOLET,
        pill, svg_document, text,
    )
else:
    from visual_tokens import (
        BORDER, CORAL, MINT, MUTED, SURFACE, TEXT, VIOLET,
        pill, svg_document, text,
    )

OUTPUTS = (
    "identity.svg",
    "project-kiwicue.svg",
    "project-pansub.svg",
    "project-till-tally.svg",
    "stack.svg",
    "contact.svg",
)

PROJECTS = (
    ("project-kiwicue.svg", "01 / 03", "KiwiCue",
     "Bilingual Auckland event discovery with smart reminders.",
     "DISCOVERY · AUTOMATION · TYPESCRIPT", ("EVENT", "MATCH", "REMIND"), MINT),
    ("project-pansub.svg", "02 / 03", "PanSub",
     "Real-time AI Chinese subtitles for lecture recordings.",
     "AI · ACCESSIBILITY · JAVASCRIPT", ("AUDIO", "AI", "SUBTITLE"), VIOLET),
    ("project-till-tally.svg", "03 / 03", "Till Tally",
     "Retail analytics that turns sales data into useful decisions.",
     "DATA · INTELLIGENCE · TYPESCRIPT", ("SALES", "SIGNAL", "DECIDE"), CORAL),
)


def identity_svg() -> str:
    body = (
        f'<line x1="330" y1="1" x2="330" y2="188" stroke="{BORDER}"/>'
        + text(42, 48, "PROFILE / 001", 13, MUTED, 600, "Consolas,monospace")
        + text(42, 101, "Yi Han.", 43, TEXT, 800)
        + text(42, 135, "FULL-STACK × AI", 14, MINT, 600, "Consolas,monospace")
        + text(372, 67, "I design and build AI-assisted products that turn repetitive", 21)
        + text(372, 99, "workflows into reliable systems people can actually use.", 21)
        + pill(372, 126, 120, "PORTFOLIO ↗", MINT)
        + pill(506, 126, 112, "LINKEDIN ↗", TEXT)
        + pill(632, 126, 91, "EMAIL ↗", TEXT)
    )
    return svg_document("Yi Han profile", "Full-stack and AI product builder.", 190, body)


def system_diagram(labels: tuple[str, str, str], accent: str) -> str:
    parts = [f'<line x1="957" y1="84" x2="1195" y2="84" stroke="{BORDER}"/>']
    for index, label in enumerate(labels):
        x = 900 + index * 120
        color = accent if index == 2 else BORDER
        label_color = accent if index == 2 else MUTED
        parts.append(
            f'<rect x="{x}" y="60" width="96" height="48" rx="10" '
            f'fill="{SURFACE}" stroke="{color}"/>'
        )
        parts.append(text(x + 48, 88, label, 11, label_color, 600,
                          "Consolas,monospace", "middle"))
    return "".join(parts)


def project_svg(
    project: tuple[str, str, str, str, str, tuple[str, str, str], str],
) -> str:
    _, number, name, description, metadata, labels, accent = project
    body = (
        f'<line x1="112" y1="1" x2="112" y2="166" stroke="{BORDER}"/>'
        f'<line x1="860" y1="1" x2="860" y2="166" stroke="{BORDER}"/>'
        + text(56, 91, number, 13, MUTED, 600, "Consolas,monospace", "middle")
        + text(153, 61, name + " ↗", 27, TEXT, 750)
        + text(153, 94, description, 17, MUTED, 400)
        + text(153, 128, metadata, 12, accent, 600, "Consolas,monospace")
        + system_diagram(labels, accent)
    )
    return svg_document(name, description, 168, body, accent)


def stack_svg() -> str:
    names = ("TypeScript", "JavaScript", "Java", "Spring Boot",
             "Vue", "MySQL", "AI APIs", "Automation")
    parts = [
        text(38, 48, "BUILDING WITH", 12, MUTED, 600, "Consolas,monospace"),
        text(38, 85, "Focused tools.", 26, TEXT, 750),
        f'<line x1="285" y1="1" x2="285" y2="126" stroke="{BORDER}"/>',
    ]
    x = 328
    for index, name in enumerate(names):
        width = 50 + len(name) * 7
        parts.append(pill(x, 46, width, name, MINT if index % 3 == 0 else TEXT))
        x += width + 10
    return svg_document("Technology stack", ", ".join(names), 128, "".join(parts))


def contact_svg() -> str:
    body = (
        text(38, 55, "Have an idea worth automating?", 24, TEXT, 750)
        + text(38, 87, "BUILDING FROM AUCKLAND, NEW ZEALAND",
               12, MUTED, 600, "Consolas,monospace")
        + f'<rect x="1080" y="37" width="153" height="52" rx="26" fill="{MINT}"/>'
        + text(1156, 69, "LET'S TALK ↗", 14, "#08100D", 800,
               "Consolas,monospace", "middle")
    )
    return svg_document(
        "Contact Yi Han",
        "Have an idea worth automating? Contact Yi Han.",
        126,
        body,
    )


def render_sections(output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    documents = {
        "identity.svg": identity_svg(),
        "stack.svg": stack_svg(),
        "contact.svg": contact_svg(),
    }
    documents.update({project[0]: project_svg(project) for project in PROJECTS})
    paths = []
    for name in OUTPUTS:
        path = output_dir / name
        path.write_text(documents[name], encoding="utf-8")
        paths.append(path)
    return paths


if __name__ == "__main__":
    rendered = render_sections(Path("assets"))
    print(f"Rendered assets: {', '.join(path.name for path in rendered)}")
