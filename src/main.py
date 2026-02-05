import os, shutil, sys

from copystatic import copy_files_recursive
from generate_page import generate_page, generate_pages_recursive



dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
dir_path_docs = "./docs"
template_path = "./template.html"
basepath = sys.argv


def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"


    print("Deleting Docs directory...")
    if os.path.exists(dir_path_docs):
        shutil.rmtree(dir_path_docs)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_docs)
    
    generate_pages_recursive(
        dir_path_content, template_path, dir_path_docs, basepath
    )

    
if __name__ == "__main__":
    main()