# main.py

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



