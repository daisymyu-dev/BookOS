# BookOS

Turn books into reusable knowledge systems: mental models, human insights, applications, action principles, review questions, and content ideas.

BookOS includes two related components:

1. **The BookOS AI Skill** in `bookos/` guides ChatGPT or Codex through rigorous book decomposition.
2. **The local companion tool** in `bookos.py` organizes Markdown notes, generates an index and knowledge graph, and converts a completed note into a Xiaohongshu-style draft.

The project is local-first. The companion tool uses only Python's standard library and sends no notes or usage data to an external service.

## Install the AI Skill

1. Download this repository as a ZIP and extract it.
2. Compress the inner `bookos/` folder as `bookos.zip`.
3. Upload `bookos.zip` to ChatGPT and ask: `Please install this BookOS Skill.`
4. After installation, start with:

```text
@bookos Deeply deconstruct The Psychology of Money. Focus on transferable models,
human behavior, business applications, action principles, and review questions.
```

For a source-grounded close reading, attach the book notes, excerpts, transcript, or other material you want analyzed.

## Use the BookOS Skill

### Deep decomposition

```text
@bookos Deeply deconstruct <book title>. Do not give me a generic summary.
Build a logic map, core models, human patterns, skeptical reading,
applications, action principles, insight cards, and review questions.
```

### Personal knowledge database

```text
@bookos Convert these reading notes into atomic insight cards that remain useful
outside the original book. Add mechanisms, boundaries, applications, and tags.
```

### Content conversion

```text
@bookos Turn the strongest insight from this completed analysis into a concise
Xiaohongshu post. Do not invent a personal story or quotation.
```

## Use the Local Companion Tool

Python 3.10 or newer is recommended. No third-party packages are required.

Generate the sample index and graph:

```bash
python bookos.py all
```

This scans `books/` and generates:

- `outputs/index.md` — searchable book index
- `outputs/graph.html` — interactive knowledge graph

Create a new book note:

```bash
python bookos.py new "The Example Book" --author "Example Author"
```

Generate a Xiaohongshu-style draft from one completed note:

```bash
python bookos.py xhs "Sample Book"
```

Run the tests:

```bash
python -m unittest discover -s tests
```

## Folder Structure

```text
BookOS-public/
  bookos/                # Installable AI Skill
    SKILL.md
    agents/openai.yaml
    references/
  books/                 # Markdown book notes
  templates/book.md      # Shared note template
  outputs/               # Generated locally; excluded from public commits
  tests/                 # Regression tests
  bookos.py              # Local CLI and graph builder
```

## Markdown Note Format

Each note starts with a small front-matter block:

```markdown
---
title: Sample Book
author: Example Author
status: reading
rating: 4
tags: [strategy, systems, decision-making]
---
```

The shared template keeps these sections together:

- 核心观点
- 案例
- 我的反应
- 金句
- 行动清单
- 相关主题标签

## Privacy

Book notes can contain sensitive personal reflections. By default, `.gitignore` keeps new files in `books/` and everything generated in `outputs/` out of public commits while retaining the anonymous sample note. Review ignored and staged files before publishing a fork.

## License

MIT
