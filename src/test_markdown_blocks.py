from markdown_blocks import *
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

class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
#     def test_paragraphs(self):
#         md = """
# This is **bolded** paragraph
# text in a p
# tag here
#
# This is another paragraph with _italic_ text and `code` here
#
# """
#
#         node = markdown_to_html_node(md)
#         html = node.to_html()
#         self.assertEqual(
#             html,
#             "<div><p>This is <b>bolded</b> paragraph\ntext in a p\ntag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
#         )
#
#     def test_codeblock(self):
#         md = """
# ```
# This is text that _should_ remain
# the **same** even with inline stuff
# ```
# """
#
#         node = markdown_to_html_node(md)
#         html = node.to_html()
#         self.assertEqual(
#             html,
#             "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
#         )
#
#     def test_heading(self):
#         md ="""
# # This is a heading
# """
#
#         node = markdown_to_html_node(md)
#         html = node.to_html()
#         self.assertEqual(
#             html,
#             "<div><h1>This is a heading</h1></div>",
#         )
#
#     def test_heading2(self):
#         md ="""
# ## This is a heading
# """
#
#         node = markdown_to_html_node(md)
#         html = node.to_html()
#         self.assertEqual(
#             html,
#             "<div><h2>This is a heading</h2></div>",
#         )
#
#     def test_quote(self):
#         md = """
# >This is a quote
# >This is the second line of the quote
# """
#
#         node = markdown_to_html_node(md)
#         html = node.to_html()
#         self.assertEqual(
#             html,
#             "<div><blockquote>This is a quote\nThis is the second line of the quote</blockquote></div>",
#         )
#
#     def test_unordered_list(self):
#         md = """
# - This is an unordered list
# - This is the second item on the list
# """
#
#         node = markdown_to_html_node(md)
#         html = node.to_html()
#         self.assertEqual(
#             html,
#             "<div><ul><li>This is an unordered list</li><li>This is the second item on the list</li></ul></div>",
#         )
#
#     def test_ordered_list(self):
#         md = """
# 1. This is an ordered list
# 2. This is the second item on the list
# """
#
#         node = markdown_to_html_node(md)
#         html = node.to_html()
#         self.assertEqual(
#             html,
#             "<div><ol><li>This is an ordered list</li><li>This is the second item on the list</li></ol></div>",
#         )

if __name__ == "__main__":
    unittest.main()
