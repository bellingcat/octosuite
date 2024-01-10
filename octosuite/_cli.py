# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

import argparse
import asyncio
import os
from datetime import datetime

import aiohttp
from rich.markdown import Markdown
from rich_argparse import RichHelpFormatter

from ._api import get_updates
from ._coreutils import console, dataframe, pathfinder
from .docs import (
    SEARCH_EXAMPLES,
    Version,
    USER_EXAMPLES,
    ORG_EXAMPLES,
    REPO_EXAMPLES,
    PROGRAM_DATA_DIRECTORY,
    DESCRIPTION,
    EPILOG,
)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


def create_parser() -> argparse.ArgumentParser:
    """
    Creates and configures an argument parser for the command line arguments.

    :return: A configured argparse.ArgumentParser object ready to parse the command line arguments.
    :rtype: argparse.ArgumentParser
    """
    # ---------------------------------------------------------------------------------- #

    main_parser = argparse.ArgumentParser(
        description=Markdown(DESCRIPTION, style="argparse.text"),
        epilog=Markdown(EPILOG, style="argparse.text"),
        formatter_class=RichHelpFormatter,
    )
    main_parser.add_argument(
        "-l", "--limit", help="output data limit", default=100, type=int
    )
    main_parser.add_argument(
        "-c",
        "--csv",
        metavar="FILENAME",
        help="write output to a csv file",
    )
    main_parser.add_argument(
        "-j",
        "--json",
        metavar="FILENAME",
        help="write output to a json file",
    )
    main_parser.add_argument(
        "-u",
        "--updates",
        help="check for updates on run",
        action="store_true",
    )
    main_parser.add_argument(
        "-v",
        "--version",
        version=f"OctoSuite CLI/Library {Version.full}",
        action="version",
    )
    subparsers = main_parser.add_subparsers(dest="entity", help="target entity")

    # ---------------------------------------------------------------------------------- #

    # User mode
    user_parser = subparsers.add_parser(
        "user",
        help="user operations",
        description=Markdown("# User Investigation"),
        epilog=Markdown(USER_EXAMPLES),
        formatter_class=RichHelpFormatter,
    )
    user_parser.add_argument("username", help="username to query")
    user_parser.add_argument(
        "-p", "--profile", help="get a user's profile.", action="store_true"
    )
    user_parser.add_argument(
        "-r",
        "--repos",
        help="get user's public repositories",
        action="store_true",
    )
    user_parser.add_argument(
        "-e",
        "--emails",
        help="get emails from user's public PushEvents",
        action="store_true",
    )
    user_parser.add_argument(
        "-o",
        "--orgs",
        help="get user's public organisations (owned/belonging to)",
        action="store_true",
    )
    user_parser.add_argument(
        "-ee",
        "--events",
        help="get user's public events",
        action="store_true",
    )
    user_parser.add_argument(
        "-g",
        "--gists",
        help="get user's public gists",
        action="store_true",
    )
    user_parser.add_argument(
        "-s",
        "--starred",
        help="get user's starred repositories",
        action="store_true",
    )
    user_parser.add_argument(
        "-f",
        "--followers",
        help="get user's followers",
        action="store_true",
    )
    user_parser.add_argument(
        "-ff",
        "--following",
        help="get accounts followed by user",
        action="store_true",
    )
    user_parser.add_argument(
        "-fff",
        "--follows",
        help="check if target follows the second specified user",
        type=str,
    )

    # ---------------------------------------------------------------------------------- #

    # Org mode
    org_parser = subparsers.add_parser(
        "org",
        help="organisation operations",
        description=Markdown("# Organisation Investigation"),
        epilog=Markdown(ORG_EXAMPLES),
        formatter_class=RichHelpFormatter,
    )
    org_parser.add_argument("organisation", help="organisation to query")

    org_parser.add_argument(
        "-p",
        "--profile",
        help="get an organisation's profile",
        action="store_true",
    )
    org_parser.add_argument(
        "-r",
        "--repos",
        help="get an organisation's public repositories",
        action="store_true",
    )
    org_parser.add_argument(
        "-e",
        "--events",
        help="get an organisation's events",
        action="store_true",
    )
    org_parser.add_argument(
        "-m",
        "--is-member",
        dest="is_member",
        help="check if the specified user is a public member of the target organisation",
        type=str,
    )
    org_parser.add_argument(
        "-mm",
        "--members",
        help="get an organisation's public members",
        action="store_true",
    )

    # ---------------------------------------------------------------------------------- #

    # Repo mode
    repo_parser = subparsers.add_parser(
        "repo",
        help="repository operations",
        description=Markdown("# Repository Investigation"),
        epilog=Markdown(REPO_EXAMPLES),
        formatter_class=RichHelpFormatter,
    )
    repo_parser.add_argument("repo_name", help="repository name to query")
    repo_parser.add_argument("repo_owner", help="repository owner username")
    repo_parser.add_argument(
        "-p",
        "--profile",
        help="get a repository's data (similar to profile data)",
        action="store_true",
    )
    repo_parser.add_argument(
        "-c",
        "--contributors",
        help="get a repository's contributors",
        action="store_true",
    )
    repo_parser.add_argument(
        "-cc",
        "--contents",
        nargs="?",
        const="/",
        help="get a repository's files from a specified path (const: %(const)s)",
    )
    repo_parser.add_argument(
        "-s", "--stargazers", help="get a repository's stargazers", action="store_true"
    )
    repo_parser.add_argument(
        "-f", "--forks", help="get a repository's forks", action="store_true"
    )
    repo_parser.add_argument(
        "-i", "--issues", help="get a repository's open issues", action="store_true"
    )
    repo_parser.add_argument(
        "-r", "--releases", help="get a repository's releases", action="store_true"
    )

    # ---------------------------------------------------------------------------------- #

    # Search mode
    search_parser = subparsers.add_parser(
        "search",
        help="search operations",
        description=Markdown("# Entity/Target Discovery"),
        epilog=Markdown(SEARCH_EXAMPLES),
        formatter_class=RichHelpFormatter,
    )

    search_parser.add_argument("query", help="search query")
    search_parser.add_argument(
        "-u", "--users", help="search users", action="store_true"
    )
    search_parser.add_argument(
        "-i", "--issues", help="search issues", action="store_true"
    )
    search_parser.add_argument(
        "-t", "--topics", help="search topics", action="store_true"
    )
    search_parser.add_argument(
        "-c", "--commits", help="search commits", action="store_true"
    )
    return main_parser


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


