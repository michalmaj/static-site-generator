# src/test_markdown_to_blocks.py

import unittest
from blocks import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_trims_and_removes_empty(self):
        md = """


   First block with leading/trailing spaces    




Second block
"""
        self.assertEqual(
            markdown_to_blocks(md),
            ["First block with leading/trailing spaces", "Second block"],
        )

    def test_multiple_blank_lines(self):
        md = """A


B



C"""
        self.assertEqual(markdown_to_blocks(md), ["A", "B", "C"])

    def test_windows_line_endings(self):
        md = "Para1 line1\r\nPara1 line2\r\n\r\n- item1\r\n- item2\r\n\r\n# Head\r\n"
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "Para1 line1\nPara1 line2",
                "- item1\n- item2",
                "# Head",
            ],
        )

    def test_empty_input(self):
        self.assertEqual(markdown_to_blocks(""), [])


if __name__ == "__main__":
    unittest.main()
