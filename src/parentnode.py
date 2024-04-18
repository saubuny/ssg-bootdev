from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str | None = None,
        children: list[HTMLNode] | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("No tag in Parent Node")
        if not self.children or len(self.children) == 0:
            raise ValueError("No children in Parent Node")
        res = ""
        for child in self.children:
            res += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{res}</{self.tag}>"
