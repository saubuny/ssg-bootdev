from block_markdown import markdown_to_html_node
import os


def extract_title(markdown: str) -> str:
    header = markdown.splitlines()[0]
    if header.startswith("# "):
        return header.lstrip("# ")
    raise Exception("No header found in markdown")


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f" * Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = open(from_path).read()
    template = open(template_path).read()
    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    html = template.replace("{{ Title }}", title).replace("{{ Content }}", content)
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    open(dest_path, "w").write(html)
