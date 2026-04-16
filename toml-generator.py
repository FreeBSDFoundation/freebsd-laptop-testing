import sys
import re
import glob
import os

COLUMNS = ["Graphics", "Networking", "Audio", "USB Ports"]


def format_score(value):
    return int(value) if value % 1 == 0 else value


def parse_file(path):
    with open(path) as f:
        lines = f.readlines()

    model = "Unknown Hardware"
    data = {c: [] for c in COLUMNS}
    scores = {c: "0/0" for c in COLUMNS}
    total_earned = 0.0
    total_possible = 0.0
    current_section = None

    for line in lines:
        line = line.rstrip()
        if line.startswith("Hardware:"):
            parts = line.split("Hardware:", 1)
            if len(parts) > 1:
                model = parts[1].strip()

        m_sec = re.match(r"-\s+(.+)", line)
        if m_sec:
            section = m_sec.group(1)
            current_section = section if section in data else None
            continue

        if current_section:
            m_dev = re.match(r"\s*device\s+=\s+'(.+)'", line)
            if m_dev:
                data[current_section].append(m_dev.group(1))

            m_score = re.search(r"Category Total Score:\s*([\d.]+)/([\d.]+)", line)
            if m_score:
                earned = float(m_score.group(1))
                possible = float(m_score.group(2))
                scores[current_section] = f"{format_score(earned)}/{format_score(possible)}"
                total_earned += earned
                total_possible += possible

    return {
        "model": model,
        "overall_score": f"{format_score(total_earned)}/{format_score(total_possible)}",
        "category_scores": scores,
        "details": data,
        "file_path": path
    }

def generate_manual_toml():
    search_path = os.path.join("test_results", "**", "*.txt")
    for filepath in glob.glob(search_path, recursive=True):
        try:
            p = parse_file(filepath)
            print(f"\n[[laptops]]")
            print(f'model = "{p["model"]}"')
            print(f'overall_score = "{p["overall_score"]}"')
            print(f'file_path = "{p["file_path"]}"')
            print(f"\n[laptops.category_scores]")
            for cat, score in p["category_scores"].items():
                print(f'"{cat}" = "{score}"')
            print(f"\n[laptops.details]")
            for cat, devices in p["details"].items():
                device_list = ", ".join([f'"{d}"' for d in devices])
                print(f'"{cat}" = [{device_list}]')

        except Exception as e:
            #print to stderr so that stdout toml output doesn't get interrupted
            import sys
            print(f"Error parsing {filepath}: {e}", file=sys.stderr)


if __name__ == "__main__":
    generate_manual_toml()

