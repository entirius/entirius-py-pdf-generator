# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import shutil

import pytest

from pdf_generator.worker.latex import PDFGenerator

# PDF generation shells out to a LaTeX engine (xelatex); skip where it is not installed
# (e.g. CI) — the generation path is exercised locally by developers who have LaTeX.
pytestmark = pytest.mark.skipif(
    shutil.which("xelatex") is None,
    reason="xelatex (LaTeX) not installed",
)


def test_creating_pdf(tmp_path):
    out_file = tmp_path / "test"
    json_data = {
        "geometry_options": {"margin": "0.7in", "includeheadfoot": True},
        "document_info": {},
        "font": "Ubuntu Mono",
        "document_contents": [
            {"type": "top_line", "extra": {"width": "1pt", "color": "black"}, "position": "center"},
            {"type": "fill_line", "multiplier": 1},
            {"type": "h1", "content": "Sample document", "extra": {"numbering": False}, "position": "center"},
            {"type": "text", "data_variable": "text1", "position": "left"},
            {"type": "image", "data_variable": "image1", "extra": {"width": "3cm"}, "foot": "L"},
        ],
    }
    pdf_generator = PDFGenerator(
        in_out_file=str(out_file),
        json_data=json_data,
        document_variables={"text1": "Unicode sample ŚŁÓŻ łśćńżźćąę", "image1": ""},
    )
    pdf_generator.generate_pdf(compiler="xelatex")
