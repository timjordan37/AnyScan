import sqlite3 as sql
import webbrowser

import pdfkit
from flask import Flask, render_template

from scanner_app.helpers.Scanner import Scanner


class ReportGenerator():

    @staticmethod
    def generatereport():
        app = Flask(__name__, template_folder='template')
        app.config['PDF_FOLDER'] = 'static/pdf/'
        app.config['TEMPLATE_FOLDER'] = 'template/'

        if Scanner._scanned == True:

            @app.route('/list')
            def list():
                # should populate the tables created in the HTML template with the appropriate VulnDB info

                conn = sql.connect('vulnDB.db')
                conn.row_factory = sql.Row

                cursor = conn.cursor()
                cursor.execute('SELECT * from Devices')
                row1 = cursor.fetchall();

                cursor.execute('SELECT * from Vulnerabilities')
                row2 = cursor.fetchall();

                cursor.execute('SELECT * from ScanHistory')
                row3 = cursor.fetchall();

                cursor.execute('SELECT * from Hosts')
                row4 = cursor.fetchall();

                cursor.execute('SELECT * from Parameters')
                row5 = cursor.fetchall();

                cursor.execute('SELECT * from PenTestHistory')
                row6 = cursor.fetchall();

                return render_template("DatabaseTemplate.html", row1=row1, row2=row2, row3=row3, row4=row4, row5=row5,
                                       row6=row6)

            @app.route('/')
            def index():
                return render_template('DatabaseTemplate.html')

            @app.route('/convert')
            def pdfconverter():
                htmlfile = app.config['TEMPLATE_FOLDER'] + 'DatabaseTemplate.html'
                pdffile = app.config['PDF_FOLDER'] + 'CurrentScanReport.pdf'
                pdfkit.from_file(htmlfile, pdffile)
                return '''Click here to open the
                    <a href="http://localhost:5000/static/pdf/CurrentScanReport.pdf">pdf</a>.'''

            url = 'http://127.0.0.1:5000'
            webbrowser.open_new(url)
            app.run(debug=False)

            print("Report has been generated.")

        else:
            print("No completed scans = no generated reports.")
