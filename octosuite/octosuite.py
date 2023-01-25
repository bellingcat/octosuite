#!usr/bin/python

import re
import os
import sys
import shutil
import logging
import getpass
import requests
import platform
import subprocess
from datetime import datetime
from requests.auth import HTTPBasicAuth
from octosuite.banner import version_tag, banner
from octosuite.config import Tree, Text, Table, Prompt, Confirm, xprint, create_parser, args, red, white, green, yellow, header_title, reset
from octosuite.message_prefixes import ERROR, WARNING, PROMPT, POSITIVE, NEGATIVE, INFO  # wondering why I name all the variables instead of just using the * wildcard?, because it's the pythonic way lol
# seriously now, the reason why I am doing this, is so that you know exactly what I am importing from a named module :)
from octosuite.helper import help_command, source_command, search_command, user_command, repo_command, \
    logs_command, csv_command, org_command, source, org, repo, user, search, logs, csv
from octosuite.log_roller import ctrl_c, error, session_opened, session_closed, viewing_logs, viewing_csv, \
    deleted, reading, file_downloading, file_downloaded, info_not_found, \
    user_not_found, org_not_found, repo_or_user_not_found, limit_output, prompt_log_csv
from octosuite.csv_loggers import log_org_profile, log_user_profile, log_repo_profile, log_repo_path_contents, \
    log_repo_contributors, log_repo_stargazers, log_repo_forks, log_repo_issues, log_repo_releases, log_org_repos, \
    log_org_profile, log_user_repos, log_user_gists, log_user_orgs, log_user_events, log_user_subscriptions, \
    log_user_following, log_user_followers, log_repos_search, log_users_search, log_topics_search, log_issues_search, \
    log_commits_search


if os.name == "nt":
    try:
        from pyreadline3 import Readline
    except ImportError:
        subprocess.run(['pip3', 'install', 'pyreadline3'], shell=False)
    readline = Readline()
else:
    import readline

    def completer(text, state):
        options = [i for i in commands if i.startswith(text)]
        if state < len(options):
            return options[state]
        else:
            return None

    readline.parse_and_bind("tab: complete")
    readline.set_completer(completer)


# path_finder()
# This function is responsible for creating/checking the availability of  the (.logs, output, downloads) folders,
# enabling logging to automatically log network/user activity to a file, and logging the start of a session.
def path_finder():
    """
    Check 3 directories (.logs, output, downloads) on startup
    If they exist, ignore, otherwise, create them
    """
    directory_list = ['.logs', 'output', 'downloads']
    for directory in directory_list:
        os.makedirs(directory, exist_ok=True)


# Configure logging to log user activities
def configure_logging():
    now = datetime.now()
    now_formatted = now.strftime("%Y-%m-%d %H-%M-%S%p")
    logging.basicConfig(filename=f".logs/{now_formatted}.log", format="[%(asctime)s] [%(levelname)s] %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S%p", level=logging.DEBUG)
    # Log the start of a session
    logging.info(session_opened.format(platform.node(), getpass.getuser()))


# Check if the remote tag_name from the latest release matches the one in the program
# if it does, it means the program is up-to-date.
# If it doesn't match, notify the user about a new release
def check_updates():
    response = requests.get("https://api.github.com/repos/bellingcat/octosuite/releases/latest").json()
    if response['tag_name'] == version_tag:
        pass
    else:
        xprint(f"[{green}UPDATE{reset}] A new release of Octosuite is available ({response['tag_name']}). Run 'pip install --upgrade octosuite' to get the updates.\n")


def list_dir_and_files():
    os.system('dir' if os.name == 'nt' else 'ls')


# Delete a specified csv file
def delete_csv():
    if args.csv_file:
        csv_file = args.csv_file
    else:
        csv_file = Prompt.ask(f"{green}.csv {white}(filename){reset}")
    os.remove(os.path.join("output", csv_file))
    logging.info(deleted.format(csv_file))
    xprint(f"{POSITIVE} {deleted.format(csv_file)}")


# Clear csv files
def clear_csv():
    clear_csv_prompt = Confirm.ask(f"{PROMPT} This will clear all {len(os.listdir('output'))} csv files, continue?")
    if clear_csv_prompt:
        shutil.rmtree('output', ignore_errors=True)
        xprint(f"{INFO} csv files cleared successfully!")
    else:
        pass


# View csv files
def view_csv():
    logging.info(viewing_csv)
    csv_files = os.listdir("output")
    csv_table = Table(show_header=True, header_style=header_title)
    csv_table.add_column("CSV", style="dim")
    csv_table.add_column("Size (bytes)")
    for csv_file in csv_files:
        csv_table.add_row(str(csv_file), str(os.path.getsize("output/" + csv_file)))
    xprint(csv_table)


# Read csv
def read_csv():
    if args.csv_file:
        csv_file = args.csv_file
    else:
        csv_file = Prompt.ask(f"{green}.csv {white}(filename){reset}")
    with open(os.path.join("output", csv_file), "r") as file:
        logging.info(reading.format(csv_file))
        text = Text(file.read())
        xprint(text)


# View logs
def view_logs():
    logging.info(viewing_logs)
    logs = os.listdir(".logs")
    logs_table = Table(show_header=True, header_style=header_title)
    logs_table.add_column("Log", style="dim")
    logs_table.add_column("Size (bytes)")
    for log in logs:
        logs_table.add_row(str(log), str(os.path.getsize(".logs/" + log)))
    xprint(logs_table)


# Read log
def read_log():
    if args.log_file:
        log_file = args.log_file
    else:
        log_file = Prompt.ask(f"{green}.log date{white} (eg. 2022-04-27 10:09:36AM){reset}")
    with open(os.path.join(".logs", log_file + ".log"), "r") as log:
        logging.info(reading.format(log_file))
        xprint("\n" + log.read())


