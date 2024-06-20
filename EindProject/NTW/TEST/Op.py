
import ipaddress

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

def generate_ip_table(ip, cidr, rooms):
    try:
        network = ipaddress.IPv4Network(f"{ip}/{cidr}", strict=False)
    except ValueError as e:
        print("Invalid IP address or CIDR:", e)
        return

    subnet_mask = network.netmask
    wildcard_mask = ipaddress.IPv4Address(int(network.hostmask))
    binary_subnet_mask = ''.join(f'{octet:08b}.' for octet in subnet_mask.packed).rstrip('.')
    ip_class = get_ip_class(ip)
    total_hosts = network.num_addresses
    usable_hosts = total_hosts - 2  # Exclude network and broadcast addresses

    # Print general network information
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
    hosts_per_vlan = 20  # Default number of hosts per VLAN
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

            # Prompt user for the number of hosts per VLAN
            num_hosts = hosts_per_vlan  # Default number of hosts
            user_input = input(f"Enter the number of hosts for Room {i + 1}, VLAN {j + 1} (default is 20): ")
            if user_input.isdigit():
                num_hosts = int(user_input)
            if num_hosts < hosts_per_vlan:
                num_hosts = hosts_per_vlan

            # Determine the number of switches needed based on the number of hosts
            num_switches = (num_hosts - 1) // 24 + 1  # Add 1 switch for every 24 hosts

            devices = ['Server', 'Router', 'Access Point'] + [f'Host {k+1}' for k in range(num_hosts)]
            device_ips = list(vlan_subnet.hosts())[0:len(devices)]
            device_iter = iter(device_ips)

            vlan_info = {
                "VLAN": j + 1,
                "Network": network_address,
                "Subnet Mask": vlan_subnet.netmask,
                "Broadcast Address": broadcast_address,
                "First Host": first_host,
                "Last Host": last_host,
                "Devices": {device: next(device_iter) for device in devices}
            }

            room_info["Subnets"].append(vlan_info)

            # Add switches
            for switch_num in range(num_switches):
                switch_info = {
                    "Switch": switch_num + 1,
                    "Network": network_address,
                    "Subnet Mask": vlan_subnet.netmask,
                    "Broadcast Address": broadcast_address,
                }
                room_info["Subnets"].append(switch_info)

        table.append(room_info)

    # Display the table
    for entry in table:
        print(f"\n--- Room {entry['Room']} ---\n")
        for subnet in entry["Subnets"]:
            if "VLAN" in subnet:
                print(f"  VLAN {subnet['VLAN']}:")
            if "Switch" in subnet:
                print(f"  Switch {subnet['Switch']}:")
            print(f"    Network: {subnet['Network']}")
            print(f"    Subnet Mask: {subnet['Subnet Mask']}")
            print(f"    Broadcast Address: {subnet['Broadcast Address']}")
            if "VLAN" in subnet:
                print(f"    First Host: {subnet['First Host']}")
                print(f"    Last Host: {subnet['Last Host']}")
                for device, ip in subnet["Devices"].items():
                    print(f"    {device}: {ip}")
        print("\n" + "-"*40 + "\n")

def main():
    ip = input("Enter the IP address (e.g., 192.168.0.1): ")
    cidr = int(input("Enter the CIDR (e.g., 24): "))
    rooms = int(input("Enter the number of rooms: "))

    generate_ip_table(ip, cidr, rooms)

if __name__ == "__main__":
    main()
