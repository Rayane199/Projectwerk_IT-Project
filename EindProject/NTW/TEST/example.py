
import ipaddress

# Function to print the default Cisco configuration
def print_default_config():
    print("enable")
    print("configure terminal")
    print("no ip domain-lookup")
    print("line vty 0 4")
    print("login local")
    print("transport input ssh")
    print("exit")

# Function to generate the IP address table
def generate_ip_table(ip, cidr, rooms):
    network = ipaddress.IPv4Network(f"{ip}/{cidr}", strict=False)
    subnet_mask = network.netmask
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
    print(f"IP Class: {ip_class}")
    print(f"CIDR Notation: /{cidr}")
    print("\n" + "-"*40 + "\n")

    for room in range(1, rooms+1):
        print(f"-----Configuration for Room {room}-----")

        for i in range(1, 21):  # Configure 20 hosts
            print(f"interface FastEthernet0/{i}")
            print(f"description Host - {list(network.hosts())[i]} - {subnet_mask}")
            print("switchport mode access")
            print(f"switchport access vlan {room}")
            print("no shutdown")
            print(f"ip address {list(network.hosts())[i]} {subnet_mask}")

        # Configure extra devices
        extra_devices = ['Router', 'Switch', 'Server', 'Access Point']
        i = 21
        for device in extra_devices:
            print(f"\n! {device} Configuration")
            print(f"description {device} - {list(network.hosts())[i]} - {subnet_mask}")
            print("switchport mode access")
            print(f"switchport access vlan {room}")
            print("no shutdown")
            print(f"ip address {list(network.hosts())[i]} {subnet_mask}")
            i += 1

        # Prompt for additional devices
        while True:
            add_devices = input("Do you want to add more devices? (yes/no): ").lower()
            if add_devices == 'yes':
                device_type = input("Enter device type (Router/Switch/Server/Access Point): ")
                device_count = int(input("Enter the number of devices: "))
                for _ in range(device_count):
                    print(f"\n! {device_type} Configuration")
                    print(f"description {device_type} - {list(network.hosts())[i]} - {subnet_mask}")
                    print("switchport mode access")
                    print(f"switchport access vlan {room}")
                    print("no shutdown")
                    print(f"ip address {list(network.hosts())[i]} {subnet_mask}")
                    i += 1
            elif add_devices == 'no':
                break
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

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
