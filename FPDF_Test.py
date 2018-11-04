import fpdf

from fpdf import FPDF

# This is a small sample program to test basic functionality of FPDF.
# I plan to further explore the complete functionality of FPDF as it
# relates to our project, but for starters this is how it works.

pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 24)  # sets font style and size
pdf.cell(40, 10, 'Testing fpdf to print text to pdf.')  # manual entry just for testing purpose
pdf.output('fpdfdemo.pdf', 'F')  # name output file and formatting parameter
