import os
import re
from datetime import datetime
import subprocess
import shutil

hw_probe_dump = os.path.expanduser("~/hwify/hw.info/devices")
ifconfig_path = os.path.expanduser("~/hwify/hw.info/logs/ifconfig")
pciconf_path = os.path.expanduser("~/hwify/hw.info/logs/pciconf")
uname_path = os.path.expanduser("~/hwify/hw.info/logs/uname")

input_string = "kenv | grep smbios.system.product"
filename_final  = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") #fallback filename for time stamp in case smbios is not present on the machine
result = subprocess.run(input_string, capture_output=True, text=True, shell=True)
output_string = result.stdout
filename = re.search('"([^"]*)"', output_string)

if filename:
    filename = filename.group(1)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename_final = f"{filename}_{timestamp}.txt"
    #Regex to get only basic characters into the filename
    step1 = re.sub(r'[^a-zA-Z0-9_\-.\s]', '_', filename_final)
    filename_final = re.sub(r'\s+', '', step1)


def get_device(input_file, search_terms):
    if isinstance(search_terms, str):
        search_terms = [search_terms]
#create combined regex to find multiple search terms under each file
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


def generate_hardware_summary(ifconfig, pciconf, hw_probe, output):
    categories = {
        #multiple aliases for devices are in pciconf, so have some logic to handle it
        "Graphics": (("vga", "display"), "graphics card"),
        "Networking": ("network", "network"),
        "Audio": (("hda", "multimedia"), "hda"),
        "Storage": ("mass storage", "storage"),
        "USB Ports": ("usb", "usb"),
        "Bluetooth": ("bluetooth", "bluetooth")
    }

    with open(output, "w") as out:
        out.write("=== FreeBSD Hardware Status Info ===\n\n")
        out.write("Running: ")
        out.write(get_uname_details())
        out.write("\n")
        for label, (pci_key, probe_key) in categories.items():

            pci_blocks = get_device(pciconf, pci_key)
            probe_devices = get_hw_devices(hw_probe, probe_key)

            out.write(f"- {label}\n")
            if pci_blocks:
                for i, block in enumerate(pci_blocks, 1):
                    hw_status = (
                        probe_devices[i - 1]["status"]
                        if i - 1 < len(probe_devices)
                        else "unknown"
                    )

                    out.write(f"  Device {i} Status: {hw_status.upper()}\n")
                    indented = "    " + block.replace("\n", "\n    ").strip()
                    out.write(f"{indented}\n")
            else:
                out.write("  Status: NOT DETECTED\n")

            out.write("\n" + "-" * 20 + "\n\n")
        out.write("=== FreeBSD Detailed Status Info ==\n\n")

        out.write("Kldstat output:")
        kld_data = get_kldstat()
        out.write(kld_data)
        out.write("\n" + "="*36 + "\n")
        out.write("ifconfig detailed output: ")
        ifconfig_status = get_ifconfig_details(ifconfig)
        out.write("- Active Connection Details: \n")
        for detail in ifconfig_status:
            out.write(f"    {detail}\n")
        out.write("\n")
        #move file into the test results dir
        try:
            shutil.move(filename_final, os.path.join("test_results", filename_final))
        except Exception as e:
            print(f"Failed to move file: {e}")
        out.write("\n")
        out.write("- CPU Info")
        out.write("\n")
        cpu_data = get_cpuinfo()
        out.write(cpu_data)
        out.write("\n" + "="*36 + "\n")

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
    kldstat = subprocess.run(["kldstat"], capture_output=True, text=True)
    return kldstat.stdout

def get_cpuinfo():
    cpu = subprocess.run(["lscpu"], capture_output=True, text=True)
    return cpu.stdout

def get_ifconfig_details(input_file):

    pattern = re.compile(r'ssid|media', re.IGNORECASE)
    results = []

    try:
        with open(input_file, 'r') as f:
            for line in f:
                if pattern.search(line):
                    results.append(line.strip())
    except FileNotFoundError:
        return ["Ifconfig file not found."]

    return results if results else ["No Wi-fi info found."]

generate_hardware_summary(ifconfig_path,pciconf_path, hw_probe_dump, filename_final)
