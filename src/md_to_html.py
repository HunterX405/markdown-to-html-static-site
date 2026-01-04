import re
from textnode import TextNode, TextType, BlockType
from htmlnode import HTMLNode, LeafNode, ParentNode


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    text = text_node.text
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text)
        case TextType.BOLD:
            return LeafNode('b', text)
        case TextType.ITALIC:
            return LeafNode('i', text)
        case TextType.CODE:
            return LeafNode('code', text)
        case TextType.LINK:
            return LeafNode('a', text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode('img', '', {"src": text_node.url, "alt": text})
        
        case _:
            raise ValueError("Invalid TextType for TextNode")


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


def extract_markdown_images(text: str) -> list:
    # A more lenient and lazy regex that allows nested brackets and parenthesis: r"!\[(.*?)\]\((.*?)\)"
    # Go to https://regexr.com/ for detailed explanation about regex
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text: str) -> list:
    # A more lenient and lazy regex that allows nested brackets and parenthesis: r"(?<!!)\[(.*?)\]\((.*?)\)"
    # Go to https://regexr.com/ for detailed explanation about regex
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


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

        
def block_to_block_type(markdown: str) -> BlockType:
    if re.match(r'^#{1,6} ', markdown):
        return BlockType.HEADING
    
    if markdown.startswith('```') and markdown.endswith('```'):
        return BlockType.CODE
    
    lines = markdown.splitlines()

    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE
    
    if all(line.startswith('- ') for line in lines):
        return BlockType.ULIST
    
    if markdown.startswith('1. '):
        matches = [re.match(r"^(\d+)\. ", line) for line in lines]
        if [int(m.group(1)) for m in matches if m] == [n for n in range(1, len(lines) + 1)]:
            return BlockType.OLIST
        
    return BlockType.PARAGRAPH


def text_to_children(text: str) -> list[LeafNode]:
    return [text_node_to_html_node(textnode) for textnode in text_to_textnodes(text)]


def text_list_to_children(text: str) -> list[LeafNode]:
    return [ParentNode('li', text_to_children(li_text)) for li_text in text.splitlines()]


def block_to_html_node(block: str, block_type: BlockType) -> ParentNode:
    match block_type:
        case BlockType.HEADING:
            level = block[:6].count('#')
            text = re.sub(rf"^{'#' * level} ", '', block)
            return ParentNode(f'h{level}', text_to_children(text))
        case BlockType.CODE:
            text = block.replace('```', '')
            if text.startswith('\n'):
                text = text[1:]
            children = [LeafNode('code', text)]
            return ParentNode('pre', children)
        case BlockType.QUOTE:
            text = re.sub(r"^>\s*", '', block, flags=re.MULTILINE).strip()
            return ParentNode('blockquote', text_to_children(text))
        case BlockType.ULIST:
            text = re.sub(r"^- ", '', block, flags=re.MULTILINE)
            return ParentNode('ul', text_list_to_children(text))
        case BlockType.OLIST:
            text = re.sub(r"^\d+\. ", '', block, flags=re.MULTILINE)
            return ParentNode('ol', text_list_to_children(text))
        case BlockType.PARAGRAPH:
            text = block.replace('\n', ' ')
            return ParentNode('p', text_to_children(text))
        
        case _:
            raise TypeError('Invalid Block Type')


def markdown_to_html_node(markdown: str) -> HTMLNode:
    children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        children.append(block_to_html_node(block, block_type))

    return ParentNode('div', children)


def extract_title(markdown: str):
    if not markdown.startswith('# '):
        raise ValueError('No h1 header in markdown.')
    first_line = markdown.split('\n', 1)[0]
    return re.sub(r"^# ", '', first_line).strip()