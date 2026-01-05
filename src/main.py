from generate import generate_public, generate_page_recursive
import sys
from pathlib import Path

def main():
    base_path = '/'
    if len(sys.argv) >= 2:
        base_path = sys.argv[1]

    public_folder = Path("docs")
    static_folder = Path("static")
    generate_public(public_folder, static_folder)

    template_file_path = Path("template.html")
    content_folder = Path("content")
    print('Generating contents...')
    generate_page_recursive(content_folder, template_file_path, public_folder, base_path)


if __name__ == '__main__':
    main()