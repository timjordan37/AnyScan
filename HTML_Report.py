from flask import Flask, render_template, request, url_for
# from flask_weasyprint import HTML, render_pdf
import sqlite3 as sql

app = Flask(__name__, template_folder='template')


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

# @app.route('/DatabaseTemplate_<name>.pdf')

# def DatabaseTemplate_pdf(name):

# Make a PDF straight from HTML in a string.
# Not sure if this works yet.  Need to test.

# html = render_template('DatabaseTemplate.html', name=name)
# return render_pdf(HTML(string=html))
