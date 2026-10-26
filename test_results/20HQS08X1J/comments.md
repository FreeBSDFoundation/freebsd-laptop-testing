laptop info: Lenovo ThinkPad X1 Carbon 5th Gen (type 20HQ), Intel Core i7-7600U, Intel HD Graphics 620, Intel Wireless 8265, 16 GB RAM

system: FreeBSD 15.1-RELEASE-p6 (GENERIC, binary updates, quarterly packages) with the Tern desktop on top
(own Wayland compositor on wlroots 0.20/scenefx, Qt 6 shell; hobby project, not part of FreeBSD). Only base
system and packages, no patched kernel or world. Changes of the desktop layer that touch hardware, so that you
can tell them apart from stock behaviour:

* Wi-Fi: `if_iwm` blocked via `devmatch_blocklist`, `if_iwlwifi` used instead with
  `compat.linuxkpi.iwlwifi_11n_disable=0`, `compat.linuxkpi.iwlwifi_disable_11ac=0`,
  `compat.linuxkpi.80211.hw_crypto=1` in loader.conf (iwm only gave 802.11a/g on this card). A small user-space
  watchdog (`tern-wifi-guard`) pings the gateway every 15 s and runs `wpa_cli reassociate`/`reconnect` or a new
  `dhclient` when the link is lost; it does not reassociate after an iwlwifi firmware crash.
* Camera: `webcamd` + `cuse` (packages webcamd, v4l-utils).
* Power: GPU frequency cap 700 MHz on battery (i915 sysctls), `hw.acpi.lid_switch_state` set by the desktop's
  settings, `kern.vt.suspendswitch=0`, `vfs.zfs.arc.max` limited to a quarter of RAM (i915 GPU hangs under memory
  pressure, see below).
* Printing: cups, cups-filters, nss_mdns, avahi (driverless IPP Everywhere).

what works (checked on this machine):
1. Wi-Fi: Intel 8265 with iwlwifi associates in VHT mode 11ac (`ifconfig wlan0`: "VHT mode 11ac"), reconnects
   to the known network after boot.
2. Graphics: i915kms (drm-kmod) with a Wayland compositor (GLES2 + blur), Xwayland for X11 programs.
3. External HDMI monitor: hot-plug, arrangement and resolution from the desktop's display settings, unplugging
   moves the windows back (tested 2026-10-26).
4. Audio: Sunrise Point-LP HDA, speakers and system sounds.
5. Camera: the integrated Chicony camera attaches to webcamd (`/dev/video0`, `/dev/video1`,
   `v4l2-ctl --list-devices`); not yet used in a video call.

known issues and bugs:
1. Bluetooth (Intel 8265, USB `ugen0.2`): `ng_ubt` is loaded but no `ubt` device attaches. The Intel firmware
   loader package (`iwmbt-firmware`/`iwmbtfw`) is not installed here, so this is probably expected; not
   investigated further.
2. i915 GPU hangs ("drmn0: [drm] GPU HANG: ecode 9:1:85d7ffff, in MainThread") on 2026-10-23 and 2026-10-24
   under load (parallel builds on the two cores plus the desktop). None since `vfs.zfs.arc.max` was limited and
   builds moved to another machine.
3. Wi-Fi: occasional loss of the connection without a reboot (watched by the user-space watchdog above, which logs
   every check); no loss logged since 2026-10-24.

not tested yet: display and keyboard backlight (devices `backlight0`, `intel_backlight0` are present), suspend/resume (S3) over hours, battery runtime, headphone switching, touchpad gestures,
virtualization, tethering.

Note: the probe file is the unchanged output of `make` (make_report.sh, commit ad0d14e). Analysis and write-up of
these comments done with AI assistance (Claude); the observations are from the machine and were reviewed by the owner
before submission.
