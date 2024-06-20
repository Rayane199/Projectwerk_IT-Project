import ipaddress

def calculer_info_reseau(adresse_ip, masque_sous_reseau):
    try:
        reseau = ipaddress.ip_network(f"{adresse_ip}/{masque_sous_reseau}", strict=False)
        return {
            "reseau": reseau.network_address,
            "plage_adresses": (reseau.network_address + 1, reseau.broadcast_address - 1),
            "broadcast": reseau.broadcast_address,
            "masque_sous_reseau": reseau.netmask,
            "masque_wildcard": reseau.hostmask
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
    print(f"Réseau : {info_reseau['reseau']} / {info_reseau['masque_sous_reseau']}")
    print(f"Plage d'adresses : {info_reseau['plage_adresses'][0]} - {info_reseau['plage_adresses'][1]}")
    print(f"Adresse de broadcast : {info_reseau['broadcast']}")
    
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
        print(f"  Imprimante {i+1} : IP : 192.168.1.{40 + i}")
    
    print("\nFin du résumé.\n")

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

if __name__ == "__main__":
    print("Bienvenue ! Nous allons configurer le réseau pour votre nouvelle entreprise.")
    print("Exemples d'adresses IP :")
    print("1. 203.0.113.1 (Masque : 255.255.255.252)")
    print("2. 198.51.100.5 (Masque : 255.255.255.248)")
    print("3. 192.0.2.17 (Masque : 255.255.255.240)")
    
    while True:
        adresse_ip = input("Veuillez fournir une adresse IP : ").strip()
        if not valider_adresse_ip(adresse_ip):
            print("Adresse IP invalide. Veuillez entrer une adresse IP valide.")
            continue
        
        while True:
            masque_sous_reseau = input("Masque de sous-réseau ou CIDR : ").strip()
            if not valider_masque_sous_reseau(masque_sous_reseau):
                print("Masque de sous-réseau invalide. Veuillez entrer un masque de sous-réseau valide.")
            else:
                break
        
        try:
            nombre_vlans = int(input("Combien de VLANs voulez-vous (1 ou 2) ? "))
            nombre_routeurs = int(input("Combien de routeurs voulez-vous ? "))
            nombre_points_acces = int(input("Combien de points d'accès voulez-vous ? "))
            nombre_switches = int(input("Combien de switches voulez-vous ? "))
            nombre_bureaux = int(input("Combien de bureaux voulez-vous configurer ? "))
            nombre_ips_par_bureau = int(input("Combien d'adresses IP voulez-vous allouer par bureau ? "))
            nombre_imprimantes = int(input("Combien d'imprimantes avez-vous ? "))
        except ValueError:
            print("Entrée invalide. Veuillez entrer des valeurs entières pour les entrées numériques.")
            continue

        afficher_configuration(adresse_ip, masque_sous_reseau, nombre_routeurs, nombre_switches, nombre_points_acces, nombre_bureaux, nombre_ips_par_bureau, nombre_imprimantes)
        
        demarrer_configuration = input("Voulez-vous démarrer la configuration du réseau ? (oui/non) ")
        if demarrer_configuration.lower() == "oui":
            configurer_reseau(adresse_ip, masque_sous_reseau, nombre_vlans, nombre_routeurs, nombre_switches, nombre_bureaux, nombre_ips_par_bureau, nombre_imprimantes, nombre_points_ac
