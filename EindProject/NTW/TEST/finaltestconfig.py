import ipaddress

def generate_ip_table(ip, cidr, rooms):
    network = ipaddress.IPv4Network(f"{ip}/{cidr}", strict=False)
    subnet_mask = network.netmask
    ip_class = get_ip_class(ip)
    total_hosts = network.num_addresses
    usable_hosts = total_hosts - 2  # Exclude network and broadcast addresses
    
    print("\n--- General Network Information ---\n")
    print(f"IP Address: {ip}")
    print(f"Network Address: {network.network_address}")
    print(f"Broadcast Address: {network.broadcast_address}")
    print(f"Total Number of Hosts: {total_hosts}")
    print(f"Number of Usable Hosts: {usable_hosts}")
    print(f"Subnet Mask: {subnet_mask}")
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

    return table

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

def generate_cisco_config(ip, cidr, rooms, ip_table):
    print("\n--- Cisco Configuration ---\n")
    for room in range(1, rooms + 1):
        print(f"! Configuration for Room {room}")
        print("enable")
        print(f"configure terminal")
        print(f"hostname Room{room}")
        print(f"enable secret PASSWORD")  # Replace PASSWORD with the actual password
        print(f"line vty 0 4")
        print(f"login local")
        print(f"transport input ssh")
        print(f"exit")
        
        for vlan in ip_table[room - 1]["Subnets"]:
            print(f"interface FastEthernet0/{vlan['VLAN']}")
            print(f"description VLAN{vlan['VLAN']} - {vlan['Network']} - {vlan['Subnet Mask']}")
            print(f"switchport mode access")
            print(f"switchport access vlan {vlan['VLAN']}")
            print(f"no shutdown")
            
            # Determine the number of hosts in the VLAN
            num_hosts = len(vlan["Devices"])
            
            # Assign IP addresses dynamically based on the number of hosts
            ip_iter = ipaddress.ip_interface(f"{vlan['Network']}/{vlan['Subnet Mask']}")
            for _ in range(num_hosts):
                print(f"ip address {ip_iter.ip} {ip_iter.netmask}")
                ip_iter = ipaddress.ip_interface(ip_iter.ip + 1)
                
            print("\n")
        print(f"exit")

def main():
    ip = input("Enter the IP address (e.g., 192.168.0.1): ")
    cidr = int(input("Enter the CIDR (e.g., 24): "))
    rooms = int(input("Enter the number of rooms: "))

    ip_table = generate_ip_table(ip, cidr, rooms)
    generate_cisco_config(ip, cidr, rooms, ip_table)

if __name__ == "__main__":
    main()