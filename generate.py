"""
Simple wordlist generator for monkeytype
"""
import random
import json
import sys
import pyperclip

def session_length(base_name):
    if base_name == "english_1k":
        return 1000, "words"
    elif base_name == "english":
        return 200, "words"
    else:
        return 4900, "chars"
        

def get_words_json(base_name):
    """gets full word list. pass in filename without .json"""
    with open(base_name + ".json", "r", encoding="utf8") as file:
        data = json.load(file)
        return data["words"]


def get_words_cache(name):
    """
    returns words from a wordcache
    """
    cache_name = name + "_cache.json"
    try:
        with open(cache_name, "r", encoding="utf8") as file:
            data = json.load(file)
            return data["words"]
    except IOError:
        return []


def split_words(base_name, words):
    """
    split words into first WORDS_PER_SESSION and then remainder
    """
    random.shuffle(words)
    amount, split_type = session_length(base_name)
    if split_type == "words":
        word_count = WORDS_PER_SESSION[base_name]
        return words[:word_count], words[word_count:]
    
    count = 0
    result = []
    remainder = words[:]
    while count < amount and len(remainder) > 0:
        result.append(remainder[0])
        count += len(result[-1]) + 1
        remainder = remainder[1:]
    return result, remainder

def write_words(base_name, words):
    """
    write words to cache file
    """
    data = {"words": words}
    cache_name = base_name + "_cache.json"
    with open(cache_name, "w", encoding="utf8") as file:
        json.dump(data, file, indent=2)


def get_words(base_name):
    """
    Return words from wordlist
    """
    words = get_words_cache(base_name)
    if len(words) == 0:
        words = get_words_json(base_name)

    result, remainder = split_words(base_name, words)
    write_words(base_name, remainder)
    return result


if __name__ == "__main__":
    word_list = get_words(sys.argv[1])
    print (len(word_list))
    clipboard = " ".join(word_list)
    print (len(clipboard))
    print(clipboard)
    pyperclip.copy(clipboard)
    
