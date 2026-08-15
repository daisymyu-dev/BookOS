import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("bookos", ROOT / "bookos.py")
bookos = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules["bookos"] = bookos
SPEC.loader.exec_module(bookos)


class BookOSTest(unittest.TestCase):
    def test_build_index_graph_and_xhs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            books = root / "books"
            outputs = root / "outputs"
            books.mkdir()
            note = books / "sample.md"
            note.write_text(
                """---
title: Sample Book
author: Example Author
status: done
rating: 5
tags: [strategy, learning]
---

# Sample Book

## 核心观点

1. Reading should change action.

## 我的反应

- This is useful.

## 金句

> Knowledge becomes memory when it connects.

## 行动清单

- [ ] Try it today.
""",
                encoding="utf-8",
            )
            index = bookos.build_index(books, outputs)
            graph = bookos.build_graph(books, outputs / "graph.html")
            xhs = bookos.generate_xhs("Sample Book", books, outputs)

            self.assertTrue(index.exists())
            self.assertTrue(graph.exists())
            self.assertTrue(xhs.exists())
            self.assertIn("Sample Book", index.read_text(encoding="utf-8"))
            self.assertIn("strategy", graph.read_text(encoding="utf-8"))
            self.assertIn("小红书草稿", xhs.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
