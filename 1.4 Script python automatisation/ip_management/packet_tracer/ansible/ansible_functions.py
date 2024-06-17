# ansible/ansible_functions.py

import subprocess

def configure_with_ansible(host, playbook_path):
    """
    Run an Ansible playbook to configure a network device.

    Args:
        host (str): The hostname or IP address of the target device.
        playbook_path (str): The file path to the Ansible playbook.

    Raises:
        subprocess.CalledProcessError: If the Ansible playbook execution fails.
    """
    try:
        subprocess.run(
            ["ansible-playbook", playbook_path, "-i", host + ","],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error running Ansible playbook: {e}")
        raise
