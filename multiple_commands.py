import pandas as pd
from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException
from getpass import getpass

def read_devices(file_path):
    df = pd.read_excel(file_path)
    return df['Hostname'].dropna().tolist()

def read_commands(file_path):
    df = pd.read_csv(file_path)
    return df['Command'].dropna().tolist()

def log_error_to_file(message, file_name='error_log.txt'):
    with open(file_name, 'a') as file:
        file.write(message + '\n')

def connect_and_execute_commands(host, username, password, enable_password, commands):
    device = {
        'device_type': 'cisco_ios',  # Change this depending on your device type
        'host': host,
        'username': username,
        'password': password,
        'secret': enable_password,
    }

    try:
        with ConnectHandler(**device) as net_connect:
            net_connect.enable()
            for command in commands:
                output = net_connect.send_command(command)
                print(f"Output from {host} for command '{command}':\n{output}\n")
    except NetMikoTimeoutException:
        error_message = f"Connection timed out for device {host}"
        print(error_message)
        log_error_to_file(error_message)
    except NetMikoAuthenticationException:
        error_message = f"Authentication failed for device {host}"
        print(error_message)
        log_error_to_file(error_message)
    except Exception as e:
        error_message = f"An error occurred with device {host}: {e}"
        print(error_message)
        log_error_to_file(error_message)

def main():
    # User credentials input
    username = input("Enter your username: ")
    password = getpass("Enter your password: ")
    enable_password = getpass("Enter your enable password (leave blank if same as login password): ")
    enable_password = enable_password or password

    # Read hostnames and commands
    hostnames = read_devices('hostnames.xlsx')
    commands = read_commands('commands.csv')

    # Connect to each device and execute commands
    for host in hostnames:
        connect_and_execute_commands(host, username, password, enable_password, commands)

if __name__ == "__main__":
    main()
