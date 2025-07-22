import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_htlm(self):
        d = {
            "href": "a-link.com",
            "target": "blank"
        }
        node = HTMLNode(props=d)
        self.assertEqual(' href="a-link.com" target="blank"', node.props_to_html())

    def test_props_to_htlm2(self):
        node = HTMLNode()
        self.assertEqual("", node.props_to_html())

    def test_repr(self):
        node = HTMLNode(tag="p", value="This is a paragraph", props={"href": "a-link.com"})
        self.assertEqual("HTMLNode(p, This is a paragraph, None, {'href': 'a-link.com'})", repr(node))

class TestLeafNode(unittest.TestCase):
    def test_leaf_node(self):
        with self.assertRaises(TypeError):
            node = LeafNode()
        with self.assertRaises(TypeError):
            node = LeafNode(None)
        with self.assertRaises(TypeError):
            node = LeafNode(value=None)
        with self.assertRaises(ValueError):
            node = LeafNode(None, None)

    def test_leaf_to_html(self):
        node = LeafNode("p", "Hello, world!")
        node.value = None
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_raw(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click", {"href": "http://youtube.com"})
        self.assertEqual(node.to_html(), '<a href="http://youtube.com">Click</a>')

    def test_repr(self):
        node = LeafNode("p", "This is a paragraph", {"href": "a-link.com"})
        self.assertEqual("LeafNode(p, This is a paragraph, {'href': 'a-link.com'})", repr(node))

if __name__ == "__main__":
    unittest.mail()
