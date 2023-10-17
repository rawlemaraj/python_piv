import csv
from netmiko import ConnectHandler

# Define a function to read a given file and return a list of its lines
def read_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

# Define a function to connect to a Cisco device using Netmiko
def connect_to_device(device_ip, username, password, secret):
    # Define device parameters required for Netmiko's ConnectHandler
    device = {
        'device_type': 'cisco_ios',
        'ip': device_ip,
        'username': username,
        'password': password,
        'secret': secret,
        'session_log': 'output.log',   # Logs session outputs to a file named 'output.log'.
    }

    # Establish the connection to the device
    connection = ConnectHandler(**device)

    # Check if the provided secret is the same as the password
    if secret == password:
        # If they are the same, enable the privileged mode using that password
        connection.enable()

    # Return the active connection object
    return connection

# Define the main function where the script logic resides
def main():
    # Prompt user for the required credentials
    username = input("Enter username: ")
    password = input("Enter password: ")
    secret = input("Enter secret (or press enter if it's the same as password): ")

    # If the secret is not provided, assume it's the same as the password
    if not secret:
        secret = password

    # Read the list of devices and commands from their respective text files
    device_list = read_file("devices.txt")
    command_list = read_file("commands.txt")

    # Open (or create) a CSV file to save the output
    with open('outputs.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write the headers to the CSV file
        writer.writerow(['Device IP', 'Command', 'Output'])

        # Iterate through each device in the device list
        for device_ip in device_list:
            try:
                print(f"Connecting to {device_ip}...")
                # Establish connection to the current device
                connection = connect_to_device(device_ip, username, password, secret)

                # Iterate through each command in the command list
                for command in command_list:
                    print(f"Executing {command} on {device_ip}...")
                    # Execute the command on the device and get the output
                    output = connection.send_command(command)

                    # Write the output to the CSV file
                    writer.writerow([device_ip, command, output])

                # Close the connection to the current device
                connection.disconnect()
            except Exception as e:
                # Print any errors encountered during the execution
                print(f"Error on {device_ip}: {str(e)}")

    print("Script execution completed!")

# Check if the script is being run as the main module
if __name__ == "__main__":
    # If it is, then execute the main function
    main()
