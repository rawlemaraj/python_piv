import csv
import getpass
from netmiko import ConnectHandler, NetmikoAuthenticationException, NetmikoTimeoutException

# Prompt for file paths
switches_csv = input("Enter the path to the CSV file with switch hostnames: ")
commands_csv = input("Enter the path to the CSV file with commands: ")

# Prompt for username and password
username = input("Enter your SSH username: ")
password = getpass.getpass("Enter your SSH/Enable password: ")

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
        'secret': password  # using the same password for enable mode
    }

    try:
        with ConnectHandler(**device) as connection:
            print(f"Connected to {hostname}")
            connection.enable()  # entering enable mode
            for command in commands:
                output = connection.send_command(command)
                print(f'Output for {command} on {hostname}:\n{output}\n')
    except NetmikoAuthenticationException:
        print(f"Authentication failed for {hostname}. Check username/password.")
    except NetmikoTimeoutException:
        print(f"Connection timed out for {hostname}. Check hostname and network connectivity.")
    except Exception as e:
        print(f"An unexpected error occurred with {hostname}: {e}")

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

    print("Script execution completed.")

if __name__ == '__main__':
    main()
