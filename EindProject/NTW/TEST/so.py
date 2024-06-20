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
def generate_ip_table(ip, cidr, rooms, hosts_per_vlan):
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
    
    # Determine the number of subnets needed
    vlans_per_room = 2
    devices_per_room = vlans_per_room * hosts_per_vlan + 4  # 20 hosts, 1 server, 1 switch, 1 router, 1 access point per VLAN
    needed_subnet_size = 32 - (devices_per_room - 1).bit_length()
    required_cidr = max(cidr + 1, needed_subnet_size)
    
    if required_cidr > 30:  # Limit for IPv4 subnets
        print("CIDR too small to accommodate all rooms. Please increase the CIDR or reduce the number of rooms.")
        return

    subnets = list(network.subnets(new_prefix=required_cidr))

    if len(subnets) < rooms:
        print("Not enough subnets to cover all rooms. Please increase the CIDR or reduce the number of rooms.")
        return

    interface_number = 1
    for i in range(rooms):
        room_subnet = subnets[i]
        room_subnets = list(room_subnet.subnets(new_prefix=required_cidr + 1))[:vlans_per_room]
        
        for j, vlan_subnet in enumerate(room_subnets):
            network_address = vlan_subnet.network_address
            devices = [f'Host {k+1}' for k in range(hosts_per_vlan)] + ['Server', 'Switch', 'Router', 'Access Point']
            device_ips = list(vlan_subnet.hosts())[1:len(devices) + 1]  # Exclude the network address

            print(f"\n! Configuration for Room {i+1}")
            for device, ip in zip(devices, device_ips):
                print(f"interface FastEthernet0/{interface_number}")
                print(f"description {device} - {ip} - {vlan_subnet.netmask}")
                print("switchport mode access")
                print(f"switchport access vlan {j+1}")
                print("no shutdown")
                print(f"ip address {ip} {vlan_subnet.netmask}")
                interface_number += 1

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
    hosts_per_vlan = int(input("Enter the number of hosts per VLAN: "))

    generate_ip_table(ip, cidr, rooms, hosts_per_vlan)

if __name__ == "__main__":
    main()