import json
import os

def main():
    with open('parsed_sections.json', 'r') as f:
        sections = json.load(f)

    os.makedirs('docs', exist_ok=True)
    with open('docs/section-tracker.md', 'w') as f:
        f.write('# Section Tracker\n\n')
        f.write('| Section | Title | Status | Notes |\n')
        f.write('|---|---|---|---|\n')
        for s in sections:
            f.write(f'| {s["id"]} | {s["title"]} | Unstarted | |\n')

if __name__ == '__main__':
    main()
