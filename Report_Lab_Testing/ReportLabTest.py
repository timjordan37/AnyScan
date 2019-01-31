from reportlab.pdfgen import canvas

def hello(c):
    c.drawString(0,0, "Hello World")

c = canvas.Canvas("HelloWorld.pdf")
hello(c)
c.showPage()
c.save()
