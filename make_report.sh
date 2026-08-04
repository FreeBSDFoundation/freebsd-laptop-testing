#!/bin/sh
#
# SPDX-FileCopyrightText: 2026 Siva Mahadevan <siva@FreeBSD.org>
#
# SPDX-License-Identifier: BSD-2-Clause
#

set -e

: "${SU:=su -m root -c}"

count_args() {
  echo $#
}

pcigrep() {
  if test $# -eq 0; then
    >&2 echo "pcigrep() needs at least one pattern"
    exit 64 # EX_USAGE
  fi
  pattern="$(printf '%s\n' "$@" | paste -sd '|' -)"
  grep -Eil "^\\s*(class|subclass)\\s*=\\s*(${pattern})" pcidev* 2>/dev/null || true
}

usbgrep() {
  if test $# -eq 0; then
    >&2 echo "usbgrep() needs at least one pattern"
    exit 64 # EX_USAGE
  fi
  pattern="$(printf '%s\n' "$@" | paste -sd '|' -)"
  grep -Eil "${pattern}" usbdev* 2>/dev/null || true
}

filter_pcidev_props() {
  test $# -eq 0 && exit 0
  grep -Eh -e '^\S*@\S*:' -e '^\s*(vendor|device|class|subclass)\s*=' "$@"
}

# See https://www.usb.org/defined-class-codes for USB
# bDeviceClass and bDeviceSubClass codes
filter_usbdev_props() {
  for f in "$@"; do
    grep -Eh -e '^\S*: <' -e '^\s*(bDeviceClass|bDeviceSubClass|iManufacturer|iProduct)\s*=' "${f}"
    head -1 "${f}" | sed -E "s/.*<(.*)>.*/  device = '\\1'/"
  done
}

pcidevs_without_drivers() {
  test $# -eq 0 && exit 0
  grep '^none[0-9][0-9]*@' "$@" | wc -l
}

