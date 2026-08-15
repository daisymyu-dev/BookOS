import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ReleaseLayoutTest(unittest.TestCase):
    def test_documented_paths_exist(self):
        expected = (
            ".gitignore",
            "bookos/SKILL.md",
            "bookos/agents/openai.yaml",
            "bookos/references/bookos-schema.md",
            "books/sample-book.md",
            "templates/book.md",
            "tests/test_bookos.py",
        )

        missing = [path for path in expected if not (ROOT / path).is_file()]

        self.assertEqual([], missing, f"Missing published files: {missing}")

    def test_accidentally_flattened_paths_are_absent(self):
        flattened = (
            "download",
            "SKILL.md",
            "openai.yaml",
            "bookos-schema.md",
            "sample-book.md",
            "book.md",
            "test_bookos.py",
        )

        present = [path for path in flattened if (ROOT / path).exists()]

        self.assertEqual([], present, f"Flattened files still present: {present}")

    def test_private_paths_have_ignore_rules(self):
        rules = {
            line.strip()
            for line in (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        }

        expected = {".env", "books/*.md", "!books/sample-book.md", "outputs/"}

        self.assertTrue(expected.issubset(rules), f"Missing ignore rules: {expected - rules}")


if __name__ == "__main__":
    unittest.main()
