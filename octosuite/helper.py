from rich.table import Table
from rich import print as xprint
from octosuite.colors import white, green, white_bold, green_bold, header_title, reset

"""
Help
This class holds the help text for available commands.
"""


class Help:
    usageText = 'Use syntax {} to get started with %s{}%s.' % (green_bold, reset)
    usageText1 = '%sUse {} to view all available subcommands.%s' % (white, reset)
    usageText2 = "%sThe {} command works with subcommands. %s" % (white, reset)

    def Org():
        xprint(
            Help.usageText2.format(f"{green_bold}org{reset}") + Help.usageText1.format(f"{green_bold}help:org{reset}"))


    def Repo():
        xprint(Help.usageText2.format(f"{green_bold}repo{reset}") + Help.usageText1.format(
            f"{green_bold}help:repo{reset}"))


    def User():
        xprint(Help.usageText2.format(f"{green_bold}user{reset}") + Help.usageText1.format(
            f"{green_bold}help:user{reset}"))


    def Search():
        xprint(Help.usageText2.format(f"{green_bold}search{reset}") + Help.usageText1.format(
            f"{green_bold}help:search{reset}"))


    def Source():
        xprint(Help.usageText2.format(f"{green_bold}source{reset}") + Help.usageText1.format(
            f"{green_bold}help:source{reset}"))


    def Logs():
        xprint(Help.usageText2.format(f"{green_bold}logs{reset}") + Help.usageText1.format(
            f"{green_bold}help:logs{reset}"))


    def Version():
        xprint(Help.usageText2.format(f"{green_bold}version{reset}") + Help.usageText1.format(
            f"{green_bold}help:version{reset}"))


    def Csv():
        xprint(
            Help.usageText2.format(f"{green_bold}csv{reset}") + Help.usageText1.format(f"{green_bold}help:csv{reset}"))


    def versionCommand():
        version_cmd_table = Table(show_header=True, header_style=header_title)
        version_cmd_table.add_column("Command", style="dim", width=12)
        version_cmd_table.add_column("Description")
        version_cmd_table.add_row("check", "Check for new release(s)")
        version_cmd_table.add_row("info", "Version information")

        syntax = f"{green}version:<command>{reset}"
        xprint(f"{Help.usageText.format(syntax, 'version management')}")
        xprint(version_cmd_table)


    def sourceCommand():
        source_cmd_table = Table(show_header=True, header_style=header_title)
        source_cmd_table.add_column("Command", style="dim", width=12)
        source_cmd_table.add_column("Description")
        source_cmd_table.add_row("zipball", "Download source code Zipball")
        source_cmd_table.add_row("tarball", "Download source code Tarball")

        syntax = f"{green}source:<command>{reset}"
        xprint(f"{Help.usageText.format(syntax, 'source code downloads')}")
        xprint(source_cmd_table)


    def searchCommand():
        search_cmd_table = Table(show_header=True, header_style=header_title)
        search_cmd_table.add_column("Command", style="dim", width=12)
        search_cmd_table.add_column("Description")
        search_cmd_table.add_row("users", "Search user(s)")
        search_cmd_table.add_row("repos", "Search repositor[y][ies]")
        search_cmd_table.add_row("topics", "Search topic(s)")
        search_cmd_table.add_row("issues", "Search issue(s)")
        search_cmd_table.add_row("commits", "Search commit(s)")

        syntax = f"{green}search:<command>{reset}"
        xprint(f"{Help.usageText.format(syntax, 'target discovery')}")
        xprint(search_cmd_table)


    def userCommand():
        user_cmd_table = Table(show_header=True, header_style=header_title)
        user_cmd_table.add_column("Command", style="dim", width=12)
        user_cmd_table.add_column("Description")
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
        xprint(f"{Help.usageText.format(syntax, 'user investigation(s)')}")
        xprint(user_cmd_table)


    def orgCommand():
        org_cmd_table = Table(show_header=True, header_style=header_title)
        org_cmd_table.add_column("Command", style="dim", width=12)
        org_cmd_table.add_column("Description")
        org_cmd_table.add_row("profile", "Get a target organization' profile info")
        org_cmd_table.add_row("repos", "Return a target organization' repositories")
        org_cmd_table.add_row("events", "Return a target organization' events")
        org_cmd_table.add_row("member", "Check if a specified user is a public member of the target organization")

        syntax = f"{green}org:<command>{reset}"
        xprint(f"{Help.usageText.format(syntax, 'organization investigation(s)')}")
        xprint(org_cmd_table)


    def repoCommand():
        repo_cmd_table = Table(show_header=True, header_style=header_title)
        repo_cmd_table.add_column("Command", style="dim", width=12)
        repo_cmd_table.add_column("Description")
        repo_cmd_table.add_row("profile", "Get a repository's info")
        repo_cmd_table.add_row("issues", "Return a repository's issues")
        repo_cmd_table.add_row("forks", "Return a repository's forks")
        repo_cmd_table.add_row("releases", "Return a repository's releases")
        repo_cmd_table.add_row("stargazers", "Return a repository's stargazers")
        repo_cmd_table.add_row("path_contents", "List contents in a path of a repository")

        syntax = f"{green}repo:<command>{reset}"
        xprint(f"{Help.usageText.format(syntax, 'repository investigation(s)')}")
        xprint(repo_cmd_table)


    def logsCommand():
        logs_cmd_table = Table(show_header=True, header_style=header_title)
        logs_cmd_table.add_column("Command", style="dim", width=12)
        logs_cmd_table.add_column("Description")
        logs_cmd_table.add_row("view", "View logs")
        logs_cmd_table.add_row("read", "Read log")
        logs_cmd_table.add_row("delete", "Delete log")

        syntax = f"{green}logs:<command>{reset}"
        xprint(f"{Help.usageText.format(syntax, 'log(s) management')}")
        xprint(logs_cmd_table)


    def csvCommand():
        csv_cmd_table = Table(show_header=True, header_style=header_title)
        csv_cmd_table.add_column("Command", style="dim", width=12)
        csv_cmd_table.add_column("Description")
        csv_cmd_table.add_row("view", "View csv files")
        csv_cmd_table.add_row("read", "Read csv")
        csv_cmd_table.add_row("delete", "Delete csv")

        syntax = f"{green}csv:<command>{reset}"
        xprint(f"{Help.usageText.format(syntax, 'csv management')}")
        xprint(csv_cmd_table)
        

    def helpCommand():
        core_cmd_table = Table(show_header=True, header_style=header_title)
        core_cmd_table.add_column("Command", style="dim", width=12)
        core_cmd_table.add_column("Description")
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
        help_sub_cmd_table.add_row("version", "List all version management commands")

        syntax = f"{green}help:<command>{reset}"
        xprint(core_cmd_table)
        xprint(f"\n\n{Help.usageText.format(syntax, 'octosuite')}")
        xprint(help_sub_cmd_table)
