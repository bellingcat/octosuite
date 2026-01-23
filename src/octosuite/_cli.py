"""
Command-line interface for octosuite.

Provides non-interactive access to GitHub data.
"""

import argparse
import json
import sys
import typing as t

from rich.status import Status

from . import __pkg__, __version__
from ._lib import export_response, preview_response, console
from .core.models import User, Org, Repo, Search


def create_parser() -> argparse.ArgumentParser:
    """
    Create the argument parser.

    :return: Configured ArgumentParser.
    """

    parser = argparse.ArgumentParser(
        prog=__pkg__,
        description="Terminal-based toolkit for GitHub data analysis - for Bellingcat",
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}, MIT Licence © Bellingcat",
    )
    parser.add_argument(
        "-i", "--interactive", action="store_true", help="launch interactive TUI"
    )
    parser.add_argument(
        "-p", "--page", type=int, default=1, help="page number (default: %(default)s)"
    )
    parser.add_argument(
        "-N",
        "--per-page",
        type=int,
        default=100,
        help="maximum number of results per page (default: %(default)s)",
    )
    parser.add_argument("-j", "--json", action="store_true", help="output as JSON")
    parser.add_argument("-d", "--dir", metavar="DIR", help="export to directory")

    subparsers = parser.add_subparsers(dest="command")

    # User command
    user_parser = subparsers.add_parser("user", help="get user data")
    user_parser.add_argument("username", help="GitHub username")
    user_group = user_parser.add_mutually_exclusive_group()
    user_group.add_argument(
        "--profile",
        action="store_const",
        const="profile",
        dest="data_type",
        help="profile data (default)",
    )
    user_group.add_argument(
        "--repos",
        action="store_const",
        const="repos",
        dest="data_type",
        help="repositories",
    )
    user_group.add_argument(
        "--subscriptions",
        action="store_const",
        const="subscriptions",
        dest="data_type",
        help="subscriptions",
    )
    user_group.add_argument(
        "--starred",
        action="store_const",
        const="starred",
        dest="data_type",
        help="starred repos",
    )
    user_group.add_argument(
        "--followers",
        action="store_const",
        const="followers",
        dest="data_type",
        help="followers",
    )
    user_group.add_argument(
        "--following",
        action="store_const",
        const="following",
        dest="data_type",
        help="following",
    )
    user_group.add_argument(
        "--orgs",
        action="store_const",
        const="orgs",
        dest="data_type",
        help="organisations",
    )
    user_group.add_argument(
        "--gists", action="store_const", const="gists", dest="data_type", help="gists"
    )
    user_group.add_argument(
        "--events",
        action="store_const",
        const="events",
        dest="data_type",
        help="events",
    )
    user_group.add_argument(
        "--received-events",
        action="store_const",
        const="received_events",
        dest="data_type",
        help="received events",
    )
    user_parser.set_defaults(data_type="profile")

    # Repo command
    repo_parser = subparsers.add_parser("repo", help="get repository data")
    repo_parser.add_argument("repository", help="repository (owner/name)")
    repo_group = repo_parser.add_mutually_exclusive_group()
    repo_group.add_argument(
        "--profile",
        action="store_const",
        const="profile",
        dest="data_type",
        help="repo data (default)",
    )
    repo_group.add_argument(
        "--forks", action="store_const", const="forks", dest="data_type", help="forks"
    )
    repo_group.add_argument(
        "--issue-events",
        action="store_const",
        const="issue_events",
        dest="data_type",
        help="issue events",
    )
    repo_group.add_argument(
        "--events",
        action="store_const",
        const="events",
        dest="data_type",
        help="events",
    )
    repo_group.add_argument(
        "--assignees",
        action="store_const",
        const="assignees",
        dest="data_type",
        help="assignees",
    )
    repo_group.add_argument(
        "--branches",
        action="store_const",
        const="branches",
        dest="data_type",
        help="branches",
    )
    repo_group.add_argument(
        "--tags", action="store_const", const="tags", dest="data_type", help="tags"
    )
    repo_group.add_argument(
        "--languages",
        action="store_const",
        const="languages",
        dest="data_type",
        help="languages",
    )
    repo_group.add_argument(
        "--stargazers",
        action="store_const",
        const="stargazers",
        dest="data_type",
        help="stargazers",
    )
    repo_group.add_argument(
        "--subscribers",
        action="store_const",
        const="subscribers",
        dest="data_type",
        help="subscribers",
    )
    repo_group.add_argument(
        "--commits",
        action="store_const",
        const="commits",
        dest="data_type",
        help="commits",
    )
    repo_group.add_argument(
        "--comments",
        action="store_const",
        const="comments",
        dest="data_type",
        help="comments",
    )
    repo_group.add_argument(
        "--issues",
        action="store_const",
        const="issues",
        dest="data_type",
        help="issues",
    )
    repo_group.add_argument(
        "--releases",
        action="store_const",
        const="releases",
        dest="data_type",
        help="releases",
    )
    repo_group.add_argument(
        "--deployments",
        action="store_const",
        const="deployments",
        dest="data_type",
        help="deployments",
    )
    repo_group.add_argument(
        "--labels",
        action="store_const",
        const="labels",
        dest="data_type",
        help="labels",
    )
    repo_parser.set_defaults(data_type="profile")

    # Org command
    org_parser = subparsers.add_parser("org", help="get organisation data")
    org_parser.add_argument("name", help="organisation name")
    org_group = org_parser.add_mutually_exclusive_group()
    org_group.add_argument(
        "--profile",
        action="store_const",
        const="profile",
        dest="data_type",
        help="profile data (default)",
    )
    org_group.add_argument(
        "--repos",
        action="store_const",
        const="repos",
        dest="data_type",
        help="repositories",
    )
    org_group.add_argument(
        "--events",
        action="store_const",
        const="events",
        dest="data_type",
        help="events",
    )
    org_group.add_argument(
        "--hooks",
        action="store_const",
        const="hooks",
        dest="data_type",
        help="webhooks",
    )
    org_group.add_argument(
        "--issues",
        action="store_const",
        const="issues",
        dest="data_type",
        help="issues",
    )
    org_group.add_argument(
        "--members",
        action="store_const",
        const="members",
        dest="data_type",
        help="members",
    )
    org_parser.set_defaults(data_type="profile")

    # Search command
    search_parser = subparsers.add_parser("search", help="search GitHub")
    search_parser.add_argument("query", help="search query")
    search_group = search_parser.add_mutually_exclusive_group()
    search_group.add_argument(
        "--repos",
        action="store_const",
        const="repos",
        dest="search_type",
        help="search repositories (default)",
    )
    search_group.add_argument(
        "--users",
        action="store_const",
        const="users",
        dest="search_type",
        help="search users",
    )
    search_group.add_argument(
        "--commits",
        action="store_const",
        const="commits",
        dest="search_type",
        help="search commits",
    )
    search_group.add_argument(
        "--issues",
        action="store_const",
        const="issues",
        dest="search_type",
        help="search issues",
    )
    search_group.add_argument(
        "--topics",
        action="store_const",
        const="topics",
        dest="search_type",
        help="search topics",
    )
    search_parser.set_defaults(search_type="repos")

    return parser


