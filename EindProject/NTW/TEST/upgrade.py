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
    total_hosts_needed = rooms * 22  # 20 connections + 1 server + 1 switch + 1 router per room

    subnets = list(network.subnets(new_prefix=cidr + 1))  # Example to split into subnets

    table = []
    for i in range(min(len(subnets), rooms)):
        subnet = subnets[i]
        network_address = subnet.network_address
        broadcast_address = subnet.broadcast_address
        first_host = list(subnet.hosts())[0]
        last_host = list(subnet.hosts())[-1]

        table.append({
            "Room": i + 1,
            "Network": network_address,
            "Subnet Mask": subnet.netmask,
            "Broadcast Address": broadcast_address,
            "First Host": first_host,
            "Last Host": last_host
        })
    
    # Display the table
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
