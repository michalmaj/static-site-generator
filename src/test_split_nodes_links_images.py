import unittest
from textnode import TextNode, TextType
from split_nodes import split_nodes_image, split_nodes_link


class TestSplitNodesImages(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_images_no_match_passthrough(self):
        node = TextNode("No images here", TextType.TEXT)
        self.assertListEqual([node], split_nodes_image([node]))

    def test_split_images_leading_and_trailing(self):
        node = TextNode(
            "![start](http://x/s.png) mid ![end](http://x/e.png)",
            TextType.TEXT,
        )
        out = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("start", TextType.IMAGE, "http://x/s.png"),
                TextNode(" mid ", TextType.TEXT),
                TextNode("end", TextType.IMAGE, "http://x/e.png"),
            ],
            out,
        )

    def test_split_images_preserves_non_text_nodes(self):
        nodes = [
            TextNode("A ![x](http://x/x.png) B", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
        ]
        out = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("A ", TextType.TEXT),
                TextNode("x", TextType.IMAGE, "http://x/x.png"),
                TextNode(" B", TextType.TEXT),
                TextNode("already bold", TextType.BOLD),
            ],
            out,
        )


class TestSplitNodesLinks(unittest.TestCase):
    def test_split_links_basic(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_split_links_ignores_images(self):
        node = TextNode(
            "![img](http://x/y.png) and [anchor](http://x/z)",
            TextType.TEXT,
        )
        out = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("![img](http://x/y.png) and ", TextType.TEXT),
                TextNode("anchor", TextType.LINK, "http://x/z"),
            ],
            out,
        )

    def test_split_links_no_match_passthrough(self):
        node = TextNode("No links here", TextType.TEXT)
        self.assertListEqual([node], split_nodes_link([node]))

    def test_split_links_leading_and_trailing(self):
        node = TextNode(
            "[lead](http://a) middle [trail](http://b)",
            TextType.TEXT,
        )
        out = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("lead", TextType.LINK, "http://a"),
                TextNode(" middle ", TextType.TEXT),
                TextNode("trail", TextType.LINK, "http://b"),
            ],
            out,
        )

    def test_split_links_preserves_non_text_nodes(self):
        nodes = [
            TextNode("A [x](http://x) B", TextType.TEXT),
            TextNode("already italic", TextType.ITALIC),
        ]
        out = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("A ", TextType.TEXT),
                TextNode("x", TextType.LINK, "http://x"),
                TextNode(" B", TextType.TEXT),
                TextNode("already italic", TextType.ITALIC),
            ],
            out,
        )


if __name__ == "__main__":
    unittest.main()
