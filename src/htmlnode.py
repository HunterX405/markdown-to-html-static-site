
class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if not self.props:
            return ''
        return "".join(f' {att}="{value}"' for att, value in self.props.items())
    
    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'
    
    def __eq__(self, node):
        return (self.tag == node.tag and
                self.value == node.value and
                self.children == node.children and
                self.props == node.props)
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        # only img have a '' value.
        if not self.value and self.tag != 'img':
            raise ValueError("All leaf nodes must have a value")
        if not self.tag:
            return self.value
        if self.tag == 'img':
            return f'<{self.tag}{self.props_to_html()}>'
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

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