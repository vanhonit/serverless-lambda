import os
from datetime import datetime
import pdfkit
from flask import Flask, render_template, Response

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
here = lambda *x: os.path.abspath(os.path.join(BASE_DIR, *x))
binary_path = here('bin/wkhtmltopdf')
configuration = pdfkit.configuration(wkhtmltopdf=binary_path)

app = Flask(__name__)

def release_id():
    return datetime.now().strftime('%Y%m%d-%H%M%S')

def render_pdf(params):
    name = params.get('name', 'Someone')
    contents = render_template('base.html', name=name)
    pdf_file = pdfkit.from_string(contents, False, configuration=configuration)
    key_name = '%s.pdf' % release_id()
    return pdf_file
    # result = upload_to_s3(pdf_file, key_name)
    # return {
    #     'key': key_name,
    #     'url': get_s3_url(key_name),
    # }


@app.route("/")
def hello():
    resp = Response(render_pdf({'name': 'Hon'}))
    resp.headers['Content-Disposition'] = "inline; filename=%s" % 'hello.pdf'
    # resp.headers['Content-Disposition'] = "attachment; filename=%s" % 'hello'
    resp.mimetype = 'application/pdf'
    return resp