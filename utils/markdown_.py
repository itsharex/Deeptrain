import markdown


def parse(md):
    return markdown.markdown(
        md, extensions=
        [
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ]
    )
