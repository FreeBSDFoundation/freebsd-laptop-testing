# Notes

## Experience
I have no issues with FreeBSD on this laptop. There are no problems preventing
me from using FreeBSD as the primary operating system on this laptop.  

## GPU
This laptop features an Intel iGPU  and a discrete NVIDIA GPU (NVIDIA Quadro M1200 Mobile). 
Currently, I only use the NVIDIA GPU and have enabled Discrete Graphics mode in the BIOS. I have installed driver version 580.178.04 from https://nvidia.com/en-us/driver/unix. This GPU is supported up through the NVIDIA 580.xx drivers, which is why it did not work with version 595.84. 
After extracting the driver to a temporary location, I ran `nvidia-xconfig` to generate the configuration automatically. My /etc/rc.conf now contains `kld_list="nvidia nvidia-modeset"` and `linux_enable="YES"`.
To adjust backlight brightness, I use the command `nvidia-settings -a backlightbrightness=VALUE` (replacing VALUE with a number from 0 to 100). To query the current brightness level, use `nvidia-settings -q backlightbrightness`. 
It is also possible to use the iGPU. To do so, set the graphics mode to Hybrid in the BIOS and follow the FreeBSD Handbook instructions for setting up an Intel graphics card.

## Contact
Feel free to reach out if you have tried running FreeBSD on a P51 and ran into issues. We can compare configuration files and try to troubleshoot together.
