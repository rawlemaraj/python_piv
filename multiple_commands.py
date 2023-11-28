import pandas as pd

# Step 1: Read from an Excel file
def read_excel(file_path, column_names):
    df = pd.read_excel(file_path)
    return df[column_names]

# Step 2: Create a CSV file with hostnames
def create_hostname_csv(data, output_file):
    hostnames = data['hostname'].unique()  # Assuming 'hostname' is one of the columns
    pd.DataFrame(hostnames, columns=['hostname']).to_csv(output_file, index=False)

# Step 3: Read commands from a CSV file
def read_commands(file_path):
    df = pd.read_csv(file_path)
    return df['command'].tolist()  # Assuming 'command' is the column name

# Step 4: Execute commands for each hostname
def execute_commands(hostnames, commands):
    for hostname in hostnames:
        for command in commands:
            # Here you would replace this print statement with the actual command execution logic
            print(f"Running command '{command}' on hostname '{hostname}'")

# Main execution
excel_file_path = 'path_to_your_excel_file.xlsx'
commands_file_path = 'path_to_your_commands_file.csv'
hostname_csv_output = 'hostnames.csv'

excel_data = read_excel(excel_file_path, ['hostname', 'another_column'])  # Replace 'another_column' as needed
create_hostname_csv(excel_data, hostname_csv_output)

hostnames = pd.read_csv(hostname_csv_output)['hostname'].tolist()
commands = read_commands(commands_file_path)

execute_commands(hostnames, commands)
