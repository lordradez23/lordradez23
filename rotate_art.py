import json
import os
import re
from datetime import date

RUNS_FILE = "runs.json"
ART_DIR = "arts"
README_PATH = "README.md"


def load_runs():
    if os.path.exists(RUNS_FILE):
        with open(RUNS_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                pass
    return {"last_rotated": "", "last_art": ""}


def save_runs(data):
    with open(RUNS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def next_art(art_files, last_art):
    """Return the next art file in sorted order, cycling back to start."""
    art_files = sorted(art_files)
    if last_art in art_files:
        idx = (art_files.index(last_art) + 1) % len(art_files)
    else:
        idx = 0
    return art_files[idx]


def rotate_art():
    runs = load_runs()
    today = str(date.today())

    if runs.get("last_rotated") == today:
        print(f"Already rotated today ({today}). Skipping.")
        return

    try:
        art_files = [f for f in os.listdir(ART_DIR) if f.endswith(".txt")]
        if not art_files:
            print("No art files found in 'arts/' directory.")
            return
    except FileNotFoundError:
        print(f"Directory '{ART_DIR}' not found.")
        return

    selected = next_art(art_files, runs.get("last_art", ""))
    art_path = os.path.join(ART_DIR, selected)

    with open(art_path, "r", encoding="utf-8") as f:
        art_content = f.read()

    style = (
        'font-family: "Courier New", monospace; line-height: 1.1; font-size: 13px; '
        'background: #000; color: #00ff41; padding: 20px; border-radius: 4px; '
        'border: 2px solid #00ff41; box-shadow: 0 0 10px #00ff41; overflow-x: auto;'
    )
    header = (
        f'<div style="background: #00ff41; color: #000; padding: 2px 10px; '
        f'font-weight: bold; font-family: monospace;">EXEC: {selected} --status RUNNING</div>'
    )
    art_block = (
        f'<!-- START_ART -->\n'
        f'<div align="center" style="margin-top: 20px;">\n'
        f'{header}\n'
        f'<pre style="{style}">\n'
        f'{art_content}\n'
        f'</pre>\n'
        f'<div style="color: #00ff41; font-family: monospace; font-size: 10px; margin-top: 5px;">'
        f'[ LOG ]: Processed at system_time_alpha_v1</div>\n'
        f'</div>\n'
        f'<!-- END_ART -->'
    )

    if not os.path.exists(README_PATH):
        print(f"'{README_PATH}' not found.")
        return

    with open(README_PATH, "r", encoding="utf-8") as f:
        readme = f.read()

    pattern = r"<!-- START_ART -->.*?<!-- END_ART -->"
    if re.search(pattern, readme, re.DOTALL):
        readme = re.sub(pattern, art_block, readme, flags=re.DOTALL)
    else:
        print("Placeholders not found. Appending art to top of README.md.")
        readme = art_block + "\n\n" + readme

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(readme)

    runs["last_rotated"] = today
    runs["last_art"] = selected
    save_runs(runs)

    print(f"Rotated to {selected} on {today}.")


if __name__ == "__main__":
    rotate_art()
