import json
from pathlib import Path

from alive_progress import alive_bar

base_wordlist = set()
for file in Path('base_wordlists').glob('*.txt'):
    base_wordlist |= set(file.read_text().strip().splitlines())

badwords = set(Path('in', 'badwords.txt').read_text().strip().splitlines())
related = json.loads(Path('in', 'related.json').read_text())

allowed = set(Path('in', 'allowed.txt').read_text().strip().splitlines())
notallowed = set(Path('in', 'notallowed.txt').read_text().strip().splitlines())

out_wordlist = set()
out_badwordlist = set()

print(f'base wordlist: {len(base_wordlist):_}')
print(f'badwords: {len(badwords):_}')
print(f'allowedwords: {len(allowed):_}')
print(f'notallowedwords: {len(notallowed):_}')

with alive_bar(len(base_wordlist)) as bar:
    for word in base_wordlist:
        if 2 <= len(word) <= 40:
            if word in allowed:
                # print(f'word: {word} in allowed')
                out_wordlist.add(word)
            elif word in notallowed:
                # print(f'word: {word} in notallowed')
                out_badwordlist.add(word)
            elif len(word) == 2 or (
                word not in badwords
                and all(badword not in related.get(word, []) for badword in badwords)
            ):
                # print(f'word: {word} not in badwords')
                out_wordlist.add(word)
            else:
                # print(f'word: {word} in badwords')
                out_badwordlist.add(word)
        bar()

print(f'wordlist: {len(out_wordlist):_}')
print(f'badwordlist: {len(out_badwordlist):_}')

Path('out', 'wordlist.txt').write_text(
    '\n'.join(sorted(out_wordlist, key=lambda x: (x.lower(),))),
)
Path('out', 'badwordlist.txt').write_text(
    '\n'.join(sorted(out_badwordlist, key=lambda x: (x.lower(),))),
)
