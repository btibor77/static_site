import re
import unittest
from block import *

class TestBlockToBlockType(unittest.TestCase):

    def test_paragraph_simple(self):
        block = "This is a simple paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_level_1(self):
        block = "# Heading level 1"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_level_6(self):
        block = "###### Heading level 6"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_invalid_no_space(self):
        block = "######Heading without space"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_invalid_too_many_hashes(self):
        block = "####### Too many hashes"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_block_single_line(self):
        block = "```print('hello')```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_multiline(self):
        block = "```\nprint('hello')\nprint('world')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote_single_line(self):
        block = "> This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_multiline(self):
        block = "> Line one\n> Line two\n> Line three"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_invalid_mixed(self):
        block = "> Line one\nNot a quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_single_line(self):
        block = "- item one"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_multiline(self):
        block = "- item one\n- item two\n- item three"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_invalid_missing_space(self):
        block = "-item one\n-item two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_simple(self):
        block = "1. first\n2. second\n3. third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_invalid_start_not_1(self):
        block = "2. second\n3. third"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_invalid_non_sequential(self):
        block = "1. first\n3. third"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_invalid_missing_dot(self):
        block = "1) first\n2) second"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_invalid_mixed(self):
        block = "1. first\n- second"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_takes_priority_over_other_patterns(self):
        # aj keby riadky vo vnútri vyzerali ako list, má to byť CODE
        block = "```\n- not a list\n1. not ordered list\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)