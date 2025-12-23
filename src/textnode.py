from enum import Enum
from htmlnode import LeafNode
class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode():
    def __init__(self, content: str, type: TextType, url=None):
        self.text = content
        self.text_type = type
        self.url = url

    def __eq__(self, node):
        return (self.text == node.text and 
                self.text_type == node.text_type and 
                self.url == node.url)
    
    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type.value}, {self.url})'
    


def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode('b', text_node.text)
        case TextType.ITALIC:
            return LeafNode('i', text_node.text)
        case TextType.CODE:
            return LeafNode('code', text_node.text)
        case TextType.LINK:
            return LeafNode('a', text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode('img', '', {"src": text_node.url, "alt": text_node.text})
        
        case _:
            raise Exception("Invalid TextType for TextNode")
        