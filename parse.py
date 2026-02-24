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

    model, ranking = None, None
    data = {c: [] for c in COLUMNS}
    current_section = None

    for line in lines:
        line = line.rstrip()
        if line.startswith("Hardware:"):
            model = line.split("Hardware:", 1)[1].strip()
        elif line.startswith("Score:"):
            ranking = line.split("Score:", 1)[1].strip()
        m = re.match(r"-\s+(.+)", line)
        if m:
            section = m.group(1)
            current_section = section if section in data else None
            continue

        m = re.match(r"\s*Status:\s+(.+)", line)
        if m and current_section:
            data[current_section].append(m.group(1))

        m = re.match(r"\s*device\s+=\s+'(.+)'", line)
        if m and current_section:
            data[current_section].append(m.group(1))

    return model, ranking, data

def emit_html(model, ranking, data, path):
    #Generate github link for user to click on
    repo = os.getenv('REPO_CONTEXT', 'unknown/repo')
    branch = os.getenv('BRANCH_NAME', 'main')
    clean_path = path.lstrip("./")
    github_link = f"https://github.com/{repo}/blob/{branch}/{clean_path}"
    print(f"<tr>", end="")

    #Model cell with link
    print(f"<td><strong>{escape(model)}</strong><br>", end="")
    print(f"<a href='{github_link}' style='font-size: 0.8em;'>View Probe</a></td>", end="")

    for c in COLUMNS:
        items = data[c]
        if not items:
            cell = "&nbsp;"
        else:
            list_contents = "".join(f"<li>{escape(x)}</li>" for x in items)
            cell = f"<ol style='margin: 0; padding-left: 1.5em;'>{list_contents}</ol>"
        print(f"<td>{cell}</td>", end="")
    score_display = ranking if ranking is not None else "&nbsp;"
    print(f"<td>{score_display}</td>", end="")
    print("</tr>")


if __name__ == "__main__":
    if "--rank" in sys.argv:
        get_rows()
    elif len(sys.argv) == 2:
        file_path = sys.argv[1] # get the path
        model, ranking, data = parse_file(file_path)
        emit_html(model, ranking, data, file_path) #pass it here
    else:
        print("Usage: python parse.py --rank  or  python script.py <filename>")
        sys.exit(1)
