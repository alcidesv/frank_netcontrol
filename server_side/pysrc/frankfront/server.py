from __future__ import print_function, absolute_import


import os
import json
from gevent.pywsgi import WSGIServer
from gevent.monkey import patch_all
patch_all()
from geventwebsocket.handler import WebSocketHandler
import flask
import werkzeug.serving

from frankfront.app import app
from frankfront.connect_console_ws import handle_websocket

app.secret_key = os.urandom(24)
app.debug = True
#host,port='192.168.1.128',5000
host,port='127.0.0.1',5000
 
def wsgi_app(environ, start_response):  
    path = environ["PATH_INFO"]  
    if path == "/":  
        return app(environ, start_response)
    elif path == "/ws/connect-console/":  
        handle_websocket(environ["wsgi.websocket"])
    else:  
        return app(environ, start_response)  

def import_all():
    # Just be sure the decorators run
    import frankfront.index
    import frankfront.of_interface
    import frankfront.connection_state
    import frankfront.documentation_node


@werkzeug.serving.run_with_reloader
def main():
    import_all()
    http_server = WSGIServer((host,port), wsgi_app, handler_class=WebSocketHandler)
    print('Server started at %s:%s'%(host,port))
    http_server.serve_forever()
    
if __name__ == '__main__':
    main()