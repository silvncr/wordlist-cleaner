<!-- omit in toc -->
# wordlist-cleaner

Compiles and cleans a wordlist according to user-specified banned words. It uses relational data to encode multiple dictionaries, filtering out unwanted words and their variations.

This program is designed to be used with a licensed digital copy of a dictionary. It is not a dictionary itself.

Tested on Linux with Python 3.12.3.

> Todo:
>
> - [ ] Test on Windows/MacOS filesystems
> - [ ] Write code comments and docstrings
> - [ ] Implement settings via `/.env` file
> - [ ] Create and document utilities

---

<!-- omit in toc -->
## Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Wordlist format](#wordlist-format)
  - [Input data](#input-data)
    - [Base wordlist](#base-wordlist)
    - [Base dictionary](#base-dictionary)
    - [Using overrides](#using-overrides)
  - [Generating the wordlist](#generating-the-wordlist)
  - [Other utilities](#other-utilities)
- [License](#license)

---

## Installation

```bash
git clone https://github.com/silvncr/wordlist-cleaner.git
cd wordlist-cleaner
pip install -r requirements.txt
```

---

## Usage

To run this program, you must first provide input data. There are subfolders for input data, output data, and other purposes.

---

### Wordlist format

- A wordlist is a `.txt` file with one word per line.
- The list is sorted alphabetically.
- All words are capitalised.
- There can be a newline at the end.

> [!CAUTION]
> Neglecting these rules will result in untested behaviour.

---

### Input data

The input folder is `/in/`. The essential files are:

- `related.json`: a JSON file containing a list of words and their related words (synonyms, inflections, etc).
- `badwords.txt`: a text file containing a list of **badwords**. The program will filter out these words AND their related words.

**Badwords** are words that are not allowed in the list. The program filters out badwords AND related words.

> [!NOTE]
> `related.json` is generated from `/compile_related.py` and `/base_dictionaries/`. To generate it, you need to have a licensed digital copy of a dictionary. This is beyond the scope of this guide.

#### Base wordlist

> [!IMPORTANT]
> All files in `/base_wordlists/` will contribute to the base wordlist. Make sure they're formatted correctly.

#### Base dictionary

> [!NOTE]
> If you want to compile a reference dictionary yourself, please contact me directly. Discord: `@silvncr`.

#### Using overrides

Badwords can be overriden using **allowedwords** and **notallowedwords**. These checks are performed after the badword check, and are not affected by related words.

- `allowed.txt`: a wordlist containing **allowedwords**; always allowed, even if they are badwords, or are related to badwords.
- `notallowed.txt`: a wordlist containing **notallowedwords**; never allowed, even if they are not related to badwords.

These overrides allow for complex filtering. Here are some examples:

- Allow "badword" but not "badwording" or "badworder".

  > - `badwords.txt`: badword
  > - `allowed.txt`: badword

- Allow "badword" and its variations, except for "badwording".

  > - `notallowed.txt`: badwording

---

### Generating the wordlist

> [!CAUTION]
> Make sure you have the required files, in the correct format, in the correct locations. The program will not check for errors in your input data.
<!---->
> [!IMPORTANT]
> Make sure your working directory is set to `wordlist-cleaner`. Otherwise, you could end up overwriting your input files.
>
> You should also make a backup of `/in/`.

Once your input data is ready, you need to run the scripts in this order:

1. `/compile_badwords.py`: generate basic filter list.

  > - Reads: `/base_wordlists/`, `/in/badwords.txt`
  > - Writes: `/in/badwords.txt`

2. `/compile_related.py`: generate master wordlist and update filter list.

  > - Reads: `/base_dictionaries/`, `/in/badwords.txt`
  > - Writes: `/in/badwords.txt`, `/in/related.json`
  <!---->
<!--
> [!TIP]
> You can ignore Step 2 and use the precompiled `related.json`, however this will negatively affect your filter's effectiveness.
-->

3. `/compile_wordlist.py`: generate final wordlist.

  > - Reads: `/in/badwords.txt`, `/in/related.json`
  > - Writes: `/out/badwordlist.txt`, `/out/wordlist.txt`

You will find the generated wordlists in `/out/`:

- `wordlist.txt`
- `badwordlist.txt`

---

### Other utilities

WIP

---

## License

This project is licensed under the [BSD 3-Clause License](LICENSE).
