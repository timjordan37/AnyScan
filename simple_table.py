# simple_table.py

from fpdf import FPDF

# Hard coded for now until I can figure out how to import from database where the
# reports will be generated and format it to pdf.
# This is just here to give you a rough visualization of a pdf vulnerability report.


def simple_table(spacing=1):
    data = [['Product Name', 'Number of Scans', 'Present Vulnerabilities', 'Location'],
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', '']
            ]

    pdf = FPDF()
    pdf.set_font("Arial", size=12)
    pdf.add_page()

    col_width = pdf.w / 4.5
    row_height = pdf.font_size
    for row in data:
        for item in row:
            pdf.cell(col_width, row_height * spacing,
                     txt=item, border=1)
        pdf.ln(row_height * spacing)

    pdf.output('simple_table.pdf')


if __name__ == '__main__':
    simple_table()
