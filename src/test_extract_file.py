import pytest
from extract_title import extract_title


def test_extract_title_basic():
    assert extract_title("# Hello") == "Hello"


def test_extract_title_with_spaces():
    assert extract_title("   #   Title here   ") == "Title here"


def test_extract_title_inline_text():
    assert extract_title("#Hello") == "Hello"


def test_extract_title_multiline():
    md = """
Some intro text
# My Title
More text
"""
    assert extract_title(md) == "My Title"


def test_extract_title_first_h1():
    md = """
# First
## Subtitle
# Second
"""
    assert extract_title(md) == "First"


def test_extract_title_no_h1():
    md = "## No H1 here\nSome text"
    with pytest.raises(ValueError):
        extract_title(md)
