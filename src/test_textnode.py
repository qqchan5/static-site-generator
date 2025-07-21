import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("This is a text node", TextType.IMAGE, "/static/image")
        node2 = TextNode("This is a text node", TextType.IMAGE, "/static/image")
        self.assertEqual(node, node2)

    def test_text_not_eq(self):
        node = TextNode("This is a text", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_type_not_eq(self):
        node = TextNode("This is a text", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url_not_eq(self):
        node = TextNode("This is a text", TextType.LINK, "/static/image")
        node2 = TextNode("This is a text", TextType.LINK, "/static/image2")
        self.assertNotEqual(node, node2)

    def test_url_not_eq2(self):
        node = TextNode("This is a text", TextType.LINK, "/static/image")
        node2 = TextNode("This is a text", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.LINK, "youtube.com")
        self.assertEqual("TextNode(This is a text node, link, youtube.com)", repr(node))

if __name__ == "__main__":
    unittest.main()
