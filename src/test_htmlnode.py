import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode()
        try:
            node.to_html()
        except Exception as e:
            self.assertEqual(type(e), NotImplementedError)

    def test_props_to_htlm(self):
        d = {
            "href": "a-link.com",
            "target": "blank"
        }
        node = HTMLNode(props=d)
        self.assertEqual(' href="a-link.com" target="blank"', node.props_to_html())

    def test_props_to_htlm2(self):
        node = HTMLNode()
        self.assertEqual(None, node.props_to_html())

    def test_repr(self):
        node = HTMLNode(tag="p", value="This is a paragraph", props={"href": "a-link.com"})
        self.assertEqual("HTMLNode(p, This is a paragraph, None, {'href': 'a-link.com'})", repr(node))

if __name__ == "__main__":
    unittest.mail()
