from inline_markdown import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node
import re

def main():
    test = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
    print("FINAL RESULT: ", test)



if __name__ == "__main__":
    main()