# src/test_text_to_textnodes.py

import unittest
from textnode import TextNode, TextType
from text_to_textnodes import text_to_textnodes


class TestTextToTextNodes(unittest.TestCase):
    def test_example_all_features(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` and an "
            "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        )
        out = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            out,
        )

    def test_plain_text(self):
        text = "Just plain text."
        out = text_to_textnodes(text)
        self.assertListEqual([TextNode("Just plain text.", TextType.TEXT)], out)

    def test_only_images_and_links(self):
        text = "![a](http://x/a.png)[b](http://x/b)"
        out = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("a", TextType.IMAGE, "http://x/a.png"),
                TextNode("b", TextType.LINK, "http://x/b"),
            ],
            out,
        )

    def test_code_inside_plain(self):
        text = "Use `print()` please"
        out = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("Use ", TextType.TEXT),
                TextNode("print()", TextType.CODE),
                TextNode(" please", TextType.TEXT),
            ],
            out,
        )

    def test_multiple_bold_and_italic(self):
        text = "A **B** C **D** and _E_ end"
        out = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("A ", TextType.TEXT),
                TextNode("B", TextType.BOLD),
                TextNode(" C ", TextType.TEXT),
                TextNode("D", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("E", TextType.ITALIC),
                TextNode(" end", TextType.TEXT),
            ],
            out,
        )

    def test_empty_string(self):
        self.assertListEqual([], text_to_textnodes(""))

    def test_does_not_split_non_text_nodes_again(self):
        # sprawdzamy, że raz wydzielone linki/obrazy nie są naruszane późniejszymi splitami
        text = "See [**bold-ish**](http://x) and ![img_with_**](http://y.png)"
        out = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("See ", TextType.TEXT),
                TextNode("**bold-ish**", TextType.LINK, "http://x"),
                TextNode(" and ", TextType.TEXT),
                TextNode("img_with_**", TextType.IMAGE, "http://y.png"),
            ],
            out,
        )


if __name__ == "__main__":
    unittest.main()
