import os
import subprocess
import sys
import typing as t
from datetime import datetime
from pathlib import Path

import pyfiglet
import questionary as q
from questionary import Style
from rich.console import Console

from .prompts import Prompts
from ..core.models import User, Repo, Org

CUSTOM_STYLE = Style(
    [
        ("highlighted", "fg:black bold bg:white"),
        ("instruction", "fg:gray"),
    ]
)

INSTRUCTIONS = "[Move] ⮃ [ENTER] ⮠"

POINTER = "🖛 "

console = Console()


def clear_screen():
    """Clear the terminal screen."""
    subprocess.run(["cls" if os.name == "nt" else "clear"])


def banner(text: str):
    console.print(pyfiglet.figlet_format(text=text, font="chunky"))


class Menus:
    def __init__(self, prompts: Prompts):
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
        self.prompts = prompts

        # Methods that don't need pagination
        self.non_paginated_methods = {"profile", "languages"}

        self.mode_handlers = {
            "user": self.user,
            "repo": self.repo,
            "org": self.org,
            "search": lambda: (
                print("Search functionality not yet implemented"),
                self.main(),
            ),
        }

    def main(self):
        """Main menu to select mode."""
        clear_screen()
        try:
            banner(text="octosuite")

            mode = q.select(
                "Select a mode to begin with",
                choices=[
                    q.Choice(
                        title="User",
                        value="user",
                        description="data about a user",
                        shortcut_key="u",
                    ),
                    q.Choice(
                        title="Repo",
                        value="repo",
                        description="data about a repository",
                        shortcut_key="r",
                    ),
                    q.Choice(
                        title="Org",
                        value="org",
                        description="data about an organisation",
                        shortcut_key="o",
                    ),
                    q.Choice(
                        title="Search",
                        value="search",
                        description="Search GitHub",
                        shortcut_key="s",
                    ),
                    q.Choice(
                        title="Check for updates",
                        value="check_updates",
                        description="Check for updates",
                        shortcut_key="c",
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
                pointer=POINTER,
                use_shortcuts=True,
            ).ask()

            if mode == "quit":
                if self.prompts.quit():
                    sys.exit()
                else:
                    self.main()
            else:
                handler = self.mode_handlers.get(mode)
                if handler:
                    handler()
                else:
                    self.main()
        except KeyboardInterrupt:
            sys.exit()

    def _execute_action(self, instance, method_name, target: str):
        """Execute a method on an instance, prompting for pagination if needed."""
        method = getattr(instance, method_name)

        # pagination params if needed
        params = (
            self.prompts.pagination_params()
            if method_name in self.paginated_methods
            else {}
        )

        # Execute with status spinner
        with console.status(f"Fetching {method_name} for {target}..."):
            return method(**params)

    def _handle_navigation(self, option, callback, *callback_args):
        """Handle navigation options (back, quit, change settings)."""
        navigation_handlers = {
            "back": lambda: self.main(),
            "quit": lambda: (
                sys.exit() if self.prompts.quit() else callback(*callback_args)
            ),
        }

        handler = navigation_handlers.get(option)
        if handler:
            handler()
            return True
        return False

    @staticmethod
    def _preview_data(data: t.Union[dict, list]):
        """Preview data as formatted JSON."""
        import json
        from rich.panel import Panel
        from rich.syntax import Syntax

        if isinstance(data, dict):
            # Show the entire dict as JSON
            json_str = json.dumps(data, indent=2)
            syntax = Syntax(json_str, "json", line_numbers=False)
            console.print(
                Panel(
                    renderable=syntax,
                    border_style="#444444",
                )
            )

        elif isinstance(data, list):
            if not data:
                console.print("[yellow]No data to preview[/yellow]")
                return

            console.print(f"Total items: {len(data)}")
            console.print(f"Showing: first 5 items")

            # Show first 5 items as JSON
            preview_data = data[:5]
            json_str = json.dumps(preview_data, indent=2)
            syntax = Syntax(json_str, "json", line_numbers=False)
            console.print(
                Panel(
                    renderable=syntax,
                    border_style="#444444",
                )
            )

        else:
            console.print("[yellow]No data to preview[/yellow]")
            return

        console.print()

    def export(self, data: t.Union[dict, list], data_type: str, target: str) -> None:
        """Export data to file in user-selected format(s)."""
        if not data:
            console.print(f"No data found for {target}")
            return

        # Show what was found
        if isinstance(data, list):
            console.print(f"\n✓ Found {len(data)} valid {data_type} for {target}")
        else:
            console.print(f"\n✓ Found valid {data_type} data for {target}")

        # Ask for export formats (multi-select)
        try:
            self._preview_data(data=data)

            if not q.confirm(
                "Would you like to export this data?",
                default=True,
            ).ask():
                console.print("[yellow]Skipping export.[/yellow]")
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
                instruction="[SPACE] ☑ [ENTER] ⮠ [CTRL+C] Skip",
                pointer=POINTER,
                validate=lambda x: len(x) > 0 or "Please select at least one format",
            ).ask()

            if not file_formats:
                console.print("[yellow]No formats selected. Skipping export.[/yellow]")
                return

            import pandas as pd

            # Create output directory if it doesn't exist
            output_dir = Path("../exports")
            output_dir.mkdir(exist_ok=True)

            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_target = target.replace("/", "_")
            filename = f"{safe_target}_{data_type}_{timestamp}"

            # Convert data to DataFrame
            if isinstance(data, dict):
                # For dict data, convert to a single-row DataFrame
                df = pd.DataFrame([data])
            else:
                # For list data
                df = pd.DataFrame(data)

            # Export to all selected formats
            exported_files = []
            for file_format in file_formats:
                filepath = output_dir / f"{filename}.{file_format}"

                if file_format == "json":
                    df.to_json(filepath, orient="records", indent=2)
                elif file_format == "csv":
                    df.to_csv(filepath, index=False)
                elif file_format == "html":
                    df.to_html(filepath, border=1, classes="table table-striped")

                exported_files.append(str(filepath))

            # Show success message
            console.print("\n[green]✓ Export successful![/green]")
            for filepath in exported_files:
                console.print(f"  • {filepath}")

        except KeyboardInterrupt:
            print("\nExport cancelled")

    def user(self, username: t.Optional[str] = None):
        """User menu for querying user data."""
        clear_screen()
        try:
            if username is None:
                banner(text="user")
                username = self.prompts.prompt(
                    message="GitHub Username", instruction="e.g., octocat"
                )

            clear_screen()
            banner(text=username)

            option = q.select(
                "Select an action",
                choices=[
                    q.Choice(
                        title="Profile", value="profile", description="Profile data"
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
                    q.Choice(title="events", value="events", description="Events"),
                    q.Choice(
                        title="Received events",
                        value="received_events",
                        description="This user's received events",
                    ),
                    q.Choice(
                        title="Change username",
                        value="change_username",
                        description="Query a different user",
                        shortcut_key="u",
                    ),
                    q.Choice(
                        title="Back",
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
                pointer=POINTER,
                use_shortcuts=True,
            ).ask()

            # Handle navigation
            if self._handle_navigation(option, self.user, username):
                return

            # Handle change username
            if option == "change_username":
                self.user()
                return

            # Execute action if it's a valid method
            valid_methods = self.paginated_methods | self.non_paginated_methods
            if option in valid_methods:
                user = User(name=username)
                data = self._execute_action(user, option, username)
                self.export(data=data, data_type=option, target=username)

            self.user(username=username)
        except KeyboardInterrupt:
            print("\n\nReturning to main menu...")
            self.main()

    def repo(self, name: t.Optional[str] = None, owner: t.Optional[str] = None):
        """Repository menu for querying repo data."""
        clear_screen()
        try:
            if name is None or owner is None:
                banner(text="Repository")
                if name is None:
                    name = self.prompts.prompt(
                        message="GitHub Repo Name",
                        instruction="e.g., spoon-knife",
                    )
                if owner is None:
                    owner = self.prompts.prompt(
                        message="GitHub Repo Owner",
                        instruction="e.g., octocat",
                    )

            clear_screen()
            banner(text=name)

            option = q.select(
                "What would you like to do?",
                choices=[
                    q.Choice(
                        title="Change repo name",
                        value="change_repo_name",
                        description="Update the name of the repo",
                    ),
                    q.Choice(
                        title="Change owner name",
                        value="change_owner",
                        description="Update the name of repo owner",
                    ),
                    q.Choice(
                        title="Change both repo and owner names",
                        value="change_both",
                        description="Update both the repo and owner names",
                    ),
                    q.Choice(
                        title="Profile",
                        value="profile",
                        description="Repository data",
                    ),
                    q.Choice(
                        title="Forks", value="forks", description="Repository forks"
                    ),
                    q.Choice(
                        title="Issue events",
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
                        title="Branches", value="branches", description="Branches"
                    ),
                    q.Choice(title="tags", value="tags", description="Tags"),
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
                    q.Choice(title="Commits", value="commits", description="Commits"),
                    q.Choice(
                        title="Comments", value="comments", description="Comments"
                    ),
                    q.Choice(title="Issues", value="issues", description="Issues"),
                    q.Choice(
                        title="Releases", value="releases", description="Releases"
                    ),
                    q.Choice(
                        title="Deployments",
                        value="deployments",
                        description="Deployments",
                    ),
                    q.Choice(title="labels", value="labels", description="Labels"),
                    q.Choice(
                        title="Back",
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
                pointer=POINTER,
                use_shortcuts=True,
            ).ask()

            # Handle navigation
            if self._handle_navigation(option, self.repo, name, owner):
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
                repo = Repo(name=name, owner=owner)
                target = f"{owner}/{name}"
                data = self._execute_action(repo, option, target)
                self.export(data=data, data_type=option, target=target)

            self.repo(name=name, owner=owner)
        except KeyboardInterrupt:
            print("\n\nReturning to main menu...")
            self.main()

    def org(self, name: t.Optional[str] = None):
        """Organization menu for querying org data."""
        clear_screen()
        try:
            if name is None:
                banner(text="org")
                name = self.prompts.prompt(
                    message="GitHub Organization Name",
                    instruction="e.g, github",
                )

            clear_screen()
            banner(text=name)

            option = q.select(
                "What would you like to do?",
                choices=[
                    q.Choice(
                        title="Change org name",
                        value="change_org",
                        description="Query a different organization",
                    ),
                    q.Choice(
                        title="Profile", value="profile", description="Profile data"
                    ),
                    q.Choice(
                        title="Repositories",
                        value="repos",
                        description="Public repositories",
                    ),
                    q.Choice(
                        title="Events",
                        value="events",
                        description="Organization events",
                    ),
                    q.Choice(title="Hooks", value="hooks", description="Webhooks"),
                    q.Choice(title="issues", value="issues", description="Issues"),
                    q.Choice(
                        title="Members",
                        value="members",
                        description="Organization members",
                    ),
                    q.Choice(
                        title="Back",
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
                pointer=POINTER,
                use_shortcuts=True,
            ).ask()

            # Handle navigation
            if self._handle_navigation(option, self.org, name):
                return

            # Handle change org
            if option == "change_org":
                self.org()
                return

            # Execute action if it's a valid method
            valid_methods = self.paginated_methods | self.non_paginated_methods
            if option in valid_methods:
                org = Org(name=name)
                data = self._execute_action(org, option, name)
                self.export(data=data, data_type=option, target=name)

            self.org(name=name)
        except KeyboardInterrupt:
            print("\n\nReturning to main menu...")
            self.main()
