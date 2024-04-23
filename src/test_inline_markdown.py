import unittest
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
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
        node = TextNode("Here is **bold** and *italic*", "text")

        # Must call in this order, since "*" also matches "**" and messes everything up
        italic_nodes = split_nodes_delimiter([node], "**", "bold")
        new_nodes = split_nodes_delimiter(italic_nodes, "*", "italic")

        self.assertEqual(
            new_nodes,
            [
                TextNode("Here is ", "text"),
                TextNode("bold", "bold"),
                TextNode(" and ", "text"),
                TextNode("italic", "italic"),
            ],
        )

    def test_extract(self):
        self.assertEqual(
            [("image", "www.google.com")],
            extract_markdown_images("![image](www.google.com)"),
        )

        self.assertEqual(
            [("link", "www.boot.dev")],
            extract_markdown_links("[link](www.boot.dev)"),
        )

    def test_image_split(self):
        node = TextNode("Here is an ![image](www.google.com) block", "text")
        new_nodes = split_nodes_image([node])

        self.assertEqual(
            new_nodes,
            [
                TextNode("Here is an ", "text"),
                TextNode("image", "image", "www.google.com"),
                TextNode(" block", "text"),
            ],
        )

    def test_node_split(self):
        node = TextNode("Here is a [link](www.boot.dev) block", "text")
        new_nodes = split_nodes_link([node])

        self.assertEqual(
            new_nodes,
            [
                TextNode("Here is a ", "text"),
                TextNode("link", "link", "www.boot.dev"),
                TextNode(" block", "text"),
            ],
        )

    def test_text_to_textnode(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"

        self.assertEqual(
            text_to_textnodes(text),
            [
                TextNode("This is ", "text"),
                TextNode("text", "bold"),
                TextNode(" with an ", "text"),
                TextNode("italic", "italic"),
                TextNode(" word and a ", "text"),
                TextNode("code block", "code"),
                TextNode(" and an ", "text"),
                TextNode(
                    "image",
                    "image",
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                ),
                TextNode(" and a ", "text"),
                TextNode("link", "link", "https://boot.dev"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
