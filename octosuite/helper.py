from rich.table import Table
from octosuite.config import Tree, xprint, white, green, white_bold, green_bold, header_title, reset

# helper.py
# This file holds the help text for available commands.
usage_text = 'Use syntax {} to get started with %s{}%s.' % (green_bold, reset)
usage_text_1 = '%sUse {} to view all available subcommands.%s' % (white, reset)
usage_text_2 = "%sThe {} command works with subcommands. %s" % (white, reset)


def org():
    xprint(usage_text_2.format(f"{green_bold}org{reset}") + usage_text_1.format(f"{green_bold}help:org{reset}"))


def repo():
    xprint(usage_text_2.format(f"{green_bold}repo{reset}") + usage_text_1.format(f"{green_bold}help:repo{reset}"))


def user():
    xprint(usage_text_2.format(f"{green_bold}user{reset}") + usage_text_1.format(f"{green_bold}help:user{reset}"))


def search():
    xprint(usage_text_2.format(f"{green_bold}search{reset}") + usage_text_1.format(f"{green_bold}help:search{reset}"))


def source():
    xprint(usage_text_2.format(f"{green_bold}source{reset}") + usage_text_1.format(f"{green_bold}help:source{reset}"))


def logs():
    xprint(usage_text_2.format(f"{green_bold}logs{reset}") + usage_text_1.format(f"{green_bold}help:logs{reset}"))


def csv():
    xprint(usage_text_2.format(f"{green_bold}csv{reset}") + usage_text_1.format(f"{green_bold}help:csv{reset}"))


def source_command():
    source_cmd_table = Table(show_header=True, header_style=header_title)
    source_cmd_table.add_column("Command", style="dim")
    source_cmd_table.add_column("Description")
    source_cmd_table.add_row("zipball", "Download source code Zipball")
    source_cmd_table.add_row("tarball", "Download source code Tarball")

    syntax = f"{green}source:<command>{reset}"
    xprint(f"{usage_text.format(syntax, 'source code downloads')}")
    xprint(source_cmd_table)


def search_command():
    search_cmd_table = Table(show_header=True, header_style=header_title)
    search_cmd_table.add_column("Command", style="dim")
    search_cmd_table.add_column("Description")
    search_cmd_table.add_row("users", "Search user(s)")
    search_cmd_table.add_row("repos", "Search repositor[y][ies]")
    search_cmd_table.add_row("topics", "Search topic(s)")
    search_cmd_table.add_row("issues", "Search issue(s)")
    search_cmd_table.add_row("commits", "Search commit(s)")

    syntax = f"{green}search:<command>{reset}"
    xprint(f"{usage_text.format(syntax, 'target discovery')}")
    xprint(search_cmd_table)


def user_command():
    user_cmd_table = Table(show_header=True, header_style=header_title)
    user_cmd_table.add_column("Command", style="dim")
    user_cmd_table.add_column("Description")
    user_cmd_table.add_row("email", "Return a target's email")
    user_cmd_table.add_row("profile", "Get a target's profile info")
    user_cmd_table.add_row("gists", "Return a users's gists")
    user_cmd_table.add_row("org", "Return organizations that a target belongs to/owns")
    user_cmd_table.add_row("repos", "Return a target's repositories")
    user_cmd_table.add_row("events", "Return a target's events")
    user_cmd_table.add_row("follows", "Check if user(A) follows user(B)")
    user_cmd_table.add_row("followers", "Return a target's followers")
    user_cmd_table.add_row("following", "Return a list of users the target is following")
    user_cmd_table.add_row("subscriptions", "Return a target's subscriptions")

    syntax = f"{green}user:<command>{reset}"
    xprint(f"{usage_text.format(syntax, 'user investigation(s)')}")
    xprint(user_cmd_table)


