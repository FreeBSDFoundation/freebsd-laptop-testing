# Notes

## Desktop

The testing device has hardware issue with display ("apple flexgate"). I didn't try configuring any desktop
environment on the laptop.

Another testing device is able to run the X11 server with
the i915 kernel module from drm-61-kmod-6.1.128.1600018_10 package.

## Serial Peripherial Interface (SPI) Controller

```
spi0@pci0:0:30:3:	class=0x118000 rev=0x21 hdr=0x00 vendor=0x8086 device=0x9d2a subvendor=0x8086 subdevice=0x7270
    vendor     = 'Intel Corporation'
    device     = 'Sunrise Point-LP Serial IO SPI Controller'
    class      = dasp
```

Detected, but very often the `atopcase0` device
the connects the built in keyboard and the touchpad
does not attach at all:

[https://bugs.freebsd.org/bugzilla/show_bug.cgi?id=283706](https://bugs.freebsd.org/bugzilla/show_bug.cgi?id=283706)

### The built-in keyboard

If the `atopcase0` attaches successfully, 
the keyboard is hard to use, during typing
it stops responding and after a small delay
the terminal spits the last typed character
repeated multiple times.

```
atopcase0: <Apple MacBook SPI Topcase> at cs 0 mode 0 on spibus0
atopcase0: Using ACPI GPE.
hidbus3: <HID bus> on atopcase0
hidbus4: <HID bus> on atopcase0
hms1: <Apple MacBook Mouse> on hidbus4
hms1: 3 buttons and [XY] coordinates ID=2
hkbd0: <Apple MacBook Keyboard> on hidbus3
kbd2 at hkbd0
```

When the typing delay/storm happens, the following
message gets logged:

```
spi0: transfer timeout
atopcase0: SPI error: 5
```

### The built-in touchpad

When the touchpad works, it is a simple device
with a single button only.

From the X.org log:

```
[   314.361] (II) config/udev: Adding input device Apple MacBook Mouse (/dev/input/event7)
[   314.361] (**) Apple MacBook Mouse: Applying InputClass "evdev pointer catchall"
[   314.361] (**) Apple MacBook Mouse: Applying InputClass "libinput pointer catchall"
[   314.361] (**) Apple MacBook Mouse: Applying InputClass "evdev keyboard catchall"
[   314.361] (II) Using input driver 'libinput' for 'Apple MacBook Mouse'
[   314.361] (**) Apple MacBook Mouse: always reports core events
[   314.362] (II) event7  - Apple MacBook Mouse: is tagged by udev as: Mouse
[   314.364] (II) event7  - Apple MacBook Mouse: device is a pointer
[   314.365] (II) event7  - Apple MacBook Mouse: device removed
[   314.365] (II) libinput: Apple MacBook Mouse: Step value 0 was provided, libinput Fallback acceleration function is used.
[   314.365] (II) libinput: Apple MacBook Mouse: Step value 0 was provided, libinput Fallback acceleration function is used.
[   314.365] (II) libinput: Apple MacBook Mouse: Step value 0 was provided, libinput Fallback acceleration function is used.
[   314.365] (II) XINPUT: Adding extended input device "Apple MacBook Mouse" (type: MOUSE, id 12)
[   314.365] (**) Apple MacBook Mouse: (accel) selected scheme none/0
[   314.365] (**) Apple MacBook Mouse: (accel) acceleration factor: 2.000
[   314.365] (**) Apple MacBook Mouse: (accel) acceleration threshold: 4
[   314.367] (II) event7  - Apple MacBook Mouse: is tagged by udev as: Mouse
[   314.368] (II) event7  - Apple MacBook Mouse: device is a pointer
```

## UART controller

```
none2@pci0:0:31:2:	class=0x058000 rev=0x21 hdr=0x00 vendor=0x8086 device=0x9d21 subvendor=0x8086 subdevice=0x7270
    vendor     = 'Intel Corporation'
    device     = 'Sunrise Point-LP PMC'
    class      = memory
```

Not recognized

### Bluetooth

Not recognized, not working.

The DSDT ACPI table indicates that the "apple-uart-blth"
device is attached to the UART controller.

```
                    Name (_HID, EisaId ("BCM2E7C"))  // _HID: Hardware ID
                    Name (_CID, "apple-uart-blth")  // _CID: Compatible ID
                    Name (_UID, One)  // _UID: Unique ID
                    Name (_ADR, Zero)  // _ADR: Address
```

## Wi-Fi

MacBook Pro 13-inch (2016) comes with Broadcom BCM4350 Wi-Fi chip. FreeBSD 15.x doesn't include a working driver
for the chip.

The testing device runs experimental out-of-tree `if_brcmfmac.ko` [kernel module][1], that adds support for the
Broadcom BCM4350 Wi-Fi chip (PCI device `brcmfmac0@pci0:2:0:0`).

git commit used: 9adbe774d3be91827d628fbd811daf63512acb6d

### Firmware

The firmware under test obtained from
https://gitlab.com/kernel-firmware/linux-firmware/
commit c3889b396e0334b388ecfbea5d37d1df7239605c

The following files got copied to /boot/firmware

brcm/brcmfmac4350c2-pcie.bin
brcm/brcmfmac4350-pcie.bin

```
brcmfmac0: <Broadcom BCM4350 WiFi> mem 0x92400000-0x92407fff,0x92000000-0x923fffff at device 0.0 on pci6
brcmfmac0: chip=4350 rev=5 socitype=AXI
brcmfmac4350c2-pcie.bin: could not load firmware image, error 8
brcmfmac0: loaded firmware brcmfmac4350c2-pcie.bin (623304 bytes)
brcmfmac4350c2-pcie.txt: could not load firmware image, error 2
brcmfmac4350c2-pcie.txt: could not load binary firmware /boot/firmware/brcmfmac4350c2-pcie.txt either
brcmfmac0: firmware: wl0: Nov 26 2015 03:48:57 version 7.35.180.133 (r602372) FWID 01-c45b39d6
brcmfmac0: MAC address 78:4f:43:xx:xx:xx
brcmfmac0: btc_mode set err=0 readback=0
brcmfmac0: isup=1 after bss_up
brcmfmac0: radio: txchain=0x3 rxchain=0x3 qtxpower=127 chanspec=0x1001 band=0 interference=0 btc_mode=5
```

`FWID: 01-c45b39d6` indicates that the `brcm/brcmfmac4350c2-pcie.bin` got loaded.

### Setup

Enable on startup using /etc/rc.conf and wpa_supplicant:

```
wlans_brcmfmac0="wlan0"
ifconfig_wlan0="WPA DHCP"
ifconfig_wlan0_ipv6="inet6 accept_rtadv"
```

Manual

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

## The webcam

```
none4@pci0:3:0:0:	class=0x048000 rev=0x00 hdr=0x00 vendor=0x14e4 device=0x1570 subvendor=0x14e4 subdevice=0x1570
    vendor     = 'Broadcom Inc. and subsidiaries'
    device     = '720p FaceTime HD Camera'
    class      = multimedia
```

Not detected, not working

## PCIe devices without any driver

(if not mentioned above)

```
none0@pci0:0:22:0:	class=0x078000 rev=0x21 hdr=0x00 vendor=0x8086 device=0x9d3a subvendor=0x8086 subdevice=0x7270
    vendor     = 'Intel Corporation'
    device     = 'Sunrise Point-LP CSME HECI'
    class      = simple comms
none2@pci0:0:31:2:	class=0x058000 rev=0x21 hdr=0x00 vendor=0x8086 device=0x9d21 subvendor=0x8086 subdevice=0x7270
    vendor     = 'Intel Corporation'
    device     = 'Sunrise Point-LP PMC'
    class      = memory
none3@pci0:6:0:0:	class=0x088000 rev=0x02 hdr=0x00 vendor=0x8086 device=0x15d2 subvendor=0x8086 subdevice=0x0000
    vendor     = 'Intel Corporation'
    device     = 'JHL6540 Thunderbolt 3 NHI (C step) [Alpine Ridge 4C 2016]'
    class      = base peripheral
```

## Audio

```
# cat /dev/sndstat 
Installed devices:
pcm0: <Cirrus Logic (0x8409) (Analog 3.1/2.0)> (play/rec)
pcm1: <Cirrus Logic (0x8409) (Analog Headphones)> (play)
pcm2: <Intel Skylake (HDMI/DP 8ch)> (play)
```

The built-in speakers do not seem to work.

snd_hda pin configuration:

```
hdaa0: <Cirrus Logic (0x8409) Audio Function Group> at nid 1 on hdacc0
pcm0: <Cirrus Logic (0x8409) (Analog 3.1/2.0)> at nid 36,37 and 60 on hdaa0
pcm1: <Cirrus Logic (0x8409) (Analog Headphones)> at nid 44 on hdaa0
hdaa1: <Intel Skylake Audio Function Group> at nid 1 on hdacc1
pcm2: <Intel Skylake (HDMI/DP 8ch)> at nid 3 on hdaa1
hdaa0: Dumping AFG pins:
hdaa0: nid   0x    as seq device       conn  jack    loc        color   misc
hdaa0: 36 90100110 1  0  Speaker       Fixed Unknown Internal   Unknown 1
hdaa0:     Caps:    OUT             
hdaa0: 37 90100111 1  1  Speaker       Fixed Unknown Internal   Unknown 1
hdaa0:     Caps:    OUT             
hdaa0: 38 400000f0 15 0  Line-out      None  Unknown 0x00       Unknown 0 DISA
hdaa0:     Caps:    OUT             
hdaa0: 39 400000f0 15 0  Line-out      None  Unknown 0x00       Unknown 0 DISA
hdaa0:     Caps:    OUT             
hdaa0: 40 400000f0 15 0  Line-out      None  Unknown 0x00       Unknown 0 DISA
hdaa0:     Caps:    OUT             
hdaa0: 41 400000f0 15 0  Line-out      None  Unknown 0x00       Unknown 0 DISA
hdaa0:     Caps:    OUT             
hdaa0: 42 400000f0 15 0  Line-out      None  Unknown 0x00       Unknown 0 DISA
hdaa0:     Caps:    OUT             
hdaa0: 43 400000f0 15 0  Line-out      None  Unknown 0x00       Unknown 0 DISA
hdaa0:     Caps:    OUT             
hdaa0: 44 002b4020 2  0  Headphones    Jack  Combo   0x00       Green   0
hdaa0:     Caps:    OUT             
hdaa0: 45 400000f0 15 0  Line-out      None  Unknown 0x00       Unknown 0 DISA
hdaa0:     Caps:    OUT             
hdaa0: 46 400000f0 15 0  Line-out      None  Unknown 0x00       Unknown 0 DISA
hdaa0:     Caps:    OUT             
hdaa0: 47 400000f0 15 0  Line-out      None  Unknown 0x00       Unknown 0 DISA
hdaa0:     Caps:    OUT             
hdaa0: 48 400000f0 15 0  Line-out      None  Unknown 0x00       Unknown 0 DISA
hdaa0:     Caps:    OUT             
hdaa0: 49 400000f0 15 0  Line-out      None  Unknown 0x00       Unknown 0 DISA
hdaa0:     Caps:    OUT             
hdaa0: 50 400000f0 15 0  Line-out      None  Unknown 0x00       Unknown 0 DISA
hdaa0:     Caps:    OUT             
hdaa0: 51 400000f0 15 0  Line-out      None  Unknown 0x00       Unknown 0 DISA
hdaa0:     Caps:    OUT             
hdaa0: 52 400000f0 15 0  Line-out      None  Unknown 0x00       Unknown 0 DISA
hdaa0:     Caps: IN                 
hdaa0: 53 400000f0 15 0  Line-out      None  Unknown 0x00       Unknown 0 DISA
hdaa0:     Caps: IN                 
hdaa0: 54 400000f0 15 0  Line-out      None  Unknown 0x00       Unknown 0 DISA
hdaa0:     Caps: IN                 
hdaa0: 55 400000f0 15 0  Line-out      None  Unknown 0x00       Unknown 0 DISA
hdaa0:     Caps: IN                 
hdaa0: 56 400000f0 15 0  Line-out      None  Unknown 0x00       Unknown 0 DISA
hdaa0:     Caps: IN                 
hdaa0: 57 400000f0 15 0  Line-out      None  Unknown 0x00       Unknown 0 DISA
hdaa0:     Caps: IN                 
hdaa0: 58 400000f0 15 0  Line-out      None  Unknown 0x00       Unknown 0 DISA
hdaa0:     Caps: IN                 
hdaa0: 59 400000f0 15 0  Line-out      None  Unknown 0x00       Unknown 0 DISA
hdaa0:     Caps: IN                 
hdaa0: 60 00ab9030 3  0  Mic           Jack  Combo   0x00       Pink    0
hdaa0:     Caps: IN                 
hdaa0: 61 400000f0 15 0  Line-out      None  Unknown 0x00       Unknown 0 DISA
hdaa0:     Caps: IN                 
hdaa0: 62 400000f0 15 0  Line-out      None  Unknown 0x00       Unknown 0 DISA
hdaa0:     Caps: IN                 
hdaa0: 63 400000f0 15 0  Line-out      None  Unknown 0x00       Unknown 0 DISA
hdaa0:     Caps: IN                 
hdaa0: 64 400000f0 15 0  Line-out      None  Unknown 0x00       Unknown 0 DISA
hdaa0:     Caps: IN                 
hdaa0: 65 400000f0 15 0  Line-out      None  Unknown 0x00       Unknown 0 DISA
hdaa0:     Caps: IN                 
hdaa0: 66 400000f0 15 0  Line-out      None  Unknown 0x00       Unknown 0 DISA
hdaa0:     Caps: IN                 
hdaa0: 67 400000f0 15 0  Line-out      None  Unknown 0x00       Unknown 0 DISA
hdaa0:     Caps: IN                 
hdaa0: 68 a0a60100 0  0  Mic           Fixed Digital External   Unknown 1 DISA
hdaa0:     Caps: IN                 
hdaa0: 69 400000f0 15 0  Line-out      None  Unknown 0x00       Unknown 0 DISA
hdaa0:     Caps: IN                 
hdaa0: NumGPIO=8 NumGPO=0 NumGPI=0 GPIWake=1 GPIUnsol=1
hdaa0:  GPIO0: disabled
hdaa0:  GPIO1: disabled
hdaa0:  GPIO2: disabled
hdaa0:  GPIO3: disabled
hdaa0:  GPIO4: disabled
hdaa0:  GPIO5: disabled
hdaa0:  GPIO6: disabled
hdaa0:  GPIO7: disabled
hdaa1: Dumping AFG pins:
hdaa1: nid   0x    as seq device       conn  jack    loc        color   misc
hdaa1:  3 18560010 1  0  Digital-out   Jack  Digital 0x18       Unknown 0
hdaa1:     Caps:    OUT              Sense: 0x00000000 (disconnected)
hdaa1: NumGPIO=0 NumGPO=0 NumGPI=0 GPIWake=0 GPIUnsol=0
```

## Disabled ACPI throttle module

For some reason, `hint.acpi_throttle.0.disabled="1"`
had to be added to `/boot/device.hints`
