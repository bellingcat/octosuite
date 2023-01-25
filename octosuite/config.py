import psutil
import platform
import argparse
from rich.tree import Tree
from rich.text import Text
from rich.table import Table
from datetime import datetime
from rich import print as xprint
from rich.prompt import Prompt, Confirm


def usage():
    return """
    Basic Usage
    ===========

        Get User Profile Info
        ---------------------
        octosuite --method user_profile --username <username>


        Get User Repos
        --------------
        octosuite --method user_repos --username <username>


        Get Organi[sz]ation Profile Info
        -----------------------------
        octosuite --method org_profile --organization <organization_name>


        Get Organi[sz]ation Repos
        -----------------------------
        octosuite --method org_repos --organization <organization_name>

        
        Get Repo Profile Info
        ---------------------
        octosuite --method repo_profile --username <username> --repository <repo_name>


        Get Repo Forks
        --------------
        octosuite --method repo_forks --username <username> --repository <repo_name>
        
    
    
    Searching
    =========

        Search Users
        ------------
        octosuite --method users_search --query <query>

        
        Search Issues
        -------------
        octosuite --method issues_search --query <query>

        
        Search Commits
        --------------
        octosuite --method commits_search --query <query>
        

        Search Topics
        -------------
        octosuite --method topics_search --query <query>
        

        Search Repositories
        -------------------
        octosuite --method repos_search --query <query>



    Log Management
    ==============

        View logs
        ---------
        octosuite --method view_logs


        Read log
        --------
        octosuite --method read_log --log-file <log_file>


        Delete log
        ----------
        octosuite --method delete_log --log-file <log_file>


        Clear logs
        ----------
        octosuite --method clear_logs



    CSV Management
    ==============

        View CSV
        ---------
        octosuite --method view_csv


        Read CSV
        --------
        octosuite --method read_csv --csv-file <csv_file>


        Delete CSV
        ----------
        octosuite --method delete_csv --csv-file <csv_file>


        Clear CSV's
        -----------
        octosuite --method clear_csv
        """


def create_parser():
    parser = argparse.ArgumentParser(description='OCTOSUITE: Advanced GitHub osint framework  — by Richard Mwewa | https://about.me/rly0nheart', usage=usage())
    parser.add_argument('-m', '--method', help='method', choices=['user_email', 'user_profile', 'user_repos', 'user_gists', 'user_orgs', 'user_events',
                                                                  'user_subscriptions', 'user_following', 'user_followers', 'user_follows',
                                                                  'org_profile', 'org_repos', 'org_events', 'org_member',
                                                                  'repo_profile', 'repo_contributors', 'repo_stargazers', 'repo_forks',
                                                                  'repo_issues', 'repo_releases', 'repo_path_contents', 'users_search', 'issues_search',
                                                                  'commits_search', 'topics_search', 'repos_search', 'view_logs', 'read_log', 'delete_log', 
                                                                  'clear_logs', 'view_csv', 'read_csv', 'delete_csv', 'clear_csv', 'about', 'author'])
    parser.add_argument('-u', '--username', help='username')
    parser.add_argument('-uB', '--username_b', help='username_B (used with user_follows)')
    parser.add_argument('-o', '--organization', '--organisation', help='organi[sz]ation name')
    parser.add_argument('-r', '--repository', help='repository name')
    parser.add_argument('-p', '--path_name', help='path name (used with repo_path_contents)')
    parser.add_argument('-q', '--query', help='query (used with search methods)')
    parser.add_argument('-l', '--limit', help='output limit (used with methods that return results in bulk) (default: %(default)s)', default=10)
    parser.add_argument('-c', '--colors', '--colours', help='specify to run octosuite cli with colo[u]rs enabled', action='store_true')
    parser.add_argument('--csv_file', help='csv file (used with csv management methods)')
    parser.add_argument('--log_file', help='log file (used with logs management methods)')
    parser.add_argument('--log-to-csv', help='log output to a csv file', action='store_true', dest='log_csv')
    return parser


parser = create_parser()
args = parser.parse_args()

# This file is responsible for enabling/disabling colo[u]rs and configuring argparse in OctoSuite
# This file gets called first at start up before any other file
# config.py is the reason why users get to choose whether to enable/disable colo[u]rs, and call the program with command line arguments
# delete this file (I dare you), the entire program breaks
system_info = [("RAM", f"{str(round(psutil.virtual_memory().total / (1024.0 ** 3)))}GB"),
               ("Node", platform.node()),
               ("Release", platform.release()),
               ("Version", platform.version()),
               ("Processor", platform.processor()),
               ("Architecture", platform.architecture())]
first_banner = f"""
            OCTOSUITE © 2023 Richard Mwewa
            {datetime.now().strftime('%A %d %B %Y, %H:%M:%S%p')}
            
"""

if args.colors:
    header_title = "bold white"
    red = "[red]"
    white = "[white]"
    green = "[green]"
    yellow = "[yellow]"
    red_bold = "[white bold]"
    white_bold = "[white bold]"
    green_bold = "[green bold]"
    reset = "[/]"
else:
    print(first_banner)
    system_tree = Tree(platform.system())
    for system_key, system_value in system_info:
        system_tree.add(f"{system_key}: {system_value}")
    xprint(system_tree)
    print("\n")
    try:
        color_chooser = Confirm.ask(f"Welcome, would you like to enable colo(u)rs for this session?")
        if color_chooser:
            header_title = "bold white"
            red = "[red]"
            white = "[white]"
            green = "[green]"
            yellow = "[yellow]"
            red_bold = "[white bold]"
            white_bold = "[white bold]"
            green_bold = "[green bold]"
            reset = "[/]"
        else:
            header_title = red = white = green = red_bold = white_bold = green_bold = reset = yellow = ""
    except KeyboardInterrupt:
        exit(f"[WARNING] Process interrupted with Ctrl+C.")
      
