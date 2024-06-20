import ipaddress

# Helper functions to convert between dotted-decimal and decimal IP formats
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
    print()
    
    subnets = list(network.subnets(new_prefix=cidr + 1))  # Example to split into subnets

    table = []
    for i in range(min(len(subnets), rooms)):
        subnet = subnets[i]
        network_address = subnet.network_address
        broadcast_address = subnet.broadcast_address
        first_host = list(subnet.hosts())[0]
        last_host = list(subnet.hosts())[-1]
        
        devices = [f'Host {j+1}' for j in range(20)] + ['Server', 'Switch', 'Router']
        device_ips = list(subnet.hosts())[:len(devices)]

        table.append({
            "Room": i + 1,
            "Network": network_address,
            "Subnet Mask": subnet.netmask,
            "Broadcast Address": broadcast_address,
            "First Host": first_host,
            "Last Host": last_host,
            "Devices": {devices[j]: device_ips[j] for j in range(len(devices))}
        })
    
    # Display the table
    for entry in table:
        print(f"Room {entry['Room']}:")
        print(f"  Network: {entry['Network']}")
        print(f"  Subnet Mask: {entry['Subnet Mask']}")
        print(f"  Broadcast Address: {entry['Broadcast Address']}")
        print(f"  First Host: {entry['First Host']}")
        print(f"  Last Host: {entry['Last Host']}")
        for device, ip in entry["Devices"].items():
            print(f"  {device}: {ip}")
        print()

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
