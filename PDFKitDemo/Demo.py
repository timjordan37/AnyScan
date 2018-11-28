from flask import Flask, render_template
import pdfkit
import os


app = Flask(__name__, template_folder='template')
app.config['PDF_FOLDER'] = 'static/pdf/'
app.config['TEMPLATE_FOLDER'] = 'template/'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/convert')
def konversi():
    htmlfile = app.config['TEMPLATE_FOLDER'] + 'index.html'
    pdffile = app.config['PDF_FOLDER'] + 'demo.pdf'
    pdfkit.from_file(htmlfile, pdffile)
    return '''Click here to open the
    <a href="http://localhost:5000/static/pdf/demo.pdf">pdf</a>.'''


if __name__ == '__main__':
    app.run(debug=True)
