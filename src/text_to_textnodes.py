# src/text_to_textnodes.py

from textnode import TextNode, TextType
from split_nodes import (
    split_nodes_image,
    split_nodes_link,
    split_nodes_delimiter,
)


def text_to_textnodes(text: str) -> list[TextNode]:
    """
    Konwertuje surowy markdownowy tekst do listy TextNode'ów:
    - najpierw obrazy,
    - potem linki,
    - następnie code (`),
    - potem bold (**),
    - na końcu italic (_).
    Taka kolejność zapobiega konfliktom między wzorcami.

    Zwraca pustą listę dla pustego wejścia.
    """
    if not text:
        return []

    nodes: list[TextNode] = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    return nodes
