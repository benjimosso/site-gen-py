from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode
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

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.OLIST:
        return olist_to_html_node(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        parts = item.split(". ", 1)
        text = parts[1]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


# def type_block_to_node(block_text ,block_type):
#     if block_type == BlockType.HEADING:
#         number = 0
#         for i in block_text:
#             if i == "#":
#                 number += 1
#         return ParentNode(f"h{number}", text_to_children(block_text[number:]))
#     if block_type == BlockType.QUOTE:
#         return ParentNode("blockquote", text_to_children(block_text[2:]))
#     if block_type == BlockType.CODE:
#         code_list = block_text.splitlines()
#         code_list = code_list[1:-1]
#         inner_text = "\n".join(code_list)
#         code_node = LeafNode("code", inner_text)
#         parent = ParentNode("pre", [code_node])
#         return parent
#
#     if block_type == BlockType.ULIST:
#         block_list = block_text.split("\n")
#         parent_node = ParentNode("ul", children=[])
#         for b in block_list:
#             b = b[2:]
#             b = text_to_children(b)
#             li_parent = ParentNode("li", children=b)
#             parent_node.children.append(li_parent)
#         return parent_node
#     if block_type == BlockType.OLIST:
#         block_list = block_text.split("\n")
#         parent_node = ParentNode("ol", children=[])
#         for b in block_list:
#             b = b[3:]
#             b = text_to_children(b)
#             li_parent = ParentNode("li", children=b)
#             parent_node.children.append(li_parent)
#         return parent_node
#     paragraph_lines = block_text.split("\n")
#     paragraph_text = " ".join(paragraph_lines)
#     children = text_to_children(paragraph_text)
#     return ParentNode("p", children=children)
#
# def text_to_children(text):
#     textnodes = text_to_textnodes(text)
#     final_nodes = []
#     for t in textnodes:
#         final_nodes.append(text_node_to_html_node(t))
#     return final_nodes
#
# def markdown_to_html_node(markdown):
#     blocks = markdown_to_blocks(markdown)
#     parent = ParentNode("div", [])
#     for block in blocks:
#         block_type = block_to_block_type(block)
#         children_html = type_block_to_node(block, block_type)
#         parent.children.append(children_html)
#     return parent