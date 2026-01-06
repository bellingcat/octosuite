import sys
import typing as t

import questionary as q
from questionary import Style
from rich.status import Status

from .dialogs import Dialogs
from .prompts import Prompts
from ..core.cache import cache
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

dialogs = Dialogs()
prompts = Prompts()

__all__ = ["Menus"]


class BaseMenu:
    """Base class providing common menu functionality and response handling for GitHub data queries."""

    def __init__(self, main_menu: t.Callable):
        """
        Initialise the BaseMenu with pagination and search method configurations.

        :param main_menu: Callable reference to the main menu function.
        """

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

        self.main_menu = main_menu

    @staticmethod
    def target_validator(
        identifier: str,
        instance: t.Union[User, Repo, Org],
        callback: t.Callable,
        *callback_args,
    ) -> bool:
        """
        Validate whether a GitHub entity exists.

        :param identifier: Name or identifier of the entity to validate.
        :param instance: The instance with an exists() method (User, Repo, or Org).
        :param callback: Function to call if validation fails.
        :param callback_args: Arguments to pass to the callback function.
        :return: True if the entity exists, False otherwise.
        """

        if isinstance(instance, User):
            target_type = "user"
        elif isinstance(instance, Repo):
            target_type = "repo"
        else:
            target_type = "org"

        with Status(
            f"[dim]Validating {target_type} ({identifier})[/dim]…",
            console=console,
        ) as status:
            exists, response = instance.exists()

            if not exists:
                status.stop()
                if response and "message" in response:
                    console.print(
                        f"[bold][yellow]✘[/yellow] {response['message']}[/bold]"
                    )
                console.input("  Press [bold]ENTER[/bold] to continue …")
                callback(*callback_args)
                return False

            return True

    def execute_and_handle_response(
        self,
        instance: t.Union[User, Repo, Org, Search],
        method_name: str,
        target_type: t.Literal["user", "repo", "org"],
        source: str,
    ):
        """
        Execute a method on an instance and handle the resulting data.

        :param instance: The instance to execute the method on.
        :param method_name: Name of the method to execute.
        :param target_type: Type of entity ("user", "repo", or "org").
        :param source: Source identifier for response handling.
        """

        valid_methods = self.paginated_methods | self.non_paginated_methods
        if method_name in valid_methods:
            with Status(
                status=f"[dim]Initialising {target_type} {method_name}[/dim]…",
                console=console,
            ) as status:
                data = self.execute_selection(
                    source=source,
                    instance=instance,
                    method_name=method_name,
                    status=status,
                )

                status.stop()
                self.response_handler(data=data, data_type=method_name, source=source)

    def execute_selection(self, status: Status, **kwargs):
        """
        Execute a method on an instance with pagination if required.

        :param status: Rich Status object for displaying progress.
        :param kwargs: Must include 'instance', 'method_name', and 'source'.
        :return: The data returned by the executed method.
        """

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
        status.update(f"[dim]Getting {method_name} from {source}[/dim]…")
        return method(**params)

    def response_handler(self, data: t.Union[dict, list], data_type: str, source: str):
        """
        Handle retrieved data by previewing and offering export options.

        :param data: The data to handle (dict or list).
        :param data_type: Type of data retrieved.
        :param source: Source identifier of the data.
        """

        try:
            if not data:
                console.print(
                    f"[bold][yellow]✘[/yellow] No data found for '{source}'[/bold]"
                )
            else:
                preview_response(data=data, source=source, _type=data_type)
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
                    style=CUSTOM_STYLE,
                    instruction=INSTRUCTIONS,
                ).ask()

                if export_choice == "skip":
                    return

                if export_choice == "quit":
                    if dialogs.quit():
                        sys.exit()
                    else:
                        clear_screen()
                        self.response_handler(
                            data=data,
                            data_type=data_type,
                            source=source,
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
                    style=CUSTOM_STYLE,
                    instruction=EXPORT_INSTRUCTIONS,
                    validate=lambda x: len(x) > 0
                    or "Please select at least one format",
                ).ask()

                export_response(
                    data=data,
                    data_type=data_type,
                    source=source,
                    file_formats=file_formats,
                )

            console.input("  Press [bold]ENTER[/bold] to continue …")
        except KeyboardInterrupt:
            console.print("\nExport cancelled")

    def navigation_handler(self, option: str, callback: t.Callable, *callback_args):
        """
        Handle common navigation options across menus.

        :param option: The selected navigation option.
        :param callback: Function to call for certain navigation actions.
        :param callback_args: Arguments to pass to the callback function.
        :return: True if navigation was handled, False otherwise.
        """

        navigation_handlers = {
            "back": lambda: self.main_menu(),
            "quit": lambda: (
                sys.exit() if dialogs.quit() else callback(*callback_args)
            ),
        }

        handler = navigation_handlers.get(option)
        if handler:
            handler()
            return True
        return False


