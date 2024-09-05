import ipCalculator as ipCalc
import hardwareConfig as hwConfig

# Demander les informations sur le réseau avec validation
ipNetwork = ipCalc.ask_for_ip('Geef de IP-adres van het netwerk: (netwerkadres) ')
naamLocatie = input('Wat is de naam van de locatie ? ')
aantalLokalen = ipCalc.ask_for_integer(f'Hoeveel lokalen zullen er zijn in {naamLocatie}? ', 1, 50)

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
wifiNetwerkDec = ipCalc.dotted2decPlus2(ipNetwork)
WifiNetwerkDotted = ipCalc.dec2dotted(wifiNetwerkDec)
subnetWifi = WifiNetwerkDotted + f'/{subnetWifiCidr}'
vlanWifi = 999 # Voor de wifi gebruiken we VLAN 999

# De subnetten van de lokalen en de wifi afprinten
print(f"\nSubnetten voor de lokalen in {naamLocatie}:")
for i, subnet in enumerate(subnetLokalen):
    print(f"Lokaal {i + 1}: VLAN {vlanLokalen + i}, Subnet {subnet}")

print(f"\nWi-Fi VLAN: VLAN {vlanWifi}, Subnet {subnetWifi}")

# Input control loop
while True:
    print(f"\nVoor welk lokaal (1-{aantalLokalen}) wilt u de switch configuratie genereren ? (tijp 'menu' om alle opties te tonen, 'exit' om te stoppen): ")
    keuze = input().lower()
    
    if keuze == 'exit':
        break

    if keuze == 'menu':
        print("\n Menu:\n")
        print(" 'router': Genereer een configuratie voor de router\n")
        print(" 'ansible': Genereer een Ansible Playbook\n")
        print(" 'schema': Genereer een aansluitschema\n")
        continue

    if keuze == 'router':
        print("\n Configuratie gegenereerd voor de router:\n")
        routerConfig = hwConfig.genereerRouterConfig(naamLocatie, vlanLokalen, subnetLokalen, subnetLokalenDotted, vlanWifi, subnetWifi, subnetWifiDotted)
        for line in routerConfig:
            print(line)
        continue

    if keuze == 'ansible':
        print("\n Genereren van Ansible Playbook...\n")

        all_switch_config = []

        for lokaal in range(aantalLokalen):
            switchConfig = hwConfig.genereerSwitchConfig(naamLocatie, lokaal, vlanLokalen, subnetLokalen[lokaal], subnetLokalenDotted[lokaal], vlanWifi, subnetWifi, subnetWifiDotted)
            all_switch_config.append(switchConfig)
        
        routerConfig = hwConfig.genereerRouterConfig(naamLocatie, vlanLokalen, subnetLokalen, subnetLokalenDotted, vlanWifi, subnetWifi, subnetWifiDotted)
        ansiblePlaybook = hwConfig.genereerAnsiblePlaybook(naamLocatie, all_switch_config, routerConfig)
        print("Ansible Playbook aangemaakt.")
        continue

    if keuze == 'schema':
        print("\nGenereren van aansluitschema...\n")
        schema = hwConfig.genereerAansluitschema(naamLocatie, aantalLokalen, vlanLokalen, vlanWifi)
        print("Aansluitschema aangemaakt.")
        continue

    try:
        lokaal = int(keuze) - 1
        if 0 <= lokaal < aantalLokalen:
            print(f"\n Configuratie gegenereerd voor lokaal {lokaal + 1}:\n")
            switchConfig = hwConfig.genereerSwitchConfig(naamLocatie, lokaal, vlanLokalen, subnetLokalen[lokaal], subnetLokalenDotted[lokaal], vlanWifi, subnetWifi, subnetWifiDotted)
            for line in switchConfig:
                print(line)
        else:
            print(f"Error: Gelieve een lokaal te kiezen tussen 1 en {aantalLokalen}.")
    except ValueError:
        print("Error: Gelieve een geldig getal in te geven of tijp 'exit' om te stoppen.")
