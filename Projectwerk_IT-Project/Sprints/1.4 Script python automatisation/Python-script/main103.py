import ipaddress

def valider_adresse_ip(adresse):
    try:
        ipaddress.ip_address(adresse)
        return True
    except ValueError:
        return False

def valider_masque_sous_reseau(masque):
    try:
        ipaddress.ip_network(f"0.0.0.0/{masque}", strict=False)
        return True
    except ValueError:
        return False

def calculer_info_reseau(adresse_ip, masque_sous_reseau):
    try:
        reseau = ipaddress.ip_network(f"{adresse_ip}/{masque_sous_reseau}", strict=False)
        return {
            "reseau": reseau.network_address,
            "plage_adresses": (reseau.network_address + 1, reseau.broadcast_address - 1),
            "broadcast": reseau.broadcast_address,
            "masque_sous_reseau": reseau.netmask,
            "masque_wildcard": reseau.hostmask,
            "nombre_total_hotes": reseau.num_addresses,
            "nombre_hotes_utilisables": reseau.num_addresses - 2,
            "cidr": reseau.prefixlen,
            "classe_ip": "A" if reseau.is_private else "B" if reseau.num_addresses < 65536 else "C",
            "type_ip": "Privée" if reseau.is_private else "Publique"
        }
    except ValueError as e:
        print(f"Erreur lors du calcul des informations du réseau : {e}")
        return None

def configurer_reseau(adresse_ip, masque_sous_reseau, nombre_vlans, nombre_routeurs, nombre_switches, nombre_bureaux, nombre_ips_par_bureau, nombre_imprimantes, nombre_points_acces):
    print("Configuration du réseau en cours...")
    
    info_reseau = calculer_info_reseau(adresse_ip, masque_sous_reseau)
    if info_reseau is None:
        print("Configuration annulée en raison d'erreurs dans les informations du réseau.")
        return

    print(f"Adresse IP donnée : {adresse_ip} / {masque_sous_reseau}")
    print(f"Réseau : {info_reseau['reseau']} / {info_reseau['masque_sous_reseau']}")
    print(f"Plage d'adresses : {info_reseau['plage_adresses'][0]} - {info_reseau['plage_adresses'][1]}")
    print(f"Adresse de broadcast : {info_reseau['broadcast']}")
    print("Passerelle par défaut : 192.168.1.1")
    print("Serveur DHCP : 192.168.1.10")
    print("Serveur DNS : 192.168.1.100")
    print("Serveur NTP : 192.168.1.50")
    
    pool_ip = (int(info_reseau['plage_adresses'][0]), int(info_reseau['plage_adresses'][1]))
    ip_actuelle = pool_ip[0]

    print("\nConfiguration des VLANs...")
    for i in range(nombre_vlans):
        print(f"  VLAN {i+1} : Configuré et en ligne.")
    
    print("\nConfiguration des routeurs...")
    for i in range(nombre_routeurs):
        print(f"  Routeur {i+1} : Configuré et en ligne. IP : {ipaddress.ip_address(ip_actuelle)}")
        ip_actuelle += 1
    
    print("\nConfiguration des points d'accès...")
    for i in range(nombre_points_acces):
        print(f"  Point d'accès {i+1} : Configuré et en ligne. IP : {ipaddress.ip_address(ip_actuelle)}")
        ip_actuelle += 1
    
    print("\nConfiguration des switches...")
    for i in range(nombre_switches):
        print(f"  Switch {i+1} : Configuré et en ligne. IP : {ipaddress.ip_address(ip_actuelle)}")
        ip_actuelle += 1
    
    print("\nConfiguration des bureaux...")
    for i in range(nombre_bureaux):
        print(f"  Bureau {i+1} :")
        for j in range(nombre_vlans):
            print(f"    VLAN {j+1} : Configuré et associé au bureau.")
    
    print("\nConfiguration des adresses IP...")
    for i in range(nombre_bureaux):
        print(f"  Bureau {i+1} :")
        for j in range(nombre_ips_par_bureau):
            print(f"    Adresse IP : 192.168.{i+1}.{j+1}")
    
    print("\nConfiguration des imprimantes...")
    for i in range(nombre_imprimantes):
        print(f"  Imprimante {i+1} : Configurée et connectée. IP : {ipaddress.ip_address(ip_actuelle)}")
        ip_actuelle += 1
    
    print("\nLe réseau a été configuré avec succès!")

