#!/usr/bin/python3

from config import *

import requests, json

import sys, time, subprocess

def GETExternalIP():
    ExternalIP_API = 'https://api.ipify.org?format=json'
    print("[*] Get external IP address! ")
    try:
        response = requests.get(ExternalIP_API)
    except Exception as err:
        print("[!] API Error: " + str(err))
        exit()
    if response.status_code == 200:
        IPAddress = str(response.json()['ip'])
        print("[*] External IP Address is: " + IPAddress)
        return str(IPAddress)
    else:
        print("[!] IP Address is not present in the response")
        exit()



def GetZoneID(DOMAIN_NAME=DOMAIN_NAME):
    print("[*] GET zone id for " + DOMAIN_NAME + " from Cloudflare.")

    try:
        response = requests.get('https://api.cloudflare.com/client/v4/zones?name={}'.format(DOMAIN_NAME),headers={'X-Auth-Key': API_KEY,'X-Auth-Email': EMAIL})
    except Exception as err:
        print('[!] Cloudflare API error: ' + str(err))
        exit()

    response = response.json()['result']
    for entry in response:
        if DOMAIN_NAME in entry['name']:
            print("[*] Zone id for " + DOMAIN_NAME + ":" + str(entry['id']))
            return str(entry['id'])
    print("[!] Error: Zone id not found: " + DOMAIN_NAME)
    exit()



def GetRecordID(ZONE_ID, SUBDOMAIN_NAME=SUBDOMAIN_NAME):
    print("[*] GET record id for " + SUBDOMAIN_NAME.upper() + " from Cloudflare.")
    try:
        response = requests.get('https://api.cloudflare.com/client/v4/zones/{}/dns_records'.format(ZONE_ID),
                                headers={'X-Auth-Key': API_KEY, 'X-Auth-Email': EMAIL})

    except Exception as err:
        print('[!] Cloudflare API error: ' + str(err))
        exit()

    response = response.json()['result']
    for entry in response:
        if SUBDOMAIN_NAME in entry['name']:
            print("[*] Record id for " + SUBDOMAIN_NAME.upper() + ":" + str(entry['id']))
            return str(entry['id'])
    print("[!] Record id not found:" + SUBDOMAIN_NAME)
    return False



def UpdateDNSRecord(RECORD_ID, ZONE_ID, ExtIP, SUBDOMAIN_NAME=SUBDOMAIN_NAME):

    print("[*] Updating DNS record " + SUBDOMAIN_NAME + " to point to " + ExtIP + " ...")
    try:
        resp = requests.put(
            'https://api.cloudflare.com/client/v4/zones/{}/dns_records/{}'.format(
                ZONE_ID, RECORD_ID),
            json={
                'type': 'A',
                'name': SUBDOMAIN_NAME,
                'content': ExtIP,
                'proxied': False
            },
            headers={
                'X-Auth-Key': API_KEY,
                'X-Auth-Email': EMAIL
            })
    except Exception as err:
        print("[!] Cloudflare Error:" + str(err))
        exit()
    if resp.status_code == 200:
        print("[*] Successfully updated " + SUBDOMAIN_NAME + " to point at " + ExtIP)
        return True
    else:
        print("[!] Failed to update " + SUBDOMAIN_NAME + " with " + ExtIP)
        return False



def CreateDNSRecord(ZONE_ID, ExtIP, SUBDOMAIN_NAME=SUBDOMAIN_NAME):

    print("[*] Creating DNS record " + SUBDOMAIN_NAME + " pointing " + ExtIP + " ...")
    try:
        resp = requests.post(
            'https://api.cloudflare.com/client/v4/zones/{}/dns_records/'.format(
                ZONE_ID),
            json={
                'type': 'A',
                'name': SUBDOMAIN_NAME,
                'content': ExtIP,
                'proxied': False
            },
            headers={
                'X-Auth-Key': API_KEY,
                'X-Auth-Email': EMAIL
            })
    except Exception as err:
        print("[!] CloudFlare Error:" + str(err))
        exit()

    if resp.status_code == 200:
        print("[*] Successfully created " + SUBDOMAIN_NAME + " to point at " + ExtIP)
        return True
    else:
        print("[!] Failed to update " + SUBDOMAIN_NAME + " with " + ExtIP)
        exit()

if __name__ == "__main__":
    # Check Args

    while True:
        IP = ''
        EXTERNAL_IP = GETExternalIP()
        if IP != EXTERNAL_IP:
            ZONE_ID = GetZoneID()
            RECORD_ID = GetRecordID(ZONE_ID)
            if RECORD_ID:
                UpdateDNSRecord(RECORD_ID, ZONE_ID, EXTERNAL_IP)
            else:
                CreateDNSRecord(ZONE_ID, EXTERNAL_IP)

        print("[*] Sleep for " + str(SLEEP) + " seconds!")
        time.sleep(int(SLEEP))


"""
if __name__ == "__main__":
    current_ip = ''

    if len(sys.argv) > 1:
        if "install" in sys.argv[1]:
            install_on_systemd()
            exit()

    while True:
        fetched_ip = get_own_device_ip()
        if current_ip != fetched_ip:
            current_ip = fetched_ip
            zone_id = find_zone_id(DOMAIN_NAME)
            record_id = find_record_id(SUBDOMAIN_NAME, zone_id)

            if record_id:
                update_dns_record(SUBDOMAIN_NAME, record_id, zone_id, current_ip)
            else:
                create_dns_record(SUBDOMAIN_NAME, record_id, zone_id, current_ip)

            print("[*] Sleeping for " + str(COOLDOWN_INTERVAL) + " seconds...")
            time.sleep(int(COOLDOWN_INTERVAL))
"""



def multi_popen(list_of_lists):  # takes a list of lists that represent the commands+arguments combos
    for args_list in list_of_lists:
        process = subprocess.Popen(args_list)
        stdout, stderr = process.communicate()
        if stdout or stderr:
            print(stdout, stderr)


def install_on_systemd():

    # print('[*] Creating the service file...')
    # with open("/etc/systemd/system/cloudflare_ddns_python.service","w+") as systemd_file:
    #    systemd_file.write(systemd_file_string)
    # print('[*] Created the service file.')
    """ cp -i cloudflare_ddns_python.py /bin/
#write out current crontab
crontab -l > mycron
#echo new cron into cron file
echo "@reboot python /bin/cloudflare_ddns_python.py" >> mycron
#install new cron file
crontab mycron
rm mycron """

    commands_list = list()
    commands_list.append(['pip', 'install', 'requests'])
    commands_list.append(['cp', '-i', '/opt/cloudflare_ddns_python.py', '/bin/'])
    commands_list.append(['crontab', '-l', '>', '/tmp/custom_cron'])
    commands_list.append(['echo', '"@reboot python /bin/cloudflare_ddns_python.py"', '>>', '/tmp/custom_cron'])
    commands_list.append(['crontab', '/tmp/custom_cron'])
    commands_list.append(['rm', '/tmp/custom_cron'])
    # commands_list.append(['cp', str(sys.argv[0]), '/opt/cloudflare_ddns_python.py'])
    # commands_list.append(['systemctl', 'enable', 'cloudflare_ddns_python.service'])
    # commands_list.append(['systemctl', 'start', 'cloudflare_ddns_python.service'])
    print('[*] Copying the code and starting the systemd service...')
    multi_popen(commands_list)
    print('[*] Installation done! Check the status with $ systemctl status cloudflare_ddns_python.service')










