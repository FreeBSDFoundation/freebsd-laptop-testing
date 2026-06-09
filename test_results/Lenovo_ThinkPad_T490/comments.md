AMD GPU was installed as part of bhyve PCI passthrough testing, so amdgpu wasn't loaded

in rc.conf
kld_list="i915kms cuse"

and in /boot/loader.conf
pptdevs="12/0/0 12/0/1"

For GPU PCIe Passthrough

eGPU is used exclusively in the VM.
