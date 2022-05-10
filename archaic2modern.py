from pathlib import Path
from uuid import uuid4

import yaml
import re


def get_unique_id():
    return uuid4().hex

def to_yaml(dict_):
    return yaml.safe_dump(dict_, sort_keys=False, allow_unicode=True)

def clean_word(word):
    if word == "ཞེས་པ།":
        return word
    unwanteds = ['ཞེས་པ་', 'དང༌', 'ཞེས་པ']
    for unwanted in unwanteds:
        word = word.replace(unwanted, '')
    return word


def parse_modern_word(word):
    alt_words = word.split('འམ་')
    for walker, alt_word in enumerate(alt_words):
        if '།' not in alt_word:
            alt_words[walker] = alt_word + '།'
    return alt_words



def parse_archaic2modern(words):
    archaic2modern = {}
    cur_word = {}
    for word_walker, word in enumerate(words,1):
        # word = clean_word(word)
        if word_walker%2==0:
            cur_word['modern'] = parse_modern_word(word)
            archaic2modern[get_unique_id()] = cur_word
            cur_word = {}
        else:
            cur_word['archaic'] = word
    
    return archaic2modern


if __name__ == "__main__":
    archaicmodern = Path('./archaic2modern').read_text(encoding='utf-8')
    words = archaicmodern.splitlines()
    arch_modern = parse_archaic2modern(words)
    arch_modern_yaml = to_yaml(arch_modern)
    Path('./arch_modern.yml').write_text(arch_modern_yaml, encoding='utf-8')

