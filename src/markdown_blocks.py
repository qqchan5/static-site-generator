from textnode import text_to_textnodes, text_node_to_html_node, TextType, TextNode
from htmlnode import ParentNode, LeafNode
from markdown_inline import *
import re

def text_nodes_to_html_nodes(text_nodes):
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                children.append(ParentNode("p", text_nodes_to_html_nodes(text_to_textnodes(re.sub("\n", " ", block)))))
            case BlockType.HEADING:
                i = 1
                while block[i] == '#':
                    i += 1
                children.append(ParentNode(f"h{i}", text_nodes_to_html_nodes(text_to_textnodes(re.sub(r"^#+ ", "", block)))))
            case BlockType.CODE:
                children.append(ParentNode("pre", [LeafNode("code", re.sub(r"(^```\n|```$)", "", block))]))
            case BlockType.QUOTE:
                children.append(ParentNode("blockquote", text_nodes_to_html_nodes(text_to_textnodes(re.sub("\n", " ", re.sub(r"^>\s+", "", block, flags=re.MULTILINE))))))
            case BlockType.UNORDERED_LIST:
                lines = block.splitlines()
                grand_children = []
                for line in lines:
                    grand_children.append(ParentNode("li", text_nodes_to_html_nodes(text_to_textnodes(re.sub(r"^- ", "", line)))))
                children.append(ParentNode("ul", grand_children))
            case BlockType.ORDERED_LIST:
                lines = block.splitlines()
                grand_children = []
                for line in lines:
                    grand_children.append(ParentNode("li", text_nodes_to_html_nodes(text_to_textnodes(re.sub(rf"^\d+\. ", "", line)))))
                children.append(ParentNode("ol", grand_children))
    return ParentNode("div", children)
