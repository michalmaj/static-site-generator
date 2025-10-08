# src/split_nodes.py

from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Dzieli węzły typu TEXT po podanym delimiterze i wstawia węzły o wskazanym text_type
    dla fragmentów "wewnątrz" delimiterów.

    Przykład:
        Input:  [TextNode("A **bold** B", TEXT)]
        Call:   split_nodes_delimiter([...], "**", TextType.BOLD)
        Output: [TextNode("A ", TEXT), TextNode("bold", BOLD), TextNode(" B", TEXT)]

    Zasady:
      - Tylko węzły TEXT są dzielone; inne przechodzą bez zmian.
      - Liczba delimiterów musi być parzysta (len(parts) nieparzyste). W przeciwnym razie ValueError.
      - Puste segmenty tekstowe są pomijane (nie tworzymy pustych TextNode(TEXT, "")).

    Parametry:
      old_nodes : list[TextNode]
      delimiter : str (np. "`", "**", "_")
      text_type : TextType (np. TextType.CODE, TextType.BOLD, TextType.ITALIC)

    Zwraca:
      list[TextNode]
    """
    if not isinstance(old_nodes, list):
        raise TypeError("old_nodes must be a list of TextNode")

    new_nodes = []
    for node in old_nodes:
        # Przechodzimy bez zmian wszystko, co nie jest czystym tekstem
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # Dzielimy po delimiterze dosłownym (bez regexów)
        parts = node.text.split(delimiter)

        # Jeżeli delimiter nie występuje — nic nie zmieniamy
        if len(parts) == 1:
            new_nodes.append(node)
            continue

        # Liczba delimiterów musi być parzysta => liczba parts nieparzysta
        # Np.: "A **b** C" -> split("**") => ["A ", "b", " C"] (3 części)
        if len(parts) % 2 == 0:
            raise ValueError(f"Unmatched delimiter '{delimiter}' in text: {node.text!r}")

        # parts: [TEXT, IN, TEXT, IN, TEXT, ...] (naprzemiennie)
        # i = 0 -> TEXT, i = 1 -> IN (typ text_type), i = 2 -> TEXT, itd.
        for i, chunk in enumerate(parts):
            if chunk == "":
                # pomijamy puste segmenty — nie tworzymy pustych TextNode(TEXT, "")
                # (np. gdy tekst zaczyna/kończy się delimiterem)
                continue

            if i % 2 == 0:
                # Parzyste indeksy -> zwykły tekst
                new_nodes.append(TextNode(chunk, TextType.TEXT))
            else:
                # Nieparzyste -> fragment wewnątrz delimiterów
                new_nodes.append(TextNode(chunk, text_type))

    return new_nodes


import re
from textnode import TextNode, TextType

# Wzorce:
#  - obrazy:  ![alt](url)
#  - linki:   [text](url) z wykluczeniem obrazów (! przed '[')
_IMG_RE  = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
_LINK_RE = re.compile(r'(?<!!)\[([^\]]*)\]\(([^)]+)\)')


def split_nodes_image(old_nodes):
    """
    Rozbija węzły TEXT po wszystkich obrazach Markdownu: ![alt](url)
    Z węzłów nie-tekstowych nic nie zdejmuje.
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        last = 0
        any_match = False

        for m in _IMG_RE.finditer(text):
            any_match = True
            start, end = m.span()
            alt = m.group(1)
            url = m.group(2)

            # Tekst przed obrazem (jeśli jest)
            if start > last:
                before = text[last:start]
                if before:
                    new_nodes.append(TextNode(before, TextType.TEXT))

            # Sam obraz jako TextNode typu IMAGE
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))

            last = end

        # Ogon po ostatnim dopasowaniu lub cały tekst, jeśli brak dopasowań
        tail = text[last:]
        if tail or not any_match:
            # jeśli nie było dopasowań, zachowujemy oryginalny TEXT
            if not any_match:
                new_nodes.append(node)
            else:
                if tail:
                    new_nodes.append(TextNode(tail, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    """
    Rozbija węzły TEXT po wszystkich linkach Markdownu: [text](url)
    (obrazy są ignorowane dzięki (?<!!)).
    Z węzłów nie-tekstowych nic nie zdejmuje.
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        last = 0
        any_match = False

        for m in _LINK_RE.finditer(text):
            any_match = True
            start, end = m.span()
            anchor = m.group(1)
            url = m.group(2)

            # Tekst przed linkiem (jeśli jest)
            if start > last:
                before = text[last:start]
                if before:
                    new_nodes.append(TextNode(before, TextType.TEXT))

            # Sam link jako TextNode typu LINK
            new_nodes.append(TextNode(anchor, TextType.LINK, url))

            last = end

        # Ogon po ostatnim dopasowaniu lub cały tekst, jeśli brak dopasowań
        tail = text[last:]
        if tail or not any_match:
            if not any_match:
                new_nodes.append(node)
            else:
                if tail:
                    new_nodes.append(TextNode(tail, TextType.TEXT))

    return new_nodes
