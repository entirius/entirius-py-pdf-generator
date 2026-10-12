# entirius-py-pdf-generator

A LaTeX-based PDF generator for Python, part of Entirius, the open-source modular ecommerce platform. It renders a PDF
from a JSON document description (headings, text, tables, lists, images) with `pylatex` and a LaTeX engine.

[![PyPI](https://img.shields.io/pypi/v/entirius-py-pdf-generator.svg)](https://pypi.org/project/entirius-py-pdf-generator/)
[![Python](https://img.shields.io/pypi/pyversions/entirius-py-pdf-generator.svg)](https://pypi.org/project/entirius-py-pdf-generator/)
[![License: MPL-2.0](https://img.shields.io/badge/license-MPL--2.0-blue.svg)](https://github.com/entirius/entirius-py-pdf-generator/blob/develop/LICENSE)

## What it does

- Builds a document from a list of typed content blocks (`document_contents`): headings, text, sections, images,
  lines and page breaks.
- Renders tables (`tabular`, `tabularx`, `tabu`) and lists (`list_itemize`, `list_enumerate`, `list_description`).
- Renders math and graphs (`math`, `matrix_equation`, `alignat_math`, `graph`).
- Compiles with the LaTeX engine named in `generate_pdf(compiler=...)`.

## Installation

```shell
uv add entirius-py-pdf-generator
pip install entirius-py-pdf-generator
```

The import name is `pdf_generator`.

## Quick start

```python
from pdf_generator.worker.latex import PDFGenerator

pdf = PDFGenerator(
    in_out_file="/tmp/report",
    json_data={"document_contents": [{"type": "h1", "content": "Hello"}]},
    document_variables={},
)
pdf.generate_pdf(compiler="xelatex")
```

## Requirements

- Python 3.11 or newer.
- `pylatex` and `PyPDF2` (installed as dependencies).
- A LaTeX engine (for example `xelatex`) on the system: `sudo apt install texlive-xetex`.

## Documentation

- Entirius documentation: https://docs.entirius.com/
- Changelog: https://github.com/entirius/entirius-py-pdf-generator/blob/develop/CHANGELOG.md

## Part of Entirius

This library renders the PDF documents of the Entirius backend service (Volkanos) and its modules.

- Backend service: https://github.com/entirius/entirius-service-volkanos
- Docker harness: https://github.com/entirius/entirius-zeno
- Consumer module: https://github.com/entirius/entirius-django-returns

## Development

```shell
make install     # sync dependencies (uv)
make check       # lint + format check (ruff)
make test        # test suite (pytest); the PDF test is skipped where xelatex is absent
```

Development and agent instructions: https://github.com/entirius/entirius-py-pdf-generator/blob/develop/AGENTS.md

## License

Mozilla Public License 2.0 (MPL-2.0) — see https://github.com/entirius/entirius-py-pdf-generator/blob/develop/LICENSE.
