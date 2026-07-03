# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from pylatex import (
    Axis,
    Center,
    Description,
    Document,
    Enumerate,
    Figure,
    FlushLeft,
    FlushRight,
    Foot,
    HFill,
    Itemize,
    LineBreak,
    LongTable,
    LongTabu,
    Math,
    MiniPage,
    NewLine,
    NewPage,
    Package,
    PageStyle,
    Plot,
    Section,
    StandAloneGraphic,
    SubFigure,
    Subsection,
    Subsubsection,
    Tabularx,
    TikZ,
)
from pylatex.base_classes import Command
from pylatex.package import Package
from pylatex.utils import bold


class PDFGenerator:
    def __init__(self, in_out_file, json_data, document_variables: dict = {}, language="en"):
        self.in_out_file = in_out_file
        self.json_data = json_data
        self.document_contents = json_data.get("document_contents", [])
        self.font = json_data.get("font", [])
        self.header = PageStyle("header")
        self.document_variables = document_variables
        document_info = json_data.pop("document_info", {})
        page_numbers = document_info.pop("page_numbers", False)

        geometry_options = json_data.pop("geometry_options", {"tmargin": "1cm", "lmargin": "10cm"})
        self.doc = Document(geometry_options=geometry_options, page_numbers=page_numbers)
        self.doc.preamble.append(Command("usepackage", "geometry"))
        self.doc.preamble.append(Command("title", in_out_file))
        if self.font:
            self.doc.preamble.append(Package("fontspec"))
            self.doc.preamble.append(Command("setmainfont", self.font))

    def choose_type(self, content_data, obj, data, extra, content_type, data_variable):
        match content_type:
            case "text":
                processing_data = data_variable if data_variable else data
                all_texts = processing_data.split("\n")
                for text in all_texts:
                    self.add_text(obj, text)
            case "math":
                self.add_math(obj, content_data["expression"])
            case "tabular":
                self.add_tabular(obj, data, extra, content_type, content_data)
            case "tabularx":
                self.add_tabular(obj, data, extra, content_type, content_data)
            case "tabu":
                self.add_tabular(obj, data, extra, content_type, content_data)
            case "long_tabel":
                self.add_tabular(obj, data, extra, content_type, content_data)
            case "matrix_equation":
                matrix = data["matrix_variable"]
                vector = data["vector_variable"]
                result = data["result_variable"]
                self.add_matrix_equation(obj, matrix, vector, result)
            case "alignat_math":
                self.add_alignat_math(obj, content_data["equations"])
            case "graph":
                self.add_graph(obj, content_data["func"], content_data["coordinates_variable"])
            case "section":
                self.add_section(obj, data, extra)
            case "image":
                self.add_image(obj, data, extra)
            case "new_line":
                self.add_new_line(obj)
            case "new_page":
                self.add_new_page(obj)
            case "line_break":
                self.add_line_break(obj)
            case "top_line":
                self.add_top_line(obj, content_data)
            case "fill_line":
                self.add_fill_line(obj, content_data)
            case "h1":
                self.add_h1(obj, data, extra)
            case "h2":
                self.add_h2(obj, data, extra)
            case "h3":
                self.add_h3(obj, data, extra)
            case "list_itemize":
                self.add_list_itemize(obj, data, extra)
            case "list_enumerate":
                self.add_list_enumerate(obj, data, extra)
            case "list_description":
                self.add_list_description(obj, data, extra)

    def add_content_to_object(self, content_data):
        content_type = content_data.get("type")
        extra = content_data.get("extra", {})
        content = content_data.get("content", "")
        foot = content_data.get("foot", None)
        position = content_data.get("position", "center")
        data_variable = self.document_variables.get(str(content_data.get("data_variable", "")), "")
        data = data_variable if data_variable else content

        if foot:
            with self.header.create(Foot(foot)) as header:
                self.choose_type(content_data, header, data, extra, content_type, data_variable)

        elif position:
            match position:
                case "center":
                    with self.doc.create(Center()) as position_on_doc:
                        self.choose_type(content_data, position_on_doc, data, extra, content_type, data_variable)
                case "left":
                    with self.doc.create(FlushLeft()) as position_on_doc:
                        self.choose_type(content_data, position_on_doc, data, extra, content_type, data_variable)
                case "right":
                    with self.doc.create(FlushRight()) as position_on_doc:
                        self.choose_type(content_data, position_on_doc, data, extra, content_type, data_variable)
                case _:
                    self.choose_type(content_data, self.doc, data, extra, content_type, data_variable)
        else:
            self.choose_type(content_data, self.doc, data, extra, content_type, data_variable)

    def generate_latex(self):
        for content_data in self.document_contents:
            self.add_content_to_object(content_data)
        self.doc.preamble.append(self.header)
        self.doc.change_document_style("header")

    def add_top_line(self, obj, top_line_data):
        width = top_line_data.pop("width", "1pt")
        color = top_line_data.pop("color", "black")
        obj.append(Command("noindent"))
        obj.append(Command("hrule"))

    def generate_pdf(self, compiler: str = "pdflatex"):
        self.generate_latex()
        self.doc.generate_pdf(
            self.in_out_file,
            clean_tex=False,
            compiler=compiler,
            clean=False,
            silent=True,
            compiler_args=["-shell-escape"],
        )

    def add_image(self, obj, filename, extra={}):
        if isinstance(obj, Foot):
            with obj.create(MiniPage(**extra)) as logo_wrapper:
                logo_wrapper.append(StandAloneGraphic(filename=filename))
        else:
            with obj.create(Figure(position="h")) as img_fig:
                with obj.create(SubFigure(**extra)) as img_fig:
                    img_fig.add_image(filename)

    def add_new_line(self, obj):
        obj.append(NewLine())

    def add_new_page(self, obj):
        obj.append(NewPage())

    def add_line_break(self, obj):
        obj.append(LineBreak())

    def add_fill_line(self, obj, content_data):
        for each in range(0, content_data.get("multiplier", 1)):
            obj.append(HFill())
            obj.append(NewLine())

    def add_section(self, obj, content, extra):
        section_type = extra.get("section_type", "section")
        section_numbering = extra.get("numbering", True)

    def add_h1(self, obj, content, extra={}):
        obj.append(Section(content, **extra))

    def add_h2(self, obj, content, extra={}):
        obj.append(Subsection(content, **extra))

    def add_h3(self, obj, content, extra={}):
        obj.append(Subsubsection(content, **extra))

    def add_spacer(self, obj):
        obj.append(self.new_spacing())

    def add_header(self, obj, content):
        obj.append(self.new_header(content))

    def add_tabular(self, obj, data, extra={}, table_type="tabular", content_data={}):
        if not data:
            pass
        num_columns = len(data[0])
        add_hline = content_data.get("add_hline", True)
        bolt_headers = content_data.get("bolt_headers", False)
        match table_type:
            case "tabular":
                tab = Tabularx("r|" + "c" * (num_columns - 1), **extra)
            case "tabularx":
                tab = Tabularx("|".join(["X"] * num_columns), **extra)
            case "long_tabu":
                tab = LongTabu("X[r]" * num_columns, **extra)
            case "long_table":
                tab = LongTable("X[r]" * num_columns, **extra)
            case _:
                tab = Tabularx("X" * num_columns, **extra)

        with obj.create(tab) as table:
            table.add_hline()
            for idx, row in enumerate(data):
                if bolt_headers and idx == 0:
                    table.add_row(row, mapper=[bold])
                else:
                    table.add_row(row)

                if add_hline:
                    table.add_hline()

    def add_text(self, obj, content):
        lines = content.split("\n")
        for each in lines:
            obj.append(content)
            obj.append(NewLine())

    def add_list_itemize(self, obj, data, extra):
        with obj.create(Itemize()) as itemize:
            for item in data:
                itemize.add_item(item)

    def add_list_enumerate(self, obj, data, extra):
        with obj.create(Enumerate(enumeration_symbol=r"\alph*)", options={"start": 20})) as enum:
            for item in data:
                enum.add_item(item)

    def add_list_description(self, obj, data, extra):
        with obj.create(Description()) as desc:
            for idx, item in enumerate(data):
                desc.add_item(idx, item)

    def add_math(self, obj, expression):
        with obj.create(Math()):
            obj.append(expression)

    def add_matrix_equation(self, obj, matrix, vector, result):
        with obj.create("equation"):
            obj.append(f"{matrix} {vector} = {result}")

    def add_alignat_math(self, obj, equations):
        with obj.create("align*"):
            for equation in equations:
                obj.append(equation)

    def add_graph(self, obj, func, coordinates):
        with obj.create(Figure(position="h!")) as plot_fig:
            plot_fig.add_caption("Graph")
            with obj.create(TikZ()):
                plot_options = "height=4cm, width=6cm, grid=major"
                with obj.create(Axis(options=plot_options)) as plot:
                    plot.append(Plot(name="model", func=func))
                    plot.append(Plot(name="estimate", coordinates=coordinates))

    def new_spacing(self):
        return "\\vspace{36pt}"

    def new_header(self, content):
        return f"\\section*{{{content}}}"
