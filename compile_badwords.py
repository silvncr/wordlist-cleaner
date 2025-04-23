from pathlib import Path
from string import ascii_uppercase

from alive_progress import alive_bar

_badwords = set(Path('in', 'badwords.txt').read_text().strip().splitlines())
base_wordlist = set()
for file in Path('base_wordlists').glob('*.txt'):
    base_wordlist |= set(file.read_text().strip().splitlines())

print(f'badwords: {len(_badwords):_}')

badwords = set()

with alive_bar(len(_badwords)) as bar:
    for _word in _badwords:
        if any(c not in f'{ascii_uppercase}-_ ' for c in _word):
            continue
        word = ''.join(c for c in _word if c.isalpha())
        if word in base_wordlist:
            badwords.add(word.upper())
        bar()

print(f'badwords: {len(badwords):_}')

Path('in', 'badwords.txt').write_text('\n'.join(sorted(badwords)))
