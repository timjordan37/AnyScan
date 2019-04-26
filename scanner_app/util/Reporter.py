from reportlab.platypus import BaseDocTemplate, Frame, NextPageTemplate, PageTemplate, SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from datetime import date


class Reporter:
    """This class pulls scan info from the DB and builds a PDF style report from that information.  The user can
    click the 'Reports' button on the default page of the application, after a successful scan, and the PDF
    report will be generated and displayed.
    """
    PAGE_HEIGHT = defaultPageSize[1]
    PAGE_WIDTH = defaultPageSize[0]
    styles = getSampleStyleSheet()
    Title = "Vulnerability Scan Report"
    pageinfo = "Report: "
    _report = {}
    _filename = ''
    _authors = []

    def __init__(self, report, filename, authors):
        """Create Reporter object

        :param report: data to be included in report
        :param filename: name to save file as
        :param authors: name to be listed as author of report
        """
        self._report = report
        self._filename = filename
        self._authors = authors

    def title_page(self, canvas, doc):
        """Create a title page with headline, author, date, and page number

        :param canvas: canvas to apply title page to
        :param doc: document to include title page in
        """
        canvas.saveState()
        canvas.setFont('Times-Bold', 16)
        canvas.drawCentredString(self.PAGE_WIDTH / 2.0, self.PAGE_HEIGHT - 220, self.Title)
        canvas.setFont('Times-Bold', 14)
        canvas.drawCentredString(self.PAGE_WIDTH / 2.0, self.PAGE_HEIGHT - 260,
                                 'Created by: %s' % self._authors)
        canvas.drawCentredString(self.PAGE_WIDTH / 2.0, self.PAGE_HEIGHT - 280,
                                 'Generated on: %s' % date.today().isoformat())
        canvas.setFont('Times-Roman', 9)
        canvas.drawString(inch, 0.75 * inch, 'Page %d' % doc.page)
        canvas.restoreState()

    def host_page(self, canvas, doc):
        """

        :param canvas: canvas to apply host page to
        :param doc: document to add host page to
        """
        canvas.saveState()
        canvas.setFont('Times-Bold', 16)
        canvas.drawCentredString(self.PAGE_WIDTH / 2.0, self.PAGE_HEIGHT - 60, "Hosts")
        canvas.setFont('Times-Roman', 9)
        canvas.drawString(inch, 0.75 * inch, 'Page %d' % doc.page)
        canvas.restoreState()

    def scan_page(self, canvas, doc):
        """

        :param canvas: canvas to apply scan page to
        :param doc: document to add scan page to
        """
        canvas.saveState()
        canvas.setFont('Times-Roman', 9)
        canvas.drawString(inch, 0.75 * inch, 'Page %d' % doc.page)
        canvas.restoreState()

    def build_pdf(self):
        """Using different internal page methods and given the data provided build the report
        """
        # doc options to abstract and set
        # doc.creator
        # doc.encrypt
        # doc.author
        # doc.subject
        # doc.title
        style = self.styles["Normal"]
        doc = BaseDocTemplate(self._filename)

        # Flowables to be added to document
        Story = []

        # could create different sized frames and set addPageTemplate frames to array frames=[frame1, frame2]
        standard_frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='sframe')

        Story.append(NextPageTemplate('host'))
        # space for title page
        Story.append(PageBreak())
        
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

        # cpe data
        Story.append(Paragraph('CPEs ---------------------', self.styles['Heading2']))
        if self._report['cpes']:
            for c in self._report['cpes']:
                if self._report['cpes'][c][0]:
                    cpe = self._report['cpes'][c][0]
                    Story.append(Paragraph(cpe, style))
                    Story.append(Spacer(1, 0.2 * inch))
        else:
            Story.append(Paragraph('No CPEs found', style))

        # Vuln Data
        Story.append(Paragraph('Vulnerabilities ---------------------', self.styles['Heading2']))
        if self._report['vulns']:
            for v in self._report['vulns']:
                Story.append(Paragraph(v, style))
        else:
            Story.append(Paragraph('No vulnerabilities found.', style))

        doc.addPageTemplates([PageTemplate(id='title', frames=standard_frame, onPage=self.title_page),
                              PageTemplate(id='host', frames=standard_frame, onPage=self.host_page)])

        doc.build(Story)

    def print(self):
        print(self._report)


# TESTING
if __name__ == "__main__":
    report_test = {'cve': '2019',
                   'some attribute': 'some data'
              }
    r = Reporter(report_test, 'pdf-test.pdf', 'Curtis')
    r.build_pdf()
