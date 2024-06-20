
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

    subnets = list(network.subnets(new_prefix=cidr + 1))
    table = []

    for i in range(rooms):
        if i >= len(subnets):
            print(f"Not enough subnets to cover room {i + 1}. Please increase the CIDR or reduce the number of rooms.")
            break

        room_subnet = subnets[i]
        room_info = {
            "Room": i + 1,
            "Subnets": []
        }

        for j in range(2):  # Default to 2 VLANs per room
            vlan_subnets = list(room_subnet.subnets(new_prefix=cidr + 1))
            if j >= len(vlan_subnets):
                print(f"Not enough VLANs available in subnet for Room {i + 1}.")
                break

            vlan_subnet = vlan_subnets[j]
            max_hosts = (2 ** (32 - vlan_subnet.prefixlen)) - 2  # Max hosts for the subnet

            while True:
                num_hosts_input = input(f"Enter the number of hosts for Room {i + 1}, VLAN {j + 1} (default is 20): ")
                num_hosts = int(num_hosts_input) if num_hosts_input.isdigit() and int(num_hosts_input) >= 20 else 20

                if num_hosts > max_hosts - 3:
                    print(f"The number of hosts exceeds the maximum allowable hosts for the current subnet ({max_hosts - 3} hosts).")
                    print(f"Please enter a number between 1 and {max_hosts - 3}.")
                else:
                    break

            devices = ['Server', 'Router', 'Access Point'] + [f'Host {k+1}' for k in range(num_hosts)]
            device_ips = list(vlan_subnet.hosts())[0:len(devices)]
            device_iter = iter(device_ips)

            vlan_info = {
                "VLAN": j + 1,
                "Network": vlan_subnet.network_address,
                "Subnet Mask": vlan_subnet.netmask,
                "Broadcast Address": vlan_subnet.broadcast_address,
                "First Host": list(vlan_subnet.hosts())[0],
                "Last Host": list(vlan_subnet.hosts())[-1],
                "Devices": {device: next(device_iter) for device in devices}
            }

            room_info["Subnets"].append(vlan_info)

        table.append(room_info)

    # Display the table
    for entry in table:
        print(f"\n--- Room {entry['Room']} ---\n")
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

def main():
    ip = input("Enter the IP address (e.g., 192.168.0.1): ")
    cidr = int(input("Enter the CIDR (e.g., 24): "))
    rooms = int(input("Enter the number of rooms: "))

    generate_ip_table(ip, cidr, rooms)

if __name__ == "__main__":
    main()
