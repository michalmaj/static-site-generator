# src/blocks.py

import re
from typing import List


def markdown_to_blocks(markdown: str) -> List[str]:
    """
    Dzieli pełny dokument Markdown na bloki rozdzielone pustą linią.
    - Normalizuje końce linii do '\n'
    - Za separator uznaje >= 1 pustą linię (z ewentualnymi spacjami/tabami)
    - Każdy blok jest stripowany z białych znaków na brzegach
    - Bloki puste (po strip) są usuwane
    """
    if not markdown:
        return []

    # Normalizacja końców linii (Windows, stare Mac)
    text = markdown.replace("\r\n", "\n").replace("\r", "\n")

    # Rozdziel po co najmniej jednej pustej linii (może zawierać spacje/taby)
    # '\n[ \t]*\n' — pusta linia (ew. z białymi znakami)
    raw_blocks = re.split(r"\n[ \t]*\n+", text)

    blocks: List[str] = []
    for blk in raw_blocks:
        b = blk.strip()
        if b:
            blocks.append(b)
    return blocks