usbdevs_without_drivers() {
  test $# -eq 0 && exit 0
  n="$(grep -E '^\S*: \S*: ' "$@" | wc -l)"
  echo $(($# - n))
}

# $1 = num_devices
# $2 = num_without_drivers
score_category() {
  if test "$1" -eq 0; then
    echo 0.0
  else
    awk "BEGIN { printf(\"%.1f\\n\", 2.0 - 2.0*$2/$1) }"
  fi
}


realpath="$(realpath "$0")"
REPO_DIR="$(dirname "${realpath}")"

MAKER="$(kenv smbios.system.product | sed -E -e 's/[^[:alnum:]]+/_/g' -e 's/(^_|_$)//g')"
if [ -z "${MAKER}" ]; then
    >&2 echo "Error: Could not determine system product."
    exit 1
fi
TARGET_DIR="${REPO_DIR}/test_results/${MAKER}"

TMPDIR="$(mktemp -d /tmp/freebsd-laptop-testing.XXXXXX)"
trap 'cd; rm -rf "${TMPDIR}"' EXIT INT TERM
>&2 echo "Working inside temporary directory: ${TMPDIR}"
cd "${TMPDIR}"

>&2 echo "Probing hardware..."
pciconf -lv > pciconf.txt
${SU} "usbconfig -v > usbconfig.txt"

csplit -skf pcidev pciconf.txt '/^.*@.*:/' '{99}' 2>/dev/null || true
csplit -skf usbdev usbconfig.txt '/^[^.]*\.[^.]*: </' '{99}' 2>/dev/null || true

graphics_pci_devs="$(pcigrep vga display)"
graphics_pci_dev_props="$(filter_pcidev_props ${graphics_pci_devs})"
num_graphics="$(count_args ${graphics_pci_devs})"
num_graphics_without_drivers="$(pcidevs_without_drivers ${graphics_pci_devs})"
graphics_score="$(score_category "${num_graphics}" "${num_graphics_without_drivers}")"

networking_pci_devs="$(pcigrep network)"
networking_pci_dev_props="$(filter_pcidev_props ${networking_pci_devs})"
num_networking="$(count_args ${networking_pci_devs})"
num_networking_without_drivers="$(pcidevs_without_drivers ${networking_pci_devs})"
networking_score="$(score_category "${num_networking}" "${num_networking_without_drivers}")"

audio_pci_devs="$(pcigrep hda multimedia)"
audio_pci_dev_props="$(filter_pcidev_props ${audio_pci_devs})"
num_audio="$(count_args ${audio_pci_devs})"
num_audio_without_drivers="$(pcidevs_without_drivers ${audio_pci_devs})"
audio_score="$(score_category "${num_audio}" "${num_audio_without_drivers}")"

storage_pci_devs="$(pcigrep 'mass storage' storage)"
storage_pci_dev_props="$(filter_pcidev_props ${storage_pci_devs})"
num_storage="$(count_args ${storage_pci_devs})"
num_storage_without_drivers="$(pcidevs_without_drivers ${storage_pci_devs})"
storage_score="$(score_category "${num_storage}" "${num_storage_without_drivers}")"

usbports_pci_devs="$(pcigrep usb)"
usbports_pci_dev_props="$(filter_pcidev_props ${usbports_pci_devs})"
num_usbports="$(count_args ${usbports_pci_devs})"
num_usbports_without_drivers="$(pcidevs_without_drivers ${usbports_pci_devs})"
usbports_score="$(score_category "${num_usbports}" "${num_usbports_without_drivers}")"

# Bluetooth devices are also likely found as USB devices
bluetooth_pci_devs="$(pcigrep bluetooth)"
bluetooth_pci_dev_props="$(filter_pcidev_props ${bluetooth_pci_devs})"
bluetooth_usb_devs="$(usbgrep bluetooth)"
bluetooth_usb_dev_props="$(filter_usbdev_props ${bluetooth_usb_devs})"
num_bluetooth="$(count_args ${bluetooth_pci_devs} ${bluetooth_usb_devs})"
num_bluetooth_pci_without_drivers="$(pcidevs_without_drivers ${bluetooth_pci_devs})"
num_bluetooth_usb_without_drivers="$(usbdevs_without_drivers ${bluetooth_usb_devs})"
num_bluetooth_without_drivers=$((num_bluetooth_pci_without_drivers + num_bluetooth_usb_without_drivers))
bluetooth_score="$(score_category "${num_bluetooth}" "${num_bluetooth_without_drivers}")"

# Anonymize the kernel version
kern_version="$(sysctl -n kern.version | head -1)"
kern_version="${kern_version%%:*}"
kern_modules="$(kldstat | awk '{ print $5 }' | tail -n+2 | sort)"
hw_model="$(sysctl -n hw.model)"

>&2 echo "Creating a laptop testing report..."
mkdir -p "${TARGET_DIR}"

cat > "${TARGET_DIR}/probe_$(date '+%F_%H-%M-%S').txt" <<EOF
=== FreeBSD Hardware Status Info ===

Running: ${kern_version}
Hardware: ${MAKER}
CPU: ${hw_model}
------------------------------------

- Graphics
${graphics_pci_dev_props}

  Category Total Score: ${graphics_score}/2.0

--------------------

- Networking
${networking_pci_dev_props}

  Category Total Score: ${networking_score}/2.0

--------------------

- Audio
${audio_pci_dev_props}

  Category Total Score: ${audio_score}/2.0

--------------------

- Storage
${storage_pci_dev_props}

  Category Total Score: ${storage_score}/2.0

--------------------

- USB Ports
${usbports_pci_dev_props}

  Category Total Score: ${usbports_score}/2.0

--------------------

- Bluetooth
${bluetooth_pci_dev_props}
${bluetooth_usb_dev_props}

  Category Total Score: ${bluetooth_score}/2.0

--------------------

=== FreeBSD Detailed Status Info ==

Currently loaded kernel modules:
${kern_modules}

====================================
EOF

>&2 echo "Finished. Thank you for your contribution!"
cd -
git status
