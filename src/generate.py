import os, shutil
from pathlib import Path
from md_to_html import extract_title, markdown_to_html_node

def copy_static_files(src_dir_path: str, dest_dir_path: str) -> None:
    os.makedirs(dest_dir_path, exist_ok=True)

    for filename in os.listdir(src_dir_path):
        src_path = os.path.join(src_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
            print(f'COPY-FILE: \'{src_path}\' -> \'{dest_path}\'')
        else:
            copy_static_files(src_path, dest_path)


def generate_public(dest_path: str, static_path: str) -> None:
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)
    os.makedirs(dest_path)
    print(f'CREATE: \'{dest_path}\' folder')

    print(f'COPY: \'{static_path}\' -> \'{dest_path}\'')
    copy_static_files(static_path, dest_path)


def generate_page_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, base_path: str) -> None:
    os.makedirs(dest_dir_path, exist_ok=True)
    
    for filename in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(src_path) and Path(src_path).suffix == '.md':
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(src_path, template_path, dest_path, base_path)
        elif os.path.isdir(src_path):
            generate_page_recursive(src_path, template_path, dest_path, base_path)


def generate_page(from_path: str, template_path: str, dest_path: str, base_path: str) -> None:
    print(f'Generating page \'{from_path}\' -> \'{dest_path}\' | Template: \'{template_path}\'')

    md = open(from_path).read()
    template_file = open(template_path).read()
    
    title = extract_title(md)
    content = markdown_to_html_node(md).to_html()

    template_html = template_file.replace('{{ Title }}', title).replace('{{ Content }}', content)
    html_text = template_html.replace('href=\"/', f'href=\"{base_path}').replace('src=\"/', f'src=\"{base_path}')

    with open(dest_path, 'w+') as html:
        html.write(html_text)