# Delete log
def delete_log():
    if args.log_file:
        log_file = args.log_file
    else:
        log_file = Prompt.ask(f"{green}.log date{white} (eg. 2022-04-27 10:09:36AM){reset}")
    os.remove(os.path.join(".logs", log_file))
    logging.info(deleted.format(log_file))
    xprint(f"{POSITIVE} {deleted.format(log_file)}")


# Clear logs
def clear_logs():
    clear_logs_prompt = Confirm.ask(f"{PROMPT} This will clear all {len(os.listdir('output'))} log files and close the current session, continue?")
    if clear_logs_prompt:
        shutil.rmtree('.logs', ignore_errors=True)
        xprint(f"{INFO} .log files cleared successfully!")
        exit()
    else:
        pass


# Exit session
def exit_session():
    exit_prompt = Confirm.ask(f"{PROMPT} This will close the current session, continue?")
    if exit_prompt:
        logging.info(session_closed.format(datetime.now()))
        xprint(f"{INFO} {session_closed.format(datetime.now())}")
        exit()
    else:
        pass


# Clear screen
def clear_screen():
    # Using 'cls' on Windows machines to clear the screen,
    # otherwise, use 'clear'
    os.system('cls' if os.name == 'nt' else 'clear')


def about():
    about_text = f"""
    OCTOSUITE © 2023 Richard Mwewa
        
An advanced and lightning fast framework for gathering open-source intelligence on GitHub users and organizations.


Whats new in v{version_tag}?
[{green}IMPROVED{reset}] Added a subcommand to the 'user' commands, that will be used to get a user's email 'user:email' (CLI only)

Read the wiki: https://github.com/bellingcat/octosuite/wiki
GitHub REST API documentation: https://docs.github.com/rest
"""
    xprint(about_text)


def get_email_from_contributor(username, repo, contributor):
    response = requests.get(f"https://github.com/{username}/{repo}/commits?author={contributor}",
                            auth=HTTPBasicAuth(username, '')).text
    latest_commit = re.search(rf'href="/{username}/{repo}/commit/(.*?)"', response)
    if latest_commit:
        latest_commit = latest_commit.group(1)
    else:
        latest_commit = 'dummy'
    commit_details = requests.get(f"https://github.com/{username}/{repo}/commit/{latest_commit}.patch",
                                  auth=HTTPBasicAuth(username, '')).text
    email = re.search(r'<(.*)>', commit_details)
    if email:
        email = email.group(1)
    return email


