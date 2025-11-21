# python
from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise SyntaxError("That's invalid Markdown syntax")

        for i, part in enumerate(parts):
            if i % 2 == 0:
                result.append(TextNode(part, TextType.TEXT))
            else:
                result.append(TextNode(part, text_type))

    return result

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes=[]
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        remaining=node.text
        while True:
            matches = extract_markdown_images(remaining)
            if not matches:
                break
            alt, url = matches[0]
            token = f"![{alt}]({url})"
            before, after = remaining.split(token, 1)
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            remaining = after
        if remaining:
            new_nodes.append(TextNode(remaining, TextType.TEXT))
    return new_nodes
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        remaining = node.text
        while True:
            matches = extract_markdown_links(remaining)
            if not matches:
                break
            label, url = matches[0]
            token = f"[{label}]({url})"
            before, after = remaining.split(token, 1)
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(label, TextType.LINK, url))
            remaining = after
        if remaining:
            new_nodes.append(TextNode(remaining, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    New_Node=TextNode(text, TextType.TEXT, None)
    Node_List=[]
    Node_List.append(New_Node)
    bold_list=split_nodes_delimiter(Node_List, "**", text_type=TextType.BOLD)
    italic_list=split_nodes_delimiter(bold_list, "_", text_type=TextType.ITALIC)
    code_list=split_nodes_delimiter(italic_list, "`", text_type=TextType.CODE)
    image_list=split_nodes_image(code_list)
    link_list=split_nodes_link(image_list)
    return link_list








