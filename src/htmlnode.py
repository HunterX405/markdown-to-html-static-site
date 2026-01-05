from dataclasses import dataclass, field
from typing import override
from enum import Enum

@dataclass
class HTMLNode:
    tag: str
    value: str | None
    children: list | None = None
    props: dict[str, str] = field(default_factory=dict)

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if not self.props:
            return ''
        return "".join(f' {att}="{value}"' for att, value in self.props.items())
    
@dataclass
class LeafNode(HTMLNode):
    value: str
    children: None = field(default=None, init=False)

    @override
    def to_html(self):
        # only img have a '' value.
        if not self.value and self.tag != 'img':
            raise ValueError("All leaf nodes must have a value")
        if not self.tag:
            return self.value
        if self.tag == 'img':
            return f'<{self.tag}{self.props_to_html()}>'
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    
@dataclass
class ParentNode(HTMLNode):
    value: None = field(default=None, init=False)
    children: list[HTMLNode] = field(default_factory=list)

    @override
    def to_html(self):
        if not self.tag:
            raise ValueError("tag is required")
        if self.children is None:
            raise ValueError("children is not provided")
        
        html = f'<{self.tag}{self.props_to_html()}>'
        for child in self.children:
            html += child.to_html()
        html += f'</{self.tag}>'
        
        return html
    

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

@dataclass
class TextNode:
    text: str
    text_type: TextType
    url: str | None = None

    def to_html_node(self) -> LeafNode:
        match self.text_type:
            case TextType.TEXT:
                return LeafNode(None, self.text)
            case TextType.BOLD:
                return LeafNode('b', self.text)
            case TextType.ITALIC:
                return LeafNode('i', self.text)
            case TextType.CODE:
                return LeafNode('code', self.text)
            case TextType.LINK:
                return LeafNode('a', self.text, {"href": self.url})
            case TextType.IMAGE:
                return LeafNode('img', '', {"src": self.url, "alt": self.text})
            
            case _:
                raise ValueError("Invalid TextType for TextNode")