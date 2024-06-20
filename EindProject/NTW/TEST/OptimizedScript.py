
import ipaddress

def generate_ip_table(ip, cidr, rooms):
    try:
        network = ipaddress.IPv4Network(f"{ip}/{cidr}", strict=False)
    except ValueError as e:
        print("Invalid IP address or CIDR:", e)
        return

    # Calculate the number of hosts per VLAN
    hosts_per_vlan = 20
    vlans_per_room = 2
    devices_per_room = vlans_per_room * hosts_per_vlan + 4  # 20 hosts, 1 server, 1 switch, 1 router, 1 access point per VLAN

    # Calculate the required CIDR based on the number of devices per room
    needed_subnet_size = 32 - (devices_per_room - 1).bit_length()
    required_cidr = max(cidr + 1, needed_subnet_size)

    # Check if the required CIDR is feasible
    if required_cidr > 30:
        print("CIDR too small to accommodate all rooms. Please increase the CIDR or reduce the number of rooms.")
        return

    # Generate subnets for each room
    subnets = list(network.subnets(new_prefix=required_cidr))
    if len(subnets) < rooms:
        print("Not enough subnets to cover all rooms. Please increase the CIDR or reduce the number of rooms.")
        return

    # Create the IP address table for each room
    for i in range(rooms):
        room_subnet = subnets[i]
        room_subnets = list(room_subnet.subnets(new_prefix=required_cidr + 1))[:vlans_per_room]

        print(f"\n--- Room {i + 1} ---\n")
        
        # Loop through each VLAN in the room
        for j, vlan_subnet in enumerate(room_subnets):
            network_address = vlan_subnet.network_address
            broadcast_address = vlan_subnet.broadcast_address
            first_host = list(vlan_subnet.hosts())[0]
            last_host = list(vlan_subnet.hosts())[-1]

            # Determine the number of switches needed based on the number of hosts
            num_hosts = vlan_subnet.num_addresses - 4  # Subtract 1 server, 1 switch, 1 router, 1 access point
            num_switches = (num_hosts - 1) // 24 + 1  # Add 1 switch for every 24 hosts
            
            print(f"VLAN {j + 1}:")
            print(f"  Network: {network_address}")
            print(f"  Subnet Mask: {vlan_subnet.netmask}")
            print(f"  Broadcast Address: {broadcast_address}")
            print(f"  First Host: {first_host}")
            print(f"  Last Host: {last_host}")

            # Generate IP addresses for devices
            devices = ['Server', 'Router', 'Access Point'] + [f'Host {k+1}' for k in range(hosts_per_vlan)]
            device_ips = list(vlan_subnet.hosts())[1:num_hosts+1]  # Exclude network address
            device_iter = iter(device_ips)
            
            # Print devices for the VLAN
            for device in devices:
                print(f"  {device}: {next(device_iter)}")

            # Print switches if needed
            for switch_num in range(num_switches):
                switch_network_address = list(room_subnet.subnets(new_prefix=required_cidr + 1 + switch_num))[j].network_address
                switch_broadcast_address = list(room_subnet.subnets(new_prefix=required_cidr + 1 + switch_num))[j].broadcast_address
                print(f"  Switch {switch_num + 1}:")
                print(f"    Network: {switch_network_address}")
                print(f"    Subnet Mask: {vlan_subnet.netmask}")
                print(f"    Broadcast Address: {switch_broadcast_address}")
        
        print("\n" + "-"*40 + "\n")

def main():
    ip = input("Enter the IP address (e.g., 192.168.0.1): ")
    cidr = int(input("Enter the CIDR (e.g., 24): "))
    rooms = int(input("Enter the number of rooms: "))

    generate_ip_table(ip, cidr, rooms)

if __name__ == "__main__":
    main()
