# Configuratie van een Cisco switch genereren
def genereerSwitchConfig(naamLocatie, lokaalNummer, vlanLokalen, subnetLokaal, subnetmaskLokaal, vlanWifi, subnetWifi, subnetmaskWifi):
    config = []

    # Configuratie van de VLAN voor de lokalen
    vlanId = vlanLokalen + lokaalNummer
    subnetIp = subnetLokaal.split('/')[0]
    config.append(f"vlan {vlanId}")
    config.append(f" name Lokaal_{lokaalNummer + 1}_{naamLocatie}")
    config.append(f"interface vlan {vlanId}")
    config.append(f" ip address {subnetIp + 1} {subnetmaskLokaal}")
    config.append(f" no shutdown")
    config.append("!")

    # Configuratie van de VLAN voor de wifi
    wifiIp = subnetWifi.split('/')[0]
    config.append(f"vlan {vlanWifi}")
    config.append(" name WiFi")
    config.append(f"interface vlan {vlanWifi}")
    config.append(f" ip address {wifiIp + 1} {subnetmaskWifi}")
    config.append(" no shutdown")
    config.append("!")

    # Configuratie van de poorten
    for port in range(1, 21):
        config.append(f"interface GigabitEthernet 0/{port}")
        config.append(f" switchport access vlan {vlanId}")
        config.append(f" switchport mode access")
        config.append("!")

    return config
