import unittest
from md_to_html import (extract_markdown_links, extract_markdown_images, 
                        split_nodes_image, split_nodes_link, 
                        split_nodes_delimiter, text_to_textnodes,
                        markdown_to_blocks
                        )
from textnode import TextNode, TextType


class TestMDtoHTMLNode(unittest.TestCase):

    # split_nodes_delimiter() test cases

    def test_split_nodes_delimiter_bold(self):
        node = TextNode(
            "This is a **bold** text node", 
            TextType.TEXT
        )
        result = split_nodes_delimiter([node], '**', TextType.BOLD)
        self.assertListEqual(
            [
                TextNode('This is a ', TextType.TEXT),
                TextNode('bold', TextType.BOLD),
                TextNode(' text node', TextType.TEXT)
            ], 
            result
        )

    def test_split_nodes_delimiter_italic(self):
        node = TextNode(
            "This is an _italic_ text node", 
            TextType.TEXT
        )
        result = split_nodes_delimiter([node], '_', TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode('This is an ', TextType.TEXT),
                TextNode('italic', TextType.ITALIC),
                TextNode(' text node', TextType.TEXT)
            ],
            result
        )

    def test_split_nodes_delimiter_code(self):
        node = TextNode(
            "This is a `code` text node", 
            TextType.TEXT
        )
        result = split_nodes_delimiter([node], '`', TextType.CODE)
        self.assertListEqual(
            [
                TextNode('This is a ', TextType.TEXT),
                TextNode('code', TextType.CODE),
                TextNode(' text node', TextType.TEXT)
            ],
            result
        )

    def test_split_nodes_delimiter_multiple_bold_node(self):
        nodes = [
            TextNode("This is a **bold** text node", TextType.TEXT),
            TextNode("This is **another bold** text node", TextType.TEXT)
        ]
        result = split_nodes_delimiter(nodes, '**', TextType.BOLD)
        self.assertListEqual(
            [
                TextNode('This is a ', TextType.TEXT),
                TextNode('bold', TextType.BOLD),
                TextNode(' text node', TextType.TEXT),
                TextNode('This is ', TextType.TEXT),
                TextNode('another bold', TextType.BOLD),
                TextNode(' text node', TextType.TEXT)
            ],
            result
        )

    def test_split_nodes_delimiter_no_delimiter(self):
        node = TextNode(
            "This is a regular text node", 
            TextType.TEXT
        )
        result = split_nodes_delimiter([node], '', TextType.TEXT)
        self.assertListEqual(
            [
                TextNode('This is a regular text node', TextType.TEXT)
            ],
            result
        )

    def test_split_nodes_delimiter_non_text_node_type(self):
        node = TextNode(
            "This is a bold text node", 
            TextType.BOLD
        )
        result = split_nodes_delimiter([node], '**', TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is a bold text node", TextType.BOLD)
            ],
            result
        )
    
    def test_split_nodes_delimiter_invalid_delimiter(self):
        node = TextNode(
            "This is an invalid **bold text node", 
            TextType.TEXT
        )
        self.assertRaises(Exception, split_nodes_delimiter, [node], '**', TextType.BOLD)

    def test_split_nodes_delimiter_different_delimiter(self):
        node = TextNode(
            "This is an _italic_ text node", 
            TextType.TEXT
        )
        result = split_nodes_delimiter([node], '**', TextType.BOLD)
        self.assertListEqual(
            [
                TextNode('This is an _italic_ text node', TextType.TEXT)
            ],
            result
        )

    # extract_markdown_images() testcases

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(text)
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"), 
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
            ],
            result
        )

    def test_extract_markdown_images2(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        result = extract_markdown_images(text)
        self.assertListEqual(
            [
                ("image", "https://i.imgur.com/zjjcJKZ.png")
            ],
            result
        )

    def test_extract_markdown_images_no_match(self):
        text = "This is text with an invalid image markdown (https://i.imgur.com/zjjcJKZ.png)"
        result = extract_markdown_images(text)
        self.assertListEqual([], result)
    
    def test_extract_markdown_images_link(self):
        text = "This is text with a [link](https://i.imgur.com/zjjcJKZ.png)"
        result = extract_markdown_images(text)
        self.assertListEqual([], result)


    # extract_markdown_links() testcases

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = extract_markdown_links(text)
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"), 
                ("to youtube", "https://www.youtube.com/@bootdotdev")
            ],
            result
        )

    def test_extract_markdown_links2(self):
        text = "This is text with a [link](https://i.imgur.com/zjjcJKZ.png)"
        result = extract_markdown_links(text)
        self.assertListEqual(
            [
                ("link", "https://i.imgur.com/zjjcJKZ.png")
            ],
            result
        )

    def test_extract_markdown_links_no_match(self):
        text = "This is text with an invalid link markdown link(https://i.imgur.com/zjjcJKZ.png)"
        result = extract_markdown_links(text)
        self.assertListEqual([], result)

    def test_extract_markdown_links_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        result = extract_markdown_links(text)
        self.assertListEqual([], result)

    # split_nodes_image() testcases

    def test_split_single_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
            ],
            new_nodes,
        )

    def test_split_image_only(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
            ],
            new_nodes,
        )

    def test_split_image_with_text_after(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) This is a default image.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" This is a default image.", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_single_image_extended(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) that is a default image.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" that is a default image.", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_two_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                )
            ],
            new_nodes,
        )

    def test_split_two_images_extended(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) that are both default images.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" that are both default images.", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_multiple_images_extended(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and yet another ![third image](https://i.imgur.com/3elNhQu.png) that are all default images.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" and yet another ", TextType.TEXT),
                TextNode(
                    "third image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" that are all default images.", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_no_image(self):
        node = TextNode(
            "This is just text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is just text", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_link_instead_of_image(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with a [link](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_non_text(self):
        node = TextNode(
            "This is a bold text",
            TextType.BOLD,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is a bold text", TextType.BOLD)
            ],
            new_nodes,
        )


    # split_nodes_links() testcases

    def test_split_single_link(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png")
            ],
            new_nodes,
        )

    def test_split_link_only(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png")
            ],
            new_nodes,
        )

    def test_split_link_with_text_after(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png) A default link.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" A default link.", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_single_link_extended(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) that is a default link.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" that is a default link.", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_two_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                )
            ],
            new_nodes,
        )

    def test_split_two_links_extended(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png) that are both default links.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" that are both default links.", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_multiple_links_extended(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png) and yet another [third link](https://i.imgur.com/3elNhQu.png) that are all default links.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" and yet another ", TextType.TEXT),
                TextNode(
                    "third link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" that are all default links.", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_no_link(self):
        node = TextNode(
            "This is just text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is just text", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_image_instead_of_link(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_non_text(self):
        node = TextNode(
            "This is a bold text",
            TextType.BOLD,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is a bold text", TextType.BOLD)
            ],
            new_nodes,
        )

    # text_to_textnodes() testcases

    def test_split_multiple_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes
        )
    
    def test_split_multiple_nodes_with_same_type(self):
        text = "This is **text** with an _italic_ word, another **bold** text, _another italic_ text, a `code block`, `another code block`, an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg), a [link](https://boot.dev), another ![image](https://i.imgur.com/zjjcJKZ.png) and [another link](https://i.imgur.com/3elNhQu.png)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word, another ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text, ", TextType.TEXT),
                TextNode("another italic", TextType.ITALIC),
                TextNode(" text, a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(", ", TextType.TEXT),
                TextNode("another code block", TextType.CODE),
                TextNode(", an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(", a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(", another ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://i.imgur.com/3elNhQu.png")
            ],
            new_nodes
        )

    def test_split_text_only(self):
        text = "This is just text"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is just text", TextType.TEXT)
            ],
            new_nodes
        )
    
    def test_split_just_bold_text(self):
        text = "**bold**"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD)
            ],
            new_nodes
        )

    def test_split_invalid_syntax(self):
        text = "A **bold** and _invalid italic**"
        self.assertRaises(SyntaxError, text_to_textnodes, text)

    def test_split_incomplete_syntax(self):
        text = "A **bold** and an incomplete _italic syntax"
        self.assertRaises(SyntaxError, text_to_textnodes, text)

    def test_split_nested_nodes(self):
        text = "This is **bold _inside_ bold** and a [link **inside**](https://x.y)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold _inside_ bold", TextType.BOLD),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link **inside**", TextType.LINK, "https://x.y")
            ],
            new_nodes
        )

    # markdown_to_blocks() testcases
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_extra_newlines(self):
        md = """
This is **bolded** paragraph


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_with_whitespaces(self):
        md = """
    This is **bolded** paragraph    


    This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line    



    - This is a list
- with items    
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

if __name__ == "__main__":
    unittest.main()