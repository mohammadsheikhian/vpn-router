#**Services for vpn**
####Watchdog for VPN
```shell script
sudo vim /etc/systemd/system/vpn-watchdog.service
```

And copy the text below into file service.

```shell script
[Unit]
Description=Connect to my VPN
After=network.target

[Service]
Type=simple
Environment=password=correcthorsebatterystaple
ExecStart=/bin/sh -c 'python3 /usr/local/bin/vpn/vpn-watchdog.py'
Restart=always
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target

```
####Create a service for VPN
**openconnect service**
```shell script

sudo vim /etc/systemd/system/vpn-openconnect.service
```

And copy the text below into file service.

```shell script
[Unit]
Description=Connect to my VPN
After=network.target

[Service]
Type=simple
Environment=password=correcthorsebatterystaple
ExecStart=/bin/sh -c 'echo password | openconnect -u username --servercert pin
-sha256:4A/UEvh3ko2FliYZcZK2fI04tMHOYk+uSFWIPJkvTIY= --passwd-on-stdin v6.speedserver.info:555'
Restart=always

[Install]
WantedBy=multi-user.target

```
