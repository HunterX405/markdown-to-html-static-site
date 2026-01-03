import unittest
from md_to_html import (text_node_to_html_node, extract_markdown_links, extract_markdown_images, 
                        split_nodes_image, split_nodes_link, 
                        split_nodes_delimiter, text_to_textnodes,
                        markdown_to_blocks, block_to_block_type,
                        block_to_html_node, markdown_to_html_node
                        )
from textnode import TextNode, TextType, BlockType
from htmlnode import ParentNode, LeafNode


class TestMDtoHTMLNode(unittest.TestCase):

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

    # block_to_block_type() testcases

    def test_block_heading(self):
        text = "# This is a heading"
        blocktype = block_to_block_type(text)
        self.assertEqual(BlockType.HEADING, blocktype)
    
    def test_block_heading2(self):
        text = "## This is an h2 heading"
        blocktype = block_to_block_type(text)
        self.assertEqual(BlockType.HEADING, blocktype)

    def test_block_multiline_heading(self):
        text = "# This is a heading\n## This is an h2 heading"
        blocktype = block_to_block_type(text)
        self.assertEqual(BlockType.HEADING, blocktype)
    
    def test_block_code(self):
        text = "```\nThis is a code block.\n```"
        blocktype = block_to_block_type(text)
        self.assertEqual(BlockType.CODE, blocktype)

    def test_block_quote(self):
        text = ">This is a quote block"
        blocktype = block_to_block_type(text)
        self.assertEqual(BlockType.QUOTE, blocktype)    

    def test_block_quote_multiline(self):
        text = ">This is a quote block\n>Another quote"
        blocktype = block_to_block_type(text)
        self.assertEqual(BlockType.QUOTE, blocktype) 

    def test_block_unordered_list(self):
        text = "- This is\n- an unordered\n- list"
        blocktype = block_to_block_type(text)
        self.assertEqual(BlockType.ULIST, blocktype)

    def test_block_ordered_list(self):
        text = "1. This is\n2. a ordered\n3. list"
        blocktype = block_to_block_type(text)
        self.assertEqual(BlockType.OLIST, blocktype)

    def test_block_paragraph(self):
        text = "This is just a paragraph"
        blocktype = block_to_block_type(text)
        self.assertEqual(BlockType.PARAGRAPH, blocktype)

    def test_block_invalid_unordered_list(self):
        text = "-This is\n-an invalid\n-unordered list"
        blocktype = block_to_block_type(text)
        self.assertEqual(BlockType.PARAGRAPH, blocktype)

    def test_block_invalid_ordered_list(self):
        text = "2. This is\n2.an invalid\n3. ordered list"
        blocktype = block_to_block_type(text)
        self.assertEqual(BlockType.PARAGRAPH, blocktype)

    def test_block_invalid_ordered_list2(self):
        text = "1. This is\n3. an invalid\n3. ordered list"
        blocktype = block_to_block_type(text)
        self.assertEqual(BlockType.PARAGRAPH, blocktype)

    def test_block_invalid_ordered_list3(self):
        text = "1. This is\n2.an invalid\n3. ordered list"
        blocktype = block_to_block_type(text)
        self.assertEqual(BlockType.PARAGRAPH, blocktype)
    
    def test_block_ten_ordered_list3(self):
        text = "1. one\n2. two\n3. three\n4. four\n5. five\n6. six\n7. seven\n8. eight\n9. nine\n10. ten"
        blocktype = block_to_block_type(text)
        self.assertEqual(BlockType.OLIST, blocktype)

    # block_to_html_node() testcases
     # strip() is used for multiline texts as this function is usually called after markdown_to_blocks() which does the strip()

    def test_block_heading(self):
        text = '## This is a heading 2'
        result = block_to_html_node(text, BlockType.HEADING)
        children = [
            LeafNode(None, 'This is a heading 2')
        ]
        self.assertEqual(ParentNode('h2', children), result)

    def test_block_heading_inline_bold(self):
        text = '## This is a heading 2 with **bold** text'
        result = block_to_html_node(text, BlockType.HEADING)
        children = [
            LeafNode(None, 'This is a heading 2 with '),
            LeafNode('b', 'bold'),
            LeafNode(None, ' text')
        ]
        self.assertEqual(ParentNode('h2', children), result)

    def test_block_code(self):
        text = '``` This is a code block ```'
        result = block_to_html_node(text, BlockType.CODE)
        children = [
            LeafNode('code', ' This is a code block ')
        ]
        self.assertEqual(ParentNode('pre', children), result)

    def test_block_code_multiline_nested(self):
        text = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        result = block_to_html_node(text.strip(), BlockType.CODE)
        children = [
            LeafNode('code', 'This is text that _should_ remain\nthe **same** even with inline stuff\n')
        ]
        self.assertEqual(ParentNode('pre', children), result)

    def test_block_quote(self):
        text = """
> quote 1
> quote 2
> quote 3
"""
        result = block_to_html_node(text.strip(), BlockType.QUOTE)
        children = [
            LeafNode(None, ' quote 1\n quote 2\n quote 3')
        ]
        self.assertEqual(ParentNode('blockquote', children), result)

    def test_block_quote_single(self):
        text = """
> quote 1
"""
        result = block_to_html_node(text.strip(), BlockType.QUOTE)
        children = [
            LeafNode(None, ' quote 1')
        ]
        self.assertEqual(ParentNode('blockquote', children), result)

    def test_block_ulist(self):
        text = """
- item 1
- item 2
- item 3
- item 4
"""
        result = block_to_html_node(text.strip(), BlockType.ULIST)
        children = [
            ParentNode('li', [LeafNode(None, 'item 1')]),
            ParentNode('li', [LeafNode(None, 'item 2')]),
            ParentNode('li', [LeafNode(None, 'item 3')]),
            ParentNode('li', [LeafNode(None, 'item 4')]),
        ]
        self.assertEqual(ParentNode('ul', children), result)

    def test_block_olist(self):
        text = """
1. item 1
2. item 2
3. item 3
4. item 4
5. item 5
"""
        result = block_to_html_node(text.strip(), BlockType.OLIST)
        children = [
            ParentNode('li', [LeafNode(None, 'item 1')]),
            ParentNode('li', [LeafNode(None, 'item 2')]),
            ParentNode('li', [LeafNode(None, 'item 3')]),
            ParentNode('li', [LeafNode(None, 'item 4')]),
            ParentNode('li', [LeafNode(None, 'item 5')]),
        ]
        self.assertEqual(ParentNode('ol', children), result)

    def test_block_paragraph(self):
        text = "This is text in a paragraph that has _italic_ and **bold** text inline"
        result = block_to_html_node(text, BlockType.PARAGRAPH)
        children = [
            LeafNode(None, 'This is text in a paragraph that has '),
            LeafNode('i', 'italic'),
            LeafNode(None, ' and '),
            LeafNode('b', 'bold'),
            LeafNode(None, ' text inline')
        ]
        self.assertEqual(ParentNode('p', children), result)

    def test_block_paragraph_multiline(self):
        text = """This is text in a
multiline paragraph
that has _italic_
and **bold** text inline
"""
        result = block_to_html_node(text.strip(), BlockType.PARAGRAPH)
        children = [
            LeafNode(None, 'This is text in a multiline paragraph that has '),
            LeafNode('i', 'italic'),
            LeafNode(None, ' and '),
            LeafNode('b', 'bold'),
            LeafNode(None, ' text inline')
        ]
        self.assertEqual(ParentNode('p', children), result)

    def test_invalid_type(self):
        text = "This is text"
        self.assertRaises(TypeError, block_to_html_node, text, 'nonetype')

    # markdown_to_html_node() testcases

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading_with_paragraphs(self):
        md = """
### This is an h3 heading

This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>This is an h3 heading</h3><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_quotes(self):
        md = """
>This is a quote from me
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote from me</blockquote></div>",
        )

    def test_quotes_multiline(self):
        md = """
>This is a 
>Multiline quote 
>from me
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a \nMultiline quote \nfrom me</blockquote></div>",
        )

    def test_ulist(self):
        md = """
- item 1
- item 2
- item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>item 1</li><li>item 2</li><li>item 3</li></ul></div>",
        )

    def test_olist(self):
        md = """
1. item 1
2. item 2
3. item 3
4. item 4
5. item 5
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>item 1</li><li>item 2</li><li>item 3</li><li>item 4</li><li>item 5</li></ol></div>",
        )
        

if __name__ == "__main__":
    unittest.main()