class Octosuite:
    def __init__(self):
        # API endpoint
        self.endpoint = 'https://api.github.com'

        # A list of tuples mapping commands to their methods
        self.command_map = [('ls', list_dir_and_files),
                            ("exit", exit_session),
                            ("clear", clear_screen),
                            ("about", about),
                            ("author", self.author),
                            ("help", help_command),
                            ("help:source", source_command),
                            ("help:search", search_command),
                            ("help:user", user_command),
                            ("help:repo", repo_command),
                            ("help:logs", logs_command),
                            ("help:csv", csv_command),
                            ("help:org", org_command),
                            ("source", source),
                            ("source:tarball", self.download_tarball),
                            ("source:zipball", self.download_zipball),
                            ("org", org),
                            ("org:events", self.org_events),
                            ("org:profile", self.org_profile),
                            ("org:repos", self.org_repos),
                            ("org:member", self.org_member),
                            ("repo", repo),
                            ("repo:path_contents", self.path_contents),
                            ("repo:profile", self.repo_profile),
                            ("repo:contributors", self.repo_contributors),
                            ("repo:stargazers", self.repo_stargazers),
                            ("repo:forks", self.repo_forks),
                            ("repo:issues", self.repo_issues),
                            ("repo:releases", self.repo_releases),
                            ("user", user),
                            ("user:email", self.get_user_email),
                            ("user:repos", self.user_repos),
                            ("user:gists", self.user_gists),
                            ("user:orgs", self.user_orgs),
                            ("user:profile", self.user_profile),
                            ("user:events", self.user_events),
                            ("user:followers", self.user_followers),
                            ("user:follows", self.user_follows),
                            ("user:following", self.user_following),
                            ("user:subscriptions", self.user_subscriptions),
                            ("search", search),
                            ("search:users", self.users_search),
                            ("search:repos", self.repos_search),
                            ("search:topics", self.topics_search),
                            ("search:issues", self.issues_search),
                            ("search:commits", self.commits_search),
                            ("logs", logs),
                            ("logs:view", view_logs),
                            ("logs:read", read_log),
                            ("logs:delete", delete_log),
                            ("logs:clear", clear_logs),
                            ("csv", csv),
                            ("csv:view", view_csv),
                            ("csv:read", read_csv),
                            ("csv:delete", delete_csv),
                            ("csv:clear", clear_csv)]

        # Arguments map will be used to run Octosuite with argparse
        self.argument_map = [("user_profile", self.user_profile),
                             ("user_email", self.get_user_email),
                             ("user_repos", self.user_repos),
                             ("user_gists", self.user_gists),
                             ("user_orgs", self.user_orgs),
                             ("user_events", self.user_events),
                             ("user_subscriptions", self.user_subscriptions),
                             ("user_following", self.user_following),
                             ("user_followers", self.user_followers),
                             ("user_follows", self.user_follows),
                             ("users_search", self.users_search),
                             ("issues_search", self.issues_search),
                             ("commits_search", self.commits_search),
                             ("topics_search", self.topics_search),
                             ("repos_search", self.repos_search),
                             ("org_profile", self.org_profile),
                             ("org_repos", self.org_repos),
                             ("org_events", self.org_events),
                             ("org_member", self.org_member),
                             ("repo_profile", self.repo_profile),
                             ("repo_contributors", self.repo_contributors),
                             ("repo_stargazers", self.repo_stargazers),
                             ("repo_forks", self.repo_forks),
                             ("repo_issues", self.repo_issues),
                             ("repo_releases", self.repo_releases),
                             ("repo_path_contents", self.path_contents),
                             ("view_logs", view_logs),
                             ("read_log", read_log),
                             ("delete_log", delete_log),
                             ("clear_logs", clear_logs),
                             ("view_csv", view_csv),
                             ("read_csv", read_csv),
                             ("delete_csv", delete_csv),
                             ("clear_csv", clear_csv),
                             ("about", about),
                             ("author", self.author)]

        # Path attribute
        self.path_attrs = ['size', 'type', 'path', 'sha', 'html_url']
        # Path attribute dictionary
        self.path_attr_dict = {'size': 'Size (bytes)',
                               'type': 'Type',
                               'path': 'Path',
                               'sha': 'SHA',
                               'html_url': 'URL'}

        # Organization attributes
        self.org_attrs = ['avatar_url', 'login', 'id', 'node_id', 'email', 'description', 'blog', 'location',
                          'followers',
                          'following', 'twitter_username', 'public_gists', 'public_repos', 'type', 'is_verified',
                          'has_organization_projects', 'has_repository_projects', 'created_at', 'updated_at']
        # Organization attribute dictionary
        self.org_attr_dict = {'avatar_url': 'Profile Photo',
                              'login': 'Username',
                              'id': 'ID',
                              'node_id': 'Node ID',
                              'email': 'Email',
                              'description': 'About',
                              'location': 'Location',
                              'blog': 'Blog',
                              'followers': 'Followers',
                              'following': 'Following',
                              'twitter_username': 'Twitter handle',
                              'public_gists': 'Gists',
                              'public_repos': 'Repositories',
                              'type': 'Account type',
                              'is_verified': 'Is verified?',
                              'has_organization_projects': 'Has organization projects?',
                              'has_repository_projects': 'Has repository projects?',
                              'created_at': 'Created at',
                              'updated_at': 'Updated at'}

        # Repository attributes
        self.repo_attrs = ['id', 'description', 'forks', 'stargazers_count', 'watchers', 'license', 'default_branch',
                           'visibility',
                           'language', 'open_issues', 'topics', 'homepage', 'clone_url', 'ssh_url', 'fork',
                           'allow_forking',
                           'private', 'archived', 'has_downloads', 'has_issues', 'has_pages', 'has_projects',
                           'has_wiki',
                           'pushed_at', 'created_at', 'updated_at']
        # Repository attribute dictionary
        self.repo_attr_dict = {'id': 'ID',
                               'description': 'About',
                               'forks': 'Forks',
                               'stargazers_count': 'Stars',
                               'watchers': 'Watchers',
                               'license': 'License',
                               'default_branch': 'Branch',
                               'visibility': 'Visibility',
                               'language': 'Language(s)',
                               'open_issues': 'Open issues',
                               'topics': 'Topics',
                               'homepage': 'Homepage',
                               'clone_url': 'Clone URL',
                               'ssh_url': 'SSH URL',
                               'fork': 'Is fork?',
                               'allow_forking': 'Is forkable?',
                               'private': 'Is private?',
                               'archived': 'Is archived?',
                               'is_template': 'Is template?',
                               'has_wiki': 'Has wiki?',
                               'has_pages': 'Has pages?',
                               'has_projects': 'Has projects?',
                               'has_issues': 'Has issues?',
                               'has_downloads': 'Has downloads?',
                               'pushed_at': 'Pushed at',
                               'created_at': 'Created at',
                               'updated_at': 'Updated at'}

        # Repo releases attributes
        self.repo_releases_attrs = ['id', 'node_id', 'tag_name', 'target_commitish', 'assets', 'draft', 'prerelease',
                                    'created_at',
                                    'published_at']
        # Repo releases attribute dictionary
        self.repo_releases_attr_dict = {'id': 'ID',
                                        'node_id': 'Node ID',
                                        'tag_name': 'Tag',
                                        'target_commitish': 'Branch',
                                        'assets': 'Assets',
                                        'draft': 'Is draft?',
                                        'prerelease': 'Is prerelease?',
                                        'created_at': 'Created at',
                                        'published_at': 'Published at'}

        # Profile attributes
        self.profile_attrs = ['avatar_url', 'login', 'id', 'node_id', 'bio', 'blog', 'location', 'followers',
                              'following',
                              'twitter_username', 'public_gists', 'public_repos', 'company', 'hireable', 'site_admin',
                              'created_at',
                              'updated_at']
        # Profile attribute dictionary
        self.profile_attr_dict = {'avatar_url': 'Profile Photo',
                                  'login': 'Username',
                                  'id': 'ID',
                                  'node_id': 'Node ID',
                                  'bio': 'Bio',
                                  'blog': 'Blog',
                                  'location': 'Location',
                                  'followers': 'Followers',
                                  'following': 'Following',
                                  'twitter_username': 'Twitter Handle',
                                  'public_gists': 'Gists (public)',
                                  'public_repos': 'Repositories (public)',
                                  'company': 'Organization',
                                  'hireable': 'Is hireable?',
                                  'site_admin': 'Is site admin?',
                                  'created_at': 'Joined at',
                                  'updated_at': 'Updated at'}

        # User attributes
        self.user_attrs = ['avatar_url', 'id', 'node_id', 'gravatar_id', 'site_admin', 'type', 'html_url']
        # User attribute dictionary
        self.user_attr_dict = {'avatar_url': 'Profile Photo',
                               'id': 'ID',
                               'node_id': 'Node ID',
                               'gravatar_id': 'Gravatar ID',
                               'site_admin': 'Is site admin?',
                               'type': 'Account type',
                               'html_url': 'URL'}

        # Topic attributes
        self.topic_attrs = ['score', 'curated', 'featured', 'display_name', 'created_by', 'created_at', 'updated_at']
        # Topic attribute dictionary
        self.topic_attr_dict = {'score': 'Score',
                                'curated': 'Curated',
                                'featured': 'Featured',
                                'display_name': 'Display name',
                                'created_by': 'Created by',
                                'created_at': 'Created at',
                                'updated_at': 'Updated at'}

        # Gists attribute
        self.gists_attrs = ['node_id', 'description', 'comments', 'files', 'git_push_url', 'public', 'truncated',
                            'updated_at']
        # Gists attribute dictionary
        self.gists_attr_dict = {'node_id': 'Node ID',
                                'description': 'About',
                                'comments': 'Comments',
                                'files': 'Files',
                                'git_push_url': 'Git Push URL',
                                'public': 'Is public?',
                                'truncated': 'Is truncated?',
                                'updated_at': 'Updated at'}

        # Issue attributes
        self.issue_attrs = ['id', 'node_id', 'score', 'state', 'number', 'comments', 'milestone', 'assignee',
                            'assignees', 'labels',
                            'locked', 'draft', 'closed_at']
        # Issue attribute dict
        self.issue_attr_dict = {'id': 'ID',
                                'node_id': 'Node ID',
                                'score': 'Score',
                                'state': 'State',
                                'closed_at': 'Closed at',
                                'number': 'Number',
                                'comments': 'Comments',
                                'milestone': 'Milestone',
                                'assignee': 'Assignee',
                                'assignees': 'Assignees',
                                'labels': 'Labels',
                                'draft': 'Is draft?',
                                'locked': 'Is locked?',
                                'created_at': 'Created at'}

        # Repo issues attributes
        self.repo_issues_attrs = ['id', 'node_id', 'state', 'reactions', 'number', 'comments', 'milestone', 'assignee',
                                  'active_lock_reason', 'author_association', 'assignees', 'labels', 'locked',
                                  'closed_at',
                                  'created_at', 'updated_at']
        # Issue attribute dict
        self.repo_issues_attr_dict = {'id': 'ID',
                                      'node_id': 'Node ID',
                                      'number': 'Number',
                                      'state': 'State',
                                      'reactions': 'Reactions',
                                      'comments': 'Comments',
                                      'milestone': 'Milestone',
                                      'assignee': 'Assignee',
                                      'assignees': 'Assignees',
                                      'author_association': 'Author association',
                                      'labels': 'Labels',
                                      'locked': 'Is locked?',
                                      'active_lock_reason': 'Lock reason',
                                      'closed_at': 'Closed at',
                                      'created_at': 'Created at',
                                      'updated_at': 'Updated at'}

        # User organizations attributes
        self.user_orgs_attrs = ['avatar_url', 'id', 'node_id', 'url', 'description']
        self.user_orgs_attr_dict = {'avatar_url': 'Profile Photo',
                                    'id': 'ID',
                                    'node_id': 'Node ID',
                                    'url': 'URL',
                                    'description': 'About'}

        # Author dictionary
        self.author_dict = {'Alias': 'rly0nheart',
                            'Country': ':zambia: Zambia, Africa',
                            'About.me': 'https://about.me/rly0nheart',
                            'Buy Me A Coffee': 'https://buymeacoffee.com/189381184'}

    def get_repos_from_username(self, username):
        response = requests.get(f"{self.endpoint}/users/{username}/repos?per_page=100&sort=pushed",
                                auth=HTTPBasicAuth(username, '')).text
        repositories = re.findall(rf'"full_name":"{username}/(.*?)",.*?"fork":(.*?),', response)
        unforked_repos = []
        for repository in repositories:
            if repository[1] == 'false':
                unforked_repos.append(repository[0])
        return unforked_repos

    def get_user_email(self):
        if args.username:
            username = args.username
        else:
            username = Prompt.ask(f"{white}@{green}Username{reset}")
        repos = self.get_repos_from_username(username)
        for repo in repos:
            email = get_email_from_contributor(username, repo, username)
            if email:
                xprint(f"{username}: {email}")
                break

    # Fetching organization info
    def org_profile(self):
        if args.organization:
            organization = args.organization
        else:
            organization = Prompt.ask(f"{white}@{green}Organi[sz]ation{reset}")
        response = requests.get(f"{self.endpoint}/orgs/{organization}")
        if response.status_code == 404:
            xprint(f"{NEGATIVE} {org_not_found.format(organization)}")
        elif response.status_code == 200:
            org_profile_tree = Tree("\n{response.json()['name']}")
            for attr in self.org_attrs:
                org_profile_tree.add(f"{self.org_attr_dict[attr]}: {response.json()[attr]}")
            xprint(org_profile_tree)

            if args.log_csv or Confirm.ask(f"\n{PROMPT} {prompt_log_csv}"):
                log_org_profile(response)
        else:
            xprint(response.json())

    # Fetching user information
    def user_profile(self):
        if args.username:
            username = args.username
        else:
            username = Prompt.ask(f"{white}@{green}Username{reset}")
        response = requests.get(f"{self.endpoint}/users/{username}")
        if response.status_code == 404:
            xprint(f"{NEGATIVE} {user_not_found.format(username)}")
        elif response.status_code == 200:
            user_profile_tree = Tree(f"\n{response.json()['name']}")
            for attr in self.profile_attrs:
                user_profile_tree.add(f"{self.profile_attr_dict[attr]}: {response.json()[attr]}")
            xprint(user_profile_tree)

            # Logging output to a csv file
            if args.log_csv or Confirm.ask(f"\n{PROMPT} {prompt_log_csv}"):
                log_user_profile(response)
        else:
            xprint(response.json())

    # Fetching repository information
    def repo_profile(self):
        if args.repository and args.username and args.limit:
            repo_name = args.repository
            username = args.username
        else:
            repo_name = Prompt.ask(f"{white}%{green}Repository{reset}")
            username = Prompt.ask(f"{white}@{green}Username{reset}")
        response = requests.get(f"{self.endpoint}/repos/{username}/{repo_name}")
        if response.status_code == 404:
            xprint(f"{NEGATIVE} {repo_or_user_not_found.format(repo_name, username)}")
        elif response.status_code == 200:
            repo_profile_tree = Tree(f"\n{response.json()['full_name']}")
            for attr in self.repo_attrs:
                repo_profile_tree.add(f"{self.repo_attr_dict[attr]}: {response.json()[attr]}")
            xprint(repo_profile_tree)

            if args.log_csv or Confirm.ask(f"\n{PROMPT} {prompt_log_csv}"):
                log_repo_profile(response)
        else:
            xprint(response.json())

    # Get path contents
    def path_contents(self):
        if args.repository and args.username and args.path_name:
            repo_name = args.repository
            username = args.username
            path_name = args.path_name
        else:
            repo_name = Prompt.ask(f"{white}%{green}Repository{reset}")
            username = Prompt.ask(f"{white}@{green}Username{reset}")
            path_name = Prompt.ask("~/path/name ")
        response = requests.get(f"{self.endpoint}/repos/{username}/{repo_name}/contents/{path_name}")
        if response.status_code == 404:
            xprint(f"{NEGATIVE} {info_not_found.format(repo_name, username, path_name)}")
        elif response.status_code == 200:
            for content_count, content in enumerate(response.json(), start=1):
                path_contents_tree = Tree("\n" + content['name'])
                for attr in self.path_attrs:
                    path_contents_tree.add(f"{self.path_attr_dict[attr]}: {content[attr]}")
                xprint(path_contents_tree)
                log_repo_path_contents(content, repo_name)
                xprint(INFO, f"Found {content_count} file(s) in {repo_name}/{path_name}.")
        else:
            xprint(response.json())

    # repo contributors
    def repo_contributors(self):
        if args.repository and args.username and args.limit:
            repo_name = args.repository
            username = args.username
            limit = args.limit
        else:
            repo_name = Prompt.ask(f"{white}%{green}Repository{reset}")
            username = Prompt.ask(f"{white}@{green}Username{reset}")
            limit = Prompt.ask(limit_output.format("contributors"))
        response = requests.get(f"{self.endpoint}/repos/{username}/{repo_name}/contributors?per_page={limit}")
        if response.status_code == 404:
            xprint(f"{NEGATIVE} {repo_or_user_not_found.format(repo_name, username)}")
        elif response.status_code == 200:
            for contributor in response.json():
                contributor_tree = Tree("\n" + contributor['login'])
                for attr in self.user_attrs:
                    contributor_tree.add(f"{self.user_attr_dict[attr]}: {contributor[attr]}")
                xprint(contributor_tree)

                if args.log_csv or Confirm.ask(f"\n{PROMPT} {prompt_log_csv}"):
                    log_repo_contributors(contributor, repo_name)
            else:
                xprint(response.json())

    # repo stargazers
    def repo_stargazers(self):
        if args.repository and args.username and args.limit:
            repo_name = args.repository
            username = args.username
            limit = args.limit
        else:
            repo_name = Prompt.ask(f"{white}%{green}Repository{reset}")
            username = Prompt.ask(f"{white}@{green}Username{reset}")
            limit = Prompt.ask(limit_output.format("stargazers"))
        response = requests.get(f"{self.endpoint}/repos/{username}/{repo_name}/stargazers?per_page={limit}")
        if response.status_code == 404:
            xprint(f"{NEGATIVE} {repo_or_user_not_found.format(repo_name, username)}")
        elif response.json() == {}:
            xprint(f"{NEGATIVE} Repository does not have any stargazers -> ({repo_name})")
        elif response.status_code == 200:
            for stargazer in response.json():
                stargazer_tree = Tree("\n" + stargazer['login'])
                for attr in self.user_attrs:
                    stargazer_tree.add(f"{self.user_attr_dict[attr]}: {stargazer[attr]}")
                xprint(stargazer_tree)
                
                if args.log_csv or Confirm.ask(f"\n{PROMPT} {prompt_log_csv}"):
                    log_repo_stargazers(stargazer, repo_name)
        else:
            xprint(response.json())

    # repo forks
    def repo_forks(self):
        if args.repository and args.username and args.limit:
            repo_name = args.repository
            username = args.username
            limit = args.limit
        else:
            repo_name = Prompt.ask(f"{white}%{green}Repository{reset}")
            username = Prompt.ask(f"{white}@{green}Username{reset}")
            limit = Prompt.ask(limit_output.format("forks"))
        response = requests.get(f"{self.endpoint}/repos/{username}/{repo_name}/forks?per_page={limit}")
        if response.status_code == 404:
            xprint(f"{NEGATIVE} {repo_or_user_not_found.format(repo_name, username)}")
        elif response.json() == {}:
            xprint(f"{NEGATIVE} Repository does not have forks -> ({repo_name})")
        elif response.status_code == 200:
            for count, fork in enumerate(response.json()):
                fork_tree = Tree("\n" + fork['full_name'])
                for attr in self.repo_attrs:
                    fork_tree.add(f"{self.repo_attr_dict[attr]}: {fork[attr]}")
                xprint(fork_tree)

                if args.log_csv or Confirm.ask(f"\n{PROMPT} {prompt_log_csv}"):
                    log_repo_forks(fork, count)
        else:
            xprint(response.json())

    # Repo issues
    def repo_issues(self):
        if args.repository and args.username and args.limit:
            repo_name = args.repository
            username = args.username
            limit = args.limit
        else:
            repo_name = Prompt.ask(f"{white}%{green}Repository{reset}")
            username = Prompt.ask(f"{white}@{green}Username{reset}")
            limit = Prompt.ask(limit_output.format("issues"))
        response = requests.get(f"{self.endpoint}/repos/{username}/{repo_name}/issues?per_page={limit}")
        if response.status_code == 404:
            xprint(f"{NEGATIVE} {repo_or_user_not_found.format(repo_name, username)}")
        elif not response.json():
            xprint(f"{NEGATIVE} Repository does not have open issues -> ({repo_name})")
        elif response.status_code == 200:
            for issue in response.json():
                issues_tree = Tree("\n" + issue['title'])
                for attr in self.repo_issues_attrs:
                    issues_tree.add(f"{self.repo_issues_attr_dict[attr]}: {issue[attr]}")
                xprint(issues_tree)
                xprint(issue['body'])
                log_repo_issues(issue, repo_name)
        else:
            xprint(response.json())

    # Repo releases
    def repo_releases(self):
        if args.repository and args.username and args.limit:
            repo_name = args.repository
            username = args.username
            limit = args.limit
        else:
            repo_name = Prompt.ask(f"{white}%{green}Repository{reset}")
            username =  Prompt.ask(f"{white}@{green}Username{reset}")
            limit = Prompt.ask(limit_output.format("repository releases"))
        response = requests.get(f"{self.endpoint}/repos/{username}/{repo_name}/releases?per_page={limit}")
        if response.status_code == 404:
            xprint(f"{NEGATIVE} {repo_or_user_not_found.format(repo_name, username)}")
        elif not response.json():
            xprint(f"{NEGATIVE} Repository does not have releases -> ({repo_name})")
        elif response.status_code == 200:
            for release in response.json():
                releases_tree = Tree("\n" + release['name'])
                for attr in self.repo_releases_attrs:
                    releases_tree.add(f"{self.repo_releases_attr_dict[attr]}: {release[attr]}")
                xprint(releases_tree)
                xprint(release['body'])

                if args.log_csv or Confirm.ask(f"\n{PROMPT} {prompt_log_csv}"):
                    log_repo_releases(release, repo_name)
        else:
            xprint(response.json())

    # Fetching organization repositories
    def org_repos(self):
        if args.organization and args.limit:
            organization = args.organization
            limit = args.limit
        else:
            organization = Prompt.ask(f"{white}@{green}Organi[sz]ation{reset}")
            limit = Prompt.ask(limit_output.format("organization repositories"))
        response = requests.get(f"{self.endpoint}/orgs/{organization}/repos?per_page={limit}")
        if response.status_code == 404:
            xprint(f"{NEGATIVE} {org_not_found.format(organization)}")
        elif response.status_code == 200:
            for repository in response.json():
                repos_tree = Tree("\n" + repository['full_name'])
                for attr in self.repo_attrs:
                    repos_tree.add(f"{self.repo_attr_dict[attr]}: {repository[attr]}")
                xprint(repos_tree)
                
                if args.log_csv or Prompt.ask(f"{PROMPT} {prompt_log_csv}") == "yes":
                    log_org_repos(repository, organization)
        else:
            xprint(response.json())

    # organization events
    def org_events(self):
        if args.organization and args.limit:
            organization = args.organization
            limit = args.limit
        else:
            organization = Prompt.ask(f"{white}@{green}Organi[sz]ation{reset}")
            limit = Prompt.ask(limit_output.format("organization events"))
        response = requests.get(f"{self.endpoint}/orgs/{organization}/events?per_page={limit}")
        if response.status_code == 404:
            xprint(f"{NEGATIVE} {org_not_found.format(organization)}")
        elif response.status_code == 200:
            for event in response.json():
                events_tree = Tree("\n" + event['id'])
                events_tree.add(f"Type: {event['type']}")
                events_tree.add(f"Created at: {event['created_at']}")
                xprint(events_tree)
                xprint(event['payload'])
            # log_org_events(event, organization)
        else:
            xprint(response.json())

    # organization member
    def org_member(self):
        if args.organization and args.username:
            organization = args.organization
            username = args.username
        else:
            organization = Prompt.ask(f"{white}@{green}Organi[sz]ation{reset}")
            username = Prompt.ask(f"{white}@{green}Username{reset}")
        response = requests.get(f"{self.endpoint}/orgs/{organization}/public_members/{username}")
        if response.status_code == 204:
            xprint(f"{POSITIVE} User ({username}) is a public member of the organization -> ({organization})")
        else:
            xprint(f"{NEGATIVE} {response.json()['message']}")

    # Fetching user repositories
    def user_repos(self):
        if args.username and args.limit:
            username = args.username
            limit = args.limit
        else:
            username = Prompt.ask(f"{white}@{green}Username{reset}")
            limit = Prompt.ask(limit_output.format("repositories"))
        response = requests.get(f"{self.endpoint}/users/{username}/repos?per_page={limit}")
        if response.status_code == 404:
            xprint(f"{NEGATIVE} {user_not_found.format(username)}")
        elif response.status_code == 200:
            for repository in response.json():
                repos_tree = Tree("\n" + repository['full_name'])
                for attr in self.repo_attrs:
                    repos_tree.add(f"{self.repo_attr_dict[attr]}: {repository[attr]}")
                xprint(repos_tree)

                if args.log_csv or Confirm.ask(f"\n{PROMPT} {prompt_log_csv}"):
                    log_user_repos(repository, username)
        else:
            xprint(response.json())

    # Fetching user's gists
    def user_gists(self):
        if args.username and args.limit:
            username = args.username
            limit = args.limit
        else:
            username = Prompt.ask(f"{white}@{green}Username{reset}")
            limit = Prompt.ask(limit_output.format('gists'))
        response = requests.get(f"{self.endpoint}/users/{username}/gists?per_page={limit}")
        if not response.json():
            xprint(f"{NEGATIVE} User does not have gists.")
        elif response.status_code == 404:
            xprint(f"{NEGATIVE} {user_not_found.format(username)}")
        elif response.status_code == 200:
            for gist in response.json():
                gists_tree = Tree("\n" + gist['id'])
                for attr in self.gists_attrs:
                    gists_tree.add(f"{self.gists_attr_dict[attr]}: {gist[attr]}")
                xprint(gists_tree)
                
                if args.log_csv or Confirm.ask(f"\n{PROMPT} {prompt_log_csv}"):
                    log_user_gists(gist)
        else:
            xprint(response.json())

    # Fetching a list of organizations that a user owns or belongs to
    def user_orgs(self):
        if args.username and args.limit:
            username = args.username
            limit = args.limit
        else:
            username = Prompt.ask(f"{white}@{green}Username{reset}")
            limit = Prompt.ask(limit_output.format("user organizations"))
        response = requests.get(f"{self.endpoint}/users/{username}/orgs?per_page={limit}")
        if not response.json():
            xprint(f"{NEGATIVE} User ({username}) does not (belong to/own) any organizations.")
        elif response.status_code == 404:
            xprint(f"{NEGATIVE} {user_not_found.format(username)}")
        elif response.status_code == 200:
            for organization in response.json():
                org_tree = Tree("\n" + organization['login'])
                for attr in self.user_orgs_attrs:
                    org_tree.add(f"{self.user_orgs_attr_dict[attr]}: {organization[attr]}")
                xprint(org_tree)
                
                if args.log_csv or Confirm.ask(f"\n{PROMPT} {prompt_log_csv}"):
                    log_user_orgs(organization, username)
        else:
            xprint(response.json())

    # Fetching a users events 
    def user_events(self):
        if args.username and args.limit:
            username = args.username
            limit = args.limit
        else:
            username = Prompt.ask(f"{white}@{green}Username{reset}")
            limit = Prompt.ask(limit_output.format("events"))
        response = requests.get(f"{self.endpoint}/users/{username}/events/public?per_page={limit}")
        if response.status_code == 404:
            xprint(f"{NEGATIVE} {user_not_found.format(username)}")
        elif response.status_code == 200:
            for event in response.json():
                events_tree = Tree("\n" + event['id'])
                events_tree.add(f"Actor: {event['actor']['login']}")
                events_tree.add(f"Type: {event['type']}")
                events_tree.add(f"Repository: {event['repo']['name']}")
                events_tree.add(f"Created at: {event['created_at']}")
                xprint(events_tree)
                xprint(event['payload'])
                log_user_events(event)
        else:
            xprint(response.json())

    # Fetching a target user's subscriptions
    def user_subscriptions(self):
        if args.username and args.limit:
            username = args.username
            limit = args.limit
        else:
            username = Prompt.ask(f"{white}@{green}Username{reset}")
            limit = Prompt.ask(limit_output.format("user subscriptions"))
        response = requests.get(f"{self.endpoint}/users/{username}/subscriptions?per_page={limit}")
        if not response.json():
            xprint(f"{NEGATIVE} User does not have any subscriptions.")
        elif response.status_code == 404:
            xprint(f"{NEGATIVE} {user_not_found.format(username)}")
        elif response.status_code == 200:
            for repository in response.json():
                subscriptions_tree = Tree("\n" + repository['full_name'])
                for attr in self.repo_attrs:
                    subscriptions_tree.add(f"{self.repo_attr_dict[attr]}: {repository[attr]}")
                xprint(subscriptions_tree)
                
                if args.log_csv or Confirm.ask(f"\n{PROMPT} {prompt_log_csv}"):
                    log_user_subscriptions(repository, username)
        else:
            xprint(response.json())

    # Fetching a list of users the target follows        
    def user_following(self):
        if args.username and args.limit:
            username = args.username
            limit = args.limit
        else:
            username = Prompt.ask(f"{white}@{green}Username{reset}")
            limit = Prompt.ask(limit_output.format("user' following"))
        response = requests.get(f"{self.endpoint}/users/{username}/following?per_page={limit}")
        if not response.json():
            xprint(f"{NEGATIVE} User ({username})does not follow anyone.")
        elif response.status_code == 404:
            xprint(f"{NEGATIVE} {user_not_found.format(username)}")
        elif response.status_code == 200:
            for user in response.json():
                following_tree = Tree("\n" + user['login'])
                for attr in self.user_attrs:
                    following_tree.add(f"{self.user_attr_dict[attr]}: {user[attr]}")
                xprint(following_tree)
                
                if args.log_csv or Confirm.ask(f"\n{PROMPT} {prompt_log_csv}"):
                    log_user_following(user, username)
        else:
            xprint(response.json())

    # Fetching user's followers
    def user_followers(self):
        if args.username and args.limit:
            username = args.username
            limit = args.limit
        else:
            username = Prompt.ask(f"{white}@{green}Username{reset}")
            limit = Prompt.ask(limit_output.format("user followers"))
        response = requests.get(f"{self.endpoint}/users/{username}/followers?per_page={limit}")
        if not response.json():
            xprint(f"{NEGATIVE} User ({username})does not have followers.")
        elif response.status_code == 404:
            xprint(f"{NEGATIVE} {user_not_found.format(username)}")
        elif response.status_code == 200:
            for follower in response.json():
                followers_tree = Tree("\n" + follower['login'])
                for attr in self.user_attrs:
                    followers_tree.add(f"{self.user_attr_dict[attr]}: {follower[attr]}")
                xprint(followers_tree)
                
                if args.log_csv or Confirm.ask(f"\n{PROMPT} {prompt_log_csv}"):
                    log_user_followers(follower, username)
        else:
            xprint(response.json())

    # Checking whether user[A] follows user[B]
    def user_follows(self):
        if args.username and args.username_b:
            user_a = args.username
            user_b = args.username_b
        else:
            user_a = Prompt.ask(f"{white}@{green}User_A{reset}")
            user_b = Prompt.ask(f"{white}@{green}User_B{reset}")
        response = requests.get(f"{self.endpoint}/users/{user_a}/following/{user_b}")
        if response.status_code == 204:
            xprint(f"{POSITIVE} @{user_a} FOLLOWS @{user_b}")
        else:
            xprint(f"{NEGATIVE} @{user_a} DOES NOT FOLLOW @{user_b}")

    # User search
    def users_search(self):
        if args.query and args.limit and args.limit:
            query = args.query
            limit = args.limit
        else:
            query = Prompt.ask(f"{white}@{green}Username{reset} (search)")
            limit = Prompt.ask(limit_output.format("user search"))
        response = requests.get(f"{self.endpoint}/search/users?q={query}&per_page={limit}").json()
        for user in response['items']:
            users_search_tree = Tree("\n" + user['login'])
            for attr in self.user_attrs:
                users_search_tree.add(f"{self.user_attr_dict[attr]}: {user[attr]}")
            xprint(users_search_tree)
            
            if args.log_csv or Confirm.ask(f"\n{PROMPT} {prompt_log_csv}"):
                log_users_search(user, query)

    # Repository search
    def repos_search(self):
        if args.query and args.limit:
            query = args.query
            limit = args.limit
        else:
            query = Prompt.ask(f"{white}%{green}Repository{reset} (search)")
            limit = Prompt.ask(limit_output.format("repositor[y][ies] search"))
        response = requests.get(f"{self.endpoint}/search/repositories?q={query}&per_page={limit}").json()
        for repository in response['items']:
            repos_search_tree = Tree("\n" + repository['full_name'])
            for attr in self.repo_attrs:
                repos_search_tree.add(f"{self.repo_attr_dict[attr]}: {repository[attr]}")
            xprint(repos_search_tree)
            
            if args.log_csv or Confirm.ask(f"\n{PROMPT} {prompt_log_csv}"):
                log_repos_search(repository, query)

    # Topics search
    def topics_search(self):
        if args.query and args.limit:
            query = args.query
            limit = args.limit
        else:
            query = Prompt.ask(f"{white}:{green}Topics{reset} (search)")
            limit = Prompt.ask(limit_output.format("topic(s) search"))
        response = requests.get(f"{self.endpoint}/search/topics?q={query}&per_page={limit}").json()
        for topic in response['items']:
            topics_search_tree = Tree("\n" + topic['name'])
            for attr in self.topic_attrs:
                topics_search_tree.add(f"{self.topic_attr_dict[attr]}: {topic[attr]}")
            xprint(topics_search_tree)
            
            if args.log_csv or Confirm.ask(f"\n{PROMPT} {prompt_log_csv}"):
                log_topics_search(topic, query)

    # Issue search
    def issues_search(self):
        if args.query and args.limit:
            query = args.query
            limit = args.limit
        else:
            query = Prompt.ask(f"{white}!{green}Issues{reset} (search)")
            limit = Prompt.ask(limit_output.format("issue(s) search"))
        response = requests.get(f"{self.endpoint}/search/issues?q={query}&per_page={limit}").json()
        for issue in response['items']:
            issues_search_tree = Tree("\n" + issue['title'])
            for attr in self.repo_issues_attrs:
                issues_search_tree.add(f"{self.repo_issues_attr_dict[attr]}: {issue[attr]}")
            xprint(issues_search_tree)
            xprint(issue['body'])
            
            if args.log_csv or Confirm.ask(f"\n{PROMPT} {prompt_log_csv}"):
                log_issues_search(issue, query)

    # Commits search
    def commits_search(self):
        if args.query and args.limit:
            query = args.query
            limit = args.limit
        else:
            query = Prompt.ask(f"{white};{green}Commits{reset} (search)")
            limit = Prompt.ask(limit_output.format("commit(s) search"))
        response = requests.get(f"{self.endpoint}/search/commits?q={query}&per_page={limit}").json()
        for commit in response['items']:
            commits_search_tree = Tree("\n" + commit['commit']['tree']['sha'])
            commits_search_tree.add(f"Author: {commit['commit']['author']['name']}")
            commits_search_tree.add(f"Username: {commit['author']['login']}")
            commits_search_tree.add(f"Email: {commit['commit']['author']['email']}")
            commits_search_tree.add(f"Commiter: {commit['commit']['committer']['name']}")
            commits_search_tree.add(f"Repository: {commit['repository']['full_name']}")
            commits_search_tree.add(f"URL: {commit['html_url']}")
            xprint(commits_search_tree)
            xprint(commit['commit']['message'])
            
            if args.log_csv or Confirm.ask(f"\n{PROMPT} {prompt_log_csv}"):
                log_commits_search(commit, query)

    # Downloading release tarball
    def download_tarball(self):
        logging.info(file_downloading.format(f"octosuite.v{version_tag}.tar"))
        xprint(INFO, file_downloading.format(f"octosuite.v{version_tag}.tar"))
        data = requests.get(f"{self.endpoint}/repos/bellingcat/octosuite/tarball/{version_tag}")
        with open(os.path.join("downloads", f"octosuite.v{version_tag}.tar"), "wb") as file:
            file.write(data.content)
            file.close()

        logging.info(file_downloaded.format(f"octosuite.v{version_tag}.tar"))
        xprint(POSITIVE, file_downloaded.format(f"octosuite.v{version_tag}.tar"))

    # Downloading release zip ball
    def download_zipball(self):
        logging.info(file_downloading.format(f"octosuite.v{version_tag}.zip"))
        xprint(INFO, file_downloading.format(f"octosuite.v{version_tag}.zip"))
        data = requests.get(f"{self.endpoint}/repos/rly0nheart/octosuite/zipball/{version_tag}")
        with open(os.path.join("downloads", f"octosuite.v{version_tag}.zip"), "wb") as file:
            file.write(data.content)
            file.close()

        logging.info(file_downloaded.format(f"octosuite.v{version_tag}.zip"))
        xprint(POSITIVE, file_downloaded.format(f"octosuite.v{version_tag}.zip"))

    # Author info
    def author(self):
        author_tree = Tree(f"{white}Richard Mwewa (Ritchie){reset}")
        for author_key, author_value in self.author_dict.items():
            author_tree.add(f"{white}{author_key}:{reset} {author_value}")
        xprint(author_tree)
