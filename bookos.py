from __future__ import annotations

import argparse
import html
import json
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parent
BOOKS_DIR = ROOT / "books"
TEMPLATE_PATH = ROOT / "templates" / "book.md"
OUTPUTS_DIR = ROOT / "outputs"


@dataclass
class BookNote:
    path: Path
    title: str
    author: str = ""
    status: str = ""
    rating: str = ""
    tags: tuple[str, ...] = ()
    sections: dict[str, str] | None = None


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[\\/:*?\"<>|]+", "-", text)
    text = re.sub(r"\s+", "-", text)
    return text.strip("-") or "untitled"


def parse_list(value: str) -> tuple[str, ...]:
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        raw = value[1:-1]
        return tuple(item.strip().strip("'\"#") for item in raw.split(",") if item.strip())
    if value:
        return (value.strip().strip("'\"#"),)
    return ()


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.S)
    if not match:
        return {}, text
    meta: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip()
    return meta, text[match.end() :]


def parse_sections(body: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    matches = list(re.finditer(r"^##\s+(.+?)\s*$", body, re.M))
    for index, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        sections[title] = body[start:end].strip()
    return sections


def read_note(path: Path) -> BookNote:
    text = path.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(text)
    sections = parse_sections(body)
    title = meta.get("title") or path.stem
    return BookNote(
        path=path,
        title=title,
        author=meta.get("author", ""),
        status=meta.get("status", ""),
        rating=meta.get("rating", ""),
        tags=parse_list(meta.get("tags", "")),
        sections=sections,
    )


def iter_notes(books_dir: Path = BOOKS_DIR) -> Iterable[BookNote]:
    if not books_dir.exists():
        return []
    return sorted((read_note(path) for path in books_dir.glob("*.md")), key=lambda note: note.title.lower())


def create_note(title: str, author: str = "", force: bool = False, root: Path = ROOT) -> Path:
    books_dir = root / "books"
    template_path = root / "templates" / "book.md"
    books_dir.mkdir(parents=True, exist_ok=True)
    target = books_dir / f"{slugify(title)}.md"
    if target.exists() and not force:
        raise FileExistsError(f"{target} already exists. Use --force to overwrite.")
    template = template_path.read_text(encoding="utf-8")
    content = (
        template.replace("{{title}}", title)
        .replace("{{author}}", author)
        .replace("{{date}}", date.today().isoformat())
    )
    target.write_text(content, encoding="utf-8")
    return target


def build_index(books_dir: Path = BOOKS_DIR, outputs_dir: Path = OUTPUTS_DIR) -> Path:
    outputs_dir.mkdir(parents=True, exist_ok=True)
    notes = list(iter_notes(books_dir))
    lines = ["# BookOS Index", ""]
    lines.append("Generated from Markdown notes in `books/`.")
    lines.append("")
    lines.append("| Book | Author | Status | Rating | Tags |")
    lines.append("|---|---|---|---|---|")
    for note in notes:
        tags = ", ".join(f"`#{tag}`" for tag in note.tags)
        rel = note.path.relative_to(books_dir.parent).as_posix()
        lines.append(
            f"| [{note.title}](../{rel}) | {note.author} | {note.status} | {note.rating} | {tags} |"
        )
    lines.append("")
    lines.append("## Tag cloud")
    tag_counts: dict[str, int] = {}
    for note in notes:
        for tag in note.tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
    if tag_counts:
        for tag, count in sorted(tag_counts.items(), key=lambda item: (-item[1], item[0])):
            lines.append(f"- `#{tag}` × {count}")
    else:
        lines.append("- No tags yet.")
    target = outputs_dir / "index.md"
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return target


def build_graph(books_dir: Path = BOOKS_DIR, output_path: Path | None = None) -> Path:
    output_path = output_path or OUTPUTS_DIR / "graph.html"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    notes = list(iter_notes(books_dir))
    nodes: list[dict[str, str]] = []
    links: list[dict[str, str]] = []
    seen: set[str] = set()

    for note in notes:
        book_id = f"book:{note.title}"
        nodes.append({"id": book_id, "label": note.title, "type": "book"})
        seen.add(book_id)
        for tag in note.tags:
            tag_id = f"tag:{tag}"
            if tag_id not in seen:
                nodes.append({"id": tag_id, "label": f"#{tag}", "type": "tag"})
                seen.add(tag_id)
            links.append({"source": book_id, "target": tag_id})

        for section_name in ("核心观点", "我的反应", "行动清单"):
            content = (note.sections or {}).get(section_name, "")
            if content.strip():
                section_id = f"section:{note.title}:{section_name}"
                nodes.append({"id": section_id, "label": section_name, "type": "section"})
                links.append({"source": book_id, "target": section_id})

    payload = json.dumps({"nodes": nodes, "links": links}, ensure_ascii=False)
    doc = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>BookOS Knowledge Graph</title>
  <style>
    body {{ margin: 0; font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #0f172a; color: #e5e7eb; }}
    header {{ padding: 24px 28px 8px; }}
    h1 {{ margin: 0 0 8px; font-size: 28px; }}
    p {{ color: #94a3b8; }}
    #graph {{ width: 100vw; height: calc(100vh - 112px); display: block; }}
    .book {{ fill: #fb7185; }}
    .tag {{ fill: #38bdf8; }}
    .section {{ fill: #a78bfa; }}
    line {{ stroke: #475569; stroke-width: 1.4; }}
    text {{ fill: #e5e7eb; font-size: 12px; paint-order: stroke; stroke: #0f172a; stroke-width: 3px; }}
  </style>
</head>
<body>
  <header>
    <h1>BookOS Knowledge Graph</h1>
    <p>Books connect to tags and high-value note sections. Drag nodes to rearrange the map.</p>
  </header>
  <svg id="graph"></svg>
  <script>
    const data = {payload};
    const svg = document.getElementById("graph");
    const width = svg.clientWidth, height = svg.clientHeight;
    svg.setAttribute("viewBox", `0 0 ${{width}} ${{height}}`);
    const cx = width / 2, cy = height / 2;
    data.nodes.forEach((node, i) => {{
      const angle = (Math.PI * 2 * i) / Math.max(data.nodes.length, 1);
      const radius = node.type === "book" ? 80 : Math.min(width, height) * 0.34;
      node.x = cx + Math.cos(angle) * radius;
      node.y = cy + Math.sin(angle) * radius;
    }});
    const nodeById = Object.fromEntries(data.nodes.map(n => [n.id, n]));
    for (const link of data.links) {{
      const source = nodeById[link.source], target = nodeById[link.target];
      const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
      line.setAttribute("x1", source.x); line.setAttribute("y1", source.y);
      line.setAttribute("x2", target.x); line.setAttribute("y2", target.y);
      svg.appendChild(line);
    }}
    for (const node of data.nodes) {{
      const group = document.createElementNS("http://www.w3.org/2000/svg", "g");
      group.setAttribute("transform", `translate(${{node.x}}, ${{node.y}})`);
      const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      circle.setAttribute("r", node.type === "book" ? 18 : 12);
      circle.setAttribute("class", node.type);
      const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
      text.setAttribute("x", 18); text.setAttribute("y", 4);
      text.textContent = node.label;
      group.appendChild(circle); group.appendChild(text); svg.appendChild(group);
    }}
  </script>
</body>
</html>
"""
    output_path.write_text(doc, encoding="utf-8")
    return output_path


def find_note(title: str, books_dir: Path = BOOKS_DIR) -> BookNote:
    wanted = title.strip().lower()
    for note in iter_notes(books_dir):
        if note.title.lower() == wanted or note.path.stem.lower() == slugify(title):
            return note
    raise FileNotFoundError(f"No book note found for {title!r}")


def first_nonempty_line(text: str) -> str:
    for line in text.splitlines():
        clean = re.sub(r"^[-*>#\d. \[\]x]+", "", line).strip()
        if clean:
            return clean
    return ""


def generate_xhs(title: str, books_dir: Path = BOOKS_DIR, outputs_dir: Path = OUTPUTS_DIR) -> Path:
    note = find_note(title, books_dir)
    sections = note.sections or {}
    idea = first_nonempty_line(sections.get("核心观点", ""))
    reaction = first_nonempty_line(sections.get("我的反应", ""))
    quote = first_nonempty_line(sections.get("金句", ""))
    tags = " ".join(f"#{tag}" for tag in note.tags)
    lines = [
        f"# 小红书草稿｜《{note.title}》",
        "",
        f"## 标题备选",
        "",
        f"1. 读完《{note.title}》，我终于明白：{idea or '真正重要的是改变行动'}",
        f"2. 这本书最击中我的，不是知识点，而是这句话",
        f"3. 如果你也想把读书变成行动，先看这本",
        "",
        "## 正文",
        "",
        f"最近整理《{note.title}》，最打动我的一句是：{quote or reaction or idea}",
        "",
        f"它提醒我：{reaction or idea or '读书真正有价值的地方，是把别人的经验变成自己的判断。'}",
        "",
        "我会把这本书拆成三个层次：",
        "",
        f"1. 核心观点：{idea or '先抓住它到底改变了我哪个判断。'}",
        "2. 案例：不要只记结论，要记作者如何证明它。",
        "3. 行动：读完以后，我今天能做什么。",
        "",
        "## 结尾互动",
        "",
        "你最近有没有读到一句让你停下来的话？可以丢给我，我帮你整理进知识图谱。",
        "",
        f"## 标签",
        "",
        tags or "#读书 #个人知识库 #知识图谱",
    ]
    target_dir = outputs_dir / "xhs"
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / f"{slugify(note.title)}.md"
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="BookOS: Markdown book notes to index and graph.")
    sub = parser.add_subparsers(dest="command", required=True)

    new_parser = sub.add_parser("new", help="Create a new book note from the template.")
    new_parser.add_argument("title")
    new_parser.add_argument("--author", default="")
    new_parser.add_argument("--force", action="store_true")

    sub.add_parser("index", help="Generate outputs/index.md.")
    sub.add_parser("graph", help="Generate outputs/graph.html.")
    sub.add_parser("all", help="Generate index and graph.")

    xhs_parser = sub.add_parser("xhs", help="Generate a Xiaohongshu-style content draft.")
    xhs_parser.add_argument("title")

    args = parser.parse_args(argv)
    if args.command == "new":
        path = create_note(args.title, args.author, args.force)
        print(path)
    elif args.command == "index":
        print(build_index())
    elif args.command == "graph":
        print(build_graph())
    elif args.command == "all":
        print(build_index())
        print(build_graph())
    elif args.command == "xhs":
        print(generate_xhs(args.title))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
