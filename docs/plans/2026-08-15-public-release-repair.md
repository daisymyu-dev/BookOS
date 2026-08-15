# BookOS Public Release Repair Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Make a fresh BookOS checkout private-by-default, installable as an AI skill, and runnable exactly as documented.

**Architecture:** Restore the repository layout already assumed by `bookos.py`, `test_bookos.py`, `SKILL.md`, and `README.md`. Add a small release-contract test before moving files, then validate the skill package and exercise every documented CLI path in an isolated copy.

**Tech Stack:** Python 3.10+, `unittest`, Git, Markdown, Codex skill validation scripts.

---

### Task 1: Add a failing release-contract test

**Files:**
- Create: `tests/test_release_layout.py`

**Step 1: Write the failing test**

Create tests that assert the documented skill, sample, template, test, and `.gitignore` paths exist; assert the accidentally flattened paths do not exist; and assert private notes, generated outputs, and `.env` are ignored by Git.

**Step 2: Run the test to verify it fails**

Run: `python -m unittest -v tests.test_release_layout`

Expected: FAIL because `.gitignore` and the documented directories do not yet exist.

### Task 2: Restore the published layout

**Files:**
- Rename: `download` to `.gitignore`
- Move: `SKILL.md` to `bookos/SKILL.md`
- Move: `openai.yaml` to `bookos/agents/openai.yaml`
- Move: `bookos-schema.md` to `bookos/references/bookos-schema.md`
- Move: `sample-book.md` to `books/sample-book.md`
- Move: `book.md` to `templates/book.md`
- Move: `test_bookos.py` to `tests/test_bookos.py`

**Step 1: Move files without changing their content**

Use `git mv` so history remains traceable.

**Step 2: Run the release-contract test**

Run: `python -m unittest -v tests.test_release_layout`

Expected: PASS.

**Step 3: Run the existing behavior test**

Run: `python -m unittest discover -s tests -v`

Expected: all tests PASS.

### Task 3: Align documentation with the verified release

**Files:**
- Modify: `README.md`

**Step 1: Add a clean-checkout verification section**

Document the working test command and a short privacy check using `git check-ignore`.

**Step 2: Run all tests again**

Run: `python -m unittest discover -s tests -v`

Expected: all tests PASS.

### Task 4: Validate installation and CLI workflows

**Files:**
- Validate: `bookos/`

**Step 1: Validate the AI skill package**

Run the Skill Creator `quick_validate.py` helper against `bookos/`.

Expected: validation succeeds.

**Step 2: Exercise commands in an isolated copy**

Run `bookos.py all`, `bookos.py new "Audit Book"`, and `bookos.py xhs "Sample Book"` outside the working tree.

Expected: every command exits zero and creates the documented files.

**Step 3: Verify privacy rules**

Run: `git check-ignore -v books/private-note.md outputs/index.md .env`

Expected: all three paths are matched by `.gitignore`.

### Task 5: Review and publish

**Files:**
- Review all intended changes.

**Step 1: Run final checks**

Run tests, skill validation, CLI smoke tests, `git diff --check`, and a high-confidence secret scan.

**Step 2: Commit**

Commit message: `fix: make public release installable and private by default`

**Step 3: Push and open a draft PR**

Push `agent/fix-public-release` and open a draft PR targeting `main` with the validation evidence.
