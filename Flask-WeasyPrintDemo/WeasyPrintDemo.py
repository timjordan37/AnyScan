from flask import Flask, render_template, url_for
from flask_weasyprint import HTML, render_pdf

app = Flask(__name__, template_folder='template')


@app.route('/hello/', defaults={'name': 'World'})
@app.route('/hello/<name>/')
def hello_html(name):
    return render_template('hello.html', name=name)


@app.route('/hello_<name>.pdf')
def hello_pdf(name):
    # Make a PDF from another view
    return render_pdf(url_for('hello_html', name=name))


# Alternatively, if the PDF does not have a matching HTML page:

@app.route('/hello_<name>.pdf')
def hello_pdf(name):
    # Make a PDF straight from HTML in a string.
    html = render_template('hello.html', name=name)
    return render_pdf(HTML(string=html))
