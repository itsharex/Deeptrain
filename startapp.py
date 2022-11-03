import logging
from typing import *
from DjangoWebsite import settings
from rich import console
import os
import pathlib
from rich.filesize import decimal
from rich.markup import escape
from rich.text import Text
from rich.tree import Tree
from applications.config import json_writer, RepositoryAddress

# from rich.layout import Layout
# from rich.panel import Panel

logging.basicConfig(
    level=logging.NOTSET,
    format="[%(levelname)s]: %(message)s",
)
console = console.Console()
available_char = list("qwertyuiopasdfghjklzxcbnm_")


def walk_directory(_directory: pathlib.Path, _tree: Tree) -> None:
    """
    Recursively build a Tree with directory contents.
    -> https://github.com/Textualize/rich/blob/master/examples/tree.py
    """
    # Sort dirs first then by filename
    paths = sorted(
        pathlib.Path(_directory).iterdir(),
        key=lambda _path: (_path.is_file(), _path.name.lower()),
    )
    for path in paths:
        # Remove hidden files
        if path.name.startswith("."):
            continue
        if path.is_dir():
            style = "dim" if path.name.startswith("__") else ""
            branch = _tree.add(
                f"[bold magenta]:open_file_folder: [link file://{path}]{escape(path.name)}",
                style=style,
                guide_style=style,
            )
            walk_directory(path, branch)
        else:
            text_filename = Text(path.name, "green")
            text_filename.highlight_regex(r"\..*$", "bold red")
            text_filename.stylize(f"link file://{path}")
            file_size = path.stat().st_size
            text_filename.append(f" ({decimal(file_size)})", "blue")
            _tree.add(text_filename)


def application_directory(directory):
    tree = Tree(
        f":open_file_folder: [link file://{directory}]{directory}",
        guide_style="bold bright_blue",
    )
    walk_directory(pathlib.Path(directory), tree)
    console.print(tree)


def _check_console_input(_input: str) -> (bool, None):
    _input = _input.lower()
    if _input.startswith("y"):
        return True
    elif _input.startswith("n"):
        return False
    return None


def _rich_decorate(string, style):
    return f" [{style}]{string}[/{style}] "


def _rich_decorate_link(string, link):
    return f"[link={link}]{string}[/link]"


def _strict_name(data: str) -> bool:
    return all([char in available_char for char in data.lower()])


# def result_output(app_name, author, profile, github_addr, ASGISupport, WSGISupport):
#     layout = Layout()
#     layout.split_column(
#         Layout(name="app-info"),
#         Layout(Panel(profile), name="profile"),
#         Layout(Panel(github_addr), name="Github address"),
#         Layout(name="Support"),
#     )
#
#     layout["app-info"].split_row(
#         Layout(Panel(app_name), name="app-name"),
#         Layout(Panel(author), name="author"),
#     )
#
#     layout["Support"].split_row(
#         Layout(Panel(str(ASGISupport)), name="ASGISupport"),
#         Layout(Panel(str(WSGISupport)), name="WSGISupport"),
#     )
#
#     console.print(layout)


def console_check(content: str, default: (bool, None) = True) -> bool:
    """
    :param content: string content

    :param default: if the user input is null, the default value is used.
        [!]: Enable <strict mode> if <default> is None.
        strict mode: [Often used for important decisions]
            if the user input is not standard, waiting for the user input.

    :return: bool
    """
    _def = "[Y/n]" if default is None else "[{}/{}]".format(
        _rich_decorate("Y", "underline yellow b" if default else "gray"),
        _rich_decorate("n", "underline yellow b" if not default else "gray"),
    )
    _fmt = f"{content} {_def}> "
    if default is None:
        # strict mode
        while True:
            _res = _check_console_input(console.input(_fmt))
            if _res is not None:
                return bool(_res)
    else:
        _res = _check_console_input(console.input(_fmt))
        if _res is None:
            return bool(default)
        return bool(_res)


_console_char = _rich_decorate(' '.join(available_char), 'bold')
_console_not_required = _rich_decorate('not required', 'sky_blue1')


def console_content(content: str, strict: bool = False, required: bool = True) -> str:
    """

    :param content: string content
    :param strict: use all legal characters
    :param required: required field
    :return: str
    """
    _fmt = f"{content}> "
    if strict:
        while True:
            _dt = console.input(_fmt).strip()
            if _strict_name(_dt):
                if required and not _dt:
                    continue
                return _dt
            else:
                console.log(
                    f"{_rich_decorate('Please enter legal characters!', 'bold red')} ({_console_char})"
                )
    else:
        if required:
            while True:
                _dt = console.input(_fmt).strip()
                if _dt:
                    return _dt
        return console.input(_fmt).strip()


