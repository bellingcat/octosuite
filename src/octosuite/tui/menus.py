import sys
import typing as t

import questionary as q
from questionary import Style
from rich.status import Status

from .dialogs import Dialogs
from .prompts import Prompts
from ..core.models import User, Repo, Org, Search
from ..lib import check_updates, preview_response, export_response, set_menu_title
from ..lib import console, clear_screen, ascii_banner

CUSTOM_STYLE = Style(
    [
        ("highlighted", "fg:black bold bg:white"),
        ("instruction", "fg:gray"),
    ]
)

INSTRUCTIONS = "↑↓ [move] • ⮠ [select]"
EXPORT_INSTRUCTIONS = "↑↓ [move] • ⮠ [confirm] • spacebar [check]"
POINTER: str = "🖝 "

dialogs = Dialogs()
prompts = Prompts()

__all__ = ["Menus"]


class Menus:
    def __init__(self):
        # Define which methods require pagination
        self.paginated_methods = {
            "repos",
            "subscriptions",
            "starred",
            "followers",
            "following",
            "orgs",
            "gists",
            "events",
            "received_events",
            "forks",
            "issue_events",
            "assignees",
            "branches",
            "tags",
            "stargazers",
            "subscribers",
            "commits",
            "comments",
            "issues",
            "releases",
            "deployments",
            "labels",
            "hooks",
            "members",
        }

        # Methods that don't need pagination
        self.non_paginated_methods = {"profile", "languages"}

        # Search methods (all require pagination)
        self.search_methods = {"repos", "users", "commits", "issues", "topics"}

        self.mode_handlers = {
            "user": self.user,
            "repo": self.repo,
            "org": self.org,
            "search": self.search,
        }

    def _execute_selection(self, status: Status, **kwargs):
        """Execute a method on an instance, prompting for pagination if needed."""
        instance = kwargs.get("instance")
        method_name = kwargs.get("method_name")
        source = kwargs.get("source")

        method = getattr(instance, method_name)
        status.stop()
        # pagination params if needed
        params = (
            prompts.pagination_params() if method_name in self.paginated_methods else {}
        )
        status.start()
        status.update(f"[dim]Getting {method_name} from {source}...[/dim]")
        return method(**params)

    def _navigation(self, option: str, callback: t.Callable, *callback_args):
        """Handle navigation options (back, quit, change settings)."""
        navigation_handlers = {
            "back": lambda: self.main(),
            "quit": lambda: (
                sys.exit() if dialogs.quit() else callback(*callback_args)
            ),
        }

        handler = navigation_handlers.get(option)
        if handler:
            handler()
            return True
        return False

    def response_handling(self, data: t.Union[dict, list], data_type: str, source: str):
        """Export data to file in user-selected format(s)."""
        preview_response(data=data, source=source, _type=data_type)

        try:
            export_choice = q.select(
                "What would you like to do?",
                choices=[
                    q.Choice(
                        title="Export",
                        value="export",
                        description="Export the data",
                        shortcut_key="e",
                    ),
                    q.Choice(
                        title="Skip",
                        value="skip",
                        description="Do nothing, and go back to previous menu",
                        shortcut_key="x",
                    ),
                    q.Choice(
                        title="Quit",
                        value="quit",
                        description="Close this session",
                    ),
                ],
                pointer=POINTER,
                style=CUSTOM_STYLE,
                instruction=INSTRUCTIONS,
            ).ask()

            if export_choice == "skip":
                return

            if export_choice == "quit":
                if dialogs.quit():
                    sys.exit()
                else:
                    self.response_handling(
                        data=data, data_type=data_type, source=source
                    )
                    return

            file_formats = q.checkbox(
                "Select export format(s)",
                choices=[
                    q.Choice(
                        title="JSON",
                        value="json",
                        description="Export as JSON file",
                    ),
                    q.Choice(
                        title="CSV",
                        value="csv",
                        description="Export as CSV file",
                    ),
                    q.Choice(
                        title="HTML",
                        value="html",
                        description="Export as HTML table",
                    ),
                ],
                pointer=POINTER,
                style=CUSTOM_STYLE,
                instruction=EXPORT_INSTRUCTIONS,
                validate=lambda x: len(x) > 0 or "Please select at least one format",
            ).ask()

            export_response(
                data=data, data_type=data_type, source=source, file_formats=file_formats
            )

        except KeyboardInterrupt:
            print("\nExport cancelled")

    def main(self):
        """Main menu to select mode."""
        set_menu_title(menu_type="home")
        clear_screen()
        try:
            ascii_banner(text="octosuite")

            action = q.select(
                "What action would you like to perform?",
                choices=[
                    q.Choice(
                        title="User",
                        value="user",
                        description="data about a user",
                    ),
                    q.Choice(
                        title="Repo",
                        value="repo",
                        description="data about a repository",
                    ),
                    q.Choice(
                        title="Org",
                        value="org",
                        description="data about an organisation",
                    ),
                    q.Choice(
                        title="Search",
                        value="search",
                        description="Search GitHub",
                    ),
                    q.Choice(
                        title="Updates",
                        value="updates",
                        description="Check for updates",
                    ),
                    q.Choice(
                        title="License",
                        value="license",
                        description="Read license notice, and copyright information",
                    ),
                    q.Choice(
                        title="Quit",
                        value="quit",
                        description="Close this session",
                    ),
                ],
                pointer=POINTER,
                style=CUSTOM_STYLE,
                instruction=INSTRUCTIONS,
            ).ask()

            if action == "quit":
                if dialogs.quit():
                    sys.exit()
                else:
                    self.main()
            elif action == "license":
                dialogs.license()
                self.main()
            elif action == "updates":
                check_updates()
                self.main()
            elif action is None:
                sys.exit()
            else:
                handler = self.mode_handlers.get(action)
                if handler:
                    handler()
                else:
                    self.main()
        except KeyboardInterrupt:
            sys.exit()

    def search(self, query: t.Optional[str] = None):
        """Search menu for querying GitHub."""
        set_menu_title(menu_type="search")
        clear_screen()
        if query is None:
            ascii_banner(text="Search")
            query = prompts.prompt(
                message="Search Query",
                instruction="e.g., machine learning",
                style=CUSTOM_STYLE,
            )

        clear_screen()
        ascii_banner(text=query)

        option = q.select(
            "What would you like to do/search?",
            choices=[
                q.Choice(
                    title="Change Query",
                    value="change_query",
                    description="Search with a different query",
                    shortcut_key="c",
                ),
                q.Choice(
                    title="Repositories",
                    value="repos",
                    description="Search for repositories",
                ),
                q.Choice(
                    title="Users",
                    value="users",
                    description="Search for users",
                ),
                q.Choice(
                    title="Commits",
                    value="commits",
                    description="Search for commits",
                ),
                q.Choice(
                    title="Issues",
                    value="issues",
                    description="Search for issues and pull requests",
                ),
                q.Choice(
                    title="Topics",
                    value="topics",
                    description="Search for topics",
                ),
                q.Choice(
                    title="Go Back",
                    value="back",
                    description="Go back to ewous menu",
                    shortcut_key="b",
                ),
                q.Choice(
                    title="Quit",
                    value="quit",
                    description="Close this session",
                    shortcut_key="q",
                ),
            ],
            pointer=POINTER,
            style=CUSTOM_STYLE,
            instruction=INSTRUCTIONS,
            use_shortcuts=True,
        ).ask()

        if option is None:
            self.main()

        # Handle navigation
        if self._navigation(option, self.search, query):
            return

        # Handle change query
        if option == "change_query":
            self.search()
            return

        # Execute search if it's a valid method
        if option in self.search_methods:
            with console.status(
                status=f"[dim]Initialising {option} search...[/dim]"
            ) as status:
                # Get pagination params

                status.stop()
                params = prompts.pagination_params()
                status.start()

                # Create Search instance
                search = Search(
                    query=query,
                    page=params["page"],
                    per_page=params["per_page"],
                )

                method = getattr(search, option)
                status.update(f"[dim]Searching {option} for {query}...[/dim]")
                data = method()

                if data:
                    items = data.get("items")
                    status.stop()
                    self.response_handling(
                        data=items if items is not None else data,
                        data_type=option,
                        source=query,
                    )

        self.search(query=query)

    def user(self, username: t.Optional[str] = None):
        """User menu for querying user data."""
        set_menu_title(menu_type="user")
        clear_screen()
        if username is None:
            ascii_banner(text="User")
            username = prompts.prompt(
                message="GitHub Username",
                instruction="e.g., octocat",
                style=CUSTOM_STYLE,
                qmark="@",
            )

        clear_screen()
        ascii_banner(text=username)

        option = q.select(
            "What would you like to do/get?",
            choices=[
                q.Choice(
                    title="Change Username",
                    value="change_username",
                    description="Query a different user",
                    shortcut_key="u",
                ),
                q.Choice(
                    title="Profile",
                    value="profile",
                    description="Profile data",
                ),
                q.Choice(
                    title="Repositories",
                    value="repos",
                    description="Public repositories",
                ),
                q.Choice(
                    title="Subscriptions",
                    value="subscriptions",
                    description="Subscribed repositories",
                ),
                q.Choice(
                    title="Starred",
                    value="starred",
                    description="Starred repositories",
                ),
                q.Choice(
                    title="Followers",
                    value="followers",
                    description="Accounts that follow this user",
                ),
                q.Choice(
                    title="Following",
                    value="following",
                    description="Accounts that this user follows",
                ),
                q.Choice(
                    title="Organisations",
                    value="orgs",
                    description="This user's organisations",
                ),
                q.Choice(
                    title="Gists",
                    value="gists",
                    description="Gists (code snippets/files)",
                ),
                q.Choice(
                    title="Events",
                    value="events",
                    description="Events",
                ),
                q.Choice(
                    title="Received Events",
                    value="received_events",
                    description="This user's received events",
                ),
                q.Choice(
                    title="Go Back",
                    value="back",
                    description="Go back to previous menu",
                    shortcut_key="b",
                ),
                q.Choice(
                    title="Quit",
                    value="quit",
                    description="Close this session",
                    shortcut_key="q",
                ),
            ],
            pointer=POINTER,
            style=CUSTOM_STYLE,
            instruction=INSTRUCTIONS,
            use_shortcuts=True,
        ).ask()

        if option is None:
            self.main()
        # Handle navigation
        if self._navigation(option, self.user, username):
            return

        # Handle change username
        if option == "change_username":
            self.user()
            return

        # Execute action if it's a valid method
        valid_methods = self.paginated_methods | self.non_paginated_methods
        if option in valid_methods:
            with Status(
                status=f"[dim]Initialising user {option}...[/dim]",
                console=console,
            ) as status:
                user = User(name=username)

                status.update(f"[dim]Validating user's ({username}) existence...[/dim]")
                if user.exists():
                    console.print(
                        f"[bold][green]✔[/green] User ({username}) exists on GitHub[/bold]"
                    )
                    data = self._execute_selection(
                        source=username,
                        instance=user,
                        method_name=option,
                        status=status,
                    )

                    status.stop()
                    self.response_handling(data=data, data_type=option, source=username)
                else:
                    status.stop()
                    console.print(
                        f"[bold][yellow]✘[/yellow] User ({username}) doesn't exist on GitHub[/bold]"
                    )
                    console.input("  Press [bold]ENTER[/bold] to continue ...")
                    self.user()

        self.user(username=username)

    def repo(self, name: t.Optional[str] = None, owner: t.Optional[str] = None):
        """Repository menu for querying repo data."""
        set_menu_title(menu_type="repo")
        clear_screen()
        if name is None or owner is None:
            ascii_banner(text="Repo")
            if name is None:
                name = prompts.prompt(
                    message="GitHub Repo Name",
                    instruction="e.g., spoon-knife",
                    style=CUSTOM_STYLE,
                )
            if owner is None:
                owner = prompts.prompt(
                    message="GitHub Repo Owner",
                    instruction="e.g., octocat",
                    style=CUSTOM_STYLE,
                    qmark="@",
                )

        clear_screen()
        ascii_banner(text=f"{owner}/{name}")

        option = q.select(
            "What would you like to do/get?",
            choices=[
                q.Choice(
                    title="Change Repo Name",
                    value="change_repo_name",
                    description="Update the name of the repo",
                ),
                q.Choice(
                    title="Change Owner Name",
                    value="change_owner",
                    description="Update the name of repo owner",
                ),
                q.Choice(
                    title="Change Repo and Owner Names",
                    value="change_both",
                    description="Update both the repo and owner names",
                ),
                q.Choice(
                    title="Profile",
                    value="profile",
                    description="Repository data",
                ),
                q.Choice(
                    title="Forks",
                    value="forks",
                    description="Repository forks",
                ),
                q.Choice(
                    title="Issue Events",
                    value="issue_events",
                    description="Issue events",
                ),
                q.Choice(
                    title="Events",
                    value="events",
                    description="Repository events",
                ),
                q.Choice(
                    title="Assignees",
                    value="assignees",
                    description="Assignees",
                ),
                q.Choice(
                    title="Branches",
                    value="branches",
                    description="Branches",
                ),
                q.Choice(
                    title="Tags",
                    value="tags",
                    description="Tags",
                ),
                q.Choice(
                    title="Languages",
                    value="languages",
                    description="Programming languages",
                ),
                q.Choice(
                    title="Stargazers",
                    value="stargazers",
                    description="Users who starred this repo",
                ),
                q.Choice(
                    title="Subscribers",
                    value="subscribers",
                    description="Users subscribed to this repo",
                ),
                q.Choice(
                    title="Commits",
                    value="commits",
                    description="Commits",
                ),
                q.Choice(
                    title="Comments",
                    value="comments",
                    description="Comments",
                ),
                q.Choice(
                    title="Issues",
                    value="issues",
                    description="Issues",
                ),
                q.Choice(
                    title="Releases",
                    value="releases",
                    description="Releases",
                ),
                q.Choice(
                    title="Deployments",
                    value="deployments",
                    description="Deployments",
                ),
                q.Choice(
                    title="Labels",
                    value="labels",
                    description="Labels",
                ),
                q.Choice(
                    title="Go Back",
                    value="back",
                    description="Go back to previous menu",
                    shortcut_key="b",
                ),
                q.Choice(
                    title="Quit",
                    value="quit",
                    description="Close this session",
                    shortcut_key="q",
                ),
            ],
            pointer=POINTER,
            style=CUSTOM_STYLE,
            instruction=INSTRUCTIONS,
            use_shortcuts=True,
        ).ask()

        if option is None:
            self.main()

        # Handle navigation
        if self._navigation(option, self.repo, name, owner):
            return

        # Handle change options
        change_handlers = {
            "change_repo_name": lambda: self.repo(owner=owner),
            "change_owner": lambda: self.repo(name=name),
            "change_both": lambda: self.repo(),
        }

        if option in change_handlers:
            change_handlers[option]()
            return

        # Execute action if it's a valid method
        valid_methods = self.paginated_methods | self.non_paginated_methods
        if option in valid_methods:
            source = f"{owner}/{name}"
            with Status(
                status=f"[dim]Initialising repository {option}...[/dim]",
                console=console,
            ) as status:
                repo = Repo(name=name, owner=owner)

                status.update(
                    f"[dim]Validating repository's ({source}) existence...[/dim]"
                )
                if repo.exists():
                    console.print(
                        f"[bold][green]✔[/green] Repository ({source}) exists on GitHub[/bold]"
                    )
                    data = self._execute_selection(
                        source=source, instance=repo, method_name=option, status=status
                    )

                    status.stop()
                    self.response_handling(data=data, data_type=option, source=source)
                else:
                    status.stop()
                    console.print(
                        f"[bold][yellow]✘[/yellow] Repository ({source}) doesn't exist on GitHub[/bold]"
                    )
                    console.input("  Press [bold]ENTER[/bold] to continue ...")
                    self.repo()

        self.repo(name=name, owner=owner)

    def org(self, name: t.Optional[str] = None):
        """Organisation menu for querying org data."""
        set_menu_title(menu_type="org")
        clear_screen()
        if name is None:
            ascii_banner(text="Org")
            name = prompts.prompt(
                message="GitHub Organisation Name",
                instruction="e.g, github",
                style=CUSTOM_STYLE,
                qmark="@",
            )

        clear_screen()
        ascii_banner(text=name)

        option = q.select(
            "What would you like to do?",
            choices=[
                q.Choice(
                    title="Change Org Name",
                    value="change_org",
                    description="Query a different organisation",
                ),
                q.Choice(
                    title="Profile",
                    value="profile",
                    description="Profile data",
                ),
                q.Choice(
                    title="Repositories",
                    value="repos",
                    description="Public repositories",
                ),
                q.Choice(
                    title="Events",
                    value="events",
                    description="Organisation events",
                ),
                q.Choice(
                    title="Hooks",
                    value="hooks",
                    description="Webhooks",
                ),
                q.Choice(
                    title="Issues",
                    value="issues",
                    description="Issues",
                ),
                q.Choice(
                    title="Members",
                    value="members",
                    description="Organisation members",
                ),
                q.Choice(
                    title="Go Back",
                    value="back",
                    description="Go back to previous menu",
                    shortcut_key="b",
                ),
                q.Choice(
                    title="Quit",
                    value="quit",
                    description="Close this session",
                    shortcut_key="q",
                ),
            ],
            style=CUSTOM_STYLE,
            instruction=INSTRUCTIONS,
            use_shortcuts=True,
        ).ask()

        if option is None:
            self.main()

        # Handle navigation
        if self._navigation(option, self.org, name):
            return

        # Handle change org
        if option == "change_org":
            self.org()
            return

        # Execute action if it's a valid method
        valid_methods = self.paginated_methods | self.non_paginated_methods
        if option in valid_methods:
            with Status(
                status=f"[dim]Initialising organisation {option}...[/dim]",
                console=console,
            ) as status:
                org = Org(name=name)

                status.update(
                    f"[dim]Validating organisation's ({name}) existence...[/dim]"
                )
                if org.exists():
                    console.print(
                        f"[bold][green]✔[/green] Organisation ({name}) exists on GitHub[/bold]"
                    )
                    data = self._execute_selection(
                        source=name, instance=org, method_name=option, status=status
                    )

                    status.stop()
                    self.response_handling(data=data, data_type=option, source=name)
                else:
                    status.stop()
                    console.print(
                        f"[bold][yellow]✘[/yellow] Organisation ({name}) doesn't exist on GitHub[/bold]"
                    )

                    console.input("  Press [bold]ENTER[/bold] to continue ...")
                    self.org()

        self.org(name=name)
