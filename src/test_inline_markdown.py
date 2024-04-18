import unittest
from inline_markdown import split_nodes_delimiter
from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_code(self):
        node = TextNode("Here is a `code` block", "text")
        new_nodes = split_nodes_delimiter([node], "`", "code")

        self.assertEqual(
            new_nodes,
            [
                TextNode("Here is a ", "text"),
                TextNode("code", "code"),
                TextNode(" block", "text"),
            ],
        )

    def test_multi(self):
        node = TextNode("Here is *bold* and **italic**", "text")

        # Must call in this order, since "*" also matches "**" and messes everything up
        italic_nodes = split_nodes_delimiter([node], "**", "italic")
        new_nodes = split_nodes_delimiter(italic_nodes, "*", "bold")

        self.assertEqual(
            new_nodes,
            [
                TextNode("Here is ", "text"),
                TextNode("bold", "bold"),
                TextNode(" and ", "text"),
                TextNode("italic", "italic"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
