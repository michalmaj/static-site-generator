# src/inline_extract.py

import re
from typing import List, Tuple


# --- Wzorce regex ---
# Obrazy: ![alt](url)
_IMG_PATTERN = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
# Linki: [text](url) — z wykluczeniem obrazów (! przed nawiasem kwadratowym)
_LINK_PATTERN = re.compile(r'(?<!!)\[(.*?)\]\((.*?)\)')


def extract_markdown_images(text: str) -> List[Tuple[str, str]]:
    """
    Zwraca listę (alt, url) dla wszystkich obrazów w Markdownie:
        ![alt](url)

    Przykład:
        "A ![cat](http://x/cat.png)" -> [("cat", "http://x/cat.png")]
    """
    if not text:
        return []
    return _IMG_PATTERN.findall(text)


def extract_markdown_links(text: str) -> List[Tuple[str, str]]:
    """
    Zwraca listę (anchor, url) dla wszystkich linków w Markdownie:
        [text](url)

    Obrazy (![...](...)) są automatycznie pomijane dzięki negative lookbehind (?<!!).

    Przykład:
        "Visit [site](http://x)" -> [("site", "http://x")]
    """
    if not text:
        return []
    return _LINK_PATTERN.findall(text)