async def stage(args: argparse.Namespace):
    # ---------------------------------------------------------------------------------- #

    from .base import OctoUser, OctoOrg, OctoRepo

    # ---------------------------------------------------------------------------------- #

    limit: int = args.limit

    user = OctoUser(username=args.username if hasattr(args, "username") else None)
    org = OctoOrg(
        organisation=args.organisation if hasattr(args, "organisation") else None
    )

    repo = OctoRepo(
        repo_name=args.repo_name if hasattr(args, "repo_name") else None,
        repo_owner=args.repo_owner if hasattr(args, "repo_owner") else None,
    )

    # ---------------------------------------------------------------------------------- #

    func_mapping: dict = {
        "user": [
            ("orgs", lambda session: user.orgs(limit=limit, session=session)),
            ("events", lambda session: user.events(limit=limit, session=session)),
            ("emails", lambda session: user.emails(session=session)),
            ("profile", lambda session: user.profile(session=session)),
            ("repos", lambda session: user.repos(limit=limit, session=session)),
            ("starred", lambda session: user.starred(limit=limit, session=session)),
            (
                "follows",
                lambda session: user.follows(
                    user=args.follows if hasattr(args, "follows") else None,
                    session=session,
                ),
            ),
            ("followers", lambda session: user.followers(limit=limit, session=session)),
            ("following", lambda session: user.following(limit=limit, session=session)),
        ],
        "repo": [
            (
                "contributors",
                lambda session: repo.contributors(limit=limit, session=session),
            ),
            (
                "contents",
                lambda session: repo.contents(
                    path=args.contents if hasattr(args, "contents") else None,
                    session=session,
                ),
            ),
            ("forks", lambda session: repo.forks(limit=limit, session=session)),
            ("profile", lambda session: repo.profile(session=session)),
            (
                "stargazers",
                lambda session: repo.stargazers(limit=limit, session=session),
            ),
        ],
        "org": [
            ("profile", lambda session: org.profile(session=session)),
            ("repos", lambda session: org.repos(limit=limit, session=session)),
            (
                "is_member",
                lambda session: org.is_member(
                    user=args.is_member if hasattr(args, "is_member") else None,
                    session=session,
                ),
            ),
            ("members", lambda session: org.members(limit=limit, session=session)),
        ],
    }

    # ---------------------------------------------------------------------------------- #

    if args.entity in func_mapping:
        async with aiohttp.ClientSession() as request_session:
            if args.updates:
                await get_updates(session=request_session)

            mode_action = func_mapping.get(args.entity)
            is_executed: bool = False

            for action, function in mode_action:
                if getattr(args, action, False):
                    function_data = await function(session=request_session)

                    if function_data:
                        # -------------------------------------------------------------- #

                        file_dir = None
                        if args.csv or args.json:
                            file_dir = os.path.join(
                                PROGRAM_DATA_DIRECTORY, args.entity, action
                            )
                            pathfinder(
                                directories=[
                                    os.path.join(file_dir, "csv"),
                                    os.path.join(file_dir, "json"),
                                ]
                            )

                        # -------------------------------------------------------------- #

                        dataframe(
                            data=function_data,
                            save_csv=args.csv,
                            save_json=args.json,
                            to_dir=file_dir,
                        )

                        # -------------------------------------------------------------- #
                    is_executed = True

            if not is_executed:
                console.log(
                    f"octosuite {args.entity}: missing one or more expected argument(s)."
                )


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


def run():
    parser = create_parser()
    args = parser.parse_args()

    start_time = datetime.now()
    print(
        """
┏┓    ┏┓  •   
┃┃┏╋┏┓┗┓┓┏┓╋┏┓
┗┛┗┗┗┛┗┛┗┻┗┗┗ """
    )
    if args.entity:
        console.log(
            f"[bold]OctoSuite CLI[/] {Version.full} started at {start_time.strftime('%a %b %d %Y, %I:%M:%S%p')}..."
        )
        try:
            asyncio.run(stage(args=args))
        except KeyboardInterrupt:
            console.log("User interruption detected (Ctrl+C)")
        finally:
            console.log(f"Stopped in {datetime.now() - start_time} seconds.")
    else:
        parser.print_usage()


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
