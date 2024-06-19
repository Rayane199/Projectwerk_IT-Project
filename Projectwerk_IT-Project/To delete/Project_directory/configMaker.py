import ipCalculator as ipCalc
import hardwareConfig as hwConfig

# Info over het netwerk vragen aan gebruiker
print('Geef de IP-adres van het netwerk:')
ipNetwork = input()
ipNetworkDec = ipCalc.dotted2dec(ipNetwork)

print('Wat is de naam van de locatie ?')
naamLocatie = input()

print(f'Hoeveel lokalen zullen er zijn in {naamLocatie} ?')
aantalLokalen = int(input())

# Aantal VLANs definieren (aantal lokalen + VLAN Wi-Fi)
aantalVlan = aantalLokalen + 1

# Aantal hosts definieren voor lokalen en wifi
aantalHostsLan = 20
aantalHostsWifi = 20 * aantalLokalen

# Subnet masker berekenen in functie van het aantal lokalen en de subnet berekenen voor de wifi VLAN
subnetLokalenCidr = ipCalc.berekenSubnetmask(aantalHostsLan)
subnetWifiCidr = ipCalc.berekenSubnetmask(aantalHostsWifi)

# Subnet masker omzetten naar decimale notatie en dan naar dotted notatie en deze afprinten
subnetLokalenDec = ipCalc.cidr2dec(subnetLokalenCidr)
subnetLokalenDotted = ipCalc.dec2dotted(subnetLokalenDec)

subnetWifiDec = ipCalc.cidr2dec(subnetWifiCidr)
subnetWifiDotted = ipCalc.dec2dotted(subnetWifiDec)

print(f'Subnet masker voor LAN: {subnetLokalenDotted}')
print(f'Subnet masker voor Wi-Fi: {subnetWifiDotted}')

# Subnet adressen berekenen voor de lokalen
subnetLokalen = ipCalc.berekenSubnetAdresen(ipNetwork, subnetLokalenCidr, aantalLokalen)
vlanLokalen = 10 # Voor de lokalen beginnen we met VLAN 10

# Subnet berekenen voor de wifi netwerk
# hier gaan we van start na de laatste subnet van de lokalen + 1 subnet ertussen laten
wifiNetwerkDec = ipCalc.dotted2dec(ipNetwork) + 2 ** (32-subnetLokalenCidr) + aantalLokalen * (2**(32 - subnetLokalenCidr)) 
WifiNetwerkDotted = ipCalc.dec2dotted(wifiNetwerkDec)
subnetWifi = WifiNetwerkDotted + f'/{subnetWifiCidr}'
vlanWifi = 999 # Voor de wifi gebruiken we VLAN 999

# De subnetten van de lokalen en de wifi afprinten
print(f"\nSubnetten voor de lokalen in {naamLocatie}:")
for i, subnet in enumerate(subnetLokalen):
    print(f"Lokaal {i + 1}: VLAN {vlanLokalen + i}, Subnet {subnet}")

print(f"\nWi-Fi VLAN: VLAN {vlanWifi}, Subnet {subnetWifi}")


# Aan de gebruiker vragen van welk lokaal hij de configuratie wil genereren en dit in een loop
while True:
    print(f"\nVoor welk lokaal (1-{aantalLokalen}) wilt u de configuratie genereren ? (tijp 'exit' om te stoppen): ")
    keuze = input()
    
    if keuze.lower() == 'exit':
        break

    try:
        lokaal = int(keuze) - 1 # -1 omdat de indexen in de array beginnen vanaf 0
        if 0 <= lokaal < aantalLokalen:
            print(f"\n Configuratie gegenereerd voor lokaal {lokaal + 1}:\n")
            switchConfig = hwConfig.genereerSwitchConfig(naamLocatie, lokaal, vlanLokalen, subnetLokalen[lokaal], subnetLokalenDotted, vlanWifi, subnetWifi, subnetWifiDotted)
            for line in switchConfig:
                print(line)
        else:
            print(f"Error: Gelieve een lokaal te kiezen tussen 1 en {aantalLokalen}.")
    except ValueError:
        print("Error: Gelieve een getal in te geven of tijp 'exit' om te stoppen.")

