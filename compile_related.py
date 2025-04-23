from __future__ import annotations

import json
import re
from pathlib import Path
from string import ascii_uppercase

from alive_progress import alive_bar

badwords = set(Path('in', 'badwords.txt').read_text().strip().splitlines())

print(f'badwords: {len(badwords):_}')

dictionary_combined = {}
related_words_map: dict[str, set] = {}

for file in Path('base_dictionaries').glob('*.txt'):
    if file.is_file():
        current_dictionary = dict(
            x.split('\t') for x in file.read_text().splitlines()[2:]
        )
        with alive_bar(len(current_dictionary)) as bar:
            for k, v in current_dictionary.items():
                if any(flag in v.lower() for flag in ['(offensive)', '(vulgar)']):
                    badwords.add(k)
                related_words_map |= {
                    k: {
                        x
                        for x in re.findall(r'(?<!-)\b[A-Z]+\b', v)
                        if len(x) > 1 and all(c in ascii_uppercase for c in x)
                    },
                }
                bar()
        dictionary_combined |= current_dictionary

all_keys = set(related_words_map.keys())
all_related: dict[str, list] = {}
with alive_bar(len(all_keys)) as bar:
    for k in all_keys:
        all_related |= {
            k: sorted(related_words_map.get(k, set()), key=lambda x: x.lower()),
        }
        bar()

any_changes_made = True
while any_changes_made:
    any_changes_made = False
    with alive_bar(len(all_related)) as bar:
        for k, refs in list(all_related.items()):
            for ref in refs:
                if ref not in all_related:
                    all_related[ref] = []
                    any_changes_made = True
                if k not in all_related[ref]:
                    all_related[ref].append(k)
                    all_related[ref].sort(key=lambda x: x.lower())
                    any_changes_made = True
            bar()

print(f'results: {len(all_related):_}')
print(f'badwords: {len(badwords):_}')

Path('in', 'related.json').write_text(
    json.dumps(all_related, indent=2, ensure_ascii=False, sort_keys=True),
)
Path('in', 'badwords.txt').write_text(
    '\n'.join(sorted(badwords, key=lambda x: x.lower())),
)
