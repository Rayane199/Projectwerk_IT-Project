import ipaddress

def main():
    ip_str = input("Enter the IP address (e.g., 192.168.0.1): ")
    cidr = int(input("Enter the CIDR (e.g., 24): "))
    rooms = int(input("Enter the number of rooms: "))

    network = ipaddress.IPv4Network(f"{ip_str}/{cidr}", strict=False)

    print("\n--- General Network Information ---\n")
    print(f"IP Address: {network.network_address}")
    print(f"Network Address: {network.network_address}")
    print(f"Usable Host IP Range: {network.network_address + 1} - {network.broadcast_address - 1}")
    print(f"Broadcast Address: {network.broadcast_address}")
    print(f"Total Number of Hosts: {network.num_addresses}")
    print(f"Number of Usable Hosts: {network.num_addresses - 2}")
    print(f"Subnet Mask: {network.netmask}")
    print(f"Wildcard Mask: {network.hostmask}")
    print(f"Binary Subnet Mask: {network.netmask}")
    print(f"IP Class: {network.network_address.__class__.__name__}")
    print(f"CIDR Notation: /{network.prefixlen}")

    print("\n----------------------------------------\n")

    vlans_info = generate_ip_table(network, rooms, cidr)
    print_configuration(vlans_info)

def generate_ip_table(network, rooms, cidr):
    vlans_info = []
    for room in range(1, rooms + 1):
        print(f"\n--- Room {room} ---\n")
        vlans = []
        for vlan in range(1, 3):  # Each room has 2 VLANs
            while True:
                available_hosts = len(list(network.hosts())) - 4 * (vlan - 1)  # Exclude network, broadcast, router, and servers
                hosts = int(input(f"Enter the number of hosts for Room {room}, VLAN {vlan} (default is 20, available: {available_hosts}): ") or 20)
                if hosts <= available_hosts:
                    devices = ['Server', 'Access Point']
                    device_ips = list(network.hosts())[vlan*hosts:(vlan+1)*hosts]
                    num_switches = (hosts + 23) // 24  # Calculate the number of switches needed
                    devices.extend([f"Switch {i+1}" for i in range(num_switches)])
                    vlans.append({
                        "VLAN": vlan,
                        "Network": network,
                        "Subnet Mask": network.netmask,
                        "Broadcast Address": network.broadcast_address,
                        "Router": network.network_address + 1,
                        "Devices": {device: str(device_ips.pop(0)) for device in devices}
                    })
                    break
                else:
                    print(f"Not enough IP addresses in the subnet for Room {room}, VLAN {vlan}. Try again with a smaller number of hosts.")
        vlans_info.append(vlans)
    return vlans_info

def print_configuration(vlans_info):
    for i, vlans in enumerate(vlans_info, start=1):
        print(f"Room {i} Configuration:\n")
        for vlan in vlans:
            print(f"  VLAN {vlan['VLAN']}:")
            print(f"    Network: {vlan['Network']}")
            print(f"    Subnet Mask: {vlan['Subnet Mask']}")
            print(f"    Broadcast Address: {vlan['Broadcast Address']}")
            print(f"    Router: {vlan['Router']}")
            for device, ip in vlan['Devices'].items():
                print(f"    {device}: {ip}")
            print()
        print("----------------------------------------\n")

if __name__ == "__main__":
    main()
