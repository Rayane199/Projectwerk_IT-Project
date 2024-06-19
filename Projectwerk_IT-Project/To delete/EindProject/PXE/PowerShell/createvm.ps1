# Set the virtual machine name
$VM_NAME = "my-linux-vm"

# Set the Linux ISO image file path
$ISO_FILE = "C:\path\to\linux.iso"

# Set the virtual machine settings
$VM_RAM = 4096  # Memory in MB
$VM_CPUS = 2    # Number of CPU cores
$VM_DISK = 20   # Disk size in GB

# Create the virtual machine
VBoxManage createvm --name "$VM_NAME" --ostype "Linux_64" --register

# Configure the virtual machine
VBoxManage modifyvm "$VM_NAME" --memory $VM_RAM --cpus $VM_CPUS
VBoxManage createhd --filename "${VM_NAME}.vdi" --size $($VM_DISK * 1024)
VBoxManage storagectl "$VM_NAME" --name "SATA Controller" --add sata --controller IntelAhci
VBoxManage storageattach "$VM_NAME" --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium "${VM_NAME}.vdi"
VBoxManage storageattach "$VM_NAME" --storagectl "SATA Controller" --port 1 --device 0 --type dvddrive --medium "$ISO_FILE"

# Start the virtual machine and install the operating system
VBoxManage startvm "$VM_NAME"