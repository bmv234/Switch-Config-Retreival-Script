
# Switch Configuration Retrieval Script

## Description

This Python script retrieves and saves the running configurations from a list of network switches/routers. It supports multiple vendors and can handle both SSH and Telnet connections. The script uses Netmiko for network device connections and logging for verbose output.

## Features

- Automatically detects device types for SSH connections using Netmiko's autodetect feature.
- Supports multiple network device vendors (Cisco, Juniper, Arista, Dell, HP, Huawei, Brocade, Extreme Networks).
- Attempts SSH connection first and falls back to Telnet if SSH fails.
- Logs detailed output to both the console and a log file (`log.txt`).
- Saves configurations to individual files named `<ip>_config.txt` in the `configs` directory.

## Requirements

- Python 3.x
- Netmiko library

## Installation

1. **Clone the repository:**

   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Install the required Python packages:**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command Line Arguments

- `-i`, `--ip`: Single IP address or multiple IP addresses separated by commas.
- `-f`, `--file`: File containing a list of IP addresses (one per line).

### Examples

1. **Retrieve configuration from a single IP address:**

   ```bash
   python script.py --ip 192.168.1.1
   ```

2. **Retrieve configurations from multiple IP addresses:**

   ```bash
   python script.py --ip 192.168.1.1,192.168.1.2
   ```

3. **Retrieve configurations from a file containing IP addresses:**

   ```bash
   python script.py --file ip_list.txt
   ```

### Script Execution

1. **Run the script with the appropriate arguments:**

   ```bash
   python script.py --ip 192.168.1.1
   ```

2. **Input the required credentials when prompted:**

   - Username
   - Password
   - Enable Password (if required)

### Example Usage

```bash
python script.py --ip 192.168.1.1,192.168.1.2
```

```bash
python script.py --file ip_list.txt
```

## Logging

The script logs detailed output to both the console and a `log.txt` file. The log file includes timestamps, log levels, and messages.

## Supported Vendors and Commands

The script supports multiple network device vendors and their respective commands for retrieving running configurations. The `COMMANDS` dictionary maps device types to their commands.

```python
COMMANDS = {
    'cisco_ios': 'show running-config',
    'cisco_nxos': 'show running-config',
    'arista_eos': 'show running-config',
    'juniper_junos': 'show configuration',
    'dell_os10': 'show running-configuration',
    'hp_procurve': 'show running-config',
    'huawei': 'display current-configuration',
    'brocade_fos': 'configshow',
    'extreme_exos': 'show config',
}
```

## Contributing

Feel free to submit issues, fork the repository, and send pull requests. Contributions are welcome!

## License

This project is licensed under the MIT License.
