# Casper Excalibur G870 — test notes

Tested system:
- Laptop: Casper Excalibur G870
- OS: FreeBSD 15.1-RELEASE (`releng/15.1-n283562-96841ea08dcf`, GENERIC)
- CPU: 12th Gen Intel Core i7-12650H
- Graphics: Intel Alder Lake-P UHD Graphics and NVIDIA GeForce RTX 4060 Max-Q (mobile)

Observed desktop/driver behavior:
- NVIDIA driver packages were installed.
- A KDE Plasma Wayland session could be started manually from the TTY, and the display output appeared normal during the user's test.
- SDDM did not start automatically during boot; Plasma had to be started manually from the TTY.
- PipeWire configuration was not completed, so full desktop audio behavior (including output switching) was not verified.

Probe observations:
- Graphics: 2.0/2.0
- Networking: 2.0/2.0
- Audio: 2.0/2.0
- Storage: 2.0/2.0
- USB Ports: 2.0/2.0
- Bluetooth: 0.0/2.0

The probe lists an Intel AX201 Bluetooth device, but the report assigns Bluetooth 0.0/2.0. Bluetooth functionality was not confirmed. The category scores above are the probe's reported scores and should not be interpreted as completion of every end-user test in the pull-request questionnaire.
