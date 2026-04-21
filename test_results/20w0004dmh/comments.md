# Summary

This is my install of FreeBSD as a daily driver on my laptop. I've kept track
of what works and what doesn't here:

https://kedara.eu/freebsd-thinkpad-t14-gen2-intel/

# System information

Laptop make/model: Lenovo ThinkPad T14 Gen 2 Intel (20W0004DMH)

`uname -a` output: `FreeBSD bsdpad.home.arpa 15.0-RELEASE-p5 FreeBSD
15.0-RELEASE-p5 releng/15.0-n281018-0730d5233286 GENERIC amd64`

# Tests Completed

## Installation

- [ ] I can install FreeBSD easily as a new user and jump into a graphical desktop environment on the next boot.
    https://github.com/FreeBSDFoundation/proj-laptop/issues/25

I have manually installed a Xfce desktop. This was relatively easy, but
probably not for new *nix users.

## Wireless

- [ ] The laptop has Wi-Fi 5 support (802.11ac)
    https://github.com/FreeBSDFoundation/proj-laptop/issues/33

- [ ] The laptop has Wi-Fi 6/6E support (802.11ax), with observed speeds of 1Gbps+.
    https://github.com/FreeBSDFoundation/proj-laptop/issues/34

I don't know how to test the two items above. The Wi-Fi is working.

- [x] The laptop automatically connects to known Wi-Fi networks without requiring me to manually reconnect each time.
    https://github.com/FreeBSDFoundation/proj-laptop/issues/4

- [ ] I can connect my laptop to the internet by tethering with my mobile phone.

- [ ] There is a built-in tool to identify available WiFi networks, choose one to connect to, and provide a passphrase.
    https://github.com/FreeBSDFoundation/proj-laptop/issues/3

Probably not applicable, because I've installed the desktop myself (instead
from within the installer, which also wasn't/isn't an option yet).

## Audio/Video

- [ ] Sound seamlessly switches to headphones when plugged in, and back to speakers when plugged out.
    https://github.com/FreeBSDFoundation/proj-laptop/issues/15

- [ ] Graphical applications (such as games and media content creation tools) run smoothly on the laptop at the screen refresh rate or higher.
    https://github.com/FreeBSDFoundation/proj-laptop/issues/11
    https://github.com/FreeBSDFoundation/proj-laptop/issues/13

Not sure about the specific refresh rate, but I can watch online videos, for
example.

- [ ] I can share my screen on all popular browsers and other applications that request the webcam.
    https://github.com/FreeBSDFoundation/proj-laptop/issues/14

The webcam is working, haven't tried meetings/screen sharing.

- [ ] I can stay connected in a virtual meeting for an hour or longer on all popular video conferencing software with no disruptions.

## Power

- [ ] The laptop lasts through an 8-hour workday on a single charge
    https://github.com/FreeBSDFoundation/proj-laptop/issues/6

Unfortunately not. I'm not sure, but it's closer to 4-6 hours.

- [ ] I can close the lid to enter sleep mode, then open the lid hours later to resume working.
    https://github.com/FreeBSDFoundation/proj-laptop/issues/7

Closing the lid and opening it results in a black screen on my graphical
session. I have to kill and restart Xfce to resume working. S3 suspend is
working, but requires a restart of the `netif` after resuming.

- [ ] The laptop can enter and resume from hibernation mode with no change to its operating state.
    https://github.com/FreeBSDFoundation/proj-laptop/issues/29

The only time I've tested this, the system tried to hibernate and then rebooted.

## User Experience

- [ ] I can change the keyboard backlight and display backlight to view at a comfortable brightness.

Keyboard backlight Fn is working, display brightness Fn keys are not working.

- [ ] I can use multi-finger touchpad gestures in my desktop environment.
    https://github.com/FreeBSDFoundation/proj-laptop/issues/18

- [ ] All of the laptop's specialty keyboard buttons (e.g. brightness, volume, etc.) work correctly and can be customized in my desktop environment.
    https://github.com/FreeBSDFoundation/proj-laptop/issues/19

Working:
- keyboard backlight
- audio output mute key

Not working:
- display brightness
- volume keys
- microphone mute key

- [ ] I can connect to an external monitor or projector using HDMI while using my desktop environment's display settings manager to configure it.
    https://github.com/FreeBSDFoundation/proj-laptop/issues/27

## Virtualization

- [ ] Suspending the laptop while a VM is running does not affect the VM's state upon resume.
    https://github.com/FreeBSDFoundation/proj-laptop/issues/9

- [ ] I can run Windows VMs on the laptop.
    https://github.com/FreeBSDFoundation/proj-laptop/issues/21

# Additional Info

I've also added a hardware probe at https://bsd-hardware.info/?probe=69e2d228f4

Thank you so much for this project! I think it's very valuable.

See https://kedara.eu/freebsd-thinkpad-t14-gen2-intel/ for additional notes.
I've made a copy below of what works/doesn't, this will be kept up to date
(more or less) on the linked web page.

**These features work**:

* **Out of the box**: graphics/ethernet/WiFi/keyboard (except Fn keys)/trackpoint/trackpad/sound playback, USB ports
* **Webcam**: works via `webcamd` (tested via `pwcview`, see [Section 9.5.1](https://docs.freebsd.org/en/books/handbook/multimedia/index.html#webcam-setup)). Use `webcamd -l` to find the device, on my laptop: `webcamd [-d ugen1.3] -N Azurewave-Integrated-Camera -S 0000 -M 0`
* **Suspend/resume**: "S3 suspend" works, if the setting in the BIOS Power menu is set to "S3". The only remaining issues with this are that the screen isn't locked before suspending, and I have to restart the networking afterwards because of `iwlwifi` errors (use `service netif restart`). 
* **Fingerprint reader**: It works after installing `libfprint` and `fprintd`. These are supposedly outdated versions, Aymeric Wibo has [written a guide](https://obiw.ac/fprint/) on how to build them from source if you so desire (I've decided to stick with the `pkg` versions for now). You'll also need to add the following line to `/etc/pam.d/system`:
```sh
auth		sufficient	/usr/local/lib/security/pam_fprintd.so
```
above the line `auth required pam_unix.so` etc. Then you can add fingerprints using `fprintd-enroll`.

**These features I haven't tried yet**:

* SD card reader
* HDMI output
* Headphone jack
* Nano-SIM card reader
* Thunderbolt output
* TPM security chip

**These features don't work (yet?):**

* **Recording sound**: I get only static, but it's low priority for me at the moment. `cat /dev/sndstat` shows: `Installed devices: pcm0: <Realtek ALC257 (Analog 2.0+HP/2.0)> (play/rec) default pcm1: <Intel Tiger Lake (HDMI/DP 8ch)> (play) No devices installed from userspace.`
