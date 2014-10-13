from __future__ import print_function, absolute_import

from flask import json
import re
import datetime

from .app import app
from .redis_connector import redis_connector

@app.route("/rest/connection_states/<which_one>")
def connection_states(which_one):
    r = redis_connector()
    state = 'disconnected'
    when = r.get('last_connect_date')
    if not when: when = 'never'
    if r.exists('connection_request_state'):
        connection_request_state = r.get('connection_request_state')
        mo = re.match( r'connected:(.*)' , connection_request_state )
        if mo != None:
            # Ok, say it 
            state = 'connected'
            when = mo.group(1)
    else:
        state = 'disconnected'
    
    return json.jsonify(
        connection_state = 
            {
                'state_now': state,
                'when_connected_last': when,
                'total_connected_last_30_days': 10
            });