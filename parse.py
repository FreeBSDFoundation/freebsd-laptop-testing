#
# SPDX-FileCopyrightText: 2026 Shreeney Ajmeri <ajmerishreeney@gmail.com>
#
# SPDX-License-Identifier: BSD-2-Clause
#
import sys
import re
import glob
from html import escape
import os

COLUMNS = ["Graphics", "Networking", "Audio", "USB Ports"]


def format_score(value):
    return int(value) if value % 1 == 0 else value


def get_rows():
    data_list = []
    for filepath in glob.glob("**/*.txt", recursive=True):
        try:
            model, ranking, _, _ = parse_file(filepath)
            if model and "/" in ranking:
                parts = ranking.split('/')
                earned = float(parts[0])
                possible = float(parts[1])

                # Filter specifically for 8/8 scores
                if earned == 8 and possible == 8:
                    data_list.append({
                        "name": model,
                        "score_str": ranking
                    })
        except Exception:
            continue

    for item in data_list[:10]:
        print(f"<tr><td>{escape(item['name'])}</td><td><span class='score-badge'>{item['score_str']}</span></td></tr>")


def parse_file(path):
    with open(path) as f:
        lines = f.readlines()

    model = "Unknown Hardware"
    data = {c: [] for c in COLUMNS}
    scores = {c: None for c in COLUMNS}

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

    ranking = f"{format_score(total_earned)}/{format_score(total_possible)}"
    return model, ranking, data, scores


def emit_html(model, ranking, data, scores, path):
    repo = os.getenv('REPO_CONTEXT', 'FreeBSDFoundation/freebsd-laptop-testing')
    branch = os.getenv('BRANCH_NAME', 'main')
    clean_path = path.lstrip("./")
    github_link = f"https://github.com/{repo}/blob/{branch}/{clean_path}"
    file_dir = os.path.dirname(path)
    comment_file = os.path.join(file_dir, "comments.md")
    comment_link_html = ""

    if os.path.exists(comment_file):
        clean_comment_path = comment_file.lstrip("./")
        comment_url = f"https://github.com/{repo}/blob/{branch}/{clean_comment_path}"
        comment_link_html = f"<br><a href='{comment_url}'>View Comments</a>"

    print(f"<tr>", end="")
    # Model cell
    print(f"<td data-label='Model'>", end="")
    print(f"<div class='mob-header'><span class='mob-label-text'>Model</span></div>", end="")
    print(f"<div class='cell-content'><strong>{escape(model)}</strong><br>", end="")
    print(f"<a href='{github_link}'>View Probe</a>", end="")
    print(f"{comment_link_html}</div></td>", end="")

    for c in COLUMNS:
        items = data[c]
        score_val = scores[c]

        if not items:
            print(f"<td data-label='{c}' data-empty='1'>&nbsp;</td>", end="")
        else:
            list_contents = "".join(f"<li>{escape(x)}</li>" for x in items)
            score_html = f"<div class='cell-score'><strong>Score: {score_val}</strong></div>" if score_val else ""
            score_pill = f"<span class='mob-score-pill'>Score {score_val}</span>" if score_val else ""
            print(f"<td data-label='{c}'>", end="")
            print(f"<div class='mob-header'><span class='mob-label-text'>{c}</span>{score_pill}</div>", end="")
            print(f"<div class='cell-content'><ol>{list_contents}</ol>{score_html}</div>", end="")
            print(f"</td>", end="")

    # Total score cell
    print(f"<td data-label='Score'>", end="")
    print(f"<div class='mob-header'><span class='mob-label-text'>Total Score</span></div>", end="")
    print(f"<span class='score-badge'>{ranking}</span></td>", end="")
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
