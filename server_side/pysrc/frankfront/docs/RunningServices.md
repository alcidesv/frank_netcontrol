
Services
--------

In ArchLinux, services are managed by [systemd.1]. For Frank,
the following services had to be implemented by me:

* A led manager. Look for it in /etc/systemd/system/led.service 
* A redis database server. Look for it in /etc/systemd/system/redis.service
* A network status-watching daemon. This is a Python script that checks and configures 
  network connectivity each a few seconds. Look for it in /etc/systemd/system/netwatch.service.
* hostapd: The guy in charge of sharing the wireless network. Read more here: [WhosWithTheWifi.md].
* frankfront: The webserver serving these pages. 

Of these services, the led manager, netwatch and hostapd need to run with root privileges, 
while redis runs with his own server (`redisdata`) and frankfront runs with the same `netcontrol` 
user. 
  
If something is wrong, chances are that some of those services be down. 
To check the state of any service, do as here (change 'led' by the actual name of the 
service you want to inspect):

     $ systemctl status led.service
     
To check the logs of a specific service, do as follows (don''t forget to fill-in the actual 
name of the service instead of "led"):

     $ journalctl -n 30 _SYSTEMD_UNIT=led.service 
     
For more details, check [journalctl.1]

Check [WhereAreThingsInstalled.md] to discover where the implementation of these services
actually reside.
