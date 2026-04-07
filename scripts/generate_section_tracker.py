import json
import os
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent

def main():
    with open(REPO_ROOT / 'parsed_sections.json', 'r', encoding='utf-8') as f:
        sections = json.load(f)

    os.makedirs(REPO_ROOT / 'docs', exist_ok=True)
    with open(REPO_ROOT / 'docs' / 'section-tracker.md', 'w', encoding='utf-8', newline='\n') as f:
        f.write('# Section Tracker\n\n')
        f.write('| Section | Title | Status | Notes |\n')
        f.write('|---|---|---|---|\n')
        for s in sections:
            f.write(f'| {s["id"]} | {s["title"]} | Unstarted | |\n')

if __name__ == '__main__':
    main()
