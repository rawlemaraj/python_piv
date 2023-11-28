import csv
import getpass
from netmiko import ConnectHandler, NetmikoAuthenticationException, NetmikoTimeoutException

# Prompt for file paths
switches_csv = input("Enter the path to the CSV file with switch hostnames: ")
commands_csv = input("Enter the path to the CSV file with commands: ")
output_file = "failed_switches.txt"  # File to store failed switch hostnames

# Prompt for username
username = input("Enter your SSH username: ")

# Prompt for password with verification
while True:
    password = getpass.getpass("Enter your SSH/Enable password: ")
    password_verify = getpass.getpass("Re-enter your password for verification: ")
    if password == password_verify:
        break
    else:
        print("Passwords do not match. Please try again.")

# Rest of your script remains the same...


# List to keep track of failed switches
failed_switches = []

# Function to read hostnames from a CSV file
def read_hostnames(filename):
    try:
        with open(filename, newline='') as file:
            reader = csv.reader(file)
            return [row[0] for row in reader]
    except Exception as e:
        print(f"Error reading hostnames from {filename}: {e}")
        return []

# Function to read commands from a CSV file
def read_commands(filename):
    try:
        with open(filename, newline='') as file:
            reader = csv.reader(file)
            return [row[0] for row in reader]
    except Exception as e:
        print(f"Error reading commands from {filename}: {e}")
        return []

# Function to connect to a switch and run commands
def run_commands_on_switch(hostname, commands):
    device = {
        'device_type': 'cisco_ios',
        'host': hostname,
        'username': username,
        'password': password,
        'secret': password,  # using the same password for enable mode
        'global_delay_factor': 2  # Adjust this as needed
    }

    try:
        with ConnectHandler(**device) as connection:
            print(f"Connected to {hostname}")
            connection.enable()  # entering enable mode
            for command in commands:
                try:
                    output = connection.send_command(command, delay_factor=2)  # Adjust delay_factor as needed
                    print(f'Output for {command} on {hostname}:\n{output}\n')
                except Exception as cmd_e:
                    print(f"Error executing command '{command}' on {hostname}: {cmd_e}")
                    failed_switches.append(hostname)
                    break  # Stop executing further commands on this switch
    except Exception as e:
        print(f"Error with {hostname}: {e}")
        failed_switches.append(hostname)

# Function to write failed switches to a file
def write_failed_switches(filename, switches):
    with open(filename, 'w') as file:
        for switch in switches:
            file.write(switch + '\n')

# Main script
def main():
    switches = read_hostnames(switches_csv)
    if not switches:
        print("No hostnames to process. Exiting.")
        return

    commands = read_commands(commands_csv)
    if not commands:
        print("No commands to execute. Exiting.")
        return

    for switch in switches:
        print(f"Processing {switch}...")
        run_commands_on_switch(switch, commands)

    if failed_switches:
        write_failed_switches(output_file, failed_switches)
        print(f"Failed switches written to {output_file}")

    print("Script execution completed.")

if __name__ == '__main__':
    main()
