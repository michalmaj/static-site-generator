# src/parentnode.py
from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        """
        ParentNode:
        - tag (wymagany)
        - children (wymagane, lista dzieci)
        - props (opcjonalne)
        - brak value (rodzic trzyma dzieci)
        """
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if self.children is None or len(self.children) == 0:
            raise ValueError("ParentNode must have children")

        inner_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{inner_html}</{self.tag}>"

