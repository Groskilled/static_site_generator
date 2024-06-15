import re
from enum import Enum
from htmlnode import LeafNode, ParentNode


class TEXT_TYPES(Enum):
    text_type_text = "text"
    text_type_bold = "bold"
    text_type_italic = "italic"
    text_type_code = "code"
    text_type_link = "link"
    text_type_image = "image"


class DELIMITERS(Enum):
    text_type_bold = "**"
    text_type_italic = "*"
    text_type_code = "`"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, node):
        return self.text == node.text and self.text_type == node.text_type and self.url == node.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TEXT_TYPES.text_type_text.value:
            return LeafNode(tag=None, value=text_node.text)
        case TEXT_TYPES.text_type_bold.value:
            return LeafNode(tag='b', value=text_node.text)
        case TEXT_TYPES.text_type_italic.value:
            #"i" tag, text
            return LeafNode(tag='i', value=text_node.text)
        case TEXT_TYPES.text_type_code.value:
            #"code" tag, text
            return LeafNode(tag='code', value=text_node.text)
        case TEXT_TYPES.text_type_link.value:
            #"a" tag, anchor text, and "href" prop
            props = {"href": text_node.url}
            return LeafNode(tag='a', value=text_node.text, children=None, props=props)
        case TEXT_TYPES.text_type_image.value:
            #"img" tag, empty string value, "src" and "alt" props ("src" is the image URL, "alt" is the alt text)
            props = {"src": text_node.url, "alt": text_node.text}
            return LeafNode(tag='img', value="", children=None, props=props)
        case _:
            raise Exception("Invalid node type")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if delimiter not in [e.value for e in DELIMITERS]:
        return old_nodes
    res = []
    for node in old_nodes:
        if node.text_type != TEXT_TYPES.text_type_text.value:
            res.append(node)
            continue
        if node.text.count(delimiter) % 2:
            raise Exception(f"Invalid string: {node.text} missing a closing delimiter.")
        splitted_text = node.text.split(delimiter)
        flag = False
        if node.text[0] == delimiter: # text starts with the delimiter
            flag = True
        for text in splitted_text:
            if not text:
                continue
            if flag:
                res.append(TextNode(text, text_type))
            else:
                res.append(TextNode(text, TEXT_TYPES.text_type_text.value))
            flag = not flag
    return res


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes):
    res = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if node.text_type != TEXT_TYPES.text_type_text.value or not images:
            res.append(node)
            continue
        text = node.text
        for image_tup in images:
            splitted = text.split(f"![{image_tup[0]}]({image_tup[1]})", 1)
            res.append(TextNode(splitted[0], TEXT_TYPES.text_type_text.value))
            res.append(TextNode(image_tup[0], TEXT_TYPES.text_type_image.value, image_tup[1]))
            text = splitted[1]
        if text:
            res.append(TextNode(text, TEXT_TYPES.text_type_text.value))
    return res


def split_nodes_link(old_nodes):
    res = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if node.text_type != TEXT_TYPES.text_type_text.value or not links:
            res.append(node)
            continue
        text = node.text
        for link_tup in links:
            splitted = text.split(f"[{link_tup[0]}]({link_tup[1]})", 1)
            res.append(TextNode(splitted[0], TEXT_TYPES.text_type_text.value))
            res.append(TextNode(link_tup[0], TEXT_TYPES.text_type_link.value, link_tup[1]))
            text = splitted[1]
    return res


def text_to_textnodes(text):
    nodes = [TextNode(text, TEXT_TYPES.text_type_text.value)]
    nodes = split_nodes_delimiter(nodes, DELIMITERS.text_type_bold.value, TEXT_TYPES.text_type_bold.value)
    nodes = split_nodes_delimiter(nodes, DELIMITERS.text_type_italic.value, TEXT_TYPES.text_type_italic.value)
    nodes = split_nodes_delimiter(nodes, DELIMITERS.text_type_code.value, TEXT_TYPES.text_type_code.value)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
nodes = text_to_textnodes(text)
for node in nodes:
    print(node)
