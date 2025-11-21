import unittest
from markdown_blocks import *
from mrkdwn_to_html import *




class TestMarkdownToHtmlNode(unittest.TestCase):

    def test_single_paragraph(self):
        md = "This is a simple paragraph."
        root = markdown_to_html_node(md)

        self.assertEqual(root.tag, "div")
        self.assertEqual(len(root.children), 1)
        p = root.children[0]
        self.assertEqual(p.tag, "p")
        self.assertEqual(p.to_html(), "<p>This is a simple paragraph.</p>")
        self.assertEqual(
            root.to_html(),
            "<div><p>This is a simple paragraph.</p></div>"
        )

    def test_heading_paragraph_list(self):
        md = "# Heading\n\nThis is a paragraph.\n\n- item one\n- item two"
        root = markdown_to_html_node(md)

        self.assertEqual(len(root.children), 3)

        h = root.children[0]
        p = root.children[1]
        ul = root.children[2]

        self.assertEqual(h.tag, "h1")
        self.assertEqual(h.to_html(), "<h1>Heading</h1>")

        self.assertEqual(p.tag, "p")
        self.assertEqual(p.to_html(), "<p>This is a paragraph.</p>")

        self.assertEqual(ul.tag, "ul")
        self.assertEqual(len(ul.children), 2)
        self.assertEqual(
            ul.to_html(),
            "<ul><li>item one</li><li>item two</li></ul>"
        )

        self.assertEqual(
            root.to_html(),
            "<div><h1>Heading</h1><p>This is a paragraph.</p><ul><li>item one</li><li>item two</li></ul></div>"
        )

    def test_ordered_list(self):
        md = "1. first\n2. second\n3. third"
        root = markdown_to_html_node(md)

        self.assertEqual(len(root.children), 1)
        ol = root.children[0]
        self.assertEqual(ol.tag, "ol")
        self.assertEqual(len(ol.children), 3)
        self.assertEqual(
            ol.to_html(),
            "<ol><li>first</li><li>second</li><li>third</li></ol>"
        )

    def test_quote_block(self):
        md = "> line one\n> line two"
        root = markdown_to_html_node(md)

        self.assertEqual(len(root.children), 1)
        bq = root.children[0]
        self.assertEqual(bq.tag, "blockquote")
        self.assertEqual(
            bq.to_html(),
            "<blockquote>line one line two</blockquote>"
        )

    def test_code_block(self):
        md = "```\nprint('hello')\nprint('world')\n```"
        root = markdown_to_html_node(md)

        self.assertEqual(len(root.children), 1)
        pre = root.children[0]
        self.assertEqual(pre.tag, "pre")
        self.assertEqual(len(pre.children), 1)

        code = pre.children[0]
        self.assertEqual(code.tag, "code")
        self.assertIn("print('hello')", code.to_html())
        self.assertIn("print('world')", code.to_html())

        # pre + code dokopy
        self.assertEqual(
            pre.to_html(),
            "<pre><code>print('hello')\nprint('world')</code></pre>"
        )

    def test_multiple_blocks_mixed(self):
        md = """# Title

This is a paragraph with some text.

1. first
2. second

> quote line
> another line
"""
        root = markdown_to_html_node(md)
        self.assertEqual(len(root.children), 4)
        self.assertEqual(root.children[0].tag, "h1")
        self.assertEqual(root.children[1].tag, "p")
        self.assertEqual(root.children[2].tag, "ol")
        self.assertEqual(root.children[3].tag, "blockquote")
