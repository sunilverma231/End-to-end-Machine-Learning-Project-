<!-- .github/copilot-instructions.md -->
# Guidance for AI coding agents working on this repository

This project is a small "end-to-end" ML packaging example. The instructions below are concise, actionable, and specific to this codebase so you can be productive immediately.

1) Big-picture layout
- **Source package**: code lives under `src/` (package name: `mlproject`). There are currently no modules beyond an empty `src/__init__.py`.
- **Top-level helpers**: `setup.py` contains packaging logic. `tempCodeRunnerFile.py` is a duplicate copy of `setup.py` and appears to be an accidental extra — treat it as non-authoritative unless the PR explicitly intends to replace or remove it.
- **Virtualenv**: a local virtual environment exists at `myenv/` (use `source myenv/bin/activate`).

2) Build / install / run workflows (explicit commands)
- Activate the virtualenv:
  - `source myenv/bin/activate`
- Install dependencies (the repository uses an editable install in `requirements.txt`):
  - `pip install -r requirements.txt`
  - or to only install this package: `python -m pip install -e .`
- Note: `requirements.txt` contains the line `-e .`, so `pip install -r requirements.txt` will attempt an editable install of the package.

3) Project-specific patterns & pitfalls to notice
- `setup.py` reads `requirements.txt` but contains a small bug: it uses `file_obj` instead of the read `requirements` list in the list comprehension. Avoid making automated fixes that change behavior without running the local install first.
  - File to inspect: `setup.py` (and `tempCodeRunnerFile.py` which mirrors it).
- There are no tests, CI, or linting configuration files in the repository. Changes that affect packaging or runtime should be validated locally (install & basic import) and communicated in the PR description.

4) When modifying or adding code
- Prefer minimal, focused changes. For packaging or dependency changes, verify by:
  - activating `myenv`, running `pip install -e .`, then importing the package in a Python REPL: `python -c "import mlproject; print(mlproject)"`
- If you change `setup.py`, also search for `tempCodeRunnerFile.py` and update or remove it as part of the same PR (its presence indicates copy-paste duplication).

5) Files to inspect first for context
- `setup.py` — packaging and dependency parsing (source of truth for install_requires)
- `requirements.txt` — declared runtime deps (contains `-e .`)
- `tempCodeRunnerFile.py` — duplicate of `setup.py` (verify intent before editing)
- `src/` — package sources
- `README.md` — currently minimal; treat it as low-trust for technical details

6) PR / commit guidance for agents
- Keep commits atomic and focused: "Fix requirements parsing in setup.py" or "Add X module to `src/`".
- In PR description include how you validated the change locally (commands used and brief output). Example:
  - `source myenv/bin/activate && python -m pip install -e . && python -c "import mlproject; print('import ok')"`
- If you make non-trivial changes to packaging, include instructions for reviewers to reproduce the install locally.

7) Things NOT to do automatically
- Do not add tests, CI, or significant new project structure without prior approval — the repository currently lacks those conventions and the maintainer may prefer to keep it minimal.
- Do not remove `myenv/` or attempt to manage the user's local virtualenv; reference activation commands instead.

If anything above is unclear or you'd like me to expand a section (for example, add example PR templates or enable a minimal CI test), tell me which area to elaborate and I'll update this file.
