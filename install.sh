# Install requirements:
pip install -f requirements.txt

# Add CloudFlare DDNS as service
cat >/etc/systemd/system/ddns.service << EOL
[Unit]
Description=Cloudflare DDNS updater written in Python
After=network.target

[Service]
Environment=PYTHONUNBUFFERED=1
ExecStart=/usr/bin/python3 /opt/CloudFlare-DDNS/ddns.py
Restart=always
KillSignal=SIGQUIT
Type=notify
NotifyAccess=all

[Install]
WantedBy=multi-user.target
EOL

sudo systemctl start ddns
sudo systemctl status ddns
sudo systemctl stop ddns
sudo systemctl restart ddns
sudo systemctl enable ddns