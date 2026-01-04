import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_none(self):
        node = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node, node2)

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


if __name__ == "__main__":
    unittest.main()