import math
import re

def dotted2dec(dotted):
	dotted_split = dotted.split('.')
	a, b, c, d = dotted_split
	a_int = int(a)
	b_int = int(b)
	c_int = int(c)
	d_int = int(d)
	dec = a_int*256**3 + b_int*256**2 + c_int*256 + d_int
	return dec

def dec2dotted(dec):
	getal = int(dec)
	a = getal % 256
	getal = getal // 256
	b = getal % 256
	getal = getal // 256
	c = getal % 256
	getal = getal // 256
	d = getal % 256
	dotted = f'{d}.{c}.{b}.{a}'
	return dotted

def dec2cidr(dec):
	binair = bin(dec)
	cidr = binair.count('1')
	return cidr

def cidr2dec(cidr):
	fill = 32 - cidr
	binair = '1' * cidr
	zerofill = '0' * fill
	binair = binair + zerofill
	dec = int(binair, 2)
	return dec


def dotted2decPlus2(dotted):
	dotted_split = dotted.split('.')
	a, b, c, d = dotted_split
	a_int = int(a)
	b_int = int(b)
	c_int = int(c) + 2
	d_int = int(d)
	dec = a_int*256**3 + b_int*256**2 + c_int*256 + d_int
	return dec

# subnet masker berekenen in codr notatie
# Eerst aantal bits nodig berekenen via log2 op aantal host doen en dan 32 bits verminderen met aantal bits nodig
def berekenSubnetmask(aantalHosts):
	aantalBits = math.ceil(math.log2(aantalHosts + 2)) # +2 omdat netwerk- en broadcastadres
	cidrSubnet = 32 - aantalBits
	return cidrSubnet

# bereken de subnet van elk lokaal en bewaar deze in een array
def berekenSubnetAdresen(ipNetwork, cidrSubnet, aantalSubnets):
    subnets = []
    ipNetworkDec = dotted2dec(ipNetwork)
    increment = 2**(32 - cidrSubnet)
    for i in range(aantalSubnets):
        subnetDec = ipNetworkDec + i * increment
        subnets.append(dec2dotted(subnetDec) + f'/{cidrSubnet}')
    return subnets


# Functie om te checken als een invoer een geldig IP-adres is
def is_valid_ip(ip):
    pattern = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    if pattern.match(ip):
        octets = ip.split(".")
        return all(0 <= int(octet) <= 255 for octet in octets)
    return False

# Functie om een geldig IP-adres te vragen en opnieuw vragen als fout
def ask_for_ip(prompt):
    while True:
        ip = input(prompt)
        if is_valid_ip(ip):
            return ip
        print("Error: Gelieve een geldige IP-adres in te geven.")
        

# Functie om een positieive integer te vragen en opnieuw vragen als fout
def ask_for_integer(prompt, min_value=1, max_value=50):
    while True:
        try:
            value = int(input(prompt))
            if min_value <= value <= max_value:
                return value
            else:
                print(f"Error: Gelieve een getal tussen {min_value} en {max_value} in te geven.")
        except ValueError:
            print("Error: Gelieve een geldig getal in te geven.")