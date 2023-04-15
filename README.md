Welcome! 

This is a very quickly put together web manager that has some basic functionality. 


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
User=root
StandardOutput=journal
Restart=on-failure
[Install]
WantedBy=multi-user.target
```

Zomboid systemd file
```
[Unit]
Description=Project Zomboid Server
After=network.target

[Service]
PrivateTmp=true
Type=simple
User=steam
WorkingDirectory=/home/steam/pz
ExecStartPre=/usr/games/steamcmd +force_install_dir "/home/steam/pz" +login anonymous +app_update 380870 validate +quit
ExecStart=/bin/sh -c "exec /home/steam/pz/start-server.sh </home/steam/pz/zomboid.control"
ExecStop=/bin/sh -c "echo save > /home/steam/pz/zomboid.control; sleep 15; echo quit > /home/steam/pz/zomboid.control"
Sockets=zomboid.socket
KillSignal=SIGCONT

[Install]
WantedBy=multi-user.target

```

Zomboid Socket 