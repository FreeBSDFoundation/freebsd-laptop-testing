# HP Presario CQ56

## System

Model: HP Presario CQ56
CPU: Intel Celeron 900
Chipset: ICH9M
Graphics: Intel 4 Series
Storage: AHCI SATA

FreeBSD version:
15.0-RELEASE

Boot mode:
Legacy BIOS (no UEFI)

Filesystem:
ZFS root (zroot)

## Hardware status

Graphics: works
Ethernet: works (re0)
WiFi: detected (iwn0)
Audio: works
USB: works

## Issues

Intermittent boot failure:

Error:

can't find boot zfsloader

Occurs randomly every 2–3 boots.

Tested fixes:

- reinstall bootcode
- change freebsd-boot partition size
- loader.conf tuning
- ZFS tuning options

Issue still present.
