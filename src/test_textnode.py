import unittest

from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
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

# text_node_to_html_node() test cases

    def test_text_node_to_html_node_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_text_node_to_html_node_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, "This is a bold node")
    
    def test_text_node_to_html_node_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'i')
        self.assertEqual(html_node.value, "This is an italic node")

    def test_text_node_to_html_node_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'code')
        self.assertEqual(html_node.value, "This is a code node")
    
    def test_text_node_to_html_node_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.boot.dev/")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev/"})

    def test_text_node_to_html_node_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "https://www.boot.dev/img/bootdev-logo-full-small.webp")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, '')
        self.assertEqual(html_node.props, {"src": "https://www.boot.dev/img/bootdev-logo-full-small.webp", "alt": "This is an image node"})
    
    def test_text_node_to_html_node_non_text_type(self):
        node = TextNode("This is an invalid node", 'number')
        self.assertRaises(ValueError, text_node_to_html_node, node)
    

if __name__ == "__main__":
    unittest.main()