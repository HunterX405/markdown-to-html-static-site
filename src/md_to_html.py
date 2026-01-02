import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if not old_node.text_type == TextType.TEXT or not delimiter:
            new_nodes.append(old_node)
            continue
        if old_node.text.count(delimiter) == 0:
            new_nodes.append(old_node)
            continue
        if old_node.text.count(delimiter) % 2 != 0:
            raise SyntaxError("Invalid Markdown Syntax")
        texts = old_node.text.split(delimiter)
        for idx in range(len(texts)):
            # If idx is odd, the texts[idx] is probably the one inside the delimiter
            # List: [text, non-text, text, ...]
            if texts[idx]:
                if idx % 2 == 0: 
                    new_nodes.append(TextNode(texts[idx], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(texts[idx], text_type))
    return new_nodes


def extract_markdown_images(text: str):
    # A more lenient and lazy regex that allows nested brackets and parenthesis: r"!\[(.*?)\]\((.*?)\)"
    # Go to https://regexr.com/ for detailed explanation about regex
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    return matches


def extract_markdown_links(text: str):
    # A more lenient and lazy regex that allows nested brackets and parenthesis: r"(?<!!)\[(.*?)\]\((.*?)\)"
    # Go to https://regexr.com/ for detailed explanation about regex
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    return matches


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        node_text = node.text
        images = extract_markdown_images(node_text)
        if not images:
            new_nodes.append(node)
            continue
        for image_alt, image_link in images:
            sections = node_text.split(f"![{image_alt}]({image_link})", 1)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            node_text = sections[1]
        
        if node_text:
            new_nodes.append(TextNode(node_text, TextType.TEXT))
    
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        node_text = node.text
        links = extract_markdown_links(node_text)
        if not links:
            new_nodes.append(node)
            continue
        for link_text, link_url in links:
            sections = node_text.split(f"[{link_text}]({link_url})", 1)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            node_text = sections[1]
        
        if node_text:
            new_nodes.append(TextNode(node_text, TextType.TEXT))
    
    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    new_nodes = [TextNode(text, TextType.TEXT)]
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    new_nodes = split_nodes_delimiter(new_nodes, '**', TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, '_', TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, '`', TextType.CODE)

    return new_nodes


def markdown_to_blocks(markdown: str) -> list[str]:
    return [block.strip() for block in markdown.split("\n\n") if block.strip()]

