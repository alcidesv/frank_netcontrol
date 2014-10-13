
The commands to connect and disconnect
--------------------------------------

### In short ### 

When you press the `connect` button in this web-interface, 
the scripts in `/home/netcontrol/softare/connect/activate.sh` gets executed. When
it is time to disconnect, the script in `/home/netcontrol/software/connect/deactivate.sh` 
gets executed. So, you can tweak the settings there! Both `activate.sh` and `deactivate.sh`
get executed with root privileges.

Supplementary information to look for: [pppd.8], [chat.8], [pon.1], [poff.1],
[plog.1]. 

### Longer version ###

When you press the `connect` button in this web-interface,
a javascript file (`quick.js`, look for it in the source code 
at `/home/netcontrol/software/frank_frontend/client_side/js/controllers` ) 
executes the method `initConnect` and wait for model updates
from the web-application server. This web-application server, in turn,
sets a key in the redis data-store. The sequence of interactions 
with the data-store is equivalent to this:

     $ redis-cli -s /var/redis/redis.sock 
     redis /var/redis/redis.sock> SET connection_request_state "request:<time-to-be-connected>"
     OK
     redis /var/redis/redis.sock> EXPIRE connection_request_state 20
     
Netcontrol, the process that runs as root,  is waiting for this and 
will execute the `activate.sh` command and then pass the connection_request_state 
key to the value `connecting`. Afterwards, when netcontrol/netwatch discovers a new point-to-point 
network interface, it will pass the `connection_request_state` redis key to `connected:<timestamp>`. It will
also set the `connection_request_state` variable to expire after the scheduled time, and the 
`connection_span` to the time asked for connection. The time itself when the connection is established 
is logged in `last_connect_date`. For knowing more about redis and the keys, check [RedisKeys.md].

If the key expires, the _web interface server_ will interpret the fact as that 
it was not possible to establish a new connection. 



