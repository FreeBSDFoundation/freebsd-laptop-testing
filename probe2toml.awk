#!/usr/bin/env -S awk -f

BEGIN {
  interesting["graphics"] = 1
  interesting["networking"] = 1
  interesting["audio"] = 1
  interesting["usb"] = 1
}

function sanitize_name(s) {
  gsub(/[^[:alnum:]]+/, "_", s);
  sub(/(^_|_$)/, "", s)
  return s
}

$1 == "Hardware:" {
  $1=""
  model = substr($0,2)
  probe_dir = sanitize_name(model)
}

/^- [A-Z]/ {
  category = tolower($2)
  num_devices = 0
}

$1 == "vendor" {
  $1=$2=""
  gsub(/['"]/, "")
  vendor = substr($0,3)
}

$1 == "device" {
  $1=$2=""
  gsub(/['"]/, "")
  #categories[category]["devices"][++num_devices] = sprintf("%s: %s", vendor, substr($0,3))
  categories[category]["devices"][++num_devices] = substr($0,3)
}

/^\s*Category Total Score:/ {
  split($NF, tmp, "/")
  score = tmp[1] + 0
  categories[category]["score"] = score
  total_score += score * interesting[category]
}

/^Model name:/ {
  $1=$2=""
  cpu = substr($0,3)
}

END {
  print "[[laptops]]"
  printf("model=\"%s\"\n", model)
  printf("cpu=\"%s\"\n", cpu)
  printf("total_score=%s\n", total_score)
  printf("probe_dir=\"%s\"\n", probe_dir)

  for (c in categories) {
    if (interesting[c]) {
      printf("[laptops.%s]\ndevices=[", c)
      for (d in categories[c]["devices"]) {
        printf("\"%s\",", categories[c]["devices"][d])
      }
      printf("]\nscore=%d\n", categories[c]["score"])
    }
  }
}
