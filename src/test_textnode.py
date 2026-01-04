import unittest

from textnode import TextNode, TextType

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

if __name__ == "__main__":
    unittest.main()