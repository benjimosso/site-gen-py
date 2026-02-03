from enum import Enum
from htmlnode import HTMLNode
from textnode import text_node_to_html_node
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def markdown_to_blocks(markdown):
    # new_markdown = markdown.strip().split("\n\n")
    # for m in new_markdown:
    #     if m == "":
    #         new_markdown.remove(m)
    # return new_markdown
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH

def type_block_to_node(block_text ,block_type):
    if block_type == BlockType.HEADING:
        number = 0
        for i in block_text:
            if i == "#":
                number += 1
        return HTMLNode(f"h{number}" ,block_text)
    if block_type == BlockType.QUOTE:
        return HTMLNode("blockquote", block_text)
    if block_type == BlockType.CODE:
        return HTMLNode("code", block_text)
    if block_type == BlockType.ULIST:
        return HTMLNode("ul", block_text)
    if block_type == BlockType.OLIST:
        return HTMLNode("li", block_text)
    return HTMLNode("p", block_text)

def text_to_children(text):
    textnodes = text_to_textnodes(text)
    # print(textnodes)
    test = []
    for t in textnodes:
        test.append(text_node_to_html_node(t))
    return test

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    print("BLOCKS!!: ", blocks)
    for block in blocks:
        block_type = block_to_block_type(block)
        createhtml = type_block_to_node(block, block_type)
        child_nodes = text_to_children(createhtml.value)
        print("child nodes: ", child_nodes)