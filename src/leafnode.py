# src/leafnode.py
from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        """
        LeafNode nie ma children.
        Wymagamy podania argumentów 'tag' i 'value' (tag może być None => surowy tekst).
        """
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")

        # Brak tagu => zwracamy surowy tekst
        if self.tag is None:
            return str(self.value)

        # Z tagiem => pełny element HTML + atrybuty
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