def console_multiline_content(content: str, required: bool = True) -> str:
    console.print(f"{content}: (wrap <{_rich_decorate('enter', 'bold')}> at the end)")
    content_list = []
    while True:
        _res = console.input(">>> ")
        if _res.strip(" "):
            content_list.append(_res)
        else:
            if not content_list and required:
                continue
            return "\n".join(content_list)


def console_list_input(title: str, elements: List[str], strict=False, required=True):
    console.print(f"{title}:")
    return {element: console_content(element, strict, required) for element in elements}


def repr_string(obj: str):
    return repr(obj) if isinstance(obj, str) else ""


def console_create_app():
    create_app(
        console_content(f"Please enter the{_rich_decorate('application name', 'yellow')}", strict=True),
        console_content(f"Please enter the your(author's){_rich_decorate('name', 'yellow')}"),
        console_multiline_content(
            f"Please enter the{_rich_decorate('application profile', 'yellow')}({_console_not_required})",
            required=False),
        console_list_input(
            f"{_rich_decorate('Repository Address(es)', 'yellow')}({_console_not_required})",
            [sup for sup in RepositoryAddress.support],
            required=False,
        ),
        console_content(f"Please enter the app {_rich_decorate('image-url', 'yellow')}", required=False),
        console_check(f"Whether to configure the url ({_rich_decorate('same as the application name', 'red')})",
                      default=True),
    )


def create_app(app_name, author, profile="", repo: dict = None, image="", UrlRoute=True):
    console.print("")
    console.rule("[bold blue]Create Application")
    console.print("")
    parent_dir = os.path.join(settings.BASE_APPLICATION_DIR, app_name)
    if os.path.isdir(parent_dir) and os.listdir(parent_dir):
        warns = 'Warning: Files already exist in the software directory. Continue execution may overwrite the ' \
                'original file. '
        if not console_check(
                f"{_rich_decorate(warns, 'bold red')}Continue or not?",
                default=False):
            return
    else:
        os.mkdir(parent_dir)

    # config
    json_writer(
        repo,
        app_name,
        author,
        profile,
        image,
        UrlRoute,
        path=parent_dir,
    )

    # migrations
    migrations_dir = os.path.join(parent_dir, "migrations")
    if not os.path.isdir(migrations_dir):
        os.mkdir(migrations_dir)
    with open(os.path.join(migrations_dir, "__init__.py"), "w", encoding="utf-8"):
        pass

    # manage startapp files
    with open(os.path.join(parent_dir, "__init__.py"), "w", encoding="utf-8"):
        pass

    with open(os.path.join(parent_dir, "admin.py"), "w", encoding="utf-8") as fp:
        fp.write("from django.contrib import admin\n\n# Register your models here.\n")

    with open(os.path.join(parent_dir, "apps.py"), "w", encoding="utf-8") as fp:
        fp.write(
            f"from django.apps import AppConfig\n\n\nclass SnakeConfig(AppConfig):\n    default_auto_field = "
            f"'django.db.models.BigAutoField'\n    name = 'applications.{app_name}'\n")

    with open(os.path.join(parent_dir, "models.py"), "w", encoding="utf-8") as fp:
        fp.write("from django.db import models\n\n# Create your models here.\n")

    with open(os.path.join(parent_dir, "tests.py"), "w", encoding="utf-8") as fp:
        fp.write("from django.test import TestCase\n\n# Create your tests here.\n")

    with open(os.path.join(parent_dir, "views.py"), "w", encoding="utf-8") as fp:
        fp.write("from django.shortcuts import render\n\n# Create your views here.\n")

    # application files
    with open(os.path.join(parent_dir, "application.py"), "w", encoding="utf-8") as fp:
        fp.write(f"""from applications.application import *
\n\n@appHandler.register\nclass Application(SyncApplication):\n    pass\n""")

    with open(os.path.join(parent_dir, "urls.py"), "w", encoding="utf-8") as fp:
        fp.write(f"""from django.conf.urls import url
from django.urls import path\n\nfrom applications.{app_name} import views\n\nurlpatterns = [\n    \n]\n""")
        application_directory(parent_dir)


if __name__ == "__main__":
    console_create_app()
    os.system("pause")
