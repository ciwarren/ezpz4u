Welcome! 

This is a very quickly put together web manager that has some basic functionality. 


Dependency !WARNING!:
https://github.com/openzomboid/pzlsm

This is used for executing the server actions, great project <3.


Installation:

```
pip install ezpz4u
```

Config file:

```
opt/pz/.env
USERNAME="admin"
PASSWORD="password"
COLLECTION_ID="########"
```

Running:
```
ezpz4u
```

Example scuffed unit file:
```
[Unit]
Description=ezpz4u Server
Wants=network-online.target
After=syslog.target network.target nss-lookup.target network-online.target

[Service]
ExecStart= /bin/bash -c "source /home/steam/.venv/pz/bin/activate && ezpz4u"
User=steam
StandardOutput=journal
Restart=on-failure
[Install]
WantedBy=multi-user.target
```