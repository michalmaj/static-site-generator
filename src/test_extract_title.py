# src/test_extract_title.py
import unittest
from page import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_trims_spaces(self):
        self.assertEqual(extract_title("   #   Tolkien Fan Club   "), "Tolkien Fan Club")

    def test_ignores_h2(self):
        md = "## Not a title\n# Real Title\nSome text"
        self.assertEqual(extract_title(md), "Real Title")

    def test_raises_when_missing(self):
        with self.assertRaises(ValueError):
            extract_title("No title here\n## H2 only\nParagraph")


if __name__ == "__main__":
    unittest.main()
