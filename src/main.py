from textnode import TextNode, TextType
from htmlnode import LeafNode

def main():
    print(TextNode('This is some anchor text', TextType.LINK, 'https://www.boot.dev'))

if __name__ == '__main__':
    main()