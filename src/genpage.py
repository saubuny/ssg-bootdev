from block_markdown import markdown_to_html_node
import os
import pathlib


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
        print(f" * Directory {os.path.dirname(dest_path)} does not exist, creating it")
        os.makedirs(os.path.dirname(dest_path))
    open(dest_path, "w").write(html)


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str
) -> None:
    for page in os.listdir(dir_path_content):
        path = os.path.join(pathlib.Path(page).cwd(), dir_path_content, page)
        dest = os.path.join(
            pathlib.Path(page).cwd(), dest_dir_path, page.rstrip(".md") + ".html"
        )
        if os.path.isfile(path):
            print(f" * {path} is a file, generating page...")
            generate_page(path, template_path, dest)
        else:
            print(f" * {path} is not a file, doing recursive call...")
            generate_pages_recursive(
                path, template_path, os.path.join(dest_dir_path, page)
            )
