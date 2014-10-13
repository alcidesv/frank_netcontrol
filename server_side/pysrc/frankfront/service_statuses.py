from __future__ import print_function, absolute_import

from flask import json
import re

from .app import app

@app.route("/rest/misc_statuss/<which_one>")
def miscstatus(which_one):
    # NOT yet implemented
    pass
