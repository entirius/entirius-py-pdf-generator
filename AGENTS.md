# AGENTS.md

LaTeX-based PDF generator — distribution `entirius-py-pdf-generator`, import `pdf_generator`.

## Commands

| Command | Meaning |
|---|---|
| `make install` | sync dependencies (uv, incl. extras) |
| `make check` | lint + format-check (ruff) |
| `make fix` | auto-fix lint + format |
| `make test` | test suite (pytest) |

## Conventions

- English only: code, docs, commits, branches, PRs.
- MPL-2.0: every non-trivial source file carries the license header (pre-commit inserts it).
- Toolchain: uv + ruff + hatchling + pytest; all config in `pyproject.toml`; `uv.lock` committed.
- Git flow: `master` (production) + `develop` (integration); changes land via PR; semver tag on `master`.
- Never rename the import package `pdf_generator` — it is a public API contract.
- Default: do not commit — git is the user's call.
- No AI attribution in commits or PR descriptions.

## Architecture

`pdf_generator/worker/latex.py`: `PDFGenerator` builds a LaTeX document from a JSON description
(`document_contents`: headings, text, images, lines) with `pylatex`, then `generate_pdf(compiler=...)`
shells out to a LaTeX engine (`xelatex`/`pdflatex`). Runtime deps: `pylatex`, `PyPDF2`.
The generation test is skipped where the LaTeX engine is absent (CI).
