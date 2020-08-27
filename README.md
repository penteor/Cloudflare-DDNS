# Cloudflare-DDNS

Dynamic DNS (DDNS or DynDNS) is a method of automatically updating a name server in the Domain Name Server (DNS), often in real time, with the active DDNS configuration of its configured hostnames, addresses or other information. 

Using Cloudflare service IP address is updated dinamically if your ISP provider offer Dynamic IP Address.

# Configuration
## DNS Settings  
edit config.py 

## Install requirements:
pip install -r requirements.txt

## Install requirements
./install.sh
## Install and configure as service (systemd) to start automatically
./ddns.py configure
## Service start/stop/status/restart
service  ddns [start / stop / status]
