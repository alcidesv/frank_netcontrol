from __future__ import print_function, absolute_import

from flask import json
import re

from .app import app

@app.route("/rest/misc_statuss/<which_one>")
def miscstatus(which_one):
    # See if you can do pin in netcontrol... 
    from netcontrol.hello import hello
    promise = hello.delay()
    # Wait for it
    try:
        salute = promise.get(timeout = 5)
    except TimeoutError:
        salute = "<< timeout >>"
    return json.jsonify(
        misc_status = 
            {
                'netcontrol_ping': salute,
            });