def afficher_configuration(adresse_ip, masque_sous_reseau, nombre_routeurs, nombre_switches, nombre_points_acces, nombre_bureaux, nombre_ips_par_bureau, nombre_imprimantes):
    adresse_ip = adresse_ip.strip()
    masque_sous_reseau = masque_sous_reseau.strip()
    info_reseau = calculer_info_reseau(adresse_ip, masque_sous_reseau)
    
    if info_reseau is None:
        print("Impossible d'afficher la configuration du réseau en raison d'erreurs.")
        return
    
    print("\nRésumé de la configuration réseau :")
    print(f"Adresse IP donnée : {adresse_ip} / {masque_sous_reseau}")
    print(f"Adresse du réseau : {info_reseau['reseau']} / {info_reseau['masque_sous_reseau']}")
    print(f"Plage d'adresses utilisables : {info_reseau['plage_adresses'][0]} - {info_reseau['plage_adresses'][1]}")
    print(f"Adresse de broadcast : {info_reseau['broadcast']}")
    print(f"Nombre total d'hôtes : {info_reseau['nombre_total_hotes']}")
    print(f"Nombre d'hôtes utilisables : {info_reseau['nombre_hotes_utilisables']}")
    print(f"Masque de sous-réseau : {info_reseau['masque_sous_reseau']}")
    print(f"Masque Wildcard : {info_reseau['masque_wildcard']}")
    print(f"Masque de sous-réseau binaire : {bin(int(info_reseau['masque_sous_reseau']))[2:]}")
    print(f"CIDR : /{info_reseau['cidr']}")
    print(f"Classe IP : {info_reseau['classe_ip']}")
    print(f"Type IP : {info_reseau['type_ip']}")
    
    print("\nDétails sur l'adresse IP :")
    print(f"  Adresse IP : {adresse_ip}")
    print(f"  Masque de sous-réseau : {info_reseau['masque_sous_reseau']}")
    print(f"  Adresse de broadcast : {info_reseau['broadcast']}")
    print(f"  Plage d'adresses : {info_reseau['plage_adresses'][0]} - {info_reseau['plage_adresses'][1]}")
    print(f"  Nombre total d'hôtes : {info_reseau['nombre_total_hotes']}")
    print(f"  Nombre d'hôtes utilisables : {info_reseau['nombre_hotes_utilisables']}")
    print(f"  Masque Wildcard : {info_reseau['masque_wildcard']}")
    print(f"  Masque de sous-réseau binaire : {bin(int(info_reseau['masque_sous_reseau']))[2:]}")
    print(f"  CIDR : /{info_reseau['cidr']}")
    print(f"  Classe IP : {info_reseau['classe_ip']}")
    print(f"  Type IP : {info_reseau['type_ip']}")
    
    print("\nRouteurs et Points d'accès :")
    for i in range(nombre_routeurs):
        print(f"  Routeur {i+1} : IP : 192.168.1.{10 + i}")
    for i in range(nombre_points_acces):
        print(f"  Point d'accès {i+1} : IP : 192.168.1.{20 + i}")

    print("\nSwitches :")
    for i in range(nombre_switches):
        print(f"  Switch {i+1} : IP : 192.168.1.{30 + i}")
    
    print("\nBureaux et adresses IP :")
    for i in range(nombre_bureaux):
        print(f"  Bureau {i+1} : Réseau 192.168.{i+1}.0/24")
        print(f"    Plage : 192.168.{i+1}.1 - 192.168.{i+1}.{nombre_ips_par_bureau}")

    print("\nImprimantes :")
    for i in range(nombre_imprimantes):
        print(f"  Imprimante {i+1} : IP : {ipaddress.ip_address(ip_act
