import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):

    def setUp(self):
        self.children = [HTMLNode("children1"), HTMLNode("children2")]
        self.props = {"href": "https://www.google.com", "target": "_blank"}
        self.node = HTMLNode("p", "hello", self.children, self.props)

    def test_init(self):
        self.assertEqual(self.node.tag, "p")
        self.assertEqual(self.node.value, "hello")
        self.assertEqual(self.node.children, self.children)
        self.assertEqual(self.node.props, self.props)

    def test_props_to_html(self):
        self.assertEqual(self.node.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\"")
        self.assertEqual(HTMLNode(props={"a": 1, "b": 2}).props_to_html(), " a=\"1\" b=\"2\"")


class TestLeafNode(unittest.TestCase):

    def setUp(self):
        self.props1 = {"a": "aa", "b": "bb"}
        self.node1 = LeafNode(tag="p", value="hello", props=self.props1)
        self.props2 = {"a": "aa"}
        self.no_value_node = LeafNode(tag="p", value=None, props=self.props2)

    def test_init(self):
        self.assertEqual(self.node1.tag, "p")
        self.assertEqual(self.node1.value, "hello")
        self.assertEqual(self.node1.children, None)
        self.assertEqual(self.node1.props, self.props1)

    def test_props_to_html(self):
        self.assertEqual(self.node1.props_to_html(), " a=\"aa\" b=\"bb\"")

    def test_to_html(self):
        self.assertEqual(self.node1.to_html(), "<p a=\"aa\" b=\"bb\">hello</p>")

    def test_to_html_raises_error(self):
        with self.assertRaises(ValueError):
            self.no_value_node.to_html()


class TestParentNode(unittest.TestCase):

    def setUp(self):
        self.children = [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
                ]
        self.node = ParentNode("p", "", self.children)

    #def test_init(self):

    #def test_props_to_html(self):
    #    self.assertEqual(self.node1.props_to_html(), " a=\"aa\" b=\"bb\"")

    def test_to_html(self):
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(self.node.to_html(), expected)

    #def test_to_html_raises_error(self):
    #    with self.assertRaises(ValueError):
    #        self.no_value_node.to_html()




if __name__ == "__main__":
    unittest.main()
