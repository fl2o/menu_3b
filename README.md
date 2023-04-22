# Description

Parsing a menu from instagram highlight weekly video:
- Download the clip using [instagrapi](https://pypi.org/project/instagrapi/). They are not stored in the repo
- Perform OCR using [easyOCR](https://pypi.org/project/easyocr/). Output is stored in data/extracted_text
- Parse the text to human readable format using [OpenAI](https://pypi.org/project/openai/) GPT3.5-turbo
- Store the output in [MENU.md](https://github.com/fl2o/menu_3b/blob/main/MENU.md)

TODOS:
- [ ] email the output
- [ ] automate with github action

# Installation

Fill .envrc and load it using direnv

Install dependencies from requirements.txt (tested with Python 3.9.16).
For instance
```
pyenv install 3.9.16
pyenv local 3.9.16
mkvirtualenv -a . -p $(which python) menu3b
pip install -r requirements.txt
```

# Usage

Run `python parse_menus.py` 🎊

Look at [MENU.md](https://github.com/fl2o/menu_3b/blob/main/MENU.md)
