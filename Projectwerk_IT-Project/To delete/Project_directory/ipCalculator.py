import math

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