class Menus(BaseMenu):
    """Main menu system providing interactive interfaces for GitHub data queries."""

    def __init__(self):
        """Initialise the Menus class with mode handlers for different query types."""

        super().__init__(main_menu=self.main)

        self.mode_handlers = {
            "user": self.user,
            "repo": self.repo,
            "org": self.org,
            "search": self.search,
        }

    def main(self):
        """Display the main menu for selecting query mode."""

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
                        title="Clear cache",
                        value="clear_cache",
                        description="Clear all in-memory cache from Octosuite",
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
            elif action == "clear_cache":
                if dialogs.clear_cache():
                    cache.clear()
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
        """
        Display the search menu for querying GitHub content.

        :param query: Optional search query string. If None, prompts user for input.
        """

        set_menu_title(menu_type="search")
        clear_screen()
        if query is None:
            ascii_banner(text="Search")
            query = prompts.prompt(
                message="Search Query",
                instruction="e.g., machine learning",
                style=CUSTOM_STYLE,
            )

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
            return

        # Handle navigation
        if self.navigation_handler(option, self.search, query):
            return

        # Handle change query
        if option == "change_query":
            self.search()
            return

        # Execute search if it's a valid method
        if option in self.search_methods:
            with Status(
                status=f"[dim]Initialising {option} search[/dim]…", console=console
            ) as status:
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
                status.update(f"[dim]Searching {option} for {query}[/dim]…")
                data = method()

                if data:
                    items = data.get("items")
                    status.stop()
                    self.response_handler(
                        data=items if items is not None else data,
                        data_type=option,
                        source=query,
                    )

        # After handling response, show menu again
        self.search(query=query)

    def user(self, username: t.Optional[str] = None, is_validated: bool = False):
        """
        Display the user menu for querying GitHub user data.

        :param username: Optional GitHub username. If None, prompts user for input.
        :param is_validated: Whether the username has already been validated.
        """

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

        user = User(name=username)

        if not self.target_validator(
            identifier=username,
            instance=user,
            callback=self.user,
        ):
            return

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
            style=CUSTOM_STYLE,
            instruction=INSTRUCTIONS,
            use_shortcuts=True,
        ).ask()

        if option is None:
            self.main()
            return

        # Handle navigation
        elif self.navigation_handler(option, self.user, username):
            return

        # Handle change username
        elif option == "change_username":
            self.user()
            return
        else:
            # Execute action and handle response
            self.execute_and_handle_response(
                instance=user,
                method_name=option,
                target_type="user",
                source=username,
            )

            # After handling response, show menu again WITHOUT re-validating
            self.user(username=username, is_validated=True)

    def repo(
        self,
        name: t.Optional[str] = None,
        owner: t.Optional[str] = None,
    ):
        """
        Display the repository menu for querying GitHub repository data.

        :param name: Optional repository name. If None, prompts user for input.
        :param owner: Optional repository owner. If None, prompts user for input.
        """

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

        repo = Repo(name=name, owner=owner)
        source = f"{owner}/{name}"

        # Only validate if not already validated
        if not self.target_validator(
            identifier=source,
            instance=repo,
            callback=self.repo,
        ):
            return

        ascii_banner(text=source)
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
            style=CUSTOM_STYLE,
            instruction=INSTRUCTIONS,
            use_shortcuts=True,
        ).ask()

        # Handle change options
        change_handlers = {
            "change_repo_name": lambda: self.repo(owner=owner),
            "change_owner": lambda: self.repo(name=name),
            "change_both": lambda: self.repo(),
        }

        if option is None:
            self.main()
            return

        # Handle navigation
        elif self.navigation_handler(option, self.repo, name, owner):
            return

        elif option in change_handlers:
            change_handlers[option]()
            return
        else:
            # Execute action and handle response
            self.execute_and_handle_response(
                instance=repo,
                method_name=option,
                target_type="repo",
                source=source,
            )

            # After handling response, show menu again WITHOUT re-validating
            self.repo(name=name, owner=owner)

    def org(self, name: t.Optional[str] = None):
        """
        Display the organisation menu for querying GitHub organisation data.

        :param name: Optional organisation name. If None, prompts user for input.
        """

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

        org = Org(name=name)

        if not self.target_validator(
            identifier=name,
            instance=org,
            callback=self.org,
        ):
            return

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
            return

        # Handle navigation
        elif self.navigation_handler(option, self.org, name):
            return

        # Handle change org
        elif option == "change_org":
            self.org()
            return

        else:
            # Execute action and handle response
            self.execute_and_handle_response(
                instance=org, method_name=option, target_type="org", source=name
            )

            # After handling response, show menu again WITHOUT re-validating
            self.org(name=name)
