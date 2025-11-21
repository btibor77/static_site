from textnode import TextNode, TextType
class HTMLNode:
    def __init__(self,tag=None, value=None, children=None, props=None ):
        self.tag=tag
        self.value=value
        self.children=children
        self.props=props
    def to_html(self):
        raise NotImplementedError


    def props_to_html(self):
        prop_list=[]
        if self.props:
            for key, value in  self.props.items():
                prop_list.append(f' {key}="{value}"')
            return ("".join(prop_list))
        return ""
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super(LeafNode, self).__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value==None:
            raise ValueError
        if self.tag==None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super(ParentNode, self).__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag==None:
            raise ValueError
        if not self.children:
            raise ValueError("No children value")
        child_list=[]
        for child in self.children:
            child_list.append(child.to_html())
        return (f'<{self.tag}{"".join(child_list)}</{self.tag}>')

def text_node_to_html_node(text_node):
    if not isinstance(text_node,TextNode):
        raise TypeError
    if text_node.text_type==TextType.TEXT:
        new_node=LeafNode(tag=None, value=text_node.text, props=None)
        return new_node
    elif text_node.text_type==TextType.BOLD:
        new_node=LeafNode(tag="b", value=text_node.text, props=None)
        return new_node
    elif text_node.text_type==TextType.ITALIC:
        new_node=LeafNode(tag="i", value=text_node.text, props=None)
        return new_node
    elif text_node.text_type == TextType.CODE:
        new_node = LeafNode(tag="code", value=text_node.text, props=None)
        return new_node
    elif text_node.text_type==TextType.LINK:
        new_node=LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        return new_node
    elif text_node.text_type==TextType.IMAGE:
        new_node=LeafNode(tag="img", value="", props={"src": text_node.url,"alt": text_node.text})
        return new_node
    else:
        raise ValueError(f"Unsupported TextType: {text_node.text_type}")