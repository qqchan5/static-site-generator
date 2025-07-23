from htmlnode import LeafNode
from enum import Enum
import re

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception(f"invalid text type: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        sections = node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise Exception("invalid markdown: unbalanced delimiters")
        block = True
        for s in sections:
            block = not block
            if s == "":
                continue
            new_nodes.append(TextNode(s, text_type if block else TextType.TEXT))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        sections = re.split(r"!\[(.*?)]\((.*?)\)", node.text)
        # if len(sections) % 2 == 0:
        #     raise Exception("invalid markdown: unbalanced delimiters")
        sec_counter = 0
        for s in sections:
            sec_counter += 1
            match sec_counter:
                case 1:
                    if s == "":
                        continue
                    new_nodes.append(TextNode(s, TextType.TEXT))
                case 2:
                    alt = s
                case 3:
                    # if s == "":
                    #     raise
                    new_nodes.append(TextNode(alt, TextType.IMAGE, s))
                    sec_counter = 0
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        sections = re.split(r"(?<!!)\[(.*?)]\((.*?)\)", node.text)
        # if len(sections) % 2 == 0:
        #     raise Exception("invalid markdown: unbalanced delimiters")
        sec_counter = 0
        for s in sections:
            sec_counter += 1
            match sec_counter:
                case 1:
                    if s == "":
                        continue
                    new_nodes.append(TextNode(s, TextType.TEXT))
                case 2:
                    alt = s
                case 3:
                    # if s == "":
                    #     raise
                    new_nodes.append(TextNode(alt, TextType.LINK, s))
                    sec_counter = 0
    return new_nodes
