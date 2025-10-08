# src/test_block_types.py

import unittest
from blocks import BlockType, block_to_block_type


class TestBlockTypes(unittest.TestCase):
    def test_heading_levels(self):
        self.assertEqual(block_to_block_type("# Title"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### H6"), BlockType.HEADING)

    def test_heading_requires_space(self):
        # Bez spacji po '#': to nie heading wg wymagań -> paragraf
        self.assertEqual(block_to_block_type("##Title"), BlockType.PARAGRAPH)

    def test_code_block(self):
        block = "```\nline1\nline2\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote_block(self):
        block = "> a\n> b\n> c"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list(self):
        block = "- item one\n- item two\n- item three"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_requires_space(self):
        # Brak spacji po '-' -> to nie UL
        block = "-item one\n-item two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        block = "1. first\n2. second\n3. third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_must_increment(self):
        self.assertEqual(block_to_block_type("1. a\n3. b"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("2. a\n3. b"), BlockType.PARAGRAPH)

    def test_paragraph_fallback(self):
        block = "Some text with **bold** and _italic_."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_mixed_block_falls_back_to_paragraph(self):
        block = "- item\nnot a list line"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
