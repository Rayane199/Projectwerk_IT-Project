import ipaddress

def calculate_network_info(ip_address, subnet_mask):
    try:
        network = ipaddress.ip_network(f"{ip_address}/{subnet_mask}", strict=False)
        return {
            "network": network.network_address,
            "address_range": (network.network_address + 1, network.broadcast_address - 1),
            "broadcast": network.broadcast_address,
            "subnet_mask": network.netmask,
            "wildcard_mask": network.hostmask
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
    for i in range(num_routers):
        print(f"Router {i+1}: Configured and online. IP: 192.168.1.{10 + i}")

    print("Configuring access points...")
    for i in range(num_access_points):
        print(f"Access point {i+1}: Configured and online. IP: 192.168.1.{20 + i}")
    
    print("Configuring switches...")
    for i in range(num_switches):
        print(f"Switch {i+1}: Configured and online. IP: 192.168.1.{30 + i}")
    
    print("Configuring offices...")
    for i in range(num_offices):
        print(f"Office {i+1}:")
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
    
    print("\nNetwork Configuration Summary:")
    print(f"Provided IP address: {provider_ip} / {subnet_mask}")
    print(f"Network: {network_info['network']} / {network_info['subnet_mask']}")
    print(f"Address range: {network_info['address_range'][0]} - {network_info['address_range'][1]}")
    print(f"Broadcast: {network_info['broadcast']}")
    
    print("\nRouters and Access Points:")
    for i in range(num_routers):
        print(f"  Router {i+1}: IP: 192.168.1.{10 + i}")
    for i in range(num_access_points):
        print(f"  Access point {i+1}: IP: 192.168.1.{20 + i}")

    print("\nSwitches:")
    for i in range(num_switches):
        print(f"  Switch {i+1}: IP: 192.168.1.{30 + i}")
    
    print("\nOffices and IP addresses:")
    for i in range(num_offices):
        print(f"  Office {i+1}: Network 192.168.{i+1}.0/24")
        print(f"    Range: 192.168.{i+1}.1 - 192.168.{i+1}.{num_ips_per_office}")

    print("\nPrinters:")
    for i in range(num_printers):
        print(f"  Printer {i+1}: IP: 192.168.1.{40 + i}")
    
    print("\nEnd of summary.\n")

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
    print("3. 192.0.2.17 (Mask: 255.255.255.240)")
    
    while True:
        provider_ip = input("Provide an IP address: ").strip()
        if not validate_ip_address(provider_ip):
            print("Invalid IP address. Please enter a valid IP address.")
            continue
        
        subnet_mask = input("Subnet mask: ").strip()
        
        try:
            num_vlans = int(input("How many VLANs do you want (1 or 2)? "))
            num_routers = int(input("How many routers do you want? "))
            num_access_points = int(input("How many access points do you want? "))
            num_switches = int(input("How many switches do you want? "))
            num_offices = int(input("How many offices do you want to configure? "))
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
