from __future__ import print_function, absolute_import

from flask import make_response, render_template
from .app import app


@app.route('/')
def index():
    return render_template('index.html')