# src/test_inline_extract.py

import unittest
from inline_extract import extract_markdown_images, extract_markdown_links


class TestInlineExtract(unittest.TestCase):
    # --- Images ---
    def test_extract_markdown_images_single(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")],
            matches,
        )

    def test_extract_markdown_images_multiple(self):
        text = (
            "Pics: ![rick roll](https://i.imgur.com/aKaOqIh.gif) and "
            "![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            matches,
        )

    def test_extract_markdown_images_empty_alt(self):
        text = "Logo: ![](https://example.com/logo.svg)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [("", "https://example.com/logo.svg")],
            matches,
        )

    def test_extract_markdown_images_none(self):
        self.assertListEqual([], extract_markdown_images("No images here"))
        self.assertListEqual([], extract_markdown_images(""))

    # --- Links ---
    def test_extract_markdown_links_single(self):
        text = "Link to [Boot.dev](https://www.boot.dev)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [("Boot.dev", "https://www.boot.dev")],
            matches,
        )

    def test_extract_markdown_links_multiple(self):
        text = (
            "Links: [to boot dev](https://www.boot.dev) and "
            "[to youtube](https://www.youtube.com/@bootdotdev)"
        )
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    def test_extract_markdown_links_ignores_images(self):
        text = "![img](https://x/y.png) and [anchor](https://x/z)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [("anchor", "https://x/z")],
            matches,
        )

    def test_extract_markdown_links_none(self):
        self.assertListEqual([], extract_markdown_links("No links here"))
        self.assertListEqual([], extract_markdown_links("![img](http://x/y.png)"))


if __name__ == "__main__":
    unittest.main()
