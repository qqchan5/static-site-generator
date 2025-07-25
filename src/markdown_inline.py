from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    if re.match(r"^#{1,6} .*", block):
        return BlockType.HEADING
    lines = block.splitlines()
    if len(lines) > 2 and lines[0] == "```" and lines[-1] == "```":
        return BlockType.CODE
    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    if all(lines[i].startswith(f"{i+1}. ") for i in range(len(lines))):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    blocks = []
    for b in markdown.split("\n\n"):
        if b == "":
            continue
        blocks.append(b.strip())
    return blocks
