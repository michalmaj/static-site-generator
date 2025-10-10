# src/markdown_to_html.py
from typing import List
import re
from blocks import markdown_to_blocks, block_to_block_type, BlockType
from textnode import TextNode, TextType, text_node_to_html_node
from text_to_textnodes import text_to_textnodes
from leafnode import LeafNode
from parentnode import ParentNode


def _text_to_children(text: str) -> List[LeafNode]:
    tnodes = text_to_textnodes(text)
    return [text_node_to_html_node(tn) for tn in tnodes]


def _make_paragraph(block: str) -> ParentNode:
    # Łączymy linie w jeden ciąg, zamieniając \n na spacje
    compact = " ".join(block.splitlines())
    return ParentNode("p", _text_to_children(compact))


def _make_heading(block: str) -> ParentNode:
    i = 0
    while i < len(block) and block[i] == "#":
        i += 1
    text = block[i:].lstrip()
    return ParentNode(f"h{i}", _text_to_children(text))


_FENCE_RE = re.compile(r"^\s*```")


def _make_code(block: str) -> ParentNode:
    """
    Blok kodu otoczony ``` ... ```
    Zachowuje dokładne nowe linie wewnątrz, ignoruje inline markdown.
    """
    lines = block.splitlines(keepends=True)
    if not lines or not _FENCE_RE.match(lines[0]):
        return _make_paragraph(block)

    lines = lines[1:]
    if lines and _FENCE_RE.match(lines[-1].rstrip("\n")):
        lines = lines[:-1]

    inner = "".join(lines)
    code_leaf = LeafNode("code", inner)
    return ParentNode("pre", [code_leaf])


def _strip_quote_prefix(block: str) -> str:
    lines = []
    for line in block.split("\n"):
        if line.startswith(">"):
            line = line[1:]
            if line.startswith(" "):
                line = line[1:]
        lines.append(line)
    return "\n".join(lines)


def _make_blockquote(block: str) -> ParentNode:
    return ParentNode("blockquote", _text_to_children(_strip_quote_prefix(block)))


def _make_ul(block: str) -> ParentNode:
    items = []
    for line in block.split("\n"):
        if not line.strip():
            continue
        items.append(ParentNode("li", _text_to_children(line[2:])))
    return ParentNode("ul", items)


def _make_ol(block: str) -> ParentNode:
    items = []
    for idx, line in enumerate(block.split("\n"), start=1):
        prefix = f"{idx}. "
        items.append(ParentNode("li", _text_to_children(line[len(prefix):])))
    return ParentNode("ol", items)


def _block_to_htmlnode(block: str) -> ParentNode:
    btype = block_to_block_type(block)
    if btype == BlockType.HEADING:
        return _make_heading(block)
    if btype == BlockType.CODE:
        return _make_code(block)
    if btype == BlockType.QUOTE:
        return _make_blockquote(block)
    if btype == BlockType.UNORDERED_LIST:
        return _make_ul(block)
    if btype == BlockType.ORDERED_LIST:
        return _make_ol(block)
    return _make_paragraph(block)


def markdown_to_html_node(markdown: str) -> ParentNode:
    """
    Główna funkcja konwertująca markdown na drzewo HTML.
    """
    blocks = markdown_to_blocks(markdown or "")
    children = [_block_to_htmlnode(b) for b in blocks]
    return ParentNode("div", children)
