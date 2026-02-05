import os
from block_markdown import markdown_to_html_node
from inline_markdown import extract_title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    markdown_file = open(from_path)
    read_markdown = markdown_file.read()
    html_creation = markdown_to_html_node(read_markdown)
    markdown_file.close()
    print(markdown_file)
    html_result = html_creation.to_html()
    title = extract_title(read_markdown)
    template_file = open(template_path)
    read_template = template_file.read()
    update_file = read_template.replace('{{ Title }}', title).replace('{{ Content }}', html_result)
    template_file.close()
    write_template = open(template_path, 'w')
    write_template.write(update_file)
    write_template.close()
    
    if os.path.dirname(dest_path):
        with open(template_path, 'r') as template:
            final = template.read()
        with open(dest_path, 'w') as file:
            file.write(final)

    # with open(template_path, 'r') as file:
    #     file_contents = file.read()

    # update_file = file_contents.replace('{{ Title }}', title).replace('{{ Content }}', html_result)

    # with open(template_path, 'w') as file:
    #     file.write(update_file)
        
