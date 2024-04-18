import unittest

from leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("a", "link", {"href": "www.boot.dev"})
        node2 = LeafNode("p", "hello world", None)
        node3 = LeafNode(None, "hai :3", None)
        node4 = LeafNode()

        self.assertEqual(node.to_html(), '<a href="www.boot.dev">link</a>')
        self.assertEqual(node2.to_html(), "<p>hello world</p>")
        self.assertEqual(node3.to_html(), "hai :3")
        self.assertRaises(ValueError, node4.to_html)


if __name__ == "__main__":
    unittest.main()
