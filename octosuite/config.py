import psutil
import platform
import argparse
from rich.tree import Tree
from datetime import datetime
from rich import print as xprint

def usage():
    return """
    Basic usage
    -----------
        # Get user profile info
        octosuite --module user_profile --username <username>
        
        # Get organization profile info
        octosuite --module org_profile --organization <organization_name>
        
        # Get repo profile info
        octosuite --module repo_profile --username <username> --repository <repo_name>
        
    
    
    Searching
    ---------
        # Search users
        octosuite --module users_search --query <query>
        
        # Search issues
        octosuite --module issues_search --query <query>
        
        # Search commits
        octosuite --module commits_search --query <query>
        
        # Search topics
        octosuite --module topics_search --query <query>
        
        # Search repositories
        octosuite --module repos_search --query <query>
        """


def create_parser():
    parser = argparse.ArgumentParser(description='OCTOSUITE: Advanced GitHub osint framework  — by Richard Mwewa | https://about.me/rly0nheart', usage=usage())
    parser.add_argument('-m', '--module', help='module', choices=['user_profile', 'user_repos', 'user_gists', 'user_orgs', 'user_events',
                                                                  'user_subscriptions', 'user_following', 'user_followers', 'user_follows',
                                                                  'org_profile', 'org_repos', 'org_events', 'org_member',
                                                                  'repo_profile', 'repo_contributors', 'repo_stargazers', 'repo_forks',
                                                                  'repo_issues', 'repo_releases', 'repo_path_contents', 'users_search', 'issues_search',
                                                                  'commits_search', 'topics_search', 'repos_search'])
    parser.add_argument('-u', '--username', help='username')
    parser.add_argument('-uB', '--username_b', help='username_B (used with user_follows)')
    parser.add_argument('-org', '--organization', help='organization name')
    parser.add_argument('-repo', '--repository', help='repository name')
    parser.add_argument('-pn', '--path_name', help='path name (used with repo_path_contents)')
    parser.add_argument('-q', '--query', help='query (used with search modules)')
    parser.add_argument('-l', '--limit', help='output limit (used with modules that return results in bulk) (default: %(default)s)', default=10)
    parser.add_argument('-c', '--colors', help='specify to run octosuite cli with colors enabled', action='store_true')
    return parser


parser = create_parser()
args = parser.parse_args()

# This file is responsible for enabling/disabling colors in OctoSuite
# This file gets called first at start up before any other file gets called
# colors.py is the reason why users get to choose whether to enable/disable colors
# delete this file, the entire program breaks
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
        color_chooser = input(f"[PROMPT] Welcome, would you like to enable colors for this session? (yes/no) ").lower()
        if color_chooser == "yes":
            header_title = "bold white"
            red = "[red]"
            white = "[white]"
            green = "[green]"
            red_bold = "[white bold]"
            white_bold = "[white bold]"
            green_bold = "[green bold]"
            reset = "[/]"
        else:
            header_title = red = white = green = red_bold = white_bold = green_bold = reset = ""
    except KeyboardInterrupt:
        exit(f"[WARNING] Process interrupted with Ctrl+C.")
      
