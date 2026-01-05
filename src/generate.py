import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, Template
from md_to_html import extract_title, markdown_to_html_node

def copy_static_files(src_dir_path: Path, dest_dir_path: Path) -> None:
    dest_dir_path.mkdir(parents=True, exist_ok=True)

    for filename in src_dir_path.iterdir():
        dest_path = dest_dir_path / filename.name
        if filename.is_file():
            shutil.copy(filename, dest_path)
            print(f'COPY-FILE: \'{filename}\' -> \'{dest_path}\'')
        else:
            copy_static_files(filename, dest_path)


def generate_public(dest_path: Path, static_path: Path) -> None:
    if dest_path.exists():
        shutil.rmtree(dest_path)
    dest_path.mkdir()
    print(f'CREATE: \'{dest_path}\' folder')

    print(f'COPY: \'{static_path}\' -> \'{dest_path}\'')
    copy_static_files(static_path, dest_path)


def generate_page_recursive(dir_path_content: Path, template_path: Path, dest_dir_path: Path, base_path: str) -> None:
    dest_dir_path.mkdir(parents=True, exist_ok=True)
    
    for filename in dir_path_content.iterdir():
        dest_path = dest_dir_path / filename.name
        if filename.is_file() and filename.suffix == '.md':
            dest_path = dest_path.with_suffix(".html")
            generate_page(filename, template_path, dest_path, base_path)
        elif filename.is_dir():
            generate_page_recursive(filename, template_path, dest_path, base_path)


def generate_page(from_path: Path, template_path: str, dest_path: Path, base_path: str) -> None:
    print(f'Generating page \'{from_path}\' -> \'{dest_path}\' | Template: \'{template_path}\'')

    md = from_path.read_text()
    title = extract_title(md)

    content: str = markdown_to_html_node(md).to_html()
    content = content.replace('href=\"/', f'href=\"{base_path}').replace('src=\"/', f'src=\"{base_path}')

    env = Environment(loader=FileSystemLoader(template_path))
    template = env.get_template("template.html")
    data = {
        "title": title,
        "content": content,
        "base_path": base_path
    }
    html = template.render(data)
    dest_path.write_text(html)