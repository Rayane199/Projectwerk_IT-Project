import ipCalculator as ipCalc

# Configuratie van een Cisco switch genereren
def genereerSwitchConfig(naamLocatie, lokaalNummer, vlanLokalen, subnetLokaal, subnetmaskLokaal, vlanWifi, subnetWifi, subnetmaskWifi):
    config = []

    # Configuratie van de VLAN voor de lokalen
    vlanId = vlanLokalen + lokaalNummer
    subnetIp = subnetLokaal.split('/')[0]
    nextSubnetIpDec = ipCalc.dotted2dec(subnetIp) + 1
    nextSubnetIp = ipCalc.dec2dotted(nextSubnetIpDec)
    config.append(f"vlan {vlanId}")
    config.append(f" name Lokaal_{lokaalNummer + 1}_{naamLocatie}")
    config.append(f"interface vlan {vlanId}")
    config.append(f" ip address {nextSubnetIp} {subnetmaskLokaal}")
    config.append(f" no shutdown")
    config.append("!")

    # Configuratie van de VLAN voor de wifi
    wifiIp = subnetWifi.split('/')[0]
    nextWifiIpDec = ipCalc.dotted2dec(wifiIp) + 1
    nextWifiIp = ipCalc.dec2dotted(nextWifiIpDec)
    config.append(f"vlan {vlanWifi}")
    config.append(" name WiFi")
    config.append(f"interface vlan {vlanWifi}")
    config.append(f" ip address {nextWifiIp} {subnetmaskWifi}")
    config.append(" no shutdown")
    config.append("!")

    # Configuratie van de poorten
    for port in range(1, 21):
        config.append(f"interface GigabitEthernet 0/{port}")
        config.append(f" switchport access vlan {vlanId}")
        config.append(f" switchport mode access")
        config.append("!")

    return config
