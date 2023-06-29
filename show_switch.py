import os
from pyats.topology import loader
from netmiko import ConnectHandler

# Access the device parameters from environment variables
device_type = os.environ['DEVICE_TYPE']
ip = os.environ['DEVICE_IP']
username = os.environ['DEVICE_USERNAME']
password = os.environ['DEVICE_PASSWORD']
secret = os.environ.get('DEVICE_SECRET', password)  # use password as secret if DEVICE_SECRET is not provided

# Define connection parameters
device_params = {
    'device_type': device_type,
    'ip':   ip,
    'username': username,
    'password': password,
    'secret': secret,
}

# Establish connection
connection = ConnectHandler(**device_params)

# Define command
command = 'show switch'

# Send command to device
output = connection.send_command(command)

# Define the correct role and priority for each switch
correct_values = {
    '1': {'role': 'Active', 'priority': '1'},
    '2': {'role': 'Standby', 'priority': '2'},
    '3': {'role': 'Member', 'priority': '3'},
    # Add more switches as needed
}

# Extract all switch numbers from command output
lines = output.split('\n')
switch_numbers = [line.split()[0] for line in lines[1:] if line.split()]

# Analyze each switch number against correct_values
results = []
for switch in switch_numbers:
    if switch in correct_values:
        role, mac_address, priority, *_ = lines[int(switch)].split()[1:]
        if role.lower() == correct_values[switch]['role'].lower() and priority == correct_values[switch]['priority']:
            result = 'PASS'
        else:
            result = 'FAIL'
        results.append(f'Switch {switch}: {result}')

# Save results to file
with open('output.txt', 'w') as f:
    for result in results:
        f.write(result + '\n')

# Disconnect
connection.disconnect()
