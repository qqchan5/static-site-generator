from markdown_inline import *
import unittest

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
            blocks,
        )

    def test_markdown_to_blocks_extra_newline(self):
        md = """
This is **bolded** paragraph


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
            blocks,
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type_h(self):
        block_type = block_to_block_type(markdown_to_blocks("# This is a heading")[0])
        self.assertEqual(BlockType.HEADING, block_type)

    def test_block_to_block_type_c(self):
        block_type = block_to_block_type(markdown_to_blocks("""
```
This is a code block
This is the same code block
```
"""
            )[0]
        )
        self.assertEqual(BlockType.CODE, block_type)

    def test_block_to_block_type_q(self):
        block_type = block_to_block_type(markdown_to_blocks("""
>This is a quote
>This is the second line of the quote
"""
            )[0]
        )
        self.assertEqual(BlockType.QUOTE, block_type)

    def test_block_to_block_type_u(self):
        block_type = block_to_block_type(markdown_to_blocks("""
- This is an unordered list
- This is the second item on the list
"""
            )[0]
        )
        self.assertEqual(BlockType.UNORDERED_LIST, block_type)

    def test_block_to_block_type_o(self):
        block_type = block_to_block_type(markdown_to_blocks("""
1. This is an ordered list
2. This is the second item on the list
"""
            )[0]
        )
        self.assertEqual(BlockType.ORDERED_LIST, block_type)

if __name__ == "__main__":
    unittest.main()
