from enum import Enum, auto
from split_node import text_to_textnodes
from textnode import TextNode, TextType
from htmlnode import text_node_to_html_node
import re



# ==========================
# HTML / TEXT NODE ŠTRUKTÚRY
# ==========================

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag          # napr. "p", "h1", "ul", "li", "code"...
        self.value = value      # text, ak ide o textový/leaf node
        self.children = children or []  # zoznam HTMLNode
        self.props = props or {}        # dict: { "href": "...", ... }

    def props_to_html(self) -> str:
        if not self.props:
            return ""
        return "".join(f' {k}="{v}"' for k, v in self.props.items())

    def to_html(self) -> str:
        # Čisto textový node (bez tagu)
        if self.tag is None:
            return self.value or ""

        # Node s tagom
        props_str = self.props_to_html()
        if self.children:
            children_html = "".join(child.to_html() for child in self.children)
            return f"<{self.tag}{props_str}>{children_html}</{self.tag}>"
        else:
            # Napr. <img>, ale tu pre jednoduchosť budeme robiť <tag>value</tag>
            inner = self.value or ""
            return f"<{self.tag}{props_str}>{inner}</{self.tag}>"


# class TextType(Enum):
#     TEXT = auto()
#     BOLD = auto()
#     ITALIC = auto()
#     CODE = auto()
#     LINK = auto()
#     IMAGE = auto()
#
#
# class TextNode:
#     def __init__(self, text: str, text_type: TextType, url: str | None = None):
#         self.text = text
#         self.text_type = text_type
#         self.url = url


# def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
#     """
#     Konverzia TextNode -> HTMLNode (leaf).
#     Pre jednoduchosť implementujeme všetky typy,
#     ale v markdown_to_html_node využijeme hlavne TEXT a CODE.
#     """
#     if text_node.text_type == TextType.TEXT:
#         return HTMLNode(tag=None, value=text_node.text)
#
#     if text_node.text_type == TextType.BOLD:
#         return HTMLNode(tag="b", children=[HTMLNode(tag=None, value=text_node.text)])
#
#     if text_node.text_type == TextType.ITALIC:
#         return HTMLNode(tag="i", children=[HTMLNode(tag=None, value=text_node.text)])
#
#     if text_node.text_type == TextType.CODE:
#         return HTMLNode(tag="code", children=[HTMLNode(tag=None, value=text_node.text)])
#
#     if text_node.text_type == TextType.LINK:
#         return HTMLNode(
#             tag="a",
#             children=[HTMLNode(tag=None, value=text_node.text)],
#             props={"href": text_node.url or "#"},
#         )
#
#     if text_node.text_type == TextType.IMAGE:
#         # Pre jednoduchosť bude image <img alt="..." src="..."></img>
#         return HTMLNode(
#             tag="img",
#             value="",
#             props={"src": text_node.url or "", "alt": text_node.text},
#         )
#
#     # fallback
#     return HTMLNode(tag=None, value=text_node.text)


def text_to_children(text: str) -> list[HTMLNode]:
    """
    Text -> TextNodes (s bold/italic/link/code/image) -> HTMLNodes.
    """
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(tn) for tn in text_nodes]


# ==========================
# MARKDOWN BLOCK PARSING
# ==========================

class BlockType(Enum):
    PARAGRAPH = auto()
    HEADING = auto()
    CODE = auto()
    QUOTE = auto()
    UNORDERED_LIST = auto()
    ORDERED_LIST = auto()


def split_blocks(markdown: str) -> list[str]:
    """
    Rozdelí celý markdown dokument na bloky oddelené prázdnym riadkom.
    Leading/trailing whitespace každého bloku sa oseká.
    """
    raw_blocks = markdown.split("\n\n")
    return [block.strip() for block in raw_blocks if block.strip()]


