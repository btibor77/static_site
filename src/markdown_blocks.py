from textnode import TextNode, TextType
import re

def markdown_to_blocks(markdown):
    blocks=(markdown.split("\n\n"))
    final_block=[]
    for block in blocks:
        strp_block=block.strip()
        if strp_block !="":
            final_block.append(strp_block)
    return final_block