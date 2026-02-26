import sys
from pathlib import Path
import re
from datetime import datetime
import subprocess

if len(sys.argv) >= 2:
    tmpdir = Path(sys.argv[1])
else:
    tmpdir = Path.home() / "hwify"  # if user wants to run the script without a temp directory

base_hwinfo = tmpdir / "hw.info"  # to test both in dir and in the repo's temp directory

hw_probe_dump = base_hwinfo / "devices"
pciconf_path = base_hwinfo / "logs" / "pciconf"
uname_path = base_hwinfo / "logs" / "uname"
kld_path = base_hwinfo / "logs" / "kldstat"
cpu_path = base_hwinfo / "logs" / "lscpu"

input_string = "kenv | grep smbios.system.product"
filename_final = datetime.now().strftime(
    "%Y-%m-%d_%H-%M-%S")  # fallback filename for time stamp in case smbios is not present on the machine
result = subprocess.run(input_string, capture_output=True, text=True, shell=True)
output_string = result.stdout
filename = re.search('"([^"]*)"', output_string)
# filename is the make of the computer
if filename:
    filename = filename.group(1)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename_final = f"probe_{timestamp}.txt"
    # Regex to get only basic characters into the filename
    step1 = re.sub(r'[^a-zA-Z0-9_\-.\s]', '_', filename_final)
    filename_final = re.sub(r'\s+', '', step1)


def get_device(input_file, search_terms):
    if isinstance(search_terms, str):
        search_terms = [search_terms]
    # create combined regex to find multiple search terms under each file
    combined_pattern = "|".join([re.escape(term) for term in search_terms])

    subclass_pat = re.compile(rf'subclass\s*=\s*({combined_pattern})', re.IGNORECASE)
    class_pat = re.compile(rf'class\s*=\s*({combined_pattern})', re.IGNORECASE)
    header_pat = re.compile(r'\S+@pci\d+:')

    def scan(pattern):
        matches = []
        buffer = []
        try:
            with open(input_file, 'r') as f_in:
                for line in f_in:
                    if header_pat.search(line):
                        buffer = [line]
                    else:
                        buffer.append(line)

                    if pattern.search(line):
                        matches.append("".join(buffer))
                        buffer = []
        except FileNotFoundError:
            return []
        return matches

    results = scan(subclass_pat)
    if not results:
        results = scan(class_pat)

    return results


def generate_hardware_summary(pciconf, hw_probe, output):
    categories = {
        "Graphics": (("vga", "display"), "graphics card"),
        "Networking": ("network", "network"),
        "Audio": (("hda", "multimedia"), "hda"),
        "Storage": ("mass storage", "storage"),
        "USB Ports": ("usb", "usb"),
        "Bluetooth": ("bluetooth", "bluetooth")
    }

    category_results = {}

    for label, (pci_key, probe_key) in categories.items():
        pci_blocks = get_device(pciconf, pci_key)
        probe_devices = get_hw_devices(hw_probe, probe_key)
        category_results[label] = (pci_blocks, probe_devices)

    with open(output, "w") as out:
        out.write("=== FreeBSD Hardware Status Info ===\n\n")
        out.write(f"Running: {get_uname_details().strip()}\n")
        out.write(f"Hardware: {filename}\n")
        out.write("-" * 36 + "\n\n")

        for label, (pci_blocks, probe_devices) in category_results.items():
            out.write(f"- {label}\n")

            category_score = 0
            device_count = len(pci_blocks)

            if pci_blocks:
                for i, block in enumerate(pci_blocks, 1):
                    hw_status = (
                        probe_devices[i - 1]["status"]
                        if i - 1 < len(probe_devices)
                        else "unknown"
                    )

                    device_score = 0
                    if hw_status.lower() in ["works", "detected"]:
                        device_score = 2
                        category_score += 2

                    out.write(f"  Device {i} Status: {hw_status.upper()}\n")
                    out.write(f"  Device Score: {device_score}/2\n")
                    indented = "    " + block.replace("\n", "\n    ").strip()
                    out.write(f"{indented}\n")

                # Print the category total score (2 points possible per device found)
                out.write(f"\n  Category Total Score: {category_score}/{device_count * 2}\n")
            else:
                out.write("  Status: NOT DETECTED\n")
                out.write("  Category Total Score: 0/0\n")

            out.write("\n" + "-" * 20 + "\n\n")

        out.write("=== FreeBSD Detailed Status Info ==\n\n")
        out.write("Currently loaded kernel modules:\n")
        out.write(get_kldstat())
        out.write("\n" + "=" * 36 + "\n\n")
        out.write("- CPU Info\n")
        out.write(get_cpuinfo())
        out.write("\n" + "=" * 36 + "\n")


def get_hw_devices(probe_file, category_name):
    devices = []
    status_pattern = re.compile(r'\b(works|failed|detected|limited|malfunc)\b', re.IGNORECASE)
    try:
        with open(probe_file, 'r') as f:
            for line in f:
                if category_name.lower() in line.lower():
                    status = "unknown"
                    m = status_pattern.search(line)
                    if m:
                        status = m.group(1).lower()
                    devices.append({
                        "raw": line.strip(),
                        "status": status
                    })
    except FileNotFoundError:
        pass
    return devices


def get_uname_details():
    uname_file = open(uname_path, "r")
    content = uname_file.read()
    return content


def get_kldstat():
    module_names = []
    with open(kld_path, "r") as kld_file:
        for line in kld_file:
            columns = line.split()
            if columns and columns[-1].endswith(".ko"):
                module_names.append(columns[-1])
    module_names.sort()
    return "\n".join(module_names)


def get_cpuinfo():
    cpu_file = open(cpu_path, "r")
    content = cpu_file.read()
    return content


generate_hardware_summary(pciconf_path, hw_probe_dump, filename_final)
