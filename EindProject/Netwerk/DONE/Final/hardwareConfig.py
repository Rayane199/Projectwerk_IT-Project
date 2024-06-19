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

    return config

# Configuratie van een Cisco Router genereren met DHCP
def genereerRouterConfig(naamLocatie, vlanLokalen, subnetLokaal, subnetmaskLokaal, vlanWifi, subnetWifi, subnetmaskWifi):
    config = []

    # Configuration des sous-interfaces et DHCP pour chaque local
    for i, subnet in enumerate(subnetLokaal):
        vlanId = vlanLokalen + i
        subnetIp = subnet.split('/')[0]
        ipGatewayLokaalDec = ipCalc.dotted2dec(subnetIp) + 1
        ipGatewayLokaal = ipCalc.dec2dotted(ipGatewayLokaalDec)
        dhcpPoolNameLokaal = f"POOL_LOKAAL_{i + 1}_{naamLocatie}"
        
        # Configuration de la sous-interface
        config.append(f"interface GigabitEthernet0/0.{vlanId}")
        config.append(f" encapsulation dot1Q {vlanId}")
        config.append(f" ip address {ipGatewayLokaal} {subnetmaskLokaal}")
        config.append(f" no shutdown")
        config.append("!")

        # Configuration du DHCP
        config.append(f"ip dhcp pool {dhcpPoolNameLokaal}")
        config.append(f" network {subnetIp} {subnetmaskLokaal}")
        config.append(f" default-router {ipGatewayLokaal}")
        config.append(f" dns-server 8.8.8.8")
        config.append("!")

    # Configuration de la sous-interface et DHCP pour le Wi-Fi
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

    return config