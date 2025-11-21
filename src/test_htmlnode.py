import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        # Create an HTMLNode with some props
        node = HTMLNode("a", "click me", None, {"href": "https://www.google.com", "target": "_blank"})
        # Check if props_to_html returns the expected string
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_props_to_html_with_no_props(self):
        node = HTMLNode("p", "some text", None, None)
        # What should props_to_html() return when there are no props?
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_single_prop(self):
        node = HTMLNode("p", "some text", None, {"href": "https://boot.dev"})
        # What should props_to_html() return when there are no props?
        self.assertEqual(node.props_to_html(), ' href="https://boot.dev"')

if __name__ == "__main__":
    unittest.main()