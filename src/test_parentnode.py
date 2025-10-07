# src/test_parentnode.py
import unittest
from leafnode import LeafNode
from parentnode import ParentNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_raises_without_tag(self):
        child = LeafNode("span", "x")
        with self.assertRaises(ValueError):
            ParentNode(None, [child]).to_html()

    def test_raises_with_children_none(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()

    def test_raises_with_children_empty_list(self):
        with self.assertRaises(ValueError):
            ParentNode("div", []).to_html()

    def test_props_rendered_on_parent(self):
        child = LeafNode("span", "x")
        node = ParentNode("div", [child], {"class": "box", "data-id": "1"})
        self.assertEqual(
            node.to_html(),
            '<div class="box" data-id="1"><span>x</span></div>'
        )

if __name__ == "__main__":
    unittest.main()

