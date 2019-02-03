from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4


def hey_test(c):
    c.translate(inch, inch)
    c.setFont('Helvetica', 14)
    c.setStrokeColorRGB(0.2, 0.5, 0.3)
    c.setFillColorRGB(1, 0, 1)

    c.line(0, 0, 0, 1.7*inch)
    c.line(0, 0, 1*inch, 0)
    c.rect(0.2*inch, 0.2*inch, 1*inch, 1.5*inch, fill=1)

    c.rotate(90)

    c.setFillColorRGB(0, 0, 0.77)

    c.drawString(0.3*inch, -inch, 'Test some stuff')

def set_header(c):
    textobj = c.beginText()
    textobj.setTextOrigin(inch, 10*inch)
    textobj.setFont('Helvetica', 18)
    textobj.textLine('Pentesting Report')
    textobj.setFillGray(0.4)

    c.line(inch, 9.8*inch, 7.5*inch, 9.8*inch)

    t2 = c.beginText()
    t2.setTextOrigin(inch, 9.5*inch)
    t2.setFont('Helvetica', 14)
    t2.textLine('Here is some data that will be populated')
    t2.setFillGray(1.0)

    c.drawText(textobj)
    c.drawText(t2)


c = canvas.Canvas('test2.pdf', pagesize=letter)
#hey_test(c)
set_header(c)
c.showPage()
c.save()