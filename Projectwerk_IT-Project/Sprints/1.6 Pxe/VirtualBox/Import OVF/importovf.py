import subprocess

# Define the paths and variables
ovf_file = r"C:\Users\slimane\Documents\UbuntuProject Images.ova"
vm_name = "NewUbuntuVM"  # Adjust the VM name as needed

try:
    # Import the OVF file to create the VM
    import_cmd = f'VBoxManage import "{ovf_file}" --vsys 0 --vmname "{vm_name}"'
    subprocess.run(import_cmd, shell=True, check=True)

    # Set network adapter type to NAT
    subprocess.run(f'VBoxManage modifyvm "{vm_name}" --nic1 nat', shell=True, check=True)

    # Start the VM in headless mode
    start_cmd = f'VBoxManage startvm "{vm_name}" --type headless'
    subprocess.run(start_cmd, shell=True, check=True)

    print(f"VM {vm_name} created and started successfully.")

except subprocess.CalledProcessError as e:
    print(f"Error: {e}")
