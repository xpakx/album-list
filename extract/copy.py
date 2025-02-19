import orgparse
import os
import json
from typing import Dict, Any


def load_config(filename: str) -> Dict[str, Any]:
    with open(filename, 'r') as file:
        return json.load(file)


def copy_file(org_file: str, year: int, name: str):
    with open(org_file, 'r', encoding='utf-8') as f:
        org_content = f.read()
    org_root = orgparse.loads(org_content)

    if org_root.children:
        first_section = org_root.children[0]
        body = first_section.body

        with open(f'data/{name}', 'w', encoding='utf-8') as output_file:
            output_file.write(f"* {year}\n{body}\n")
    else:
        print("No sections found in the Org file.")


def get_emacs_data():
    config = load_config("extract/config.json")
    files = config["years"]
    main = os.path.expanduser(config['main_dir'])

    for file in files:
        org = main + file['org']
        year = file['year']
        name = file['name'] if 'name' in file else f"{year}.org"
        copy_file(org, year, name)


get_emacs_data()
