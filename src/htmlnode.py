
class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ""
        return " " + " ".join([f"{key}=\"{value}\"" for key, value in self.props.items()])

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    
    def __init__(self, tag=None, value=None, children=None, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)
        self.children = None

    def to_html(self):
        if not self.value:
            raise ValueError
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.children = children
        self.tag = tag
        self.props = props

    def to_html(self):
        if not self.tag:
            raise ValueError
        if not self.children:
            raise ValueError("children are required")
        res = ""
        for child in self.children:
            res += child.to_html()
        return f"<{self.tag}>{res}</{self.tag}>"

