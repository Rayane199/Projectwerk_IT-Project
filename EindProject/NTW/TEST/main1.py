import ipaddress

def calculer_informations_reseau(adresse_ip, masque_sous_reseau):
    reseau = ipaddress.ip_network(f"{adresse_ip}/{masque_sous_reseau}", strict=False)
    return {
        "reseau": reseau.network_address,
        "plage_adresses": (reseau.network_address + 1, reseau.broadcast_address - 1),
        "broadcast": reseau.broadcast_address,
        "masque_sous_reseau": reseau.netmask,
        "masque_wildcard": reseau.hostmask
    }

def configurer_reseau(adresse_fournisseur, masque_sous_reseau, nb_vlan, nb_router, nb_switch, nb_bureaux, nb_ip_par_bureau, nb_imprimantes, nb_access_point):
    print("Configuration du réseau en cours...")
    
    print("Adresse du fournisseur:", adresse_fournisseur)
    print("Masque de sous-réseau:", masque_sous_reseau)
    
    # Informations supplémentaires
    print("Passerelle par défaut: 192.168.1.1")
    print("Serveur DHCP: 192.168.1.10")
    print("Serveur DNS: 192.168.1.100")
    print("Serveur NTP: 192.168.1.50")
    
    print("Configuration des réseaux VLAN...")
    for i in range(nb_vlan):
        print(f"VLAN {i+1}: Configuré et en ligne.")
    
    print("Configuration des routeurs...")
    for i in range(nb_router):
        print(f"Routeur {i+1}: Configuré et en ligne.")
    
    print("Configuration des points d'accès...")
    for i in range(nb_access_point):
        print(f"Point d'accès {i+1}: Configuré et en ligne.")
    
    print("Configuration des commutateurs (switch)...")
    for i in range(nb_switch):
        print(f"Commutateur {i+1}: Configuré et en ligne.")
    
    print("Configuration des bureaux...")
    for i in range(nb_bureaux):
        print(f"Bureau {i+1}:")
        for j in range(nb_vlan):
            print(f"  VLAN {j+1}: Configuré et associé au bureau.")
    
    print("Configuration des adresses IP...")
    for i in range(nb_bureaux):
        print(f"Bureau {i+1}:")
        print(f"  Première adresse IP: 192.168.{i+1}.1")
        print(f"  Dernière adresse IP: 192.168.{i+1}.{nb_ip_par_bureau}")
    
    print("Configuration des imprimantes...")
    for i in range(nb_imprimantes):
        print(f"Imprimante {i+1}: Configurée et connectée.")
    
    print("Le réseau est configuré avec succès !")


def afficher_configuration(adresse_fournisseur, masque_sous_reseau, nb_router, nb_switch, nb_access_point, nb_bureaux, nb_ip_par_bureau, nb_imprimantes):
    adresse_fournisseur = adresse_fournisseur.strip()
    masque_sous_reseau = masque_sous_reseau.strip()
    infos_reseau = calculer_informations_reseau(adresse_fournisseur, masque_sous_reseau)
    
    print("\nRésumé de la configuration du réseau :")
    print("Adresse du fournisseur:", adresse_fournisseur)
    print("Masque de sous-réseau:", masque_sous_reseau)
    print("Réseau:", infos_reseau["reseau"])
    print("Plage d'adresses:", infos_reseau["plage_adresses"])
    print("Adresse de diffusion (Broadcast):", infos_reseau["broadcast"])
    print("Masque joker (Wildcard mask):", infos_reseau["masque_wildcard"])
    
    # Informations supplémentaires
    print("Passerelle par défaut: 192.168.1.1")
    print("Serveur DHCP: 192.168.1.10")
    print("Serveur DNS: 192.168.1.100")
    print("Serveur NTP: 192.168.1.50")
    
    print("\nRouteurs :")
    for i in range(nb_router):
        print(f"  Routeur {i+1}: Configuré")

    print("\nPoints d'accès :")
    for i in range(nb_access_point):
        print(f"  Point d'accès {i+1}: Configuré")
    
    print("\nCommutateurs (Switch) :")
    for i in range(nb_switch):
        print(f"  Commutateur {i+1}: Configuré")
    
    print("\nBureaux et adresses IP :")
    for i in range(nb_bureaux):
        # Calculer les informations du réseau pour chaque bureau
        bureau_reseau = ipaddress.ip_network(f"192.168.{i+1}.0/24", strict=False)
        print(f"  Bureau {i+1}:")
        print(f"    VLAN associé: {i % 2 + 1}")  # Exemple simple d'association VLAN
        print(f"    Réseau: {bureau_reseau.network_address}")
        print(f"    Plage d'adresses: {bureau_reseau.network_address + 1} - {bureau_reseau.broadcast_address - 1}")
        print(f"    Adresse de diffusion: {bureau_reseau.broadcast_address}")
        print(f"    Première adresse IP: 192.168.{i+1}.1")
        print(f"    Dernière adresse IP: 192.168.{i+1}.{nb_ip_par_bureau}")

    print("\nImprimantes :")
    for i in range(nb_imprimantes):
        print(f"  Imprimante {i+1}: Configurée et connectée")
    
    print("\nFin du résumé.\n")


if __name__ == "__main__":
    print("Bienvenue ! Nous allons configurer le réseau pour votre nouvelle société.")
    print("Exemples d'adresses IP de fournisseur :")
    print("1. 203.0.113.1 (Masque: 255.255.255.252)")
    print("2. 198.51.100.5 (Masque: 255.255.255.248)")
    print("3. 192.0.2.17 (Masque: 255.255.255.240)")
    while True:
        adresse_fournisseur = input("Adresse IP du fournisseur : ").strip()
        masque_sous_reseau = input("Masque de sous-réseau du fournisseur : ").strip()
        
        nb_vlan = int(input("Combien de réseaux VLAN souhaitez-vous (1 ou 2) ? "))
        
        nb_router = int(input("Combien de routeurs voulez-vous ? "))
        nb_access_point = int(input("Combien de points d'accès (access points) voulez-vous ? "))
        nb_switch = int(input("Combien de commutateurs (switch) voulez-vous ? "))
        nb_bureaux = int(input("Combien de bureaux voulez-vous configurer ? "))
        nb_ip_par_bureau = int(input("Combien d'adresses IP souhaitez-vous bloquer par bureau ? "))
        nb_imprimantes = int(input("Combien d'imprimantes avez-vous ? "))

        afficher_configuration(adresse_fournisseur, masque_sous_reseau, nb_router, nb_switch, nb_access_point, nb_bureaux, nb_ip_par_bureau, nb_imprimantes)
        
        lancer_configuration = input("Voulez-vous lancer la configuration du réseau ? (oui/non) ")
        if lancer_configuration.lower() == "oui":
            configurer_reseau(adresse_fournisseur, masque_sous_reseau, nb_vlan, nb_router, nb_switch, nb_bureaux, nb_ip_par_bureau, nb_imprimantes, nb_access_point)
            break
        elif lancer_configuration.lower() == "non":
            continue
        else:
            print("Réponse invalide. Veuillez répondre par 'oui' ou 'non'.")

