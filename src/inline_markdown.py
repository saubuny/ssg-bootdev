from textnode import TextNode
import re


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: str
) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != "text":
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid Markdown")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], "text"))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        matches = extract_markdown_images(old_node.text)
        if len(matches) == 0:
            new_nodes.append(old_node)
            continue
        for i in range(len(matches)):
            text = old_node.text.split(f"![{matches[0][0]}]({matches[0][1]})", 1)
            if i < len(text):
                new_nodes.append(TextNode(text[i], "text"))
            new_nodes.append(TextNode(matches[i][0], "image", matches[i][1]))
            if i + 1 < len(text) and text[i + 1] != "":
                new_nodes.append(TextNode(text[i + 1], "text"))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        matches = extract_markdown_links(old_node.text)
        if len(matches) == 0:
            new_nodes.append(old_node)
            continue
        for i in range(len(matches)):
            text = old_node.text.split(f"[{matches[0][0]}]({matches[0][1]})", 1)
            if i < len(text):
                new_nodes.append(TextNode(text[i], "text"))
            new_nodes.append(TextNode(matches[i][0], "link", matches[i][1]))
            if i + 1 < len(text) and text[i + 1] != "":
                new_nodes.append(TextNode(text[i + 1], "text"))
    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    node = TextNode(text, "text")
    with_bold = split_nodes_delimiter([node], "**", "bold")
    with_italic = split_nodes_delimiter(with_bold, "*", "italic")
    with_code = split_nodes_delimiter(with_italic, "`", "code")
    with_image = split_nodes_image(with_code)
    return split_nodes_link(with_image)
