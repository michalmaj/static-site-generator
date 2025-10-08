# src/test_split_nodes_delimiter.py

import unittest
from textnode import TextNode, TextType
from split_nodes import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_no_delimiter_passthrough(self):
        nodes = [TextNode("No markup here", TextType.TEXT)]
        out = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(out, nodes)

    def test_simple_bold(self):
        nodes = [TextNode("This is **bold** text", TextType.TEXT)]
        out = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(
            out,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_simple_italic(self):
        nodes = [TextNode("A _word_ here", TextType.TEXT)]
        out = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(
            out,
            [
                TextNode("A ", TextType.TEXT),
                TextNode("word", TextType.ITALIC),
                TextNode(" here", TextType.TEXT),
            ],
        )

    def test_simple_code(self):
        nodes = [TextNode("Use `print()` please", TextType.TEXT)]
        out = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(
            out,
            [
                TextNode("Use ", TextType.TEXT),
                TextNode("print()", TextType.CODE),
                TextNode(" please", TextType.TEXT),
            ],
        )

    def test_multiple_bold_segments(self):
        nodes = [TextNode("A **B** C **D** E", TextType.TEXT)]
        out = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(
            out,
            [
                TextNode("A ", TextType.TEXT),
                TextNode("B", TextType.BOLD),
                TextNode(" C ", TextType.TEXT),
                TextNode("D", TextType.BOLD),
                TextNode(" E", TextType.TEXT),
            ],
        )

    def test_leading_delimiter(self):
        nodes = [TextNode("**Lead** text", TextType.TEXT)]
        out = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(
            out,
            [
                TextNode("Lead", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_trailing_delimiter(self):
        nodes = [TextNode("End **tag**", TextType.TEXT)]
        out = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(
            out,
            [
                TextNode("End ", TextType.TEXT),
                TextNode("tag", TextType.BOLD),
            ],
        )

    def test_unmatched_raises(self):
        nodes = [TextNode("Broken **bold here", TextType.TEXT)]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes, "**", TextType.BOLD)


    def test_non_text_nodes_pass_through(self):
        nodes = [
            TextNode("plain **x**", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
        ]
        out = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(
            out,
            [
                TextNode("plain ", TextType.TEXT),
                TextNode("x", TextType.BOLD),
                TextNode("already bold", TextType.BOLD),
            ],
        )
