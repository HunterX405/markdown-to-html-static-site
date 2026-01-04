from enum import Enum
from htmlnode import LeafNode
import re

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


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
        