import ipaddress

def calculate_network_info(ip_address, subnet_mask):
    try:
        network = ipaddress.ip_network(f"{ip_address}/{subnet_mask}", strict=False)
        total_hosts = network.num_addresses
        usable_hosts = total_hosts - 2 if total_hosts > 2 else total_hosts  # Ensure at least 0 usable hosts
        
        # Determine the IP class
        first_octet = int(str(network.network_address).split('.')[0])
        if first_octet <= 126:
            ip_class = 'A'
        elif first_octet <= 191:
            ip_class = 'B'
        elif first_octet <= 223:
            ip_class = 'C'
        else:
            ip_class = 'D/E'

        return {
            "network": network.network_address,
            "address_range": (network.network_address + 1, network.broadcast_address - 1),
            "broadcast": network.broadcast_address,
            "total_hosts": total_hosts,
            "usable_hosts": usable_hosts,
            "subnet_mask": network.netmask,
            "wildcard_mask": network.hostmask,
            "binary_subnet_mask": bin(int(network.netmask)),
            "ip_class": 'A' if network.network_address.is_private else 'B',
            "cidr_notation": network.prefixlen,
            "ip_type": "Private" if network.network_address.is_private else "Public",
            "short": network.network_address.compressed,
            "binary_id": ''.join(f'{int(octet):08b}' for octet in network.network_address.packed),
            "integer_id": int(network.network_address),
            "hex_id": hex(int(network.network_address)),
            "reverse_dns": network.reverse_pointer,
            "ipv4_mapped_address": f'::ffff:{network.network_address}' if network.version == 4 else None,
            "6to4_prefix": network.network_address.exploded if network.version == 6 else None
        }
    except ValueError as e:
        print(f"Error calculating network information: {e}")
        return None

def configure_network(provider_ip, subnet_mask, num_vlans, num_routers, num_switches, num_offices, num_ips_per_office, num_printers, num_access_points):
    print("Network configuration in progress...")
    
    print("Provided IP address:", provider_ip)
    print("Subnet mask:", subnet_mask)
    
    # Additional Information
    print("Default gateway: 192.168.1.1")
    print("DHCP server: 192.168.1.10")
    print("DNS server: 192.168.1.100")
    print("NTP server: 192.168.1.50")
    
    print("Configuring VLANs...")
    for i in range(num_vlans):
        print(f"VLAN {i+1}: Configured and online.")
    
    print("Configuring routers...")
    router_ips = [f"192.168.1.{10 + i}" for i in range(num_routers)]
    for i in range(num_routers):
        print(f"Router {i+1}: Configured and online. IP: {router_ips[i]}")

    print("Configuring access points...")
    ap_ips = [f"192.168.1.{20 + i}" for i in range(num_access_points)]
    for i in range(num_access_points):
        print(f"Access point {i+1}: Configured and online. IP: {ap_ips[i]}")
    
    print("Configuring switches...")
    switch_ips = [f"192.168.1.{30 + i}" for i in range(num_switches)]
    for i in range(num_switches):
        print(f"Switch {i+1}: Configured and online. IP: {switch_ips[i]}")
    
    print("Configuring offices...")
    for i in range(num_offices):
        print(f"Office {i+1}:")
        print(f"  Server IP: 192.168.1.100")
        print(f"  Router IP: {router_ips[i % num_routers]}")
        print(f"  Switch IP: {switch_ips[i % num_switches]}")
        print(f"  Access Point IP: {ap_ips[i % num_access_points]}")
        for j in range(num_vlans):
            print(f"  VLAN {j+1}: Configured and associated with the office.")
    
    print("Configuring IP addresses...")
    for i in range(num_offices):
        print(f"Office {i+1}:")
        print(f"  First IP address: 192.168.{i+1}.1")
        print(f"  Last IP address: 192.168.{i+1}.{num_ips_per_office}")
    
    print("Configuring printers...")
    for i in range(num_printers):
        print(f"Printer {i+1}: Configured and connected. IP: 192.168.1.{40 + i}")
    
    print("The network has been successfully configured!")

