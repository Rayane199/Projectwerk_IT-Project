import ipaddress

# Helper functions to convert between dotted-decimal and decimal IP formats




def generate_cisco_config(ip, cidr, rooms, ip_table):
    router_config = """
! Router configuration
hostname Router
ip domain-name example.com
crypto key generate rsa modulus 2048
username admin privilege 15 secret admin_password
enable secret enable_password
line vty 0 15
    transport input ssh
    login local
"""

    switch_config = """
! Switch configuration
hostname Switch
enable secret enable_password
ip domain-name example.com
crypto key generate rsa modulus 2048
username admin privilege 15 secret admin_password
line vty 0 15
    transport input ssh
    login local
"""

    vlan_config = """
! VLAN configuration
"""

    port_config = """
! Port configuration
"""

    vlan_id = 10
    for room in range(1, rooms + 1):
        vlan_config += f"\nvlan {vlan_id}\n    name Room{room}\n"
        port_config += f"\n! Room {room} port configuration\n"
        for vlan in ip_table[room - 1]["Subnets"]:
            for device, ip_address in vlan["Devices"].items():
                port_config += f"interface FastEthernet0/{ip_table[room - 1]['Subnets'].index(vlan) * 20 + int(device.split(' ')[-1])}\n"
                port_config += f"    description {device} in Room{room}\n"
                port_config += "    switchport mode access\n"
                port_config += f"    switchport access vlan {vlan_id}\n"
                port_config += f"    ip address {ip_address}/{cidr}\n\n"
        vlan_id += 10

    print("\n--- Cisco Configuration ---\n")
    print(router_config)
    print(switch_config)
    print(vlan_config)
    print(port_config)

    # Additional configurations for other devices/interfaces can be added here

# Rest of the script...


    
    

def dotted2dec(ip):
    ip_split = ip.split('.')
    a, b, c, d = ip_split
    a_int = int(a)
    b_int = int(b)
    c_int = int(c)
    d_int = int(d)
    getal = a_int * 256 ** 3 + b_int * 256 ** 2 + c_int * 256 + d_int
    return getal

def dec2dotted(antwoord):
    getal = int(antwoord)
    a = getal % 256
    getal = getal // 256
    b = getal % 256
    getal = getal // 256
    c = getal % 256
    getal = getal // 256
    d = getal % 256
    ip = f'{d}.{c}.{b}.{a}'
    return ip

def dec2cidr(getal):
    binair = bin(getal)
    i = binair.count('1')
    return i

def cidr2dec(cidr):
    fill = 32 - cidr
    binair = '1' * cidr
    zerofill = '0' * fill
    binair = binair + zerofill
    x = int(binair, 2)
    return x

# Function to generate the IP address table
def generate_ip_table(ip, cidr, rooms):
    network = ipaddress.IPv4Network(f"{ip}/{cidr}", strict=False)
    subnet_mask = network.netmask
    wildcard_mask = ipaddress.IPv4Address(int(network.hostmask))
    binary_subnet_mask = ''.join(f'{octet:08b}.' for octet in subnet_mask.packed).rstrip('.')
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
    hosts_per_vlan = 10  # Assume each VLAN has 10 hosts
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

    table = []
    for i in range(rooms):
        room_subnet = subnets[i]
        room_subnets = list(room_subnet.subnets(new_prefix=required_cidr + 1))[:vlans_per_room]
        
        room_info = {
            "Room": i + 1,
            "Subnets": []
        }

        for j, vlan_subnet in enumerate(room_subnets):
            network_address = vlan_subnet.network_address
            broadcast_address = vlan_subnet.broadcast_address
            first_host = list(vlan_subnet.hosts())[0]
            last_host = list(vlan_subnet.hosts())[-1]
            
            devices = [f'Host {k+1}' for k in range(hosts_per_vlan)] + ['Server', 'Switch', 'Router', 'Access Point']
            device_ips = list(vlan_subnet.hosts())[:len(devices)]

            room_info["Subnets"].append({
                "VLAN": j + 1,
                "Network": network_address,
                "Subnet Mask": vlan_subnet.netmask,
                "Broadcast Address": broadcast_address,
                "First Host": first_host,
                "Last Host": last_host,
                "Devices": {devices[k]: device_ips[k] for k in range(len(devices))}
            })
        
        table.append(room_info)
    
    # Display the table
    for entry in table:
        print(f"Room {entry['Room']}:")
        for subnet in entry["Subnets"]:
            print(f"  VLAN {subnet['VLAN']}:")
            print(f"    Network: {subnet['Network']}")
            print(f"    Subnet Mask: {subnet['Subnet Mask']}")
            print(f"    Broadcast Address: {subnet['Broadcast Address']}")
            print(f"    First Host: {subnet['First Host']}")
            print(f"    Last Host: {subnet['Last Host']}")
            for device, ip in subnet["Devices"].items():
                print(f"    {device}: {ip}")
        print("\n" + "-"*40 + "\n")

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

    ip_table = generate_ip_table(ip, cidr, rooms)
    generate_cisco_config(ip, cidr, rooms, ip_table)

if __name__ == "__main__":
    main()

