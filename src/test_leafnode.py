import unittest
from htmlnode import *

def test_leaf_to_html_p(self):
    node = LeafNode("p", "Hello, world!")
    self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

def test_leaf_props(self):
    node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

def no_value_test(self):
    node = LeafNode(tag="p", value=None)
    self.assertRaises(ValueError, node.to_html) # Notice no parentheses after to_html

def test_no_tag(self):
    node = LeafNode(tag=None, value="Hello, world!")
    self.assertEqual(node.to_html(), "Hello, world!")


if __name__ == "__main__":
    unittest.main()