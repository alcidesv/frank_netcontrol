
Who is the guy with the wifi 
----------------------------

The daemon/service in charge of the wifi is called `hostapd`. Look for its config in `/etc/hostapd`.
The files on that directory are source-controlled by mercurial, and the only one useful AFAIK is 
`hostapd.conf`, in that directory. If you get into problems trying to connect, inspect that file. 