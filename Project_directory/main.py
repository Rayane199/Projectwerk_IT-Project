# main.py

import sys
from ip_management.ip_functions import find_available_ip
from packet_tracer.pt_functions import configure_packet_tracer
from ansible.ansible_functions import configure_with_ansible

def main():
    # Exemple d'utilisation
    bureau = 1
    vlan = "Wi-Fi"
    available_ip = find_available_ip(bureau, vlan)
    if available_ip:
        print(f"IP disponible pour Bureau {bureau}, VLAN {vlan} : {available_ip}")
        try:
            # Configurer avec Packet Tracer
            configure_packet_tracer("nom_du_routeur", "nom_de_l_ordinateur", "192.168.1.1", available_ip, "255.255.255.0", "192.168.1.1")

            # Configurer avec Ansible
            configure_with_ansible("192.168.1.1", "path/to/your/playbook.yml")

        except Exception as e:
            print(f"Failed to configure devices: {e}")
    else:
        print(f"No available IP found for Bureau {bureau}, VLAN {vlan}")

if __name__ == "__main__":
    main()



# ### //-- main.py
# import sys
# from ip_management.ip_functions import reserve_ip, release_ip, validate_ip
# from packet_tracer.pt_functions import configure_packet_tracer_device
# from ansible.ansible_functions import run_ansible_playbook

# def main():
#     print("Bienvenue dans le script d'automatisation réseau")
    
#     while True:
#         print("\nOptions:")
#         print("1. Réserver une adresse IP")
#         print("2. Libérer une adresse IP")
#         print("3. Valider une adresse IP")
#         print("4. Configurer un appareil dans Packet Tracer")
#         print("5. Exécuter un playbook Ansible")
#         print("6. Quitter")
        
#         choice = input("Choisissez une option: ")
        
#         if choice == '1':
#             ip_address = input("Entrez l'adresse IP à réserver: ")
#             result = reserve_ip(ip_address)
#             if result:
#                 print(f"Adresse IP {ip_address} réservée avec succès.")
#             else:
#                 print(f"Échec de la réservation de l'adresse IP {ip_address}.")
        
#         elif choice == '2':
#             ip_address = input("Entrez l'adresse IP à libérer: ")
#             result = release_ip(ip_address)
#             if result:
#                 print(f"Adresse IP {ip_address} libérée avec succès.")
#             else:
#                 print(f"Échec de la libération de l'adresse IP {ip_address}.")
        
#         elif choice == '3':
#             ip_address = input("Entrez l'adresse IP à valider: ")
#             result = validate_ip(ip_address)
#             if result:
#                 print(f"L'adresse IP {ip_address} est valide.")
#             else:
#                 print(f"L'adresse IP {ip_address} est invalide.")
        
#         elif choice == '4':
#             device_name = input("Entrez le nom de l'appareil à configurer: ")
#             config_result = configure_packet_tracer_device(device_name)
#             if config_result:
#                 print(f"Appareil {device_name} configuré avec succès dans Packet Tracer.")
#             else:
#                 print(f"Échec de la configuration de l'appareil {device_name} dans Packet Tracer.")
        
#         elif choice == '5':
#             playbook_path = input("Entrez le chemin du playbook Ansible: ")
#             ansible_result = run_ansible_playbook(playbook_path)
#             if ansible_result:
#                 print(f"Playbook Ansible {playbook_path} exécuté avec succès.")
#             else:
#                 print(f"Échec de l'exécution du playbook Ansible {playbook_path}.")
        
#         elif choice == '6':
#             print("Quitter le script.")
#             sys.exit()
        
#         else:
#             print("Choix invalide. Veuillez réessayer.")

# if __name__ == "__main__":
#     main()
# ### 