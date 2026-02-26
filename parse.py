import sys
import re
import glob
from html import escape
import os

COLUMNS = ["Graphics", "Networking", "Audio", "Storage", "USB Ports"]


def get_rows():
    data_list = []
    for filepath in glob.glob("**/*.txt", recursive=True):
        try:
            with open(filepath, 'r') as f:
                content = f.read()
                hw_match = re.search(r"Hardware:\s*(.*)", content)
                score_match = re.search(r"Score:\s*(\d+)/", content)
                if hw_match and score_match:
                    data_list.append({
                        "name": hw_match.group(1).strip(),
                        "score": int(score_match.group(1))
                    })
        except Exception:
            continue

    data_list.sort(key=lambda x: x['score'], reverse=True)
    for item in data_list[:5]: #Slice off last 5 items for top score
        print(f"<tr><td>{escape(item['name'])}</td><td>{item['score']}</td></tr>")


def parse_file(path):
    with open(path) as f:
        lines = f.readlines()

    model = "Unknown Hardware"
    data = {c: [] for c in COLUMNS}
    scores = {c: None for c in COLUMNS}

    total_earned = 0
    total_possible = 0
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
            m_score = re.search(r"Category Total Score:\s*(\d+)/(\d+)", line)
            if m_score:
                earned = int(m_score.group(1))
                possible = int(m_score.group(2))
                scores[current_section] = f"{earned}/{possible}"
                total_earned += earned
                total_possible += possible

    ranking = f"{total_earned}/{total_possible}"
    return model, ranking, data, scores


def emit_html(model, ranking, data, scores, path):
    repo = os.getenv('REPO_CONTEXT', 'unknown/repo')
    branch = os.getenv('BRANCH_NAME', 'main')
    clean_path = path.lstrip("./")
    github_link = f"https://github.com{repo}/blob/{branch}/{clean_path}"

    print(f"<tr>", end="")
    print(f"<td><strong>{escape(model)}</strong><br>", end="")
    print(f"<a href='{github_link}' style='font-size: 0.8em;'>View Probe</a></td>", end="")

    for c in COLUMNS:
        items = data[c]
        score_val = scores[c]

        if not items:
            cell = "&nbsp;"
        else:
            list_contents = "".join(f"<li>{escape(x)}</li>" for x in items)
            score_html = f"<div style='margin-top: 5px; border-top: 1px solid #ddd; font-size: 0.9em;'><strong>Score: {score_val}</strong></div>" if score_val else ""
            cell = f"<ol style='margin: 0; padding-left: 1.5em;'>{list_contents}</ol>{score_html}"

        print(f"<td>{cell}</td>", end="")

    print(f"<td><strong>{ranking}</strong></td>", end="")
    print("</tr>")


if __name__ == "__main__":
    if "--rank" in sys.argv:
        get_rows()
    elif len(sys.argv) == 2:
        file_path = sys.argv[1]
        model, ranking, data, scores = parse_file(file_path)
        emit_html(model, ranking, data, scores, file_path)
    else:
        print("Usage: python parse.py --rank  or  python script.py <filename>")
        sys.exit(1)
