import sys
from pyats.topology import loader
from genie.libs.ops.interface.iosxe.interface import Interface as InterfaceOps
from genie.libs.parser.iosxe.show_interface import ShowInterfaces

def collect_configs(switch_list):
    testbed = loader.load('your_testbed_file.yaml')
    configs = {}
    failed_switches = []

    for switch in switch_list:
        try:
            device = testbed.devices[switch]
            device.connect()
            
            # Collect configurations here, e.g., using Genie parsers
            interface_ops = InterfaceOps(device)
            interface_ops.learn()
            configs[switch] = interface_ops.info

            device.disconnect()
        except Exception as e:
            print(f"Failed to collect config from {switch}: {str(e)}")
            failed_switches.append(switch)

    return configs, failed_switches

if __name__ == "__main__":
    switches = sys.argv[1:]  # Switch hostnames passed as command-line arguments
    configs, failed_switches = collect_configs(switches)
    
    # Output the configurations and failed switches
    print("Collected Configurations:")
    print(configs)
    print("\nFailed Switches:")
    print(failed_switches)
