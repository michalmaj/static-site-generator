from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


from leafnode import LeafNode


def text_node_to_html_node(text_node):
    """
    Konwertuje obiekt TextNode na LeafNode zgodnie z jego typem TextType.

    Zwraca:
        LeafNode:
            - TEXT   -> tag=None, value=text
            - BOLD   -> tag="b", value=text
            - ITALIC -> tag="i", value=text
            - CODE   -> tag="code", value=text
            - LINK   -> tag="a", value=text, props={"href": url}
            - IMAGE  -> tag="img", value="", props={"src": url, "alt": text}

    Rzuca:
        ValueError, jeśli przekazany obiekt ma nieobsługiwany typ lub brakuje URL-a dla LINK/IMAGE.
    """

    if text_node is None:
        raise ValueError("text_node cannot be None")

    ttype = text_node.text_type
    text = text_node.text
    url = text_node.url

    if ttype == TextType.TEXT:
        return LeafNode(None, text)

    elif ttype == TextType.BOLD:
        return LeafNode("b", text)

    elif ttype == TextType.ITALIC:
        return LeafNode("i", text)

    elif ttype == TextType.CODE:
        return LeafNode("code", text)

    elif ttype == TextType.LINK:
        if not url:
            raise ValueError("LINK type requires a non-empty URL")
        return LeafNode("a", text, {"href": url})

    elif ttype == TextType.IMAGE:
        if not url:
            raise ValueError("IMAGE type requires a non-empty URL")
        return LeafNode("img", "", {"src": url, "alt": text})

    else:
        raise ValueError(f"Unsupported TextType: {ttype}")

