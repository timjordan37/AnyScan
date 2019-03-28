from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from datetime import date

"""
This class pulls scan info from the DB and builds a PDF style report from that information.  The user can click the
'Reports' button on the default page of the application, after a successful scan, and the PDF report will be 
generated and displayed.
"""


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
        canvas.drawString(inch, 0.75 * inch, 'Page %d' % doc.page)
        canvas.restoreState()

    def host_page(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 9)
        canvas.drawString(inch, 0.75 * inch, 'Page %d' % doc.page)
        canvas.restoreState()

    def scan_page(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 9)
        canvas.drawString(inch, 0.75 * inch, 'Page %d' % doc.page)
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
        # print('STYLES: ', self.styles.list())

        style = self.styles["Normal"]

        # Host data
        Story.append(Paragraph('Scanned Hosts ---------------------', self.styles['Heading2']))
        for h in self._report['hosts']:
            if h.get_display_val():
                hname = f'Hostname: {h.get_display_name()}'
                ip = f'IP Address: {h.get_ip()}'
                mac = f'MAC Address: {h.get_mac_address()}'
                Story.append(Paragraph(hname, style))
                Story.append(Paragraph(ip, style))
                Story.append(Paragraph(mac, style))
                Story.append(Spacer(1, 0.2 * inch))

        # Next Pages
        Story.append(PageBreak())

        # cpe data
        Story.append(Paragraph('CPEs ---------------------', self.styles['Heading2']))
        for c in self._report['cpes']:
            cpe = self._report['cpes'][c][0]
            Story.append(Paragraph(cpe, style))
            Story.append(Spacer(1, 0.2 * inch))

        # Next Pages
        Story.append(PageBreak())

        # Vuln Data
        Story.append(Paragraph('Vulnerabilities ---------------------', self.styles['Heading2']))
        for v in self._report['vulns']:
            Story.append(Paragraph(v, style))

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
