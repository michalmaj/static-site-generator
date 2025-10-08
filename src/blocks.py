# src/blocks.py

import re
from enum import Enum
from typing import List


def markdown_to_blocks(markdown: str) -> List[str]:
    """
    Dzieli pełny dokument Markdown na bloki rozdzielone pustą linią.
    """
    if not markdown:
        return []
    text = markdown.replace("\r\n", "\n").replace("\r", "\n")
    raw_blocks = re.split(r"\n[ \t]*\n+", text)
    blocks: List[str] = []
    for blk in raw_blocks:
        b = blk.strip()
        if b:
            blocks.append(b)
    return blocks


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


_HEADING_RE = re.compile(r"^(#{1,6})\s+.+$")


def block_to_block_type(block: str) -> BlockType:
    """
    Określa typ bloku Markdown.

    Zasady:
      - heading: linia zaczyna się od 1..6 znaków '#' + spacja i tekst
      - code:    cały blok rozpoczyna się '```' i kończy się '```'
      - quote:   każda linia zaczyna się od '>' (z lub bez spacji po nim)
      - ul:      każda linia zaczyna się od '- ' (myślnik + spacja)
      - ol:      każda linia: 'N. ' z N rosnącym od 1 co 1
      - w innym wypadku: paragraph
    """
    # Heading
    if _HEADING_RE.match(block):
        return BlockType.HEADING

    # Code block
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    lines = block.split("\n")

    # Quote
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # Unordered list
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # Ordered list: 1. ..., 2. ..., sekwencyjnie
    def _is_ordered_lines(ls: List[str]) -> bool:
        for i, line in enumerate(ls, start=1):
            prefix = f"{i}. "
            if not line.startswith(prefix):
                return False
        return True

    if _is_ordered_lines(lines):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
