# Additional testing notes

## FreeBSD version

FreeBSD 15.1-RELEASE amd64, fresh install from distrubution sets

## Wireless networking

Built-in Intel wireless adapter associates successfully with 802.11ac access point with iwlwifi.

However, the interface does not seem to be able to pass usable network traffic.

Observed:

- scanning works
- WPA2 association succeeds
- interface reports "status: associated"
- DHCP repeatedly sends DHCPDISCOVER but doesn't receive a lease
- manual IP configuration and adding default route doesn't result in usable network traffic
- USB ethernet adapter ue0 worked on same network

Also tested on 15.1-STABLE.

Disabling HT / VHT allowed connectivity on another network (/boot/loader.conf.d/iwlwifi.conf):

```
compat.linuxkpi.80211.hw_crypto=1
compat.linuxkpi.iwlwifi_11n_disable=1
compat.linuxkpi.iwlwifi_disable_11n=0
compat.linuxkpi.iwlwifi_disable_11ac=1
```


```
iwlwifi0@pci0:0:20:3:   class=0x028000 rev=0x20 hdr=0x00 vendor=0x8086 device=0xa0f0 subvendor=0x8086 subdevice=0x0070
    vendor     = 'Intel Corporation'
    device     = 'Wi-Fi 6 AX201'
    class      = network
 
7    1 0xffffffff83ce6000    c4498 if_iwlwifi.ko
 8    1 0xffffffff83dab000    181b0 if_iwx.ko

15.1-RELEASE
```

