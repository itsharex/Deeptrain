import markdown


def parse_markdown(md):
    return markdown.markdown(
        md, extensions=
        [
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ]
    )
