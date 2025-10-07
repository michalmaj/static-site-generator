# src/htmlnode.py

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        """Child klasy nadpiszą to przy realnym renderowaniu."""
        raise NotImplementedError

    def props_to_html(self):
        """Zwraca atrybuty HTML jako łańcuch z poprzedzającą spacją."""
        if not self.props:
            return ""
        return " " + " ".join(f'{k}="{v}"' for k, v in self.props.items())

    def __repr__(self):
        return (
            f"HTMLNode(tag={self.tag}, value={self.value}, "
            f"children={self.children}, props={self.props})"
        )

