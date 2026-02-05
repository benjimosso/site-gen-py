import os
from pathlib import Path
from block_markdown import markdown_to_html_node
# from inline_markdown import extract_title


# def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
#     # print("Source dir: ", dir_path_content)
#     # print("Dest dir: ",dest_dir_path)
#     if os.path.isdir(dir_path_content):
#         list_dir = os.listdir(dir_path_content)
#         for l in list_dir:
#             # l_path = pathlib.Path(dir_path_content) / l
#             l_path = os.path.join(dir_path_content, l)
#             # print(l_path.is_file())
#             if os.path.isfile(l_path):
#                 dest_file = os.path.join(dest_dir_path, "index.html")
#                 generate_page(l_path, template_path, dest_file)
#             else:
#                 dest_dir = os.path.join(dest_dir_path, l)
#                 generate_pages_recursive(l_path, template_path, dest_dir)

## Bootdev Solution:
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    print(from_path)
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)


def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")

    ## My version:

    # html_creation = markdown_to_html_node(read_markdown)
    # print(markdown_file)
    # html_result = html_creation.to_html()
    # title = extract_title(read_markdown)
    # template_file = open(template_path)
    # read_template = template_file.read()
    # update_file = read_template.replace('{{ Title }}', title).replace('{{ Content }}', html_result)
    # template_file.close()
    # write_template = open(template_path, 'w')
    # write_template.write(update_file)
    # write_template.close()
    
    # if os.path.dirname(dest_path):
    #     with open(template_path, 'r') as template:
    #         final = template.read()
    #     with open(dest_path, 'w') as file:
    #         file.write(final)

    # with open(template_path, 'r') as file:
    #     file_contents = file.read()

    # update_file = file_contents.replace('{{ Title }}', title).replace('{{ Content }}', html_result)

    # with open(template_path, 'w') as file:
    #     file.write(update_file)
        