def org_command():
    org_cmd_table = Table(show_header=True, header_style=header_title)
    org_cmd_table.add_column("Command", style="dim")
    org_cmd_table.add_column("Description")
    org_cmd_table.add_row("profile", "Get a target organization' profile info")
    org_cmd_table.add_row("repos", "Return a target organization' repositories")
    org_cmd_table.add_row("events", "Return a target organization' events")
    org_cmd_table.add_row("member", "Check if a specified user is a public member of the target organization")

    syntax = f"{green}org:<command>{reset}"
    xprint(f"{usage_text.format(syntax, 'organization investigation(s)')}")
    xprint(org_cmd_table)


def repo_command():
    repo_cmd_table = Table(show_header=True, header_style=header_title)
    repo_cmd_table.add_column("Command", style="dim")
    repo_cmd_table.add_column("Description")
    repo_cmd_table.add_row("profile", "Get a repository's info")
    repo_cmd_table.add_row("issues", "Return a repository's issues")
    repo_cmd_table.add_row("forks", "Return a repository's forks")
    repo_cmd_table.add_row("releases", "Return a repository's releases")
    repo_cmd_table.add_row("stargazers", "Return a repository's stargazers")
    repo_cmd_table.add_row("contributors", "Return a repository's contributors")
    repo_cmd_table.add_row("path_contents", "List contents in a path of a repository")

    syntax = f"{green}repo:<command>{reset}"
    xprint(f"{usage_text.format(syntax, 'repository investigation(s)')}")
    xprint(repo_cmd_table)


def logs_command():
    logs_cmd_table = Table(show_header=True, header_style=header_title)
    logs_cmd_table.add_column("Command", style="dim")
    logs_cmd_table.add_column("Description")
    logs_cmd_table.add_row("view", "View logs")
    logs_cmd_table.add_row("read", "Read log")
    logs_cmd_table.add_row("delete", "Delete log")
    logs_cmd_table.add_row("clear", "clear logs")

    syntax = f"{green}logs:<command>{reset}"
    xprint(f"{usage_text.format(syntax, 'log(s) management')}")
    xprint(logs_cmd_table)


def csv_command():
    csv_cmd_table = Table(show_header=True, header_style=header_title)
    csv_cmd_table.add_column("Command", style="dim")
    csv_cmd_table.add_column("Description")
    csv_cmd_table.add_row("view", "View csv files")
    csv_cmd_table.add_row("read", "Read csv")
    csv_cmd_table.add_row("delete", "Delete csv")
    csv_cmd_table.add_row("clear", "clear csv files")

    syntax = f"{green}csv:<command>{reset}"
    xprint(f"{usage_text.format(syntax, 'csv management')}")
    xprint(csv_cmd_table)


def help_command():
    core_cmd_table = Table(show_header=True, header_style=header_title)
    core_cmd_table.add_column("Command", style="dim", width=12)
    core_cmd_table.add_column("Description")
    core_cmd_table.add_row("ls", "List contents of the specified directory")
    core_cmd_table.add_row("cd", "Move to specified directory")
    core_cmd_table.add_row("help", "Help menu")
    core_cmd_table.add_row("exit", "Close session")
    core_cmd_table.add_row("clear", "Clear screen")
    core_cmd_table.add_row("about", "Program's info")
    core_cmd_table.add_row("author", "Developer's info")

    help_sub_cmd_table = Table(show_header=True, header_style=header_title)
    help_sub_cmd_table.add_column("Command", style="dim", width=12)
    help_sub_cmd_table.add_column("Description")
    help_sub_cmd_table.add_row("csv", "List all csv management commands")
    help_sub_cmd_table.add_row("logs", "List all logs management commands")
    help_sub_cmd_table.add_row("org", "List all organization investigation commands")
    help_sub_cmd_table.add_row("user", "List all users investigation commands")
    help_sub_cmd_table.add_row("repo", "List all repository investigation commands")
    help_sub_cmd_table.add_row("search", "List all target discovery commands")
    help_sub_cmd_table.add_row("source", "List all source code download commands (for developers)")

    syntax = f"{green}help:<command>{reset}"
    xprint(core_cmd_table)
    xprint(f"\n\n{usage_text.format(syntax, 'octosuite')}")
    xprint(help_sub_cmd_table)
