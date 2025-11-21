import unittest
from split_node import *

def test_extract_markdown_images(self):
    matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
    self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

def test_extract_multiple_images(self):
    text = "Hi ![one](https://a.com/1.png) and ![two](https://b.com/2.jpg)"
    matches = extract_markdown_images(text)
    self.assertListEqual(
        [("one", "https://a.com/1.png"), ("two", "https://b.com/2.jpg")],
        matches,
    )

def test_extract_images_none(self):
    text = "Nothing to see here, only text and [a link](https://x.com)"
    matches = extract_markdown_images(text)
    self.assertListEqual([], matches)