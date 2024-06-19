# ip_management/ip_functions.py

import ipaddress
from .data import data, used_ips

def parse_ip_range(ip_range):
    """
    Parse an IP range string and return the start and end IP addresses.

    Args:
        ip_range (str): The IP range string (e.g., '192.168.0.2 - 192.168.0.62').

    Returns:
        tuple: A tuple containing the start IP address and the end IP address as strings.
    """
    try:
        start_ip, end_ip = ip_range.split(' - ')
        return start_ip.strip(), end_ip.strip()
    except ValueError:
        raise ValueError("Invalid IP range format. Expected format: 'start_ip - end_ip'.")

def generate_ip_list(start_ip, end_ip):
    """
    Generate a list of IP addresses from a start IP to an end IP.

    Args:
        start_ip (str): The start IP address.
        end_ip (str): The end IP address.

    Returns:
        list: A list of IP addresses as strings.
    """
    try:
        start = ipaddress.ip_address(start_ip)
        end = ipaddress.ip_address(end_ip)
        return [str(ip) for ip in ipaddress.summarize_address_range(start, end)]
    except ValueError as e:
        raise ValueError(f"Invalid IP address: {e}")

def find_available_ip(bureau, vlan):
    """
    Find an available IP address for a given bureau and VLAN.

    Args:
        bureau (int): The bureau number.
        vlan (str): The VLAN name.

    Returns:
        str: An available IP address as a string, or None if no available IP is found.
    """
    for entry in data:
        if entry["Bureau"] == bureau and entry["VLAN"].lower() == vlan.lower():
            try:
                start_ip, end_ip = parse_ip_range(entry["Plage d'adresses IP"])
                ip_list = generate_ip_list(start_ip, end_ip)
                for ip in ip_list:
                    if ip not in used_ips:
                        used_ips.add(ip)
                        return ip
            except ValueError as e:
                print(f"Error processing IP range for bureau {bureau}, VLAN {vlan}: {e}")
                continue
    return None
