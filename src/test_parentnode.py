import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_empty(self):
        node = ParentNode()
        self.assertRaises(ValueError, node.to_html)

    def test_no_children(self):
        node = ParentNode("p")
        self.assertRaises(ValueError, node.to_html)

    def test_render_children(self):
        node = ParentNode(
            "div",
            [
                LeafNode("a", "link", {"href": "www.boot.dev"}),
                LeafNode("p", "hello world", None),
                LeafNode(None, "hai :3", None),
            ],
        )

        self.assertEqual(
            node.to_html(),
            '<div><a href="www.boot.dev">link</a><p>hello world</p>hai :3</div>',
        )

    def test_render_props(self):
        node = ParentNode(
            "div",
            [
                LeafNode("a", "link", {"href": "www.boot.dev"}),
                LeafNode("p", "hello world", None),
                LeafNode(None, "hai :3", None),
            ],
            {"class": "exploding"},
        )

        self.assertEqual(
            node.to_html(),
            '<div class="exploding"><a href="www.boot.dev">link</a><p>hello world</p>hai :3</div>',
        )

    def test_nested(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "p", [LeafNode(None, "This text is "), LeafNode("b", "bold")]
                ),
                LeafNode("a", "link", {"href": "www.boot.dev"}),
                LeafNode("p", "hello world", None),
                LeafNode(None, "hai :3", None),
            ],
        )

        self.assertEqual(
            node.to_html(),
            '<div><p>This text is <b>bold</b></p><a href="www.boot.dev">link</a><p>hello world</p>hai :3</div>',
        )


if __name__ == "__main__":
    unittest.main()
