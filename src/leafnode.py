from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value:
            if not self.tag:
                return self.value
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        raise ValueError("No value in Leaf Node")
