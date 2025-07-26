from textnode import TextType, TextNode
import re

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

def split_nodes_image2(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        matches = extract_markdown_images(node.text)
        string = node.text
        for alt, url in matches:
            split_string = string.split(f"![{alt}]({url})")
            if split_string[0] != "":
                new_nodes.append(TextNode(split_string[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            string = split_string[1]
        if split_string[1] != "":
            new_nodes.append(TextNode(split_string[1], TextType.TEXT))
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

def split_nodes_link2(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        matches = extract_markdown_links(node.text)
        string = node.text
        for alt, url in matches:
            split_string = string.split(f"![{alt}]({url})")
            if split_string[0] != "":
                new_nodes.append(TextNode(split_string[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.LINK, url))
            string = split_string[1]
        if split_string[1] != "":
            new_nodes.append(TextNode(split_string[1], TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    text_nodes = [TextNode(text, TextType.TEXT)]
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    text_nodes = split_nodes_delimiter(text_nodes, '**', TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, '_', TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, '`', TextType.CODE)
    return text_nodes
