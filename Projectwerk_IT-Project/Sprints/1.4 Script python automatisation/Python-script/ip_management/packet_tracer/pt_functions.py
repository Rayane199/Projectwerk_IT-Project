# packet_tracer/pt_functions.py

import pka

def configure_packet_tracer(router_name, computer_name, router_ip, computer_ip, subnet_mask, gateway):
    """
    Configure a router and a computer in Packet Tracer with the specified IP settings.

    Args:
        router_name (str): The name of the router.
        computer_name (str): The name of the computer.
        router_ip (str): The IP address for the router.
        computer_ip (str): The IP address for the computer.
        subnet_mask (str): The subnet mask.
        gateway (str): The gateway IP address.

    Raises:
        Exception: If an error occurs while configuring Packet Tracer.
    """
    try:
        session = pka.session()
        topology = session.open("chemin/vers/votre/fichier/topologie.pkt")

        router = topology.get(router_name)
        computer = topology.get(computer_name)

        if not router or not computer:
            raise Exception("Router or computer not found in the topology.")

        router.interface("GigabitEthernet0/0").ip = router_ip
        computer.configure(ip=computer_ip, subnet_mask=subnet_mask, gateway=gateway)

        session.close()
    except Exception as e:
        print(f"Error configuring Packet Tracer: {e}")
        raise
