# Notes

## Desktop

The testing device has hardware issue with display ("apple flexgate"). I didn't try configuring any desktop
environment on the laptop.

## Wi-Fi

MacBook Pro 13-inch (2016) comes with Broadcom BCM4350 Wi-Fi chip. FreeBSD 15.x doesn't include a working driver
for the chip.

The testing device runs experimental out-of-tree `if_brcmfmac.ko` [kernel module][1], that adds support for the
Broadcom BCM4350 Wi-Fi chip (PCI device `brcmfmac0@pci0:2:0:0`).

### Setup

```
# Create wlan0 interface and attach it to the brcmfmac0 device
ifconfig wlan0 create wlandev brcmfmac0

# Enable the interface
ifconfig wlan0 up scan

# Connect to the Wi-Fi access point:
# /etc/wpa_supplicant.conf must contain credentials of the AP
wpa_supplicant -iwlan0 -c/etc/wpa_supplicant.conf -B

# Verify the wlan0 interface is associated with the AP
ifconfig wlan0

# Configure the interface through the DHCP
dhclient wlan0
```

[1]: https://github.com/narqo/freebsd-brcmfmac
