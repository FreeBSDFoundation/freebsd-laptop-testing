import sys
import re
import glob
import os

COLUMNS = ["Graphics", "Networking", "Audio", "USB Ports"]
REPO_URL = "https://github.com/FreeBSDFoundation/freebsd-laptop-testing/tree/main"

def format_score(value):
    return int(value) if value % 1 == 0 else value

def parse_file(path):
    with open(path) as f:
        lines = f.readlines()

    model = "Unknown Hardware"
    data = {c: [] for c in COLUMNS}
    scores = {c: 0 for c in COLUMNS}
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
                # Store only the earned value as a formatted number
                scores[current_section] = format_score(earned)
                total_earned += earned
                total_possible += possible

    comments_file = os.path.join(os.path.dirname(path), "comments.md")
    comments_link = f"{REPO_URL}/{comments_file}" if os.path.exists(comments_file) else ""

    return {
        "model": model,
        "category_scores": scores,
        "details": data,
        "probe_url": f"{REPO_URL}/{path}",
        "comments_link": comments_link
    }

def generate_manual_toml():
    search_path = os.path.join("test_results", "**", "*.txt")
    for filepath in glob.glob(search_path, recursive=True):
        try:
            p = parse_file(filepath)
            print(f"\n[[laptops]]")
            print(f'model = "{p["model"]}"')
            print(f'probe_url = "{p["probe_url"]}"')
            if p["comments_link"]:
                print(f'comments_link = "{p["comments_link"]}"')

            # Flattened Scores
            for cat, score in p["category_scores"].items():
                key = cat.lower().replace(" ", "_")
                print(f'{key}_score = {score}')

            # Flattened Details
            for cat, devices in p["details"].items():
                key = cat.lower().replace(" ", "_")
                device_list = ", ".join([f'"{d}"' for d in devices])
                print(f'{key}_devices = [{device_list}]')

        except Exception as e:
            print(f"Error parsing {filepath}: {e}", file=sys.stderr)

if __name__ == "__main__":
    generate_manual_toml()
