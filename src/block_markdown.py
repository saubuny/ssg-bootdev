from htmlnode import HTMLNode
from inline_markdown import text_to_textnodes
from parentnode import ParentNode
from leafnode import LeafNode
from textnode import text_node_to_html_mode


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = []
    raw_blocks = markdown.split("\n\n")
    for block in raw_blocks:
        if block == "":
            continue
        blocks.append(block.strip())
    return blocks


def block_to_block_type(block: str) -> str:
    lines = block.split("\n")

    if (
        block.startswith("# ")
        or block.startswith("## ")
        or block.startswith("### ")
        or block.startswith("#### ")
        or block.startswith("##### ")
        or block.startswith("###### ")
    ):
        return "heading"

    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return "code"

    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return "paragraph"
        return "quote"

    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return "paragraph"
        return "unordered_list"

    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return "paragraph"
        return "unordered_list"

    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return "paragraph"
            i += 1
        return "ordered_list"

    return "paragraph"


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children)


def block_to_html_node(block: str) -> HTMLNode:
    block_type = block_to_block_type(block)
    if block_type == "quote":
        return md_quote_to_html(block)
    if block_type == "unordered_list":
        return md_ul_to_html(block)
    if block_type == "ordered_list":
        return md_ol_to_html(block)
    if block_type == "code":
        return md_code_to_html(block)
    if block_type == "heading":
        return md_heading_to_html(block)
    if block_type == "paragraph":
        return md_paragraph_to_html(block)
    raise Exception("Invalid block type")


def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_mode(text_node)
        children.append(html_node)
    return children


def md_quote_to_html(markdown: str) -> HTMLNode:
    lines = markdown.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def md_ul_to_html(markdown: str) -> HTMLNode:
    items = markdown.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def md_ol_to_html(markdown: str) -> HTMLNode:
    items = markdown.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def md_code_to_html(markdown: str) -> HTMLNode:
    if not markdown.startswith("```") or not markdown.startswith("```"):
        raise ValueError("Invalid code block")
    text = markdown[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def md_heading_to_html(markdown: str) -> HTMLNode:
    level = 0
    for char in markdown:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(markdown):
        raise ValueError(f"Invalid heading level: {level}")
    text = markdown[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def md_paragraph_to_html(markdown: str) -> HTMLNode:
    lines = markdown.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)
