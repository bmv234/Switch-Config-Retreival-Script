import argparse
import csv
from getpass import getpass
from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException, ReadTimeout
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("log.txt"),
                              logging.StreamHandler()])

def save_config(ip, username, password, enable_password, output_dir):
    #session_log = f"session_log_{ip}.txt"

    device_params_ssh = {
        'device_type': 'dell_force10',  # Dell switches are stubborn and this device_type still works for most Cisco switches
        'host': ip,
        'username': username,
        'password': password,
        'secret': enable_password,
        'timeout': 100,
        'blocking_timeout': 8,
        'banner_timeout': 200,
        'auth_timeout': 50,
        #'global_delay_factor': 2,  # Adjust delay factor if needed
        #'session_log': session_log,  # Enable session logging
        #'global_cmd_verify': False  # Turn off global command verification

    }

    device_params_telnet = {
        'device_type': 'dell_dnos6_telnet',
        'host': ip,
        'username': username,
        'password': password,
        'secret': enable_password,
        'timeout': 100,
        'blocking_timeout': 8,
        'banner_timeout': 200,
        'auth_timeout': 50,
    }

    try:
        logging.info(f"Attempting to connect to {ip} using SSH...")
        net_connect = ConnectHandler(**device_params_ssh)
    except (NetMikoTimeoutException, NetMikoAuthenticationException, OSError, ReadTimeout) as ssh_error:
        logging.error(f"SSH connection to {ip} failed: {ssh_error}")
        logging.info(f"Attempting to connect to {ip} using Telnet...")
        try:
            net_connect = ConnectHandler(**device_params_telnet)
            logging.warning(f"Warning: Telnet is not secure. Reconfigure the switch {ip} to use SSH.")
        except (NetMikoTimeoutException, NetMikoAuthenticationException, OSError, ReadTimeout) as telnet_error:
            logging.error(f"Telnet connection to {ip} failed: {telnet_error}")
            logging.error(f"Failed to connect to {ip} using both SSH and Telnet.")
            return

    try:
        logging.info(f"Entering enable mode on {ip}...")
        net_connect.enable()

        logging.info(f"Setting terminal length on {ip}...")
        net_connect.send_command('terminal length 0')

        # Retrieve the hostname
        hostname = net_connect.find_prompt().strip('#').strip('>')

        logging.info(f"Connected to {ip}. Retrieving running configuration using command: 'show running-config'")
        running_config = net_connect.send_command(
            'show running-config',
            expect_string=r'#',
            strip_prompt=True,
            strip_command=True,
            read_timeout=60
        )
        
        output_file = os.path.join(output_dir, f'{ip}_{hostname}_config.txt')
        with open(output_file, 'w') as file:
            file.write(running_config.strip())
        
        net_connect.disconnect()
        logging.info(f"Configuration saved for {ip} to {output_file}")
    except Exception as e:
        logging.error(f"An error occurred while retrieving the configuration from {ip}: {e}")

def parse_ips_from_file(file_path):
    ip_list = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            ip_list.extend(ip.strip() for ip in row if ip.strip())
    return ip_list

def main():
    parser = argparse.ArgumentParser(
        description='Retrieve and save running configs from Dell OS6 switches.',
        epilog='Example usage: script.py --ip 192.168.1.1 or script.py --ip 192.168.1.1,192.168.1.2'
    )
    parser.add_argument('-i', '--ip', help='Single IP address or multiple IP addresses separated by commas')
    parser.add_argument('-f', '--file', type=str, help='File containing list of IP addresses')
    args = parser.parse_args()
    
    if not args.ip and not args.file:
        parser.error('No IPs provided, add --ip or --file')
    
    ip_list = []

    if args.file:
        logging.info(f"Reading IP addresses from file: {args.file}")
        ip_list.extend(parse_ips_from_file(args.file))

    if args.ip:
        ip_list.extend(args.ip.split(','))

    ip_list = [ip.strip() for ip in ip_list]

    logging.info(f"IP addresses to be processed: {ip_list}")

    username = input('Username: ')
    password = getpass('Password: ')
    enable_password = getpass('Enable Password (if required): ')

    output_dir = 'configs'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logging.info(f"Created output directory: {output_dir}")
    else:
        logging.info(f"Using existing output directory: {output_dir}")
    
    for ip in ip_list:
        save_config(ip, username, password, enable_password, output_dir)
    
    logging.info('Configuration retrieval complete.')

if __name__ == '__main__':
    main()