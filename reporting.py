from enum import Enum

import markdown

from emails import send_email


class Heading1:
    def __init__(self, title):
        self.title = title
        self.content = []

    def add_content(self, *sections, content):
        try:
            title, sections = sections[0], sections[1:]
        except IndexError:
            self.content.append(content)
            return

        header = next((c for c in self.content if c.title == title), None)

        if header:
            header.add_content(content=content)
        else:
            header = Heading2(title)
            header.add_content(content=content)
            self.content.append(header)


class Heading2:
    def __init__(self, title):
        self.title = title
        self.content = []

    def add_content(self, content):
        self.content.append(content)


class Report:
    def __init__(self, title):
        self.title = title
        self.content = []

    def email(self, to):
        send_email(to, subject=self.title, body=self.render(Renderer.HTML))

    def render(self, type):
        return renderers[type](self.content)

    def add_content(self, *sections, content):
        try:
            title, sections = sections[0], sections[1:]
        except IndexError:
            self.content.append(content)
            return

        header = next((c for c in self.content if c.title == title), None)

        if header:
            header.add_content(*sections, content=content)
        else:
            header = Heading1(title)
            header.add_content(*sections, content=content)
            self.content.append(header)


class Renderer(Enum):
    MARKDOWN = 0
    HTML = 1


def render_markdown(content, rendered_content=""):
    for section in content:
        if isinstance(section, Heading1):
            rendered_content += f"# {section.title}\n"
            rendered_content = render_markdown(section.content, rendered_content)
        elif isinstance(section, Heading2):
            rendered_content += f"## {section.title}\n"
            rendered_content = render_markdown(section.content, rendered_content)
        else:
            rendered_content += f"{section}\n"

    return rendered_content


def render_html(content):
    markdown_content = render_markdown(content)
    html = markdown.markdown(markdown_content)

    return html


renderers = {
    Renderer.MARKDOWN: render_markdown,
    Renderer.HTML: render_html,
}


