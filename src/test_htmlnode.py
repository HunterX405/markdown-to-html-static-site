import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, TextType, TextNode


class TestHTMLNode(unittest.TestCase):

    # HTMLNode() testcases
    def test_eq(self):
        node = HTMLNode("p", "This is a paragraph.")
        node2 = HTMLNode("p", "This is a paragraph.")
        self.assertEqual(node, node2)

    def test_link(self):
        props = {"href": "https://www.google.com",
                 "target": "_blank"}
        node = HTMLNode("a", "Google.com", None, props)
        node2 = HTMLNode("a", "Google.com", None, props)
        self.assertEqual(node, node2)

    def test_none(self):
        self.assertRaises(TypeError, HTMLNode)
    
    def test_props_to_html(self):
        props = {"href": "https://www.google.com",
                 "target": "_blank"}
        node = HTMLNode("a", "Google.com", None, props)
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
    
    def test_props_to_html_no_props(self):
        node = HTMLNode("p", "This is a paragraph")
        self.assertEqual(node.props_to_html(), '')

    def test_not_eq(self):
        props = {"href": "https://www.google.com",
                 "target": "_blank"}
        node = HTMLNode("p", "This is a paragraph.")
        node2 = HTMLNode("a", "Google.com", None, props)
        self.assertNotEqual(node, node2)

    # LeafNode() testcases

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        props = {"href": "https://www.google.com",
                 "target": "_blank"}
        node = LeafNode("a", "Google.com", props)
        self.assertEqual(node.to_html(), '<a href="https://www.google.com" target="_blank">Google.com</a>')

    def test_leaf_to_html_no_value(self):
        props = {"href": "https://www.google.com",
                 "target": "_blank"}
        node = LeafNode("a", None, props)
        self.assertRaises(ValueError, node.to_html)

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "This is a sentence.")
        self.assertEqual(node.to_html(), "This is a sentence.")

    def test_leaf_no_args(self):
        self.assertRaises(TypeError, LeafNode)

    # ParentNode() testcases

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    # TextNode() testcases

    def test_textnode_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_textnode_not_eq(self):
        node = TextNode('This is some anchor text', TextType.LINK, 'https://www.boot.dev')
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_textnode_not_eq_type(self):
        node = TextNode('This is a text node', TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_textnode_diff_link(self):
        node = TextNode('This is some anchor text', TextType.LINK, 'https://www.boot.dev')
        node2 = TextNode('This is some anchor text', TextType.LINK, 'https://www.boot.dev/u/hunterx405')
        self.assertNotEqual(node, node2)

    # TextNode to_html_node() test cases

    def test_text_node_to_html_node_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_text_node_to_html_node_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, "This is a bold node")
    
    def test_text_node_to_html_node_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, 'i')
        self.assertEqual(html_node.value, "This is an italic node")

    def test_text_node_to_html_node_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, 'code')
        self.assertEqual(html_node.value, "This is a code node")
    
    def test_text_node_to_html_node_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.boot.dev/")
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev/"})

    def test_text_node_to_html_node_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "https://www.boot.dev/img/bootdev-logo-full-small.webp")
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, '')
        self.assertEqual(html_node.props, {"src": "https://www.boot.dev/img/bootdev-logo-full-small.webp", "alt": "This is an image node"})
    
    def test_text_node_to_html_node_non_text_type(self):
        node = TextNode("This is an invalid node", 'number')
        self.assertRaises(ValueError, node.to_html_node)


if __name__ == "__main__":
    unittest.main()