# pdf-generator

LaTeX-based PDF generator — renders a PDF from a JSON document description
(headings, text, images, lines) via `pylatex` and a LaTeX engine.

## Installation

```shell
pip install entirius-py-pdf-generator
```

PDF generation requires a LaTeX engine (e.g. `xelatex`) on the system:

```shell
sudo apt install texlive-xetex
```

## Usage

```python
from pdf_generator.worker.latex import PDFGenerator

pdf = PDFGenerator(
    in_out_file="/tmp/report",
    json_data={"document_contents": [{"type": "h1", "content": "Hello"}]},
    document_variables={},
)
pdf.generate_pdf(compiler="xelatex")
```

## Development

```shell
make install     # sync dependencies (uv)
make check       # lint + format check (ruff)
make test        # test suite (pytest) — PDF test skipped where xelatex is absent
```

Development and agent instructions: [AGENTS.md](AGENTS.md).

## License

Mozilla Public License 2.0 — see [LICENSE](LICENSE).
