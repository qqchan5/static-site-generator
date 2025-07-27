#from textnode import *
from markdown_blocks import markdown_to_html_node
import os
import shutil
import re

LOG_FILE = ""
static_dir = "static"
public_dir = "public"
content_dir = "content"
template_file = "template.html"

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        template = f.read()

    html_string = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    index = template.replace("{{ Title }}", title)
    index = index.replace("{{ Content }}", html_string)
    with open(dest_path, 'w') as f:
        f.write(index)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    os.makedirs(dest_dir_path, exist_ok=True)
    for i_path in os.listdir(dir_path_content):
        if not os.path.isfile(f"{dir_path_content}/{i_path}"):
            generate_pages_recursive(f"{dir_path_content}/{i_path}", template_path, f"{dest_dir_path}/{i_path}")
        elif re.search(r"\.md$", i_path):
            generate_page(f"{dir_path_content}/{i_path}", template_path, f"{dest_dir_path}/{re.sub(r"md$", "html", i_path)}")

def extract_title(markdown):
    match = re.search(r"^# (.*)", markdown)
    return match.group(1)

def copy_dir(dir, log=None):
    dst = dir.replace(static_dir, public_dir, 1)
    print(f"mkdir {dst}")
    if log:
        log.write(f"mkdir {dst}\n")
    os.mkdir(f"{dst}")
    for i in os.listdir(dir):
        i_path = f"{dir}/{i}"
        if os.path.isfile(i_path):
            print(f"cp {i_path} to {dst}")
            if log:
                log.write(f"cp {i_path} to {dst}\n")
            shutil.copy(i_path, f"{dst}")
        else:
            copy_dir(i_path, log)

def main():
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    copy_dir(static_dir)
    generate_pages_recursive(content_dir, template_file, public_dir)

if __name__ == "__main__":
    main()
