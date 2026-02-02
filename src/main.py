from inline_markdown import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node
from block_markdown import markdown_to_blocks, block_to_block_type, markdown_to_html_node
import re

def main():
    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
    result = markdown_to_html_node(md)
    print(result)

if __name__ == "__main__":
    main()