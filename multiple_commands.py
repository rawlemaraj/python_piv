import pandas as pd
from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException
from getpass import getpass

def read_devices(file_path):
    df = pd.read_excel(file_path)
    return df['Hostname'].dropna().tolist()

def read_commands(file_path):
    df = pd.read_csv(file_path)
    return df['Command'].dropna().tolist()

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
        print(f"Connection timed out for device {host}")
    except NetMikoAuthenticationException:
        print(f"Authentication failed for device {host}")
    except Exception as e:
        print(f"An error occurred with device {host}: {e}")

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