def block_to_block_type(block: str) -> BlockType:
    """
    Určí typ markdown bloku podľa pravidiel z predošlého zadania.
    """
    # CODE block: začína aj končí na ```
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    lines = block.split("\n")

    # HEADING: prvý riadok má 1-6 # + medzera + text
    if re.match(r"^(#{1,6})\s+.+$", lines[0]):
        return BlockType.HEADING

    # QUOTE: každý riadok začína '>'
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # UNORDERED_LIST: každý riadok začína "- "
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # ORDERED_LIST: každý riadok začína "n. " a n ide 1,2,3,...
    ordered = True
    for index, line in enumerate(lines, start=1):
        m = re.match(r"^(\d+)\. ", line)
        if not m:
            ordered = False
            break
        number = int(m.group(1))
        if number != index:
            ordered = False
            break

    if ordered:
        return BlockType.ORDERED_LIST

    # Inak paragraf
    return BlockType.PARAGRAPH


# ==========================
# MARKDOWN -> HTML STROM
# ==========================

def _heading_block_to_html_node(block: str) -> HTMLNode:
    first_line = block.split("\n", 1)[0]
    m = re.match(r"^(#{1,6})\s+(.+)$", first_line)
    if not m:
        # fallback – ak by niečo zlyhalo, spravíme paragraf
        return HTMLNode(tag="p", children=text_to_children(block))

    level = len(m.group(1))
    text = m.group(2).strip()
    tag = f"h{level}"
    return HTMLNode(tag=tag, children=text_to_children(text))


def _paragraph_block_to_html_node(block: str) -> HTMLNode:
    # V paragrafu nechávame newlines => nahradíme ich medzerou
    text = " ".join(block.split("\n"))
    return HTMLNode(tag="p", children=text_to_children(text))


def _quote_block_to_html_node(block: str) -> HTMLNode:
    lines = block.split("\n")
    cleaned = [line.lstrip(">").lstrip() for line in lines]
    text = " ".join(cleaned)
    # p_node = HTMLNode(tag="p", children=text_to_children(text))
    return HTMLNode(tag="blockquote", children=text_to_children(text))


def _unordered_list_block_to_html_node(block: str) -> HTMLNode:
    lines = block.split("\n")
    li_nodes = []
    for line in lines:
        item_text = line[2:]  # odstránime "- "
        li_nodes.append(HTMLNode(tag="li", children=text_to_children(item_text)))
    return HTMLNode(tag="ul", children=li_nodes)


def _ordered_list_block_to_html_node(block: str) -> HTMLNode:
    lines = block.split("\n")
    li_nodes = []
    for line in lines:
        # odstránime "1. ", "2. " atď.
        m = re.match(r"^\d+\. (.+)$", line)
        item_text = m.group(1) if m else line
        li_nodes.append(HTMLNode(tag="li", children=text_to_children(item_text)))
    return HTMLNode(tag="ol", children=li_nodes)


def _code_block_to_html_node(block: str) -> HTMLNode:
    """
    CODE block: špeciálny prípad – nerobíme inline parsing.
    Odstránime obalové ``` a zvyšok vložíme ako TextNode typu CODE.
    """
    inner = block[3:-3]  # odstráni prvé a posledné ```
    # odstráni jeden leading a trailing newline, ak sú:
    inner = inner.lstrip("\n").rstrip("\n")

    text_node = TextNode(inner, TextType.CODE)
    code_child = text_node_to_html_node(text_node)  # <code>...</code>
    # obalíme do <pre>
    return HTMLNode(tag="pre", children=[code_child])


def block_to_html_node(block: str) -> HTMLNode:
    btype = block_to_block_type(block)

    if btype == BlockType.HEADING:
        return _heading_block_to_html_node(block)

    if btype == BlockType.PARAGRAPH:
        return _paragraph_block_to_html_node(block)

    if btype == BlockType.QUOTE:
        return _quote_block_to_html_node(block)

    if btype == BlockType.UNORDERED_LIST:
        return _unordered_list_block_to_html_node(block)

    if btype == BlockType.ORDERED_LIST:
        return _ordered_list_block_to_html_node(block)

    if btype == BlockType.CODE:
        return _code_block_to_html_node(block)

    # fallback – ak by sa objavil neznámy typ
    return _paragraph_block_to_html_node(block)


def markdown_to_html_node(markdown: str) -> HTMLNode:
    """
    Konvertuje celý markdown dokument do jedného rodičovského HTMLNode.
    Rodič je <div> a všetky bloky sú jeho children.
    """
    blocks = split_blocks(markdown)
    children = [block_to_html_node(block) for block in blocks]
    return HTMLNode(tag="div", children=children)

