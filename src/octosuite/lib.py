import csv
import json
import os
import subprocess
import typing as t
from datetime import datetime
from pathlib import Path

import pyfiglet
from prompt_toolkit.shortcuts import message_dialog
from rich.console import Console
from rich.text import Text
from rich.tree import Tree
from update_checker import UpdateChecker

from . import __pkg__, __version__

__all__ = [
    "__pkg__",
    "__version__",
    "console",
    "preview_response",
    "export_response",
    "check_updates",
    "clear_screen",
    "ascii_banner",
    "set_menu_title",
]

console = Console(log_time=False)


def preview_response(data: t.Union[dict, list], source: str, _type: str):
    """
    Display a preview of response data in a tree structure.

    :param data: The data to preview (dict or list).
    :param source: The source identifier of the data.
    :param _type: The type of data being previewed.
    """

    if isinstance(data, dict):
        tree = Tree(
            label=f"\n[bold]{data.get('name') or data.get('login') or data.get('id') or 'Data'}[/bold]",
            guide_style="#444444",
            highlight=True,
        )
        fill_tree(tree=tree, data=data)
        console.print(tree)
        print()

    elif isinstance(data, list):
        preview_data = data[:5]
        tree = Tree(
            label=f"\n[bold]First {len(preview_data)} of {len(data)} {_type} for '{source}'[/bold]",
            guide_style="#444444",
            highlight=True,
        )

        for item in preview_data:
            if isinstance(item, dict):
                branch_label = (
                    item.get("full_name")
                    or item.get("name")
                    or item.get("login")
                    or item.get("type")
                    or item.get("id")
                    or "Item"
                )
                branch = tree.add(label=f"[bold]{branch_label}[/bold]", highlight=True)
                fill_tree(tree=branch, data=item)

        console.print(tree)
        print()
    else:
        console.print(data)


def export_response(
    data: t.Union[dict, list],
    data_type: str,
    source: str,
    file_formats: list,
    output_dir: str = "../exports",
):
    """
    Export response data to one or more file formats.

    :param data: The data to export (dict or list).
    :param data_type: The type of data being exported.
    :param source: The source identifier of the data.
    :param file_formats: List of file formats to export to (json, csv, html).
    :param output_dir: Directory path where exported files will be saved.
    :return: List of exported file paths.
    """

    # Create output directory if it doesn't exist
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_source = source.replace("/", "_")
    filename = f"{safe_source}_{data_type}_{timestamp}"

    # Normalize data to list of dicts
    if isinstance(data, dict):
        data_list = [data]
    else:
        data_list = data

    # Export to all selected formats
    exported_files = []
    for file_format in file_formats:
        filepath = output_dir / f"{filename}.{file_format}"

        if file_format == "json":
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data_list, f, indent=2, ensure_ascii=False)

        elif file_format == "csv":
            if data_list:
                # Get all unique keys from all dicts
                keys = set()
                for item in data_list:
                    if isinstance(item, dict):
                        keys.update(item.keys())
                keys = sorted(keys)

                with open(filepath, "w", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=keys)
                    writer.writeheader()
                    for item in data_list:
                        if isinstance(item, dict):
                            writer.writerow(item)

        elif file_format == "html":
            with open(filepath, "w", encoding="utf-8") as file:
                file.write("<!DOCTYPE html>\n<html>\n<head>\n")
                file.write('<meta charset="UTF-8">\n')
                file.write("<style>table { border-collapse: collapse; width: 100%; }\n")
                file.write(
                    "th, td { border: 1px solid black; padding: 8px; text-align: left; }\n"
                )
                file.write("th { background-color: #f2f2f2; }</style>\n")
                file.write("</head>\n<body>\n")
                file.write('<table class="table table-striped" border="1">\n')

                if data_list:
                    # Get all unique keys
                    keys = set()
                    for item in data_list:
                        if isinstance(item, dict):
                            keys.update(item.keys())
                    keys = sorted(keys)

                    # Write header
                    file.write("<thead>\n<tr>\n")
                    for key in keys:
                        file.write(f"<th>{key}</th>\n")
                    file.write("</tr>\n</thead>\n")

                    # Write rows
                    file.write("<tbody>\n")
                    for item in data_list:
                        if isinstance(item, dict):
                            file.write("<tr>\n")
                            for key in keys:
                                value = item.get(key, "")
                                file.write(f"<td>{value}</td>\n")
                            file.write("</tr>\n")
                    file.write("</tbody>\n")

                file.write("</table>\n</body>\n</html>")

        exported_files.append(str(filepath))

    # Show success message
    console.print("\n[green]✓ Export successful![/green]")
    for filepath in exported_files:
        console.print(f"  • {filepath}")

    return exported_files


def fill_tree(tree: Tree, data: t.Union[dict, list]) -> Tree:
    """
    Recursively populate a Rich Tree with data.

    :param tree: The Tree object to populate.
    :param data: The data to add to the tree (dict or list).
    :return: The populated Tree object.
    """

    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict) or isinstance(value, list):
                branch = tree.add(f"{key}")
                fill_tree(tree=branch, data=value)
            else:
                tree.add(f"[dim]{key.replace('_', ' ').title()}[/dim]: {value}")

    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict) or isinstance(item, list):
                fill_tree(tree=tree, data=item)
            else:
                tree.add(str(item))

    else:
        tree.add(str(data))

    return tree


def check_updates():
    """Check for available package updates and display the result."""

    with console.status("[dim]Checking for updates[/dim]…") as status:
        checker = UpdateChecker()
        result = checker.check(__pkg__, __version__)
        if result is not None:
            status.stop()
            message_dialog(title="Update Available", text=str(result)).run()
        else:
            status.stop()
            message_dialog(
                title="Up to Date",
                text=f"You're running the current version, {__version__}",
            ).run()


def clear_screen():
    """Clear the terminal screen."""
    subprocess.run(["cls" if os.name == "nt" else "clear"])


def ascii_banner(text: str):
    """Display a colourful ASCII art banner with gradient styling.

    :param text: The text to convert to ASCII art.
    """
    clear_screen()

    ascii_text = pyfiglet.figlet_format(text=text, font="chunky")
    banner_text = Text(ascii_text)

    length = len(ascii_text)
    for i in range(length):
        ratio = i / max(length - 1, 1)
        r = int(255 - 127 * ratio)
        g = int(200 - 200 * ratio)
        b = 255

        banner_text.stylize(f"rgb({r},{g},{b})", i, i + 1)
    console.print(banner_text)


def set_menu_title(menu_type: t.Literal["home", "user", "org", "repo", "search"]):
    """
    Set the terminal window title based on the current menu.

    :param menu_type: The type of menu being displayed.
    """

    title: str = __pkg__.title()
    title += f" | {menu_type.title()}"
    console.set_window_title(title=title)
