import re
import json
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent

def parse_spec():
    with open(REPO_ROOT / 'Master Spec.md', 'r', encoding='utf-8') as f:
        content = f.read()

    sections = re.findall(r'## SECTION (\d+) — (.+?)\n\n(.*?)(?=\n## SECTION |\Z)', content, re.DOTALL)

    with open(REPO_ROOT / 'parsed_sections.json', 'w', encoding='utf-8') as f:
        json.dump([{"id": s[0], "title": s[1].strip(), "content": s[2].strip()} for s in sections], f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    parse_spec()
