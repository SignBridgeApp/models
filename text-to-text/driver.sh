sudo apt-get update
sudo apt-get install -y cuda-drivers nvidia-kernel-open-545 cuda-drivers-545

wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
rm cuda-keyring_1.1-1_all.deb

sudo apt-get update
sudo apt-get -y install cuda-toolkit-12-3 cudnn-cuda-12 nvidia-cuda-toolkit nvidia-driver-535 nvidia-dkms-535

sudo wget -O- https://developer.download.nvidia.com/compute/cuda/repos/debian12/x86_64/3bf863cc.pub | gpg --dearmor | sudo tee /usr/share/keyrings/nvidia-drivers.gpg
echo 'deb [signed-by=/usr/share/keyrings/nvidia-drivers.gpg] https://developer.download.nvidia.com/compute/cuda/repos/debian12/x86_64/ /' | sudo tee /etc/apt/sources.list.d/nvidia-drivers.list

sudo apt update && sudo apt upgrade -y
sudo apt install nvidia-driver nvidia-settings nvidia-smi nvidia-xconfig nvidia-opencl-icd nvidia-opencl-common nvidia-detect
