import ipCalculator as ipCalc

# Configuratie van een Cisco Switch genereren
def genereerSwitchConfig(naamLocatie, lokaalNummer, vlanLokalen, subnetLokaal, subnetmaskLokaal, vlanWifi, subnetWifi, subnetmaskWifi):
    config = []

    # Configuratie van de VLAN voor de lokalen
    vlanId = vlanLokalen + lokaalNummer
    subnetIp = subnetLokaal.split('/')[0]
    ipVlanLokaalDec = ipCalc.dotted2dec(subnetIp) + 2
    ipVlanLokaal = ipCalc.dec2dotted(ipVlanLokaalDec)
    config.append(f"vlan {vlanId}")
    config.append(f" name Lokaal_{lokaalNummer + 1}_{naamLocatie}")
    config.append(f"interface vlan {vlanId}")
    config.append(f" ip address {ipVlanLokaal} {subnetmaskLokaal}")
    config.append(f" no shutdown")
    config.append("!")

    # Configuratie van de VLAN voor de wifi
    wifiIp = subnetWifi.split('/')[0]
    ipVlanWifiDec = ipCalc.dotted2dec(wifiIp) + 2
    ipVlanWifi = ipCalc.dec2dotted(ipVlanWifiDec)
    config.append(f"vlan {vlanWifi}")
    config.append(" name WiFi")
    config.append(f"interface vlan {vlanWifi}")
    config.append(f" ip address {ipVlanWifi} {subnetmaskWifi}")
    config.append(" no shutdown")
    config.append("!")

    # Configuratie van de poorten
    for port in range(1, 21):
        config.append(f"interface GigabitEthernet 0/{port}")
        config.append(f" switchport access vlan {vlanId}")
        config.append(f" switchport mode access")
        config.append("!")

    # Poorten beveiligen met enkele policies mbv port-security (max 2 MAC adressen, restrict violation, aging time 2 min)
    for port in range(1, 21):
        config.append(f"interface GigabitEthernet 0/{port}")
        config.append(f" switchport access vlan {vlanId}")
        config.append(f" switchport mode access")
        config.append(f" switchport port-security")
        config.append(f" switchport port-security maximum 2")
        config.append(f" switchport port-security violation restrict")
        config.append(f" switchport port-security aging time 2")
        config.append("!")
        
    # Ongebruikte poorten op showdown zetten
    for port in range(21, 25):
        config.append(f"interface GigabitEthernet 0/{port}")
        config.append(f" shutdown")
        config.append("!")

    return config

# Configuratie van een Cisco Router genereren met DHCP
def genereerRouterConfig(naamLocatie, vlanLokalen, subnetLokaal, subnetmaskLokaal, vlanWifi, subnetWifi, subnetmaskWifi):
    config = []

    # Config van subinterfaces en DHCP voor elk lokaal
    for i, subnet in enumerate(subnetLokaal):
        vlanId = vlanLokalen + i
        subnetIp = subnet.split('/')[0]
        ipGatewayLokaalDec = ipCalc.dotted2dec(subnetIp) + 1
        ipGatewayLokaal = ipCalc.dec2dotted(ipGatewayLokaalDec)
        dhcpPoolNameLokaal = f"POOL_LOKAAL_{i + 1}_{naamLocatie}"
        
        # Config van subinterface
        config.append(f"interface GigabitEthernet0/0.{vlanId}")
        config.append(f" encapsulation dot1Q {vlanId}")
        config.append(f" ip address {ipGatewayLokaal} {subnetmaskLokaal}")
        config.append(f" no shutdown")
        config.append("!")

        # Config van DHCP
        config.append(f"ip dhcp pool {dhcpPoolNameLokaal}")
        config.append(f" network {subnetIp} {subnetmaskLokaal}")
        config.append(f" default-router {ipGatewayLokaal}")
        config.append(f" dns-server 8.8.8.8")
        config.append("!")

    # Config van subinterface en DHCP voor de wifi
    wifiIp = subnetWifi.split('/')[0]
    ipGatewayWifiDec = ipCalc.dotted2dec(wifiIp) + 1
    ipGatewayWifi = ipCalc.dec2dotted(ipGatewayWifiDec)
    dhcpPoolNameWifi = f"POOL_WIFI_{subnetmaskWifi}"

    config.append(f"interface GigabitEthernet0/0.{vlanWifi}")
    config.append(f" encapsulation dot1Q {vlanWifi}")
    config.append(f" ip address {ipGatewayWifi} {subnetmaskWifi}")
    config.append(f" no shutdown")
    config.append("!")

    config.append(f"ip dhcp pool {dhcpPoolNameWifi}")
    config.append(f" network {wifiIp} {subnetmaskWifi}")
    config.append(f" default-router {ipGatewayWifi}")
    config.append(f" dns-server 8.8.8.8")
    config.append("!")

    # Activeer NAT/PAT
    config.append("ip nat inside source list 1 interface GigabitEthernet0/0 overload")
    config.append("access-list 1 permit 192.168.0.0 0.0.255.255")
    config.append("!")

    return config

# Ansible Playbook genereren
def genereerAnsiblePlaybook(naamLocatie, switchConfigs, routerConfig):
    with open(f'{naamLocatie}_switch_config.yml', 'w') as switch_file:
        switch_file.write('---\n')
        switch_file.write('- hosts: switches\n')
        switch_file.write('  tasks:\n')
        for switchConfig in switchConfigs:
            for line in switchConfig:
                switch_file.write(f'    - name: {line}\n')
                switch_file.write(f'      command: {line}\n')

    with open(f'{naamLocatie}_router_config.yml', 'w') as router_file:
        router_file.write('---\n')
        router_file.write('- hosts: routers\n')
        router_file.write('  tasks:\n')
        for line in routerConfig:
            router_file.write(f'    - name: {line}\n')
            router_file.write(f'      command: {line}\n')

# Aansluitschema genereren
def genereerAansluitschema(naamLocatie, aantalLokalen, vlanLokalen, vlanWifi):
    schema = []
    schema.append(f"Aansluitschema voor {naamLocatie}:\n")
    for i in range(aantalLokalen):
        schema.append(f"Lokaal {i + 1}: VLAN {vlanLokalen + i}")
    schema.append(f"Wi-Fi VLAN: {vlanWifi}")
    
    with open(f'{naamLocatie}_aansluitschema.txt', 'w') as schema_file:
        for line in schema:
            schema_file.write(line + "\n")