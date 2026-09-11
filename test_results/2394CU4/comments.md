# Notes
The Lenovo T530 was produced between 2012 and 2014. I have used FreeBSD as my daily driver for a few weeks, and so far, I haven't encountered any problems. The battery lasts about 2–3 hours, but that is simply because it is old. This is acceptable to me. The battery has 9 cells and provided up to 94Wh of power. 

During the first few weeks, the computer got hot quite quickly, and the fan was often loud—spinning up whenever several programs were running simultaneously. 

If you have the necessary technical skills, I suggest taking the laptop apart, cleaning the fan, refreshing the thermal compound, and removing any dust accumulated inside. To clean the fan thoroughly, open its housing by removing the screws, detach the plastic rotor blade unit, and wash it in water. If necessary, use a fine tool to remove any remaining stubborn dirt, then let it dry completely in the sun before reassembly. After putting it back together, I noticed that the fan was significantly quieter than before, though this observation is purely subjective.

## Brightness
Brightness control works as expected after installing `drm-kmod` (adding the `i915kms` kernel module to `/etc/rc.conf`), `xorg`, and `xfce4`, and adding my standard user account (not root) to the `video` group. There are two devices listed under `/dev/backlight` (`backlight0` and `intel_backlight0`), but the `backlight` utility works fine with both.

## Desktop environment
I use XFCE4. I created .xinitrc in my home directory 
containing the line `ck-launch-session dbus-launch --exit-with-session startxfce4`. I start it with the command `startxfce4`.

## Networking
I created `wpa_supplicant.conf` in /etc/ and added an entry for my wireless network. Currently, I use this laptop on only one network. The laptop's wireless interface uses iwn, the Intel IEEE 802.11n driver. In the near future, I will be connecting to different networks again. I don't have experience managing multiple Wi-Fi networks on FreeBSD yet, so I am looking forward to trying it out.

## Sound
The default volume was too low at first. I adjusted the PCM level using the mixer command: `mixer pcm=100%`. Volume can be adjusted via the software controls or the physical media buttons above the T530's keyboard, which allow increasing, decreasing, or muting the audio. Adjusting the volume in XFCE4 or via the physical buttons modifies the `vol` device setting, while the `pcm` level remains at 100%.

## Printing
I successfully configured two printers: a Hewlett-Packard LaserJet Pro M402dne and an Epson ET-2820. For the Epson, the scanning functionality also works reliably using `xsane`.

## Miscellaneous
I haven't tested the microphone or webcam yet. Below the screen are two small LEDs: one signals network activity, and the other signals hard disk drive access. If I turn off networking physically using the laptop's hardware switch, the network LED turns off immediately; it turns back on when I flip the switch back.
As for the hard drive LED, if I execute a C program that creates files and writes large amounts of data using write(), the LED blinks almost continuously. 
Both LEDs seem to reflect system activity, which is a nice feature that is rarely seen on more modern laptops.
Older ThinkPads featured the ThinkLight, an LED above the screen that can be turned on using Fn + Spacebar, which works as expected on this T530.

## Contact
Feel free to reach out if you have tried running FreeBSD on a T530 and ran into issues. We can compare configuration files and try to troubleshoot together.
