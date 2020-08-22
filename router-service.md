**Check VPN service**
```bash
[Unit]
Description=Connect to my VPN
After=network.target

[Service]
Type=simple
Environment=password=correcthorsebatterystaple
ExecStart=/bin/sh -c 'python3 /usr/local/bin/vpn/vpn-checker.py'
Restart=always
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target

```

**openconnect service**

```bash
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
