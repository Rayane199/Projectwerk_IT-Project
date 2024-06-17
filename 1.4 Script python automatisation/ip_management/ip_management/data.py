# ip_management/data.py

data = [
    {"Bureau": 1, "VLAN": "Wi-Fi", "Sous-réseau": "192.168.0.0/26", "Plage d'adresses IP": "192.168.0.2 - 192.168.0.62"},
    {"Bureau": 1, "VLAN": "Ethernet", "Sous-réseau": "192.168.0.64/26", "Plage d'adresses IP": "192.168.0.66 - 192.168.0.126"},
    {"Bureau": 2, "VLAN": "Wi-Fi", "Sous-réseau": "192.168.0.128/26", "Plage d'adresses IP": "192.168.0.130 - 192.168.0.190"},
    {"Bureau": 2, "VLAN": "Ethernet", "Sous-réseau": "192.168.0.192/26", "Plage d'adresses IP": "192.168.0.194 - 192.168.1.254"},
    {"Bureau": 3, "VLAN": "Wi-Fi", "Sous-réseau": "192.168.1.0/26", "Plage d'adresses IP": "192.168.1.2 - 192.168.1.62"},
    {"Bureau": 3, "VLAN": "Ethernet", "Sous-réseau": "192.168.1.64/26", "Plage d'adresses IP": "192.168.1.66 - 192.168.1.126"},
    # Ajouter le reste des données...
]

used_ips = set([
    '192.168.0.1', '192.168.0.2', '192.168.0.65', '192.168.0.66',
    '192.168.0.129', '192.168.0.130', '192.168.0.193', '192.168.0.194',
    '192.168.1.1', '192.168.1.2', '192.168.1.65', '192.168.1.66'
])