def display_configuration(provider_ip, subnet_mask, num_routers, num_switches, num_access_points, num_offices, num_ips_per_office, num_printers):
    provider_ip = provider_ip.strip()
    subnet_mask = subnet_mask.strip()
    network_info = calculate_network_info(provider_ip, subnet_mask)
    
    if network_info is None:
        print("Unable to display network configuration due to errors.")
        return
    
    router_ips = [f"192.168.1.{10 + i}" for i in range(num_routers)]
    ap_ips = [f"192.168.1.{20 + i}" for i in range(num_access_points)]
    switch_ips = [f"192.168.1.{30 + i}" for i in range(num_switches)]

    print("\nNetwork Configuration Summary:")
    print(f"Provided IP address: {provider_ip} / {subnet_mask}")
    print(f"Network IP address: {network_info['network']}")
    print(f"Network address: {network_info['network']}")
    print(f"Usable IP address range: {network_info['address_range'][0]} - {network_info['address_range'][1]}")
    print(f"Broadcast address: {network_info['broadcast']}")
    print(f"Total hosts: {network_info['total_hosts']}")
    print(f"Usable hosts: {network_info['usable_hosts']}")
    print(f"Subnet mask: {network_info['subnet_mask']}")
    print(f"Wildcard mask: {network_info['wildcard_mask']}")
    print(f"Binary subnet mask: {network_info['binary_subnet_mask']}")
    print(f"IP class: {network_info['ip_class']}")
    print(f"CIDR notation: /{network_info['cidr_notation']}")
    print(f"IP type: {network_info['ip_type']}")
    print(f"Short: {network_info['short']}")
    print(f"Binary ID: {network_info['binary_id']}")
    print(f"Integer ID: {network_info['integer_id']}")
    print(f"Hex ID: {network_info['hex_id']}")
    print(f"Reverse DNS: {network_info['reverse_dns']}")
    print(f"IPv4 mapped address: {network_info['ipv4_mapped_address']}")
    print(f"6to4 prefix: {network_info['6to4_prefix']}")

    print("\nRouters and Access Points:")
    for i in range(num_routers):
        print(f"  Router {i+1}: IP: 192.168.1.{10 + i}")
    for i in range(num_access_points):
        print(f"  Access Point {i+1}: IP: 192.168.1.{20 + i}")

    print("\nSwitches:")
    for i in range(num_switches):
        print(f"  Switch {i+1}: IP: 192.168.1.{30 + i}")
    
    print("\nOffices and IP Addresses:")
    for i in range(num_offices):
        print(f"  Office {i+1}: Network 192.168.{i+1}.0/24")
        print(f"    Server IP: 192.168.1.100")
        print(f"    Router IP: {router_ips[i % num_routers]}")
        print(f"    Switch IP: {switch_ips[i % num_switches]}")
        print(f"    Access Point IP: {ap_ips[i % num_access_points]}")
        for j in range(num_vlans):
            print(f"    VLAN {j+1}: IP: 192.168.{i+1}.{100 + j}")  # Example VLAN IP address

    print("\nPrinters:")
    for i in range(num_printers):
        print(f"  Printer {i+1}: IP: 192.168.1.{40 + i}")
    
    print("\nEnd of Summary.\n")

def validate_ip_address(address):
    try:
        ipaddress.ip_address(address)
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    print("Welcome! We will configure the network for your new company.")
    print("Examples of provider IP addresses:")
    print("1. 203.0.113.1 (Mask: 255.255.255.252)")
    print("2. 198.51.100.5 (Mask: 255.255.255.248)")
    
    while True:
        provider_ip = input("Provide an IP address: ").strip()
        if not validate_ip_address(provider_ip):
            print("Invalid IP address. Please enter a valid IP address.")
            continue
              
        subnet_mask = input("Subnet mask or cidr/: ").strip()
                
        try:
            num_offices = int(input("How many offices do you want to configure? "))
            num_vlans = int(input("How many VLANs do you want ? "))
            num_switches = int(input("How many switches do you want? "))
            num_routers = int(input("How many routers do you want? "))
            num_access_points = int(input("How many access points do you want? "))
            num_ips_per_office = int(input("How many IP addresses do you want to allocate per office? "))
            num_printers = int(input("How many printers do you have? "))
        except ValueError:
            print("Invalid input. Please enter integer values for numeric inputs.")
            continue

        display_configuration(provider_ip, subnet_mask, num_routers, num_switches, num_access_points, num_offices, num_ips_per_office, num_printers)
        
        start_configuration = input("Do you want to start the network configuration? (yes/no) ")
        if start_configuration.lower() == "yes":
            configure_network(provider_ip, subnet_mask, num_vlans, num_routers, num_switches, num_offices, num_ips_per_office, num_printers, num_access_points)
            break
        elif start_configuration.lower() == "no":
            continue
        else:
            print("Invalid response. Please answer with 'yes' or 'no'.")
