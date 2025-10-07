# src/test_htmlnode.py
import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        node = HTMLNode(tag="a", value="Boot.dev", props=None)
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_multiple(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode(tag="a", value="Google", props=props)
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"'
        )

    def test_to_html_not_implemented(self):
        node = HTMLNode(tag="p", value="Hello")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr_contains_fields(self):
        node = HTMLNode(tag="a", value="Link", props={"href": "https://example.com"})
        s = repr(node)
        self.assertIn("HTMLNode(", s)
        self.assertIn("tag=a", s)
        self.assertIn("value=Link", s)
        self.assertIn("props={'href': 'https://example.com'}", s)


if __name__ == "__main__":
    unittest.main()

