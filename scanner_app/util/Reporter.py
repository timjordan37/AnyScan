from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from datetime import date



class Reporter:
    PAGE_HEIGHT = defaultPageSize[1]
    PAGE_WIDTH = defaultPageSize[0]
    styles = getSampleStyleSheet()
    Title = "Vulnerability Scan Report"
    pageinfo = "Report: "
    _report = {}
    _filename = ''
    _authors = []

    def __init__(self, report, filename, authors):
        self._report = report
        self._filename = filename
        self._authors = authors

    def title_page(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Bold', 16)
        canvas.drawCentredString(self.PAGE_WIDTH / 2.0, self.PAGE_HEIGHT - 120, self.Title)
        canvas.setFont('Times-Bold', 14)
        canvas.drawCentredString(self.PAGE_WIDTH / 2.0, self.PAGE_HEIGHT - 160,
                                 'Created by: %s' % self._authors)
        canvas.drawCentredString(self.PAGE_WIDTH / 2.0, self.PAGE_HEIGHT - 180,
                                 'Generated on: %s' % date.today().isoformat())
        canvas.setFont('Times-Roman', 9)
        canvas.drawString(inch, 0.75 * inch, 'Page number of 1st page stuff')
        canvas.restoreState()

    def host_page(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 9)
        canvas.drawString(inch, 0.75 * inch, 'Page %d %s' % (doc.page, self.pageinfo))
        canvas.restoreState()

    def scan_page(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 9)
        canvas.drawString(inch, 0.75 * inch, 'Page %d %s' % (doc.page, self.pageinfo))
        canvas.restoreState()

    def build_pdf(self):
        # doc options to abstract and set
        # doc.creator
        # doc.encrypt
        # doc.author
        # doc.subject
        # doc.title
        doc = SimpleDocTemplate(self._filename)
        # create story with space first
        Story = [Spacer(1, 2 * inch)]

        # print styles to see what we can use
        print('STYLES: ', self.styles.list())

        style = self.styles["Normal"]

        #todo add data to page

        # Host data
        Story.append(Paragraph('Hosts - - - - - - - - -', self.styles['Heading2']))
        for h in self._report['hosts']:
            if h.get_display_val():
                Story.append(Paragraph(h.get_display_val(), style))
                Story.append(Spacer(1, 0.2 * inch))
                Story.append(Spacer(1, 0.2 * inch))

        Story.append(PageBreak())

        # cpe data
        Story.append(Paragraph('CPEs - - - - - - - - -', self.styles['Heading2']))
        for c in self._report['cpes']:
            Story.append(Paragraph(c, style))
            Story.append(Spacer(1, 0.2 * inch))
            Story.append(Spacer(1, 0.2 * inch))

        # for i in range(20):
        #     some_text = ('Attribute: %s. ' % i)*20
        #     p = Paragraph(some_text, style)
        #     Story.append(p)
        #     Story.append(Spacer(1, 0.2 * inch))
        #     Story.append(Paragraph('This is text!', style))
        #     Story.append(Spacer(1, 0.2*inch))
        # Story.append(Paragraph(self._report['cve'], self.styles['Heading1']))
        #########


        doc.build(Story, onFirstPage=self.title_page, onLaterPages=self.scan_page)

    def print(self):
        print(self._report)


# TESTING
if __name__ == "__main__":
    report = {'cve': '2019',
              'some attribute': 'some data'
              }
    r = Reporter(report, 'pdf-test.pdf', 'Curtis')
    r.build_pdf()
    