from hashlib import new
from sitecustomize import new_prefix

from textnode import TextType, TextNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.extend(old_nodes)
            continue
        if node.text.count(delimiter) % 2 != 0:
            raise Exception("Invalid Markdown syntax, you need to close your blocks")
        split_string = old_nodes[0].text.split(delimiter)
        for i in range(len(split_string)):
            if split_string[i] == "":
                continue
            if i % 2 == 0:
                new_list.append(TextNode(split_string[i], TextType.TEXT))
            else:
                new_list.append(TextNode(split_string[i], text_type))
    return new_list

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue
        text = node.text
        extraction = extract_markdown_images(text)
        for e in extraction:
            image_alt = e[0]
            image_link = e[1]
            sections = text.split(f"![{image_alt}]({image_link})", 1)
            if sections[0] != "":
                new_list.append(TextNode(sections[0], TextType.TEXT))
            new_list.append(TextNode(image_alt, TextType.IMAGES, image_link))
            text = sections[1]
        if text != "":
            new_list.append(TextNode(text, TextType.TEXT))
    return new_list

def split_nodes_link(old_nodes):
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue
        text = node.text
        extraction = extract_markdown_links(text)
        if len(extraction) == 0:
            new_list.append(node)
            continue
        for e in extraction:
            link_alt = e[0]
            link_url = e[1]
            sections = text.split(f"[{link_alt}]({link_url})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_list.append(TextNode(sections[0], TextType.TEXT))
            new_list.append(TextNode(link_alt, TextType.LINK, link_url))
            text = sections[1]
        if text != "":
            new_list.append(TextNode(text, TextType.TEXT))
    return new_list


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter([nodes[2]], "_", TextType.ITALIC)
    nodes = split_nodes_delimiter([nodes[2]], "`", TextType.CODE)
    # nodes = split_nodes_link(nodes)
    # nodes = split_nodes_image(nodes)
    return nodes


