import os
from pyats.topology import loader
from genie.libs.ops.interface.iosxe.interface import Interface
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# get details from the environment
DEVICE_NAME = os.environ.get('DEVICE_NAME')
DEVICE_USERNAME = os.environ.get('DEVICE_USERNAME')
DEVICE_PASSWORD = os.environ.get('DEVICE_PASSWORD')
DEVICE_TYPE = os.environ.get('DEVICE_TYPE')

# load the testbed file
testbed = loader.load('testbed.yaml')

# assign device details from testbed file
device = testbed.devices[DEVICE_NAME]

device.connect(via='cli', alias='uut')

# set correct roles and priorities
correct_values = {
    '*1': {'role': 'Active', 'priority': '1'},
    '2': {'role': 'Member', 'priority': '1'},
    '3': {'role': 'Standby', 'priority': '1'}
}

try:
    # run the command and get the output
    command_output = device.execute('show switch')
    print("Command output: ", command_output)

    # split the output into lines
    lines = command_output.splitlines()
    print("Lines: ", lines)

    start_line = next((i for i, line in enumerate(lines) if '----' in line), None)
    print("Start line: ", start_line)

    switch_lines = lines[start_line + 1:]
    print("Switch lines: ", switch_lines)

    # iterate over each switch
    for switch_line in switch_lines:
        # split the switch detail line into parts
        parts = switch_line.split()
        print("Parts: ", parts)

        # get the switch number (remove any leading asterisk)
        switch_number = parts[0].replace('*', '')

        # get the role and priority
        role = parts[1]
        priority = parts[3]

        print(f'checking switch: {switch_number}')

        # compare the role and priority with the correct values
        if correct_values[switch_number]['role'] == role and correct_values[switch_number]['priority'] == priority:
            # write pass result to file
            with open('output.txt', 'a') as file:
                file.write(f'PASS - Switch {switch_number}: Role {role}, Priority {priority}\n')
        else:
            # write fail result to file
            with open('output.txt', 'a') as file:
                file.write(f'FAIL - Switch {switch_number}: Expected Role {correct_values[switch_number]["role"]}, Priority {correct_values[switch_number]["priority"]}. Got Role {role}, Priority {priority}\n')
except SchemaEmptyParserError as e:
    print("No output from the command.")
