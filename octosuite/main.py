# import everything from the octosuite.py file
import argparse
from octosuite.octosuite import *  # I drifted away from the 'pythonic way' here


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
    parser.add_argument('--colors', help='enable or disable colors (default: %(default)s)', type=bool, default=True)
    return parser


parser = create_parser()
args = parser.parse_args()


def octosuite():
    try:
        run = Octosuite(args)
        path_finder()
        clear_screen()
        configure_logging()
        check_updates()
        xprint(ascii_banner()[1], ascii_banner()[0])
        if args.module == "user_profile":
            run.user_profile()
        elif args.module == "user_repos":
            run.user_repos()
        elif args.module == "user_gists":
            run.user_gists()
        elif args.module == "user_orgs":
            run.user_orgs()
        elif args.module == "user_events":
            run.user_events()
        elif args.module == "user_subscriptions":
            run.user_subscriptions()
        elif args.module == "user_following":
            run.user_following()
        elif args.module == "user_followers":
            run.user_followers()
        elif args.module == "user_follows":
            run.user_follows()
        elif args.module == "users_search":
            run.users_search()
        elif args.module == "issues_search":
            run.issues_search()
        elif args.module == "commits_search":
            run.commits_search()
        elif args.module == "topics_search":
            run.topics_search()
        elif args.module == "repos_search":
            run.repos_search()
        elif args.module == "org_profile":
            run.org_profile()
        elif args.module == "org_repos":
            run.org_repos()
        elif args.module == "org_events":
            run.org_events()
        elif args.module == "org_member":
            run.org_member()
        elif args.module == "repo_profile":
            run.repo_profile()
        elif args.module == "repo_contributors":
            run.repo_contributors()
        elif args.module == "repo_stargazers":
            run.repo_stargazers()
        elif args.module == "repo_forks":
            run.repo_forks()
        elif args.module == "repo_issues":
            run.repo_issues()
        elif args.module == "repo_releases":
            run.repo_releases()
        elif args.module == "repo_path_contents":
            run.path_contents()
        else:
            """
            Main loop keeps octosuite running, this will break if Octosuite detects a KeyboardInterrupt (Ctrl+C)
            or if the 'exit' command is entered.
            """
            while True:
                xprint(f"{white}┌──({red}{getpass.getuser()}{white}@{red}octosuite{white})\n├──[~{green}{os.getcwd()}{white}]\n└╼ {reset}",end="")
                command_input = input().lower()
                print("\n")
                """
                Iterate over the command_map and check if the user input matches any command in it [command_map],
                if there's a match, we return its method. If no match is found, we ignore it.
                """
                for command, method in run.command_map:
                    if command_input == command:
                        method()
                        print("\n")
                    else:
                        pass
        
    except KeyboardInterrupt:
        logging.warning(ctrl_c)
        xprint(f"\n{WARNING} {ctrl_c}")

    except Exception as e:
        logging.error(error.format(e))
        xprint(f"{ERROR} {error.format(e)}")
