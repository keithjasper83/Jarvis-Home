import re
import json

def parse_spec():
    with open('Master Spec.md', 'r') as f:
        content = f.read()

    sections = re.findall(r'## SECTION (\d+) — (.+?)\n\n(.*?)(?=\n## SECTION |\Z)', content, re.DOTALL)

    with open('parsed_sections.json', 'w') as f:
        json.dump([{"id": s[0], "title": s[1].strip(), "content": s[2].strip()} for s in sections], f, indent=2)

if __name__ == '__main__':
    parse_spec()
