
Keys with valuable information the the local Redis server
---------------------------------------------------------

### About Redis ### 

Redis is a flat networked keystore. In this installation, redis
simply listen in Unix domain socket, at `/var/redis/redis.sock`. That
is, if you want to connect to Redis, you do:

    $ redis-cli -s /var/redis/redis.sock

Redis admits several databases, all numbered. In this case, I use the
default one, with number zero. 

### The keys ### 

Here are the keys that I''m using with Redis:

* `ledsong`: Used to instruct the led to blink in several ways.
   This variable admits a string of bytes, with the meanings as
   specified the source code program at
   `/home/alcides/Projects/led_blinker`. I hope it be of use.

* `connection_request_state`: Used to coordinate the connection state
  to the externally bound network (say, the modem). Check the next
  section for the states
   
* `last_connect_date`: Used to keep track of when was last connected the 
  system.

* `HAVE_SOURCE`: If netcontrol believes that there is connectivity through
  an external interface.

* `HAVE_WIFI`: If netcontrol asserts that wifi is working allright

* `HAVE_ROUTING`: If the routing setup rule to the external network
  is correctly configured.

* `connection_span`: Total time to be connected.
