
from __future__ import print_function, absolute_import

import gevent
import json
import re
import redis 
from functools import partial
from geventwebsocket.exceptions import WebSocketError

from frankfront.redis_connector import redis_connector

def handle_websocket(ws):
    while True:
        message = ws.receive()
        if message is None:
            break
        as_json = json.loads( message )
        if as_json.get('action') == 'connect':
            # I know what to do with this...
            r = redis_connector()
            key_value = "request:{0}".format( as_json.get('max-time', 10) * 60 )
            r.set("connection_request_state", key_value)
            # Now I might seat to wait peacefully for things to happen
            gevent.spawn( update_on_redis_change, ws )
            ws.send(json.dumps({'type': 'update-log', 'output': "/(frankfront) : Requested connection" }))
        elif as_json.get('action') == 'disconnect':
            r = redis_connector()
            #key_value = "request-disconnect"
            del r["connection_request_state"]
            # Now I might seat to wait peacefully for things to happen
            gevent.spawn( update_on_redis_change, ws )
            ws.send(json.dumps({'type': 'update-log', 'output': "/(frankfront) : Requested disconnection" }))            
        else:
            ws.send(json.dumps({'type': 'update-log', 'output': "/(frankfront) : Could not understand request" }))

        
def update_on_redis_change( ws ):
    r = redis_connector()
    # Now subscribe to changes...
    pubsub = r.pubsub()
    pubsub.subscribe( [
        "__keyspace@0__:connection_request_state", 
        "connect_live_log",
        "__keyspace@0__:HAVE_SOURCE"
    ])
    # ... if they come...
    for message in pubsub.listen():
        print( message )
        back_msg = None
        out_message = None
        if message['data'] == 'set' and message['channel'] == '__keyspace@0__:connection_request_state':
            new_request_state = r.get('connection_request_state')
            back_msg = "Connection request signaled as \'" + new_request_state + "\'"
            if re.match(r'connected:.*', new_request_state):
                out_message = {'type': 'update-state', 'hint': 'connect' }
            else:
                out_message = {'type': 'update-log', 'output': back_msg }
        elif message['channel'] == "connect_live_log":
            print( message )
            back_msg = "/(netcontrol) " + str( message['data'] )
            out_message = {'type': 'update-log', 'output': back_msg }
        elif message['channel'] == '__keyspace@0__:HAVE_SOURCE':
            if message['data'] == 'set':
                have_source = r.get('HAVE_SOURCE')
                if have_source:
                    # Well, the connection is pretty much established now 
                    out_message = {'type': 'update-state', 'hint': 'connect'} 
                else:
                    # No warranties, keep waiting...
                    pass
        elif message['channel'] == '__keyspace@0__:connection_request_state' and message['data'] == 'del':
            # The key expired, so, it was a failure I guess
            out_message = {'type': 'update-state', 'hint': 'disconnect'} 
        if out_message != None:
            try:
                ws.send(json.dumps(out_message)) 
            except WebSocketError:
                # Listener stopped listening...
                break 
