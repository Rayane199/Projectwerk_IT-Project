import random

# Demandes d'informations
ip = input("Entrez l'adresse IP du réseau (par exemple, 192.168.0.1/24) : ")
nb_machines = int(input("Entrez le nombre de machines à connecter : "))

# Séparation de l'adresse IP et du masque de sous-réseau
ip, subnet_mask = ip.split('/')
subnet_mask = int(subnet_mask)

# Conversion du masque de sous-réseau en décimal
subnet_mask = (0xFFFFFFFF >> (32 - subnet_mask)) << (32 - subnet_mask)

# Génération des adresses IP
adresses_ip = []
for _ in range(nb_machines):
    adresse_ip = list(map(int, ip.split('.')))
    adresse_ip[3] = random.randint(1, 254)
    adresses_ip.append('.'.join(map(str, adresse_ip)))

# Génération des numéros de commutateurs, switchs et access points
numeros_commutateurs = [f"Commutateur {i}" for i in range(1, 5)]
numeros_switchs = [f"Switch {i}" for i in range(1, 5)]
numeros_access_points = [f"Access Point {i}" for i in range(1, 5)]

# Tableau complet avec les informations générales et chaque adresse IP attribuée
tableau = [
    ["Adresse IP", "Commutateur", "Switch", "Access Point"],
    *[[adresse_ip, numero_commutateur, numero_switch, numero_access_point] for adresse_ip, numero_commutateur, numero_switch, numero_access_point in zip(adresses_ip, numeros_commutateurs, numeros_switchs, numeros_access_points)],
]

# Affichage du tableau
for ligne in tableau:
    print(" | ".join(ligne))