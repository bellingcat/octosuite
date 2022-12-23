# import everything from the octosuite.py file
from octosuite.octosuite import *  # I drifted away from the 'pythonic way' here


def octosuite():
    try:
        run = Octosuite(args)
        path_finder()
        clear_screen()
        configure_logging()
        check_updates()
        xprint(banner()[0], banner()[1])
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
                """
                Iterate over the command_map and check if the user input matches any command in it [command_map],
                if there's a match, we return its method. If no match is found, we ignore it.
                """
                if command_input[:2] == 'cd':
                    os.chdir(command_input[3:])
                elif command_input[:2] == 'ls':
                    os.system(f'dir {command_input[3:]}' if os.name == 'nt' else f'ls {command_input[3:]}')
                else:
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