def output(
    data: t.Union[dict, list],
    as_json: bool,
    source: str,
    data_type: str,
    export_dir: t.Optional[str] = None,
):
    """
    Output data in the appropriate format.

    :param data: Data to output.
    :param as_json: Output as JSON.
    :param source: Source identifier.
    :param data_type: Type of data.
    :param export_dir: Export directory.
    """

    if not data:
        console.print(f"[yellow]No {data_type} data found for '{source}'[/yellow]")
        return

    if export_dir:
        export_response(
            data=data,
            data_type=data_type,
            source=source,
            file_formats=["json"],
            output_dir=export_dir,
        )
    elif as_json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        preview_response(data=data, source=source, _type=data_type)


def run():
    """Run the CLI."""

    parser = create_parser()
    args = parser.parse_args()

    if args.interactive:
        from .tui import run as run_tui

        run_tui()
        return

    if not args.command:
        parser.print_help()
        return

    try:
        if args.command == "user":
            user = User(name=args.username)

            with Status(
                f"[dim]Validating user ({args.username})[/dim]…", console=console
            ):
                exists, _ = user.exists()

            if not exists:
                console.print(f"[red]User '{args.username}' not found[/red]")
                sys.exit(1)

            method = getattr(user, args.data_type)
            with Status(
                f"[dim]Getting {args.data_type} from {args.username}[/dim]…",
                console=console,
            ):
                data = (
                    method()
                    if args.data_type == "profile"
                    else method(page=args.page, per_page=min(args.per_page, 100))
                )
            output(
                data=data,
                as_json=args.json,
                source=args.username,
                data_type=args.data_type,
                export_dir=args.dir,
            )

        elif args.command == "repo":
            if "/" not in args.repository:
                console.print("[red]Repository must be in 'owner/name' format[/red]")
                sys.exit(1)

            owner, name = args.repository.split("/", 1)
            repo = Repo(name=name, owner=owner)

            with Status(
                f"[dim]Validating repo ({args.repository})[/dim]…", console=console
            ):
                exists, _ = repo.exists()

            if not exists:
                console.print(f"[red]Repository '{args.repository}' not found[/red]")
                sys.exit(1)

            method = getattr(repo, args.data_type)
            with Status(
                f"[dim]Getting {args.data_type} from {args.repository}[/dim]…",
                console=console,
            ):
                data = (
                    method()
                    if args.data_type in ("profile", "languages")
                    else method(page=args.page, per_page=min(args.per_page, 100))
                )
            output(
                data=data,
                as_json=args.json,
                source=args.repository,
                data_type=args.data_type,
                export_dir=args.dir,
            )

        elif args.command == "org":
            org = Org(name=args.name)

            with Status(f"[dim]Validating org ({args.name})[/dim]…", console=console):
                exists, _ = org.exists()

            if not exists:
                console.print(f"[red]Organisation '{args.name}' not found[/red]")
                sys.exit(1)

            method = getattr(org, args.data_type)
            with Status(
                f"[dim]Getting {args.data_type} from {args.name}[/dim]…",
                console=console,
            ):
                data = (
                    method()
                    if args.data_type == "profile"
                    else method(page=args.page, per_page=min(args.per_page, 100))
                )
            output(
                data=data,
                as_json=args.json,
                source=args.name,
                data_type=args.data_type,
                export_dir=args.dir,
            )

        elif args.command == "search":
            search = Search(
                query=args.query,
                page=args.page,
                per_page=min(args.per_page, 100),
            )
            method = getattr(search, args.search_type)
            with Status(
                f"[dim]Searching {args.search_type} for '{args.query}'[/dim]…",
                console=console,
            ):
                result = method()
            data = result.get("items", result) if isinstance(result, dict) else result
            output(
                data=data,
                as_json=args.json,
                source=args.query,
                data_type=args.search_type,
                export_dir=args.dir,
            )

    except KeyboardInterrupt:
        console.print("\n[dim]Cancelled[/dim]")
        sys.exit(130)
