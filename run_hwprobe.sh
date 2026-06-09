#
# SPDX-FileCopyrightText: 2026 Shreeney Ajmeri <ajmerishreeney@gmail.com>
#
# SPDX-License-Identifier: BSD-2-Clause     
#



#!/bin/sh
set -e

REPO_DIR=$(pwd)

TMPDIR=$(mktemp -d /tmp/hwprobe.XXXXXX)
trap 'rm -rf "$TMPDIR"' EXIT INT TERM

echo "Temporary directory: $TMPDIR"

echo "Checking for required programs..."
command -v python3 >/dev/null 2>&1 || { echo "Error: python3 not found."; exit 1; }
command -v hw-probe >/dev/null 2>&1 || { echo "Error: hw-probe not found."; exit 1; }
echo "All required programs are available."

echo "Running hardware probe..."
su -m root -c "hw-probe -all -save $TMPDIR"

echo "Extracting hardware dump..."
for tgz in "$TMPDIR"/*.tgz; do
    [ -e "$tgz" ] || continue
    tar -xf "$tgz" -C "$TMPDIR"
done

echo "Running script..."
cd "$TMPDIR"
python3 "$REPO_DIR/main.py" "$TMPDIR"

MAKER=$(kenv smbios.system.product | sed -E -e 's/[^[:alnum:]]+/_/g' -e 's/(^_|_$)//g')
if [ -z "$MAKER" ]; then
    echo "Error: Could not determine system product."
    exit 1
fi

TARGET_DIR="$REPO_DIR/test_results/$MAKER"
mkdir -p "$TARGET_DIR"

FOUND=0
for f in "$TMPDIR"/*.txt; do
    if [ -e "$f" ]; then
        FOUND=1
        mv "$f" "$TARGET_DIR/"
    fi
done

if [ "$FOUND" -eq 0 ]; then
    echo "Warning: No .txt files found to move."
fi

echo "Finished. Thank you for your contribution!"

