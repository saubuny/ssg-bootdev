import unittest

from htmlnode import HTMLNode


class TestTextNode(unittest.TestCase):
    def test_props(self):
        node = HTMLNode("b", "meow", None, None)
        self.assertEqual(node.props_to_html(), "")

        node2 = HTMLNode("b", "meow", None, {"class": "red blue"})
        self.assertEqual(node2.props_to_html(), ' class="red blue"')

        node3 = HTMLNode(
            "b", "meow", None, {"class": "red blue", "href": "www.boot.dev"}
        )
        self.assertEqual(node3.props_to_html(), ' class="red blue" href="www.boot.dev"')


if __name__ == "__main__":
    unittest.main()
