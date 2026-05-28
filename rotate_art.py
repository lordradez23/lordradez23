import os
import random
import re

def rotate_art():
    art_dir = "arts"
    readme_path = "README.md"
    
    # 1. Get all art files
    try:
        art_files = [f for f in os.listdir(art_dir) if f.endswith(".txt")]
        if not art_files:
            print("No art files found in 'arts/' directory.")
            return
    except FileNotFoundError:
        print(f"Directory '{art_dir}' not found.")
        return

    # 2. Pick a random art file
    selected_art_file = random.choice(art_files)
    art_path = os.path.join(art_dir, selected_art_file)
    
    with open(art_path, "r", encoding="utf-8") as f:
        art_content = f.read()

    # 3. Prepare the replacement block
    # We wrap it in a <pre> tag with a "Matrix Green" executable look
    style = 'font-family: "Courier New", monospace; line-height: 1.1; font-size: 13px; background: #000; color: #00ff41; padding: 20px; border-radius: 4px; border: 2px solid #00ff41; box-shadow: 0 0 10px #00ff41; overflow-x: auto;'
    header = f'<div style="background: #00ff41; color: #000; padding: 2px 10px; font-weight: bold; font-family: monospace;">EXEC: {selected_art_file} --status RUNNING</div>'
    art_block = f'<!-- START_ART -->\n<div align="center" style="margin-top: 20px;">\n{header}\n<pre style="{style}">\n{art_content}\n</pre>\n<div style="color: #00ff41; font-family: monospace; font-size: 10px; margin-top: 5px;">[ LOG ]: Processed at system_time_alpha_v1</div>\n</div>\n<!-- END_ART -->'

    # 4. Read README.md
    if not os.path.exists(readme_path):
        print(f"'{readme_path}' not found.")
        return

    with open(readme_path, "r", encoding="utf-8") as f:
        readme_content = f.read()

    # 5. Replace the art section
    pattern = r"<!-- START_ART -->.*?<!-- END_ART -->"
    if re.search(pattern, readme_content, re.DOTALL):
        new_readme_content = re.sub(pattern, art_block, readme_content, flags=re.DOTALL)
    else:
        # If placeholders don't exist, append to the top (or bottom)
        print("Placeholders not found. Appending art to the top of README.md")
        new_readme_content = art_block + "\n\n" + readme_content

    # 6. Save the updated README.md
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_readme_content)
    
    print(f"Successfully updated README.md with {selected_art_file}")

if __name__ == "__main__":
    rotate_art()
