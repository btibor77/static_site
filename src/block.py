from enum import Enum, auto
import re

class BlockType(Enum):
    PARAGRAPH = auto()
    HEADING = auto()
    CODE = auto()
    QUOTE = auto()
    UNORDERED_LIST = auto()
    ORDERED_LIST = auto()


def block_to_block_type(block: str) -> BlockType:
    """
    Určí typ markdown bloku podľa zadaných pravidiel.
    Predpokladá sa, že block už nemá leading/trailing whitespace.
    """

    # 1. CODE: musí začínať a končiť s ``` (trojitý backtick)
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    lines = block.split("\n")

    # 2. HEADING: 1-6 # na začiatku, potom medzera a text
    # len prvý riadok sa berie ako heading
    heading_match = re.match(r"^(#{1,6})\s+.+$", lines[0])
    if heading_match:
        return BlockType.HEADING

    # 3. QUOTE: každý riadok musí začínať znakom '>'
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # 4. UNORDERED_LIST: každý riadok musí začínať "- " (pomlčka + medzera)
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # 5. ORDERED_LIST:
    # každý riadok musí začínať číslom, potom '.' a medzera
    # čísla musia začínať od 1 a po jednom sa zvyšovať
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

    # 6. Inak je to obyčajný paragraf
    return BlockType.PARAGRAPH
