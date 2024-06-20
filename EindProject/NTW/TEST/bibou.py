
import ipaddress

# Function to print the default Cisco configuration
def print_default_config():
    print("enable")
    print("configure terminal")
    print("no ip domain-lookup")
    print("line vty 0 4")
    print("login local")
    print("transport input ssh")
    print("exit")

# Function to generate the IP address table
def generate_ip_table(ip, cidr, rooms):
    network = ipaddress.IPv4Network(f"{ip}/{cidr}", strict=False)
    subnet_mask = network.netmask
    wildcard_mask = ipaddress.IPv4Address(int(network.hostmask))
    binary_subnet_mask = ''.join(f'{octet:08b}' for octet in subnet_mask.packed).rstrip('.')
    ip_class = get_ip_class(ip)
    total_hosts = network.num_addresses
    usable_hosts = total_hosts - 2  # Exclude network and broadcast addresses
    
    print("\n--- General Network Information ---\n")
    print(f"IP Address: {ip}")
    print(f"Network Address: {network.network_address}")
    print(f"Usable Host IP Range: {list(network.hosts())[0]} - {list(network.hosts())[-1]}")
    print(f"Broadcast Address: {network.broadcast_address}")
    print(f"Total Number of Hosts: {total_hosts}")
    print(f"Number of Usable Hosts: {usable_hosts}")
    print(f"Subnet Mask: {subnet_mask}")
    print(f"Wildcard Mask: {wildcard_mask}")
    print(f"Binary Subnet Mask: {binary_subnet_mask}")
    print(f"IP Class: {ip_class}")
    print(f"CIDR Notation: /{cidr}")
    print("\n" + "-"*40 + "\n")

    for room in range(1, rooms+1):
        print(f"! Configuration for Room {room}")
        print_default_config()  # Print default Cisco configuration

        print("\n! Router Configuration")
        print("enable")
        print("configure terminal")
        print("no ip domain-lookup")
        print("line vty 0 4")
        print("login local")
        print("transport input ssh")
        print("exit")

        for i in range(1, 21):  # Configure 20 hosts
            print(f"interface FastEthernet0/{i}")
            print(f"description Host - {list(network.hosts())[i]} - {subnet_mask}")
            print("switchport mode access")
            print(f"switchport access vlan {room}")
            print("no shutdown")
            print(f"ip address {list(network.hosts())[i]} {subnet_mask}")

        for j, device in enumerate(['Router', 'Switch', 'Server', 'Access Point']):
            print(f"\n! {device} Configuration")
            print(f"interface FastEthernet0/{i+j+1}")
            print(f"description {device} - {list(network.hosts())[i+j+1]} - {subnet_mask}")
            print("switchport mode access")
            print(f"switchport access vlan {room}")
            print("no shutdown")
            print(f"ip address {list(network.hosts())[i+j+1]} {subnet_mask}")

def get_ip_class(ip):
    first_octet = int(ip.split('.')[0])
    if first_octet <= 127:
        return 'A'
    elif first_octet <= 191:
        return 'B'
    elif first_octet <= 223:
        return 'C'
    elif first_octet <= 239:
        return 'D'
    else:
        return 'E'

def main():
    ip = input("Enter the IP address (e.g., 192.168.0.1): ")
    cidr = int(input("Enter the CIDR (e.g., 24): "))
    rooms = int(input("Enter the number of rooms: "))

    generate_ip_table(ip, cidr, rooms)

if __name__ == "__main__":
    main()
