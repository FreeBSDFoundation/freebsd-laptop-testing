#
# SPDX-FileCopyrightText: 2026 Shreeney Ajmeri <ajmerishreeney@gmail.com>
#
# SPDX-License-Identifier: BSD-2-Clause
#

#!/bin/sh
set -e

: ${SU:=su -m root -c}

pcigrep() {
  pattern="$(printf '%s\n' "$@" | paste -sd '|' -)"
  grep -Eil "^\\s*(class|subclass)\\s*=\\s*(${pattern})" pcidev* || true
}

filter_pcidev_props() {
  if test $# -gt 0; then
    grep -Eh -e '^\S*@\S*:' -e '^\s*(vendor|device|class|subclass)\s*=' "$@"
  else
    echo NOT DETECTED
  fi
}

score_pcidevs() {
  if test $# -gt 0; then
    num_without_drivers="$(grep '^none[0-9][0-9]*@' "$@" | wc -l)"
    num_devices=$#
    score="$(echo "scale=1; (${num_devices} - ${num_without_drivers}) * 2 / ${num_devices}" | bc)"
  else
    score=0.0
  fi

  echo "${score}/2.0"
}

# See https://www.usb.org/defined-class-codes for USB
# bDeviceClass and bDeviceSubClass codes

realpath="$(realpath "$0")"
REPO_DIR="$(dirname "${realpath}")"

>&2 echo "Checking for required programs..."
command -v hw-probe >/dev/null 2>&1 || { >&2 echo "Error: hw-probe not found."; exit 1; }
>&2 echo "All required programs are available."

MAKER="$(kenv smbios.system.product | sed -E -e 's/[^[:alnum:]]+/_/g' -e 's/(^_|_$)//g')"
if [ -z "$MAKER" ]; then
    >&2 echo "Error: Could not determine system product."
    exit 1
fi
TARGET_DIR="$REPO_DIR/test_results/$MAKER"

TMPDIR="$(mktemp -d /tmp/hwprobe.XXXXXX)"
trap 'cd -; rm -rf "$TMPDIR"' EXIT INT TERM
cd $TMPDIR
>&2 echo "Working inside temporary directory: $PWD"

>&2 echo "Running hardware probe..."
${SU} "hw-probe -all -save $PWD" >&2

>&2 echo "Extracting hardware dump..."
tar -xf hw.info.tgz

>&2 echo "Creating a laptop testing report..."
mkdir -p "$TARGET_DIR"

csplit -skf pcidev hw.info/logs/pciconf '/^.*@.*:/' '{99}' 2>/dev/null || true
#csplit -skf usbdev hw.info/logs/usbconfig '/^.*: </' '{99}' 2>/dev/null || true

# graphics

graphics_pci_devs="$(pcigrep vga display)"
networking_pci_devs="$(pcigrep network)"
audio_pci_devs="$(pcigrep hda multimedia)"
storage_pci_devs="$(pcigrep 'mass storage' storage)"
usb_pci_devs="$(pcigrep usb)"
bluetooth_pci_devs="$(pcigrep bluetooth)"

# Anonymize the kernel version
kern_version="$(sysctl -n kern.version | head -1)"
kern_version="${kern_version%%:*}"

cat <<EOF
=== FreeBSD Hardware Status Info ===

Running: ${kern_version}
Hardware: ${MAKER}
CPU: $(sysctl -n hw.model)
------------------------------------

- Graphics
$(filter_pcidev_props ${graphics_pci_devs})

  Category Total Score: $(score_pcidevs ${graphics_pci_devs})

--------------------

- Networking
$(filter_pcidev_props ${networking_pci_devs})

  Category Total Score: $(score_pcidevs ${networking_pci_devs})

--------------------

- Audio
$(filter_pcidev_props ${audio_pci_devs})

  Category Total Score: $(score_pcidevs ${audio_pci_devs})

--------------------

- Storage
$(filter_pcidev_props ${storage_pci_devs})

  Category Total Score: $(score_pcidevs ${storage_pci_devs})

--------------------

- USB Ports
$(filter_pcidev_props ${usb_pci_devs})

  Category Total Score: $(score_pcidevs ${usb_pci_devs})

--------------------

- Bluetooth
$(filter_pcidev_props ${bluetooth_pci_devs})

  Category Total Score: $(score_pcidevs ${bluetooth_pci_devs})

--------------------

=== FreeBSD Detailed Status Info ==

Currently loaded kernel modules:
$(kldstat | awk '{ print $5 }' | tail -n+2 | sort)

====================================
EOF

>&2 echo "Finished. Thank you for your contribution!"
