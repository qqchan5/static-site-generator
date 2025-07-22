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
    def test_node(self):
        with self.assertRaises(TypeError):
            node = LeafNode()
        with self.assertRaises(TypeError):
            node = LeafNode(None)
        with self.assertRaises(TypeError):
            node = LeafNode(value=None)
        with self.assertRaises(ValueError):
            node = LeafNode(None, None)

    def test_to_html(self):
        node = LeafNode("p", "Hello, world!")
        node.value = None
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_raw(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_b(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")

    def test_to_html_a(self):
        node = LeafNode("a", "Click", {"href": "http://youtube.com"})
        self.assertEqual(node.to_html(), '<a href="http://youtube.com">Click</a>')

    def test_repr(self):
        node = LeafNode("p", "This is a paragraph", {"href": "a-link.com"})
        self.assertEqual("LeafNode(p, This is a paragraph, {'href': 'a-link.com'})", repr(node))

class TestParentNode(unittest.TestCase):
    def test_node(self):
        with self.assertRaises(TypeError):
            node = ParentNode()
        with self.assertRaises(TypeError):
            node = ParentNode(None)
        with self.assertRaises(TypeError):
            node = ParentNode(children=None)
        with self.assertRaises(ValueError):
            node = ParentNode(None, None)
        with self.assertRaises(ValueError):
            node = ParentNode("a", None)
        with self.assertRaises(ValueError):
            node = ParentNode(None, "a")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_grandchildren2(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        grandchild_node2 = LeafNode("i", "grandchild2")
        child_node2 = ParentNode("span", [grandchild_node2])
        parent_node = ParentNode("div", [child_node, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span><span><i>grandchild2</i></span></div>",
        )

    def test_repr(self):
        child_node = LeafNode("span", "child")
        node = ParentNode("p", [child_node], {"href": "a-link.com"})
        self.assertEqual("ParentNode(p, [LeafNode(span, child, None)], {'href': 'a-link.com'})", repr(node))

if __name__ == "__main__":
    unittest.main()
