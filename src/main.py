from generate import generate_public, generate_page_recursive


def main():
    public_folder = './public'
    static_folder = './static'   
    generate_public(public_folder, static_folder)

    template_file_path = './template.html'
    content_folder = './content'
    print('Generating contents...')
    generate_page_recursive(content_folder, template_file_path, public_folder)


if __name__ == '__main__':
    main()