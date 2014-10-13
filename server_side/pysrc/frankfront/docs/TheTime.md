
How to adjust the time 
----------------------

Frank's time use a simple concept: there is no way that any computer can obtain 
accurate time from a network server if it is in Cuba. That's because there are no 
atomic clocks in Cuba which happen to be publicly accessible as NTP servers. Servers 
outside Cuba would be accessed, if possible after restrictive proxy-ing rules, with 
non-controllable latency. So, I have wired two real-time clocks to Frank, one of them
is extremely precise. 

The way it works is as follows. On boot, an udev rule in `/etc/udev/rules.d/92-rtc.rules`
watches for the i2c bus 1 to come up, and then executes a configuration commands contained 
in `/home/netcontrol/software/hwclock/activate.sh` to load kernel modules for the hardware 
clocks. Another effect of the rule is to tag `/dev/rtc0` with `systemd`.

Then, later in the boot sequence, the service `hwclock.service` is one-shot, but before 
ntpd.service; so that ntpd be sure about the current time. From there on, you can simply 
synchronize your laptop from our very precise air...

You don't want to adjust the hardware clocks, and if you really *need* to do that, 
read how to do it in [hwclock.8]. 