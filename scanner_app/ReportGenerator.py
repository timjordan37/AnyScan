from flask import Flask, render_template
import pdfkit
import sqlite3 as sql

app = Flask(__name__, template_folder='template')
app.config['PDF_FOLDER'] = 'static/pdf/'
app.config['TEMPLATE_FOLDER'] = 'template/'


@app.route('/list')
def list():
    # should populate the tables created in the HTML template with the appropriate VulnDB info

    conn = sql.connect('vulnDB.db')
    conn.row_factory = sql.Row

    cursor = conn.cursor()
    cursor.execute('SELECT * from Devices')
    rows = cursor.fetchall();
    return render_template("DatabaseTemplate.html", rows=rows)

    cursor.execute('SELECT * from Vulnerabilities')
    rows = cursor.fetchall();
    return render_template("DatabaseTemplate.html", rows=rows)

    cursor.execute('SELECT * from ScanHistory')
    rows = cursor.fetchall();
    return render_template("DatabaseTemplate.html", rows=rows)

    cursor.execute('SELECT * from Parameters')
    rows = cursor.fetchall();
    return render_template("DatabaseTemplate.html", rows=rows)

    cursor.execute('SELECT * from PenTestHistory')
    rows = cursor.fetchall();
    return render_template("DatabaseTemplate.html", rows=rows)


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


if __name__ == '__main__':
    app.run(debug=True)
