import pandas as pd

# Step 1: Read from an Excel file from a specific tab
def read_excel(file_path, sheet_name, column_names):
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    return df[column_names]

# Step 2: Create a CSV file with combined data as hostnames
def create_hostname_csv(data, column_names, output_file):
    # Combine the columns into one and name it 'Hostname'
    data['Hostname'] = data[column_names].astype(str).agg(' '.join, axis=1)
    data[['Hostname']].to_csv(output_file, index=False)

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
sheet_name = 'your_sheet_name'  # Replace with your Excel sheet name
commands_file_path = 'path_to_your_commands_file.csv'
hostname_csv_output = 'hostnames.csv'
column_names = ['ColumnA', 'ColumnB']  # Replace with your actual column names

excel_data = read_excel(excel_file_path, sheet_name, column_names)
create_hostname_csv(excel_data, column_names, hostname_csv_output)

hostnames = pd.read_csv(hostname_csv_output)['Hostname'].tolist()
commands = read_commands(commands_file_path)

execute_commands(hostnames, commands)
