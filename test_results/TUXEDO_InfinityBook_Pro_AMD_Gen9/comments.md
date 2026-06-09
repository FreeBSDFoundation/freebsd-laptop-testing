# Notes

## Does not work

Features that tested as working under Debian 13, but do not work under FreeBSD 15.

### suspend/resume

At first glance suspend works as laptop seem to go to sleep, but on trying to resume it executes full boot sequence.

### screen brightness controls

Laptop has screen brightness keys, but they don't work in FreeBSD.

## Unsure

### Bluetooth

Device is found after kernel module load, but could not connect anything (e.g. headphones). Must be lack of easy to use tools in userspace. It works under Debian 13.

### WiFi

Speed should be better. Under FreeBSD it's only WiFi 2 with speeds up to 144 Mbps for download and 54 Mbps for upload. Under Debian it works as WiFi 6 with speeds of 300 Mbps or better.

### Wired network

Ethernet is not configured at all as WiFi is available for this machine everywhere. Probably the reason why it's marked as failed.
