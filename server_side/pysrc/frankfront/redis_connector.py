
from __future__ import print_function 

import gevent
import json
import redis 
from functools import partial
from geventwebsocket.exceptions import WebSocketError

redis_connector = partial( 
    redis.StrictRedis, unix_socket_path='/var/redis/redis.sock', db=0 )