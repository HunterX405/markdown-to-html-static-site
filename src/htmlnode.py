# so type checkers won't throw a not defined warning for 
# class value types referencing to themselves
from __future__ import annotations
from dataclasses import dataclass, field
from typing import override
from enum import Enum

# slots=True so the class values are strictly the only ones initiated
# spelling errors for class values throws an error 'node.tga' throws an error
# can't add other values outside the class and saves memory
@dataclass(slots=True)
class HTMLNode:
    tag: str
    value: str | None
    children: list[HTMLNode] | None = None
    props: dict[str, str] = field(default_factory=dict)

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if not self.props:
            return ''
        return "".join(f' {att}="{value}"' for att, value in self.props.items())
    
@dataclass(slots=True)
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
    
@dataclass(slots=True)
class ParentNode(HTMLNode):
    value: None = field(default=None, init=False)
    children: list[HTMLNode] = field(default_factory=list)

    @override
    def to_html(self):
        if not self.tag:
            raise ValueError("tag is required")
        if not self.children:
            raise ValueError("ParentNode must have at least one child")
        
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


@dataclass(slots=True)
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