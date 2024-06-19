import getpass
import os
import yaml

# Function to encrypt password
def encrypt_password(password):
    return password.encode('utf-8')

# Function to generate YAML file
def generate_yaml_file():
    # Get user input
    hostname = input("Enter the hostname (e.g., myrouter): ")  # Example: myrouter
    domain_name = input("Enter the domain name (e.g., example.com): ")  # Example: example.com
    ssh_version = input("Enter the SSH version (e.g., 2): ")  # Example: 2
    ssh_timeout = input("Enter the SSH timeout (e.g., 60): ")  # Example: 60
    ssh_retries = input("Enter the SSH authentication retries (e.g., 5): ")  # Example: 5
    admin_password = getpass.getpass("Enter the admin password: ")
    admin_password = encrypt_password(admin_password)
    ospf_process_id = input("Enter the OSPF process ID (e.g., 1): ")  # Example: 1
    ospf_networks = input("Enter the OSPF networks (comma-separated, e.g., 10.0.0.0/24, 192.168.1.0/24): ")  # Example: 10.0.0.0/24, 192.168.1.0/24
    ospf_networks = ospf_networks.split(',')
    ospf_networks = [network.strip() for network in ospf_networks]
    vlan_ids = input("Enter the VLAN IDs (comma-separated, e.g., 10, 20, 30): ")  # Example: 10, 20, 30
    vlan_ids = vlan_ids.split(',')
    vlan_ids = [int(id) for id in vlan_ids]
    vlan_names = input("Enter the VLAN names (comma-separated, e.g., Management, Data, Voice): ")  # Example: Management, Data, Voice
    vlan_names = vlan_names.split(',')
    vlan_names = [name.strip() for name in vlan_names]
    vlan_ip_addresses = input("Enter the VLAN IP addresses (comma-separated, e.g., 192.168.10.1, 192.168.20.1, 192.168.30.1): ")  # Example: 192.168.10.1, 192.168.20.1, 192.168.30.1
    vlan_ip_addresses = vlan_ip_addresses.split(',')
    vlan_ip_addresses = [address.strip() for address in vlan_ip_addresses]
    vlan_subnet_masks = input("Enter the VLAN subnet masks (comma-separated, e.g., 255.255.255.0, 255.255.255.0, 255.255.255.0): ")  # Example: 255.255.255.0, 255.255.255.0, 255.255.255.0
    vlan_subnet_masks = vlan_subnet_masks.split(',')
    vlan_subnet_masks = [mask.strip() for mask in vlan_subnet_masks]
    default_gateway = input("Enter the default gateway (e.g., 192.168.10.254): ")  # Example: 192.168.10.254
    ethernet_interfaces = input("Enter the Ethernet interfaces (comma-separated, e.g., Ethernet0/0, Ethernet0/1, Ethernet0/2): ")  # Example: Ethernet0/0, Ethernet0/1, Ethernet0/2
    ethernet_interfaces = ethernet_interfaces.split(',')
    ethernet_interfaces = [interface.strip() for interface in ethernet_interfaces]
    ethernet_descriptions = input("Enter the Ethernet interface descriptions (comma-separated, e.g., 'Uplink', 'LAN', 'DMZ'): ")  # Example: Uplink, LAN, DMZ
    ethernet_descriptions = ethernet_descriptions.split(',')
    ethernet_descriptions = [description.strip() for description in ethernet_descriptions]
    ethernet_modes = input("Enter the Ethernet interface modes (comma-separated, e.g., 'access', 'trunk', 'routed'): ")  # Example: access, trunk, routed
    ethernet_modes = ethernet_modes.split(',')
    ethernet_modes = [mode.strip() for mode in ethernet_modes]
    ethernet_vlans = input("Enter the Ethernet interface VLANs (comma-separated, e.g., '10', '20,30', '': ")  # Example: 10, 20,30, 
    ethernet_vlans = ethernet_vlans.split(',')
    ethernet_vlans = [vlan.strip() for vlan in ethernet_vlans]

    # Generate YAML file
    yaml_data = {
        'hosts': 'routers',
        'connection': 'network_cli',
        'gather_facts': False,
        'tasks': [
            {
                'name': 'Set hostname and domain name',
                'ios_system': {
                    'hostname': hostname,
                    'domain_name': domain_name
                }
            },
            {
                'name': 'Generate RSA key pair for SSH',
                'ios_config': {
                    'lines': ['crypto key generate rsa']
                }
            },
            {
                'name': 'Configure SSH settings',
                'ios_config': {
                    'lines': [
                        f'ip ssh version {ssh_version}',
                        f'ip ssh time-out {ssh_timeout}',
                        f'ip ssh authentication-retries {ssh_retries}'
                    ]
                }
            },
            {
                'name': 'Create local user',
                'ios_user': {
                    'name': 'admin',
                    'privilege': 15,
                    'password': admin_password,
                    'state': 'present'
                }
            },
            {
                'name': 'Enable password encryption',
                'ios_config': {
                    'lines': ['service password-encryption']
                }
            },
            {
                'name': 'Configure OSPF',
                'ios_ospf': {
                    'process_id': ospf_process_id,
                    'networks': [
                        {
                            'prefix': network,
                            'wildcard_bits': '0.0.0.255',
                            'area': '0'
                        } for network in ospf_networks
                    ]
                }
            },
            {
                'name': 'Configure VLANs',
                'ios_vlan': [
                    {
                        'vlan_id': vlan_id,
                        'name': vlan_name
                    } for vlan_id, vlan_name in zip(vlan_ids, vlan_names)
                ]
            },
            {
                'name': 'Configure VLAN interfaces',
                'ios_interface': [
                    {
                        'name': f'Vlan{vlan_id}',
                        'description': vlan_name,
                        'enabled': True,
                        'ip_address': vlan_ip_address,
                        'subnet_mask': vlan_subnet_mask
                    } for vlan_id, vlan_name, vlan_ip_address, vlan_subnet_mask in zip(vlan_ids, vlan_names, vlan_ip_addresses, vlan_subnet_masks)
                ]
            },
            {
                'name': 'Configure Ethernet interfaces',
                'ios_interface': [
                    {
                        'name': interface,
                        'description': description,
                        'mode': mode,
                        'access_vlan': vlan if mode == 'access' else None,
                        'trunk_allowed_vlans': vlan if mode == 'trunk' else None
                    } for interface, description, mode, vlan in zip(ethernet_interfaces, ethernet_descriptions, ethernet_modes, ethernet_vlans)
                ]
            },
            {
                'name': 'Configure default gateway',
                'ios_config': {
                    'lines': [f'ip route 0.0.0.0 0.0.0.0 {default_gateway}']
                }
            },
            {
                'name': 'Enable required services',
                'ios_config': {
                    'lines': [
                        'ip routing',
                        'ip http server',
                        'ip telnet server'
                    ]
                }
            }
        ]
    }

    # Save YAML file
    with open('playbook.yaml', 'w') as file:
        yaml.dump(yaml_data, file, default_flow_style=False)

    print("YAML file 'playbook.yaml' has been successfully created.")

# Generate YAML file
generate_yaml_file()
