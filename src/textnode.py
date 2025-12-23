from enum import Enum

class TextType(Enum):
    PLAIN_TEXT = "plain"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code"
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