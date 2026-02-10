import sys
import re
from html import escape

COLUMNS = ["Graphics", "Networking", "Audio", "Storage", "USB Ports", "Bluetooth"]

def parse_file(path):
    with open(path) as f:
        lines = f.readlines()

    model = None
    data = {c: [] for c in COLUMNS}

    current_section = None
    current_status = None

    for line in lines:
        line = line.rstrip()

        if line.startswith("Hardware:"):
            model = line.split("Hardware:", 1)[1].strip()
            continue

        m = re.match(r"-\s+(.+)", line)
        if m:
            section = m.group(1)
            if section in data:
                current_section = section
            else:
                current_section = None
            current_status = None
            continue

        m = re.match(r"\s*Device \d+ Status:\s+(\w+)", line)
        if m and current_section:
            current_status = m.group(1)
            continue

        m = re.match(r"\s*Status:\s+(.+)", line)
        if m and current_section:
            data[current_section].append(m.group(1))
            continue

        m = re.match(r"\s*device\s+=\s+'(.+)'", line)
        if m and current_section and current_status:
            device = m.group(1)
            data[current_section].append(f"{device} ({current_status})")
            continue

    return model, data

def emit_html(model, data):
    print(f"<tr><td>{escape(model)}</td>", end="")
    for c in COLUMNS:
        cell = "<br>".join(escape(x) for x in data[c]) or "&nbsp;"
        print(f"<td>{cell}</td>", end="")
    print("</tr>")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python hw_to_html.py <file>")
        sys.exit(1)

    model, data = parse_file(sys.argv[1])
    emit_html(model, data)
