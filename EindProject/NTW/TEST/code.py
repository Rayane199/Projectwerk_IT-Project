import random

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
    subnet_mask = cidr2dec(cidr)
    total_hosts_needed = rooms * 22  # 20 connections + 1 server + 1 switch + 1 router per room
    ip_decimal = dotted2dec(ip)
    network_address = ip_decimal & subnet_mask
    broadcast_address = network_address + (subnet_mask ^ 0xFFFFFFFF)

    table = []
    for room in range(rooms):
        room_network_address = network_address + room * 32  # 32 IP addresses per room (22 + some buffer)
        first_host = room_network_address + 1
        last_host = room_network_address + 22  # Only assigning 22 hosts per room

        table.append({
            "Room": room + 1,
            "Network": dec2dotted(room_network_address),
            "Subnet Mask": dec2dotted(subnet_mask),
            "Broadcast Address": dec2dotted(room_network_address + 31),
            "First Host": dec2dotted(first_host),
            "Last Host": dec2dotted(last_host)
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
