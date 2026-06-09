#!/bin/sh

set -eu

cd test_results
for d in *; do
  ../probe2toml.awk $(ls -1 "${d}"/probe_*.txt | sort | tail -1)
done
