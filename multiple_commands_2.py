import csv
import getpass
import os
from netmiko import ConnectHandler
from concurrent.futures import ThreadPoolExecutor, as_completed
from netmiko.ssh_exception import NetMikoTimeoutException, NetMikoAuthenticationException

# Create a directory for log files if it doesn't exist
log_directory = "log_files_changes"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Prompt for file paths
switches_csv = input("Enter the path to the CSV file with switch hostnames: ")
commands_csv = input("Enter the path to the CSV file with commands: ")

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

# Function to read hostnames from a CSV file
def read_hostnames(filename):
    try:
        with open(filename, newline='') as file:
            reader = csv.reader(file)
            return [row[0] for row in reader]
    except FileNotFoundError:
        print(f"Hostname file not found: {filename}")
        return []
    except Exception as e:
        print(f"Error reading hostnames from {filename}: {e}")
        return []

# Function to read commands from a CSV file
def read_commands(filename):
    try:
        with open(filename, newline='') as file:
            reader = csv.reader(file)
            return [row[0] for row in reader]
    except FileNotFoundError:
        print(f"Commands file not found: {filename}")
        return []
    except Exception as e:
        print(f"Error reading commands from {filename}: {e}")
        return []

# Function to connect to a switch and run configuration commands
def configure_switch(hostname, commands):
    log_file_path = os.path.join(log_directory, f'netmiko_session_{hostname}.log')
    device = {
        'device_type': 'cisco_ios',
        'host': hostname,
        'username': username,
        'password': password,
        'secret': password,
        'session_log': log_file_path  # Log session details
    }

    try:
        with ConnectHandler(**device) as connection:
            connection.enable()  # Entering enable mode
            connection.send_config_set(commands)  # Sending configuration commands
            connection.save_config()  # Saving the configuration
            return f"Configuration applied to {hostname}"
    except NetMikoTimeoutException:
        return f"Connection timed out for {hostname}."
    except NetMikoAuthenticationException:
        return f"Authentication failed for {hostname}."
    except Exception as e:
        return f"Unexpected error with {hostname}: {e}"

# Main script with multi-threading
def main():
    switches = read_hostnames(switches_csv)
    if not switches:
        return

    commands = read_commands(commands_csv)
    if not commands:
        return

    max_threads = 5  # Adjust the number of threads based on your environment

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {executor.submit(configure_switch, switch, commands): switch for switch in switches}
        for future in as_completed(futures):
            print(future.result())

    print("Script execution completed.")

if __name__ == '__main__':
    main()
