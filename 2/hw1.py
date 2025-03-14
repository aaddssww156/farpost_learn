"""
Given a file containing text. Complete using only default collections:
    1) Find 10 longest words consisting from largest amount of unique symbols
    2) Find rarest symbol for document
    3) Count every punctuation char
    4) Count every non ascii char
    5) Find most common non ascii char for document
"""

from typing import List
import string
from collections import Counter


def get_text(file_path: str) -> str:
    with open(file_path, encoding="utf-8") as file:
        return file.read()


def get_longest_diverse_words(file_path: str) -> List[str]:
    with open(file_path, encoding="utf-8") as file:
        words = set()
        for line in file:
            for word in line.split():
                cleaned_word = word.strip(string.punctuation)
                words.add(cleaned_word)

    words = sorted(words, key=lambda w: (-len(set(w)), -len(w)))
    return words[:10]


def get_rarest_char(file_path: str) -> str:
    text = get_text(file_path)
    char_counts = Counter(text)
    if not char_counts:
        return ""

    return min(char_counts, key=char_counts.get)


def count_punctuation_chars(file_path: str) -> int:
    text = get_text(file_path)
    return sum(1 for char in text if char in string.punctuation)


def count_non_ascii_chars(file_path: str) -> int:
    text = get_text(file_path)
    return sum(1 for char in text if ord(char) > 127)


def get_most_common_non_ascii_char(file_path: str) -> str:
    text = get_text(file_path)
    non_ascii_chars = [char for char in text if ord(char) > 127]

    if not non_ascii_chars:  # Если список пуст
        return ""

    char_counts = Counter(non_ascii_chars)
    return max(char_counts, key=char_counts.get)


if __name__ == "__main__":
    filename = "data.txt"
    print(get_longest_diverse_words(filename))
    print(get_rarest_char(filename))
    print(count_punctuation_chars(filename))
    print(count_non_ascii_chars(filename))
    print(get_most_common_non_ascii_char(filename))
