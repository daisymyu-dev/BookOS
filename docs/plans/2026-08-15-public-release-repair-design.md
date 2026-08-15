# BookOS Public Release Repair Design

## Goal

Make the public repository match its documentation, protect personal reading data from accidental commits, and ensure a fresh clone can install the AI skill and run the local companion tool.

## Scope

- Restore the documented directory layout without changing BookOS behavior.
- Rename the misplaced ignore-rules file to `.gitignore`.
- Place the sample note, note template, tests, skill metadata, and reference material at the paths used by the code and README.
- Add release-structure regression tests and correct the documented verification commands.
- Keep the MIT license and existing public API unchanged.

## Target layout

```text
BookOS/
├── .gitignore
├── LICENSE
├── README.md
├── bookos.py
├── bookos/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── references/bookos-schema.md
├── books/sample-book.md
├── templates/book.md
└── tests/test_bookos.py
```

## Behavior and data flow

The CLI continues to read Markdown notes from `books/`, use `templates/book.md` for new notes, and write generated artifacts to `outputs/`. The installable AI skill is the self-contained `bookos/` directory. Private notes and generated artifacts remain local through `.gitignore`.

## Error handling

Existing CLI error behavior remains unchanged. Regression tests verify that every required packaged path exists, private paths are ignored, and the documented sample commands operate successfully from a fresh checkout.

## Verification

- Validate the skill with the bundled `quick_validate.py` helper.
- Run `python -m unittest discover -s tests -v`.
- Run the documented `all`, `new`, and `xhs` commands in an isolated temporary copy.
- Check ignored paths with `git check-ignore`.
- Confirm the committed tree contains no generated or private artifacts.
