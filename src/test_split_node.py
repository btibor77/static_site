# python
import unittest
from split_node import split_nodes_delimiter
from textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_no_delim(self):
        old_nodes = [TextNode("hello world", TextType.TEXT)]
        got = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        want = [TextNode("hello world", TextType.TEXT)]
        self.assertEqual(got, want)
