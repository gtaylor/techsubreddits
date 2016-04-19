"""
This file contains our sub-reddit definitions.
"""

CATEGORY_PROGRAMMING_LANG = "programming-language"

CATALOG = {}


def add_programming_languages():
    langs = (
        'python', 'ruby', 'golang', 'java', 'cplusplus', 'csharp',
        'C_Programming', 'cpp', 'haskell', 'php', 'scala', 'javascript',
        'perl', 'swift',
    )
    for lang in langs:
        CATALOG[lang] = {'categories': [CATEGORY_PROGRAMMING_LANG]}


add_programming_languages()
