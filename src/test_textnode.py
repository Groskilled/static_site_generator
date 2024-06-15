import unittest
from textnode import  (
        TEXT_TYPES,
        TextNode,
        text_node_to_html_node,
        split_nodes_delimiter,
        split_nodes_image,
        split_nodes_link,
        text_to_textnodes
        )


class TestTextNode(unittest.TestCase):
    
    def setUp(self):
        self.node = TextNode("This is a text node", "bold")
        self.node2 = TextNode("This is a text node", "bold")
        self.node3 = TextNode("This is a text node", "bold", None)
        self.node4 = TextNode("This is another text node", "bold")
        self.node5 = TextNode("This is a text node", "bald")

    def test_eq(self):
        self.assertEqual(self.node, self.node2)
        self.assertEqual(self.node, self.node3)

    def test_not_eq(self):
        self.assertNotEqual(self.node, self.node4)
        self.assertNotEqual(self.node, self.node5)


class TestTextNodeToHTMLNode(unittest.TestCase):

    def setUp(self):
        #self.text = TextNode("this is a text node", "text")
        #self.bold = TextNode("this is a bold node", "bold")
        #self.italic = TextNode("this is a italic node", "italic")
        #self.code = TextNode("this is a code node", "code")
        #self.link = TextNode("this is a link node", "link")
        #self.image = TextNode("this is an image node", "image")
        self.invalid = TextNode("this is a just node", "just")

    def test_text_node_to_html_node_raises_exception(self):
        with self.assertRaises(Exception):
            text_node_to_html_node(self.invalid)


class TestSplitNodeDelimiter(unittest.TestCase):

    def setUp(self):
        self.node = TextNode("This is text with a `code block` word", TEXT_TYPES.text_type_text.value)
        self.invalid = TextNode("This is text with a *block* word*", TEXT_TYPES.text_type_text.value)

    def test_split_nodes_delimiter(self):
        new_nodes = split_nodes_delimiter([self.node], "`", TEXT_TYPES.text_type_code.value)
        expected = [
                TextNode("This is text with a ", TEXT_TYPES.text_type_text.value),
                TextNode("code block", TEXT_TYPES.text_type_code.value),
                TextNode(" word", TEXT_TYPES.text_type_text.value),
            ]
        self.assertEqual(new_nodes, expected)


    def test_split_nodes_delimiter_raises_exception(self):
        with self.assertRaises(Exception) as e:
            split_nodes_delimiter([self.invalid], "*", "bold")

        self.assertEqual(str(e.exception), "Invalid string: This is text with a *block* word* missing a closing delimiter.")


class TestSplitNodesImage(unittest.TestCase):

    def setUp(self):
        self.node = TextNode(
                "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
                "text",
                )
        self.expected = [
                TextNode("This is text with an ", "text"),
                TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                TextNode(" and another ", "text"),
                TextNode(
                    "second image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
                    ),
                ]

    def test_split_nodes_image(self):
        new_nodes = split_nodes_image([self.node])
        self.assertEqual(new_nodes, self.expected)



class TestSplitNodesLink(unittest.TestCase):

    def setUp(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        self.node = TextNode(text, "text")
        self.expected = [
                TextNode("This is text with a ", "text", None),
                TextNode("link", "link", "https://www.example.com"),
                TextNode(" and ", "text", None),
                TextNode(
                    "another", "link", "https://www.example.com/another",
                    ),
                ]

    def test_split_nodes_image(self):
        new_nodes = split_nodes_link([self.node])
        self.assertEqual(new_nodes, self.expected)


class TestTextToTextNode(unittest.TestCase):

    def setUp(self):
        self.text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        self.expected =[
                TextNode("This is ", "text"),
                TextNode("text", "bold"),
                TextNode(" with an ", "text"),
                TextNode("italic", "italic"),
                TextNode(" word and a ", "text"),
                TextNode("code block", "code"),
                TextNode(" and an ", "text"),
                TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                TextNode(" and a ", "text"),
                TextNode("link", "link", "https://boot.dev"),
                ] 

    def test_text_to_textnodes(self):
        new_nodes = text_to_textnodes(self.text)
        self.assertEqual(new_nodes, self.expected)




if __name__ == "__main__":
    unittest.main()
