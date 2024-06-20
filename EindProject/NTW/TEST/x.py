import ipaddress

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

def generate_ip_table(ip, cidr, rooms):
    network = ipaddress.IPv4Network(f"{ip}/{cidr}", strict=False)
    subnet_mask = network.netmask
    total_hosts = rooms * 22  # 20 connections + 1 server + 1 switch + 1 router per room

    print(f"Network: {network}")
    print(f"Subnet Mask: {subnet_mask}")
    print(f"Total Hosts Needed: {total_hosts}")
    
    subnets = list(network.subnets(new_prefix=cidr + 1))  # Example to split into subnets

    table = []
    for i in range(min(len(subnets), rooms)):
        subnet = subnets[i]
        table.append({
            "Room": i + 1,
            "Network": subnet.network_address,
            "Subnet Mask": subnet.netmask,
            "Broadcast Address": subnet.broadcast_address,
            "First Host": list(subnet.hosts())[0],
            "Last Host": list(subnet.hosts())[-1]
        })
    
    for entry in table:
        print(f"Room {entry['Room']}:")
        print(f"  Network: {entry['Network']}")
        print(f"  Subnet Mask: {entry['Subnet Mask']}")
        print(f"  Broadcast Address: {entry['Broadcast Address']}")
        print(f"  First Host: {entry['First Host']}")
        print(f"  Last Host: {entry['Last Host']}")
        print()

def main():
    ip = input("Enter the IP address (e.g., 192.168.0.1): ")
    cidr = int(input("Enter the CIDR (e.g., 24): "))
    rooms = int(input("Enter the number of rooms: "))

    generate_ip_table(ip, cidr, rooms)

if __name__ == "__main__":
    main()