import os
import subprocess
import argparse
import urllib.request

def download_debian_iso():
    iso_url = "https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/debian-12.5.0-amd64-netinst.iso"
    iso_file = "./debian.iso"
    if not os.path.isfile(iso_file):
        print(f"Downloading Debian ISO from {iso_url}...")
        urllib.request.urlretrieve(iso_url, iso_file)
        print("Download complete.")
    else:
        print(f"{iso_file} already exists, skipping download.")

def create_vm(machine_name):
    # Create VM
    subprocess.run(["VBoxManage", "createvm", "--name", machine_name, "--ostype", "Debian_64", "--register"])

    # Set memory and network
    subprocess.run(["VBoxManage", "modifyvm", machine_name, "--ioapic", "on"])
    subprocess.run(["VBoxManage", "modifyvm", machine_name, "--memory", "1024"])
    subprocess.run(["VBoxManage", "modifyvm", machine_name, "--vram", "128"])
    subprocess.run(["VBoxManage", "modifyvm", machine_name, "--nic1", "nat"])

    # Create Disk
    subprocess.run(["VBoxManage", "createhd", "--filename", f"{os.getcwd()}/{machine_name}/{machine_name}_DISK.vdi",
                    "--size", "80000", "--format", "VDI"])

    # Attach Debian Iso
    subprocess.run(["VBoxManage", "storagectl", machine_name, "--name", "SATA Controller", "--add", "sata", "--controller", "IntelAhci"])
    subprocess.run(["VBoxManage", "storageattach", machine_name, "--storagectl", "SATA Controller", "--port", "0", "--device", "0",
                    "--type", "hdd", "--medium", f"{os.getcwd()}/{machine_name}/{machine_name}_DISK.vdi"])
    subprocess.run(["VBoxManage", "storagectl", machine_name, "--name", "IDE Controller", "--add", "ide", "--controller", "PIIX4"])
    subprocess.run(["VBoxManage", "storageattach", machine_name, "--storagectl", "IDE Controller", "--port", "1", "--device", "0",
                    "--type", "dvddrive", "--medium", "./debian.iso"])
    subprocess.run(["VBoxManage", "modifyvm", machine_name, "--boot1", "dvd", "--boot2", "disk", "--boot3", "none", "--boot4", "none"])

    # Enable RDP
    subprocess.run(["VBoxManage", "modifyvm", machine_name, "--vrde", "on"])
    subprocess.run(["VBoxManage", "modifyvm", machine_name, "--vrdemulticon", "on", "--vrdeport", "10001"])

    # Start the VM
    subprocess.Popen(["VBoxHeadless", "--startvm", machine_name])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to create and start a VirtualBox VM")
    parser.add_argument("machine_name", type=str, help="Name of the Virtual Machine")
    args = parser.parse_args()

    # Download Debian ISO if not already present
    download_debian_iso()

    # Create and configure VM
    create_vm(args.machine_name)
