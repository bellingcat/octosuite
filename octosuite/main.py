#!usr/bin/python

import os 
import sys
import logging
import getpass
import requests
import platform
import subprocess
from rich.table import Table
from datetime import datetime
from rich import print as xprint
from octosuite.helper import Help
from octosuite.sign_vars import SignVar
from octosuite.log_roller import logRoller
from octosuite.csv_loggers import csvLogger
from octosuite.banner import name_logo, version_tag
from octosuite.colors import red, white, green, white_bold, green_bold, header_title, reset

# API endpoint
endpoint = 'https://api.github.com'
# Path attribute
path_attrs = ['size', 'type', 'path', 'sha', 'html_url']
# Path attribute dictionary
path_attr_dict = {'size': 'Size (bytes)',
                  'type': 'Type',
                  'path': 'Path',
                  'sha': 'SHA',
                  'html_url': 'URL'}


# Organization attributes
org_attrs = ['avatar_url', 'login', 'id', 'node_id', 'email', 'description', 'blog', 'location', 'followers',
             'following', 'twitter_username', 'public_gists', 'public_repos', 'type', 'is_verified',
             'has_organization_projects', 'has_repository_projects', 'created_at', 'updated_at']
# Organization attribute dictionary
org_attr_dict = {'avatar_url': 'Profile Photo',
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
repo_attrs = ['id', 'description', 'forks', 'stargazers_count', 'watchers', 'license', 'default_branch', 'visibility',
              'language', 'open_issues', 'topics', 'homepage', 'clone_url', 'ssh_url', 'fork', 'allow_forking',
              'private', 'archived', 'has_downloads', 'has_issues', 'has_pages', 'has_projects', 'has_wiki',
              'pushed_at', 'created_at', 'updated_at']
# Repository attribute dictionary
repo_attr_dict = {'id': 'ID',
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
repo_releases_attrs = ['id', 'node_id', 'tag_name', 'target_commitish', 'assets', 'draft', 'prerelease', 'created_at',
                       'published_at']
# Repo releases attribute dictionary
repo_releases_attr_dict = {'id': 'ID',
                           'node_id': 'Node ID',
                           'tag_name': 'Tag',
                           'target_commitish': 'Branch',
                           'assets': 'Assets',
                           'draft': 'Is draft?',
                           'prerelease': 'Is prerelease?',
                           'created_at': 'Created at',
                           'published_at': 'Published at'}


# Profile attributes
profile_attrs = ['avatar_url', 'login', 'id', 'node_id', 'bio', 'blog', 'location', 'followers', 'following',
                 'twitter_username', 'public_gists', 'public_repos', 'company', 'hireable', 'site_admin', 'created_at',
                 'updated_at']
# Profile attribute dictionary
profile_attr_dict = {'avatar_url': 'Profile Photo',
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
user_attrs = ['avatar_url', 'id', 'node_id', 'gravatar_id', 'site_admin', 'type', 'html_url']
# User attribute dictionary
user_attr_dict = {'avatar_url': 'Profile Photo',
                  'id': 'ID',
                  'node_id': 'Node ID',
                  'gravatar_id': 'Gravatar ID',
                  'site_admin': 'Is site admin?',
                  'type': 'Account type',
                  'html_url': 'URL'}


# Topic atrributes
topic_attrs = ['score', 'curated', 'featured', 'display_name', 'created_by', 'created_at', 'updated_at']
# Topic attribute dictionary
topic_attr_dict = {'score': 'Score',
                   'curated': 'Curated',
                   'featured': 'Featured',
                   'display_name': 'Display name',
                   'created_by': 'Created by',
                   'created_at': 'Created at',
                   'updated_at': 'Updated at'}


# Gists attributes
gists_attrs = ['node_id', 'description', 'comments', 'files', 'git_push_url', 'public', 'truncated', 'updated_at']
# Gists attribute dictionary
gists_attr_dict = {'node_id': 'Node ID',
                   'description': 'About',
                   'comments': 'Comments',
                   'files': 'Files',
                   'git_push_url': 'Git Push URL',
                   'public': 'Is public?',
                   'truncated': 'Is truncated?',
                   'updated_at': 'Updated at'}


# Issue attributes
issue_attrs = ['id', 'node_id', 'score', 'state', 'number', 'comments', 'milestone', 'assignee', 'assignees', 'labels',
               'locked', 'draft', 'closed_at']
# Issue attribute dict
issue_attr_dict = {'id': 'ID',
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
repo_issues_attrs = ['id', 'node_id', 'state', 'reactions', 'number', 'comments', 'milestone', 'assignee',
                     'active_lock_reason', 'author_association', 'assignees', 'labels', 'locked', 'closed_at',
                     'created_at', 'updated_at']
# Issue attribute dict
repo_issues_attr_dict = {'id': 'ID',
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
user_orgs_attrs = ['avatar_url', 'id', 'node_id', 'url', 'description']
user_orgs_attr_dict = {'avatar_url': 'Profile Photo',
                       'id': 'ID',
                       'node_id': 'Node ID',
                       'url': 'URL',
                       'description': 'About'}


# Author dictionary
author_dict = {'Alias': 'rly0nheart',
               'Country': ':zambia: Zambia, Africa',
               'About.me': 'https://about.me/rly0nheart',
               'Buy Me A Coffee': 'https://buymeacoffee.com/189381184'}


'''
pathFinder()
This function is responsible for creating/checking the availability of  the (.logs, output, downloads) folders,
enabling logging to automatically log network/user activity to a file,
and logging the start of a session.
'''


def pathFinder():

    """
    Here we create/check 3 directories (.logs, output, downloads) on startup
    If they exist, we ignore, otherwise, we create them
    """

    directory_list = ['.logs', 'output', 'downloads']
    for directory in directory_list:
        os.makedirs(directory, exist_ok=True)

    '''
    Configure logging to log activities to a file, which will be named by the date and time a session was opened.
    '''
    now = datetime.now()
    now_formatted = now.strftime("%Y-%m-%d %H-%M-%S%p")
    logging.basicConfig(filename=f".logs/{now_formatted}.log", format="[%(asctime)s] [%(levelname)s] %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S%p", level=logging.DEBUG)
    # Log the start of a session
    logging.info(logRoller.sessionOpened.format(platform.node(), getpass.getuser()))


'''
onStart()
This is the main function, responsible for mapping commands, calling other functions, and catching exceptions
'''


def onStart():
    pathFinder()
    # A list of tuples mapping commands to their functions
    command_map = [("exit", exitSession),
                   ("clear", clearScreen),
                   ("about", about),
                   ("author", author),
                   ("help", Help.helpCommand),
                   ("help:version", Help.versionCommand),
                   ("help:source", Help.sourceCommand),
                   ("help:search", Help.searchCommand),
                   ("help:user", Help.userCommand),
                   ("help:repo", Help.repoCommand),
                   ("help:logs", Help.logsCommand),
                   ("help:csv", Help.csvCommand),
                   ("help:org", Help.orgCommand),
                   ("version", Help.Version),
                   ("version:info", versionInfo),
                   ("version:check", versionCheck),
                   ("source", Help.Source),
                   ("source:tarball", downloadTarball),
                   ("source:zipball", downloadZipball),
                   ("org", Help.Org),
                   ("org:events", orgEvents),
                   ("org:profile", orgProfile),
                   ("org:repos", orgRepos),
                   ("org:member", orgMember),
                   ("repo", Help.Repo),
                   ("repo:path_contents", pathContents),
                   ("repo:profile", repoProfile),
                   ("repo:contributors", repoContributors),
                   ("repo:stargazers", repoStargazers),
                   ("repo:forks", repoForks),
                   ("repo:issues", repoIssues),
                   ("repo:releases", repoReleases),
                   ("user", Help.User),
                   ("user:repos", userRepos),
                   ("user:gists", userGists),
                   ("user:orgs", userOrgs),
                   ("user:profile", userProfile),
                   ("user:events", userEvents),
                   ("user:followers", userFollowers),
                   ("user:follows", userFollows),
                   ("user:following", userFollowing),
                   ("user:subscriptions", userSubscriptions),
                   ("search", Help.Search),
                   ("search:users", userSearch),
                   ("search:repos", repoSearch),
                   ("search:topics", topicSearch),
                   ("search:issues", issueSearch),
                   ("search:commits", commitsSearch),
                   ("logs", Help.Logs),
                   ("logs:view", viewLogs),
                   ("logs:read", readLog),
                   ("logs:delete", deleteLog),
                   ("csv", Help.Csv),
                   ("csv:view", viewCsv),
                   ("csv:read", readCsv),
                   ("csv:delete", deleteCsv)]

    
    xprint(name_logo)
    '''
    Main loop keeps octosuite running, this will break if Octosuite detects a KeyboardInterrupt (Ctrl+C)
    or if the 'exit' command is entered.
    '''
    while True:
        try:
            xprint(
                f"{white}┌──({red}{getpass.getuser()}{white}@{red}octosuite{white})\n├──[~{green}{os.getcwd()}{white}]\n└╼ {reset}",
                end="")
            command_input = input().lower()
            print("\n")
            '''
            Iterating over the command_map and check if the user input matches any command in it [command_map],
            if there's a match, we return its function. If no match is found, we ignore it.
            '''
            for command, function in command_map:
                if command_input == command:
                    function()
                    print("\n")
                else:
                    pass

        # This catches the KeyboardInterrupt exception (Ctrl+C)
        except KeyboardInterrupt:
            logging.warning(logRoller.Ctrl.format("Ctrl+C"))
            xprint(f"{SignVar.warning} {logRoller.Ctrl.format('Ctrl+C')}")
            break

        # This initially catches all exceptions (except the KeyboardInterrupt)
        except Exception as e:
            logging.error(logRoller.Error.format(e))
            xprint(f"{SignVar.error} {logRoller.Error.format(e)}")

        # Fetching organization info


def orgProfile():
    xprint(f"{white}>> @{green}Organization {white}(username){reset} ", end="")
    organization = input()
    response = requests.get(f"{endpoint}/orgs/{organization}")
    if response.status_code == 404:
        xprint(f"{SignVar.negative} {logRoller.orgNotFound.format(organization)}")
    elif response.status_code == 200:
        xprint(f"\n{white}{response.json()['name']}{reset}")
        for attr in org_attrs:
            xprint(f"{white}├─ {org_attr_dict[attr]}:{reset} {response.json()[attr]}")
        csvLogger.logOrgProfile(response)
    else:
        xprint(response.json())


# Fetching user information        
def userProfile():
    xprint(f"{white}>> @{green}Username{reset} ", end="")
    username = input()
    response = requests.get(f"{endpoint}/users/{username}")
    if response.status_code == 404:
        xprint(f"{SignVar.negative} {logRoller.userNotFound.format(username)}")
    elif response.status_code == 200:
        xprint(f"\n{white}{response.json()['name']}{reset}")
        for attr in profile_attrs:
            xprint(f"{white}├─ {profile_attr_dict[attr]}:{reset} {response.json()[attr]}")
        csvLogger.logUserProfile(response)
    else:
        xprint(response.json())


# Fetching repository information   	
def repoProfile():
    xprint(f"{white}>> %{green}Repository{reset} ", end="")
    repo_name = input()
    xprint(f"{white}>> @{green}Owner{white} (username) ", end="")
    username = input()
    response = requests.get(f"{endpoint}/repos/{username}/{repo_name}")
    if response.status_code == 404:
        xprint(f"{SignVar.negative} {logRoller.repoOrUserNotFound.format(repo_name, username)}")
    elif response.status_code == 200:
        xprint(f"\n{white}{response.json()['full_name']}{reset}")
        for attr in repo_attrs:
            xprint(f"{white}├─ {repo_attr_dict[attr]}:{reset} {response.json()[attr]}")
        csvLogger.logRepoProfile(response)
    else:
        xprint(response.json())


# Get path contents        
def pathContents():
    xprint(f"{white}>> %{green}Repository{reset} ", end="")
    repo_name = input()
    xprint(f"{white}>> @{green}Owner{white} (username) ", end="")
    username = input()
    xprint(f"{white}>> ~{green}/path/name{reset} ", end="")
    path_name = input()
    response = requests.get(f"{endpoint}/repos/{username}/{repo_name}/contents/{path_name}")
    if response.status_code == 404:
        xprint(f"{SignVar.negative} {logRoller.infoNotFound.format(repo_name, username, path_name)}")
    elif response.status_code == 200:
        content_count = 0
        for content in response.json():
            content_count += 1
            xprint(f"\n{white}{content['name']}{reset}")
            for attr in path_attrs:
                xprint(f"{white}├─ {path_attr_dict[attr]}:{reset} {content[attr]}")
            csvLogger.logRepoPathContents(content, repo_name)
        xprint(SignVar.info, f"Found {content_count} file(s) in {repo_name}/{path_name}.")
    else:
        xprint(response.json())


# repo contributors
def repoContributors():
    xprint(f"{white}>> %{green}Repository{reset} ", end="")
    repo_name = input()
    xprint(f"{white}>> @{green}Owner{white} (username) ", end="")
    username = input()
    xprint(SignVar.prompt, logRoller.limitInput.format("contributors"), end="")
    limit = int(input())
    response = requests.get(f"{endpoint}/repos/{username}/{repo_name}/contributors?per_page={limit}")
    if response.status_code == 404:
        xprint(f"{SignVar.negative} {logRoller.repoOrUserNotFound.format(repo_name, username)}")
    elif response.status_code == 200:
        for contributor in response.json():
            xprint(f"\n{white}{contributor['login']}{reset}")
            for attr in user_attrs:
                xprint(f"{white}├─ {user_attr_dict[attr]}:{reset} {contributor[attr]}")
            csvLogger.logRepoContributors(contributor, repo_name)
    else:
        xprint(response.json())


# repo stargazers
def repoStargazers():
    xprint(f"{white}>> %{green}Repository{reset} ", end="")
    repo_name = input()
    xprint(f"{white}>> @{green}Owner{white} (username){reset} ", end="")
    username = input()
    xprint(SignVar.prompt, logRoller.limitInput.format("repository stargazers"), end="")
    limit = int(input())
    response = requests.get(f"{endpoint}/repos/{username}/{repo_name}/stargazers?per_page={limit}")
    if response.status_code == 404:
        xprint(f"{SignVar.negative} {logRoller.repoOrUserNotFound.format(repo_name, username)}")
    elif response.json() == {}:
        xprint(f"{SignVar.negative} Repository does not have any stargazers -> ({repo_name})")
    elif response.status_code == 200:
        for stargazer in response.json():
            xprint(f"\n{white}{stargazer['login']}{reset}")
            for attr in user_attrs:
                xprint(f"{white}├─ {user_attr_dict[attr]}:{reset} {stargazer[attr]}")
            csvLogger.logRepoStargazers(stargazer, repo_name)
    else:
        xprint(response.json())


# repo forks
def repoForks():
    xprint(f"{white}>> %{green}Repository{reset} ", end="")
    repo_name = input()
    xprint(f"{white}>> @{green}Owner{white} (username){reset} ", end="")
    username = input()
    xprint(SignVar.prompt, logRoller.limitInput.format("repository forks"), end="")
    limit = int(input())
    response = requests.get(f"{endpoint}/repos/{username}/{repo_name}/forks?per_page={limit}")
    if response.status_code == 404:
        xprint(f"{SignVar.negative} {logRoller.repoOrUserNotFound.format(repo_name, username)}")
    elif response.json() == {}:
        xprint(f"{SignVar.negative} Repository does not have forks -> ({repo_name})")
    elif response.status_code == 200:
        count = 0
        for fork in response.json():
            count += 1
            xprint(f"\n{white}{fork['full_name']}{reset}")
            for attr in repo_attrs:
                xprint(f"{white}├─ {repo_attr_dict[attr]}:{reset} {fork[attr]}")
            csvLogger.logRepoForks(fork, count)
    else:
        xprint(response.json())


# Repo issues
def repoIssues():
    xprint(f"{white}>> %{green}Repository{reset} ", end="")
    repo_name = input()
    xprint(f"{white}>> @{green}Owner{white} (username){reset} ", end="")
    username = input()
    xprint(SignVar.prompt, logRoller.limitInput.format("repository issues"), end="")
    limit = int(input())
    response = requests.get(f"{endpoint}/repos/{username}/{repo_name}/issues?per_page={limit}")
    if response.status_code == 404:
        xprint(f"{SignVar.negative} {logRoller.repoOrUserNotFound.format(repo_name, username)}")
    elif response.json() == []:
        xprint(f"{SignVar.negative} Repository does not have open issues -> ({repo_name})")
    elif response.status_code == 200:
        for issue in response.json():
            xprint(f"\n{white}{issue['title']}{reset}")
            for attr in repo_issues_attrs:
                xprint(f"{white}├─ {repo_issues_attr_dict[attr]}:{reset} {issue[attr]}")
            xprint(issue['body'])
            csvLogger.logRepoIssues(issue, repo_name)
    else:
        xprint(response.json())


# Repo releases
def repoReleases():
    xprint(f"{white}>> %{green}Repository{reset} ", end="")
    repo_name = input()
    xprint(f"{white}>> @{green}Owner{white} (username){reset} ", end="")
    username = input()
    xprint(SignVar.prompt, logRoller.limitInput.format("repository releases"), end="")
    limit = int(input())
    response = requests.get(f"{endpoint}/repos/{username}/{repo_name}/releases?per_page={limit}")
    if response.status_code == 404:
        xprint(f"{SignVar.negative} {logRoller.repoOrUserNotFound.format(repo_name, username)}")
    elif response.json() == []:
        xprint(f"{SignVar.negative} Repository does not have releases -> ({repo_name})")
    elif response.status_code == 200:
        for release in response.json():
            xprint(f"\n{white}{release['name']}{reset}")
            for attr in repo_releases_attrs:
                xprint(f"{white}├─ {repo_releases_attr_dict[attr]}:{reset} {release[attr]}")
            xprint(release['body'])
            csvLogger.logRepoReleases(release, repo_name)
    else:
        xprint(response.json())


# Fetching organization repositories        
def orgRepos():
    xprint(f"{white}>> @{green}Organization{white} (username){reset} ", end="")
    organization = input()
    xprint(SignVar.prompt, logRoller.limitInput.format("organization repositories"), end="")
    limit = int(input())
    response = requests.get(f"{endpoint}/orgs/{organization}/repos?per_page={limit}")
    if response.status_code == 404:
        xprint(f"{SignVar.negative} {logRoller.orgNotFound.format(organization)}")
    elif response.status_code == 200:
        for repository in response.json():
            xprint(f"\n{white}{repository['full_name']}{reset}")
            for attr in repo_attrs:
                xprint(f"{white}├─ {repo_attr_dict[attr]}:{reset} {repository[attr]}")
            csvLogger.logOrgRepos(repository, organization)
    else:
        xprint(response.json())


# organization events        
def orgEvents():
    xprint(f"{white}>> @{green}Organization{white} (username){reset} ", end="")
    organization = input()
    xprint(SignVar.prompt, logRoller.limitInput.format("organization repositories"), end="")
    limit = int(input())
    response = requests.get(f"{endpoint}/orgs/{organization}/events?per_page={limit}")
    if response.status_code == 404:
        xprint(f"{SignVar.negative} {logRoller.orgNotFound.format(organization)}")
    elif response.status_code == 200:
        for event in response.json():
            xprint(f"\n{white}{event['id']}{reset}")
            xprint(f"{white}├─ Type:{reset} {event['type']}\n{white}├─ Created at:{reset} {event['created_at']}")
            xprint(event['payload'])
        csvLogger.logOrgEvents(event, organization)
    else:
        xprint(response.json())


# organization member        	
def orgMember():
    xprint(f"{white}>> @{green}Organization{white} (username){reset} ", end="")
    organization = input()
    xprint(f"{white}>> @{green}Username{reset} ", end="")
    username = input()
    response = requests.get(f"{endpoint}/orgs/{organization}/public_members/{username}")
    if response.status_code == 204:
        xprint(f"{SignVar.positive} User ({username}) is a public member of the organization -> ({organization})")
    else:
        xprint(f"{SignVar.negative} {response.json()['message']}")


# Fetching user repositories        
def userRepos():
    xprint(f"{white}>> @{green}Username{reset} ", end="")
    username = input()
    xprint(SignVar.prompt, logRoller.limitInput.format("repositories"), end="")
    limit = int(input())
    response = requests.get(f"{endpoint}/users/{username}/repos?per_page={limit}")
    if response.status_code == 404:
        xprint(f"{SignVar.negative} {logRoller.userNotFound.format(username)}")
    elif response.status_code == 200:
        for repository in response.json():
            xprint(f"\n{white}{repository['full_name']}{reset}")
            for attr in repo_attrs:
                xprint(f"{white}├─ {repo_attr_dict[attr]}:{reset} {repository[attr]}")
            csvLogger.logUserRepos(repository, username)
    else:
        xprint(response.json())


# Fetching user's gists
def userGists():
    xprint(f"{white}>> @{green}Username{reset} ", end="")
    username = input()
    xprint(SignVar.prompt, logRoller.limitInput.format('gists'), end="")
    limit = int(input())
    response = requests.get(f"{endpoint}/users/{username}/gists?per_page={limit}")
    # xprint(response.json())
    if response.json() == []:
        xprint(f"{SignVar.negative} User does not have gists.")
    elif response.status_code == 404:
        xprint(f"{SignVar.negative} {logRoller.userNotFound.format(username)}")
    elif response.status_code == 200:
        for gist in response.json():
            xprint(f"\n{white}{gist['id']}{reset}")
            for attr in gists_attrs:
                xprint(f"{white}├─ {gists_attr_dict[attr]}:{reset} {gist[attr]}")
            csvLogger.logUserGists(gist)
    else:
        xprint(response.json())

        	

# Fetching a list of organizations that a user owns or belongs to        	
def userOrgs():
    xprint(f"{white}>> @{green}Username{reset} ", end="")
    username = input()
    xprint(SignVar.prompt, logRoller.limitInput.format("user organizations"), end="")
    limit = int(input())
    response = requests.get(f"{endpoint}/users/{username}/orgs?per_page={limit}")
    if response.json() == []:
        xprint(f"{SignVar.negative} User ({username}) does not (belong to/own) any organizations.")
    elif response.status_code == 404:
        xprint(f"{SignVar.negative} {logRoller.userNotFound.format(username)}")
    elif response.status_code == 200:
        for organization in response.json():
            print(f"\n{white}{organization['login']}{reset}")
            for attr in user_orgs_attrs:
                xprint(f"{white}├─ {user_orgs_attr_dict[attr]}:{reset} {organization[attr]}")
            csvLogger.logUserOrgs(organization, username)
    else:
        xprint(response.json())


# Fetching a users events 
def userEvents():
    xprint(f"{white}>> @{green}Username{reset} ", end="")
    username = input()
    xprint(SignVar.prompt, logRoller.limitInput.format("events"), end="")
    limit = int(input())
    response = requests.get(f"{endpoint}/users/{username}/events/public?per_page={limit}")
    if response.status_code == 404:
        xprint(f"{SignVar.negative} {logRoller.userNotFound.format(username)}")
    elif response.status_code == 200:
        for event in response.json():
            xprint(f"\n{white}{event['id']}{reset}")
            xprint(f"{white}├─ Actor:{reset} {event['actor']['login']}")
            xprint(f"{white}├─ Type:{reset} {event['type']}")
            xprint(f"{white}├─ Repository:{reset} {event['repo']['name']}")
            xprint(f"{white}├─ Created at:{reset} {event['created_at']}")
            xprint(event['payload'])
            csvLogger.logUserEvents(event)
    else:
        xprint(response.json())


# Fetching a target user's subscriptions 
def userSubscriptions():
    xprint(f"{white}>> @{green}Username{reset} ", end="")
    username = input().lower()
    xprint(SignVar.prompt, logRoller.limitInput.format("user subscriptions"), end="")
    limit = int(input())
    response = requests.get(f"{endpoint}/users/{username}/subscriptions?per_page={limit}")
    if response.json() == []:
        xprint(f"{SignVar.negative} User does not have any subscriptions.")
    elif response.status_code == 404:
        xprint(f"{SignVar.negative} {logRoller.userNotFound.format(username)}")
    elif response.status_code == 200:
        for repository in response.json():
            xprint(f"\n{white}{repository['full_name']}{reset}")
            for attr in repo_attrs:
                xprint(f"{white}├─ {repo_attr_dict[attr]}:{reset} {repository[attr]}")
            csvLogger.logUserSubscriptions(repository, username)
    else:
        xprint(response.json())


# Fetching a list of users the target follows        
def userFollowing():
    xprint(f"{white}>> @{green}Username{reset} ", end="")
    username = input().lower()
    xprint(SignVar.prompt, logRoller.limitInput.format("user' following"), end="")
    limit = int(input())
    response = requests.get(f"{endpoint}/users/{username}/following?per_page={limit}")
    if response.json() == []:
        xprint(f"{SignVar.negative} User ({username})does not follow anyone.")
    elif response.status_code == 404:
        xprint(f"{SignVar.negative} {logRoller.userNotFound.format(username)}")
    elif response.status_code == 200:
        for user in response.json():
            xprint(f"\n{white}@{user['login']}{reset}")
            for attr in user_attrs:
                xprint(f"{white}├─ {user_attr_dict[attr]}:{reset} {user[attr]}")
            csvLogger.logUserFollowing(user, username)
    else:
        xprint(response.json())


# Fetching user's followers
def userFollowers():
    xprint(f"{white}>> @{green}Username{reset} ", end="")
    username = input().lower()
    xprint(SignVar.prompt, logRoller.limitInput.format("user followers"), end="")
    limit = int(input())
    response = requests.get(f"{endpoint}/users/{username}/followers?per_page={limit}")
    if response.json() == []:
        xprint(f"{SignVar.negative} User ({username})does not have followers.")
    elif response.status_code == 404:
        xprint(f"{SignVar.negative} {logRoller.userNotFound.format(username)}")
    elif response.status_code == 200:
        for follower in response.json():
            xprint(f"\n{white}@{follower['login']}{reset}")
            for attr in user_attrs:
                xprint(f"{white}├─ {user_attr_dict[attr]}:{reset} {follower[attr]}")
            csvLogger.logUserFollowers(follower, username)
    else:
        xprint(response.json())


# Checking whether user[A] follows user[B]
def userFollows():
    xprint(f"{white}>> @{green}user{white}(A) (username){reset} ", end="")
    user_a = input()
    xprint(f"{white}>> @{green}user{white}(B) (username){reset} ", end="")
    user_b = input()
    response = requests.get(f"{endpoint}/users/{user_a}/following/{user_b}")
    if response.status_code == 204:
        xprint(f"{SignVar.positive} @{user_a} FOLLOWS @{user_b}")
    else:
        xprint(f"{SignVar.negative} @{user_a} DOES NOT FOLLOW @{user_b}")

    # User search    	    


def userSearch():
    xprint(f"{white}>> @{green}Query{white} (eg. john){reset} ", end="")
    query = input()
    xprint(SignVar.prompt, logRoller.limitInput.format("user search"), end="")
    limit = int(input())
    response = requests.get(f"{endpoint}/search/users?q={query}&per_page={limit}").json()
    for user in response['items']:
        xprint(f"\n{white}@{user['login']}{reset}")
        for attr in user_attrs:
            xprint(f"{white}├─ {user_attr_dict[attr]}:{reset} {user[attr]}")
        csvLogger.logUserSearch(user, query)


# Repository search
def repoSearch():
    xprint(f"{white}>> %{green}Query{white} (eg. git){reset} ", end="")
    query = input()
    xprint(SignVar.prompt, logRoller.limitInput.format("repositor[y][ies] search"), end="")
    limit = int(input())
    response = requests.get(f"{endpoint}/search/repositories?q={query}&per_page={limit}").json()
    for repository in response['items']:
        xprint(f"\n{white}{repository['full_name']}{reset}")
        for attr in repo_attrs:
            xprint(f"{white}├─ {repo_attr_dict[attr]}:{reset} {repository[attr]}")
        csvLogger.logRepoSearch(repository, query)


# Topics search
def topicSearch():
    xprint(f"{white}>> #{green}Query{white} (eg. osint){reset} ", end="")
    query = input()
    xprint(SignVar.prompt, logRoller.limitInput.format("topic(s) search"), end="")
    limit = int(input())
    response = requests.get(f"{endpoint}/search/topics?q={query}&per_page={limit}").json()
    for topic in response['items']:
        xprint(f"\n{white}{topic['name']}{reset}")
        for attr in topic_attrs:
            xprint(f"{white}├─ {topic_attr_dict[attr]}:{reset} {topic[attr]}")
        csvLogger.logTopicSearch(topic, query)


# Issue search
def issueSearch():
    xprint(f"{white}>> !{green}Query{white} (eg. error){reset} ", end="")
    query = input()
    xprint(SignVar.prompt, logRoller.limitInput.format("issue(s) search"), end="")
    limit = int(input())
    response = requests.get(f"{endpoint}/search/issues?q={query}&per_page={limit}").json()
    for issue in response['items']:
        xprint(f"\n\n{white}{issue['title']}{reset}")
        for attr in repo_issues_attrs:
            xprint(f"{white}├─ {repo_issues_attr_dict[attr]}:{reset} {issue[attr]}")
        xprint(issue['body'])
        csvLogger.logIssueSearch(issue, query)


# Commits search
def commitsSearch():
    xprint(f"{white}>> :{green}Query{white} (eg. filename:index.php){reset} ", end="")
    query = input()
    xprint(SignVar.prompt, logRoller.limitInput.format("commit(s) search"), end="")
    limit = int(input())
    response = requests.get(f"{endpoint}/search/commits?q={query}&per_page={limit}").json()
    for commit in response['items']:
        xprint(f"\n{white}{commit['commit']['tree']['sha']}{reset}")
        xprint(f"{white}├─ Author:{reset} {commit['commit']['author']['name']}")
        xprint(f"{white}├─ Username:{reset} {commit['author']['login']}")
        xprint(f"{white}├─ Email:{reset} {commit['commit']['author']['email']}")
        xprint(f"{white}├─ Commiter:{reset} {commit['commit']['committer']['name']}")
        xprint(f"{white}├─ Repository:{reset} {commit['repository']['full_name']}")
        xprint(f"{white}├─ URL:{reset} {commit['html_url']}")
        xprint(commit['commit']['message'])
        csvLogger.logCommitsSearch(commit, query)


# View csv files    	
def viewCsv():
    logging.info(logRoller.viewingCsv)
    csv_files = os.listdir("output")
    csv_table = Table(show_header=True, header_style=header_title)
    csv_table.add_column("CSV", style="dim", width=12)
    csv_table.add_column("Size (bytes)")
    for csv_file in csv_files:
        csv_table.add_row(str(csv_file), str(os.path.getsize("output/" + csv_file)))
    xprint(csv_table)


# Read a specified csv file    
def readCsv():
    xprint(f"{white}>> {green}.csv {reset}(filename) ", end="")
    csv_file = input()
    with open(f"output/{csv_file}.csv", "r") as file:
        logging.info(logRoller.readingCsv.format(csv_file))
        xprint("\n" + file.read())


# Delete a specified csv file    
def deleteCsv():
    xprint(f"{white}>> {green}.csv {reset}filename{reset} ", end="")
    csv_file = input()
    os.remove(f'output/{csv_file}')
    logging.info(logRoller.deletedCsv.format(csv_file))
    xprint(f"{SignVar.positive} {logRoller.deletedCsv.format(csv_file)}")


# View octosuite log files    	
def viewLogs():
    logging.info(logRoller.viewingLogs)
    logs = os.listdir(".logs")
    logs_table = Table(show_header=True, header_style=header_title)
    logs_table.add_column("Log", style="dim", width=12)
    logs_table.add_column("Size (bytes)")
    for log in logs:
        logs_table.add_row(str(log), str(os.path.getsize(".logs/" + log)))
    xprint(logs_table)


# Read a specified log file    
def readLog():
    xprint(f"{white}>> {green}.log date{reset} (eg. 2022-04-27 10:09:36AM) ", end="")
    log_file = input()
    with open(f".logs/{log_file}.log", "r") as log:
        logging.info(logRoller.readingLog.format(log_file))
        xprint("\n" + log.read())


# Delete a specified log file    
def deleteLog():
    xprint(f"{white}>> {green}.log date{reset} (eg. 2022-04-27 10:09:36AM) ", end="")
    log_file = input()
    os.remove(f'.logs/{log_file}')
    logging.info(logRoller.deletedLog.format(log_file))
    xprint(f"{SignVar.positive} {logRoller.deletedLog.format(log_file)}")


# Downloading release tarball
def downloadTarball():
    logging.info(logRoller.fileDownloading.format(f"octosuite.v{version_tag}.tar"))
    xprint(SignVar.info, logRoller.fileDownloading.format(f"octosuite.v{version_tag}.tar"))
    data = requests.get(f"{endpoint}/repos/rly0nheart/octosuite/tarballball/{version_tag}")
    with open(f"downloads/octosuite.v{version_tag}.tar", "wb") as file:
        file.write(data.content)
        file.close()

    logging.info(logRoller.fileDownloaded.format(f"octosuite.v{version_tag}.tar"))
    xprint(SignVar.positive, logRoller.fileDownloaded.format(f"octosuite.v{version_tag}.tar"))


# Downloading release zipball
def downloadZipball():
    logging.info(logRoller.fileDownloading.format(f"octosuite.v{version_tag}.zip"))
    xprint(SignVar.info, logRoller.fileDownloading.format(f"octosuite.v{version_tag}.zip"))
    data = requests.get(f"{endpoint}/repos/rly0nheart/octosuite/zipball/{version_tag}")
    with open(f"downloads/octosuite.v{version_tag}.zip", "wb") as file:
        file.write(data.content)
        file.close()

    logging.info(logRoller.fileDownloaded.format(f"octosuite.v{version_tag}.zip"))
    xprint(SignVar.positive, logRoller.fileDownloaded.format(f"octosuite.v{version_tag}.zip"))


def versionCheck():
    response = requests.get(f"{endpoint}/repos/rly0nheart/octosuite/releases/latest")
    if response.json()['tag_name'] == version_tag:
        xprint(f"{SignVar.positive} Octosuite is up to date. Check again soon! :)")
    else:
        xprint(
            f"{SignVar.info} A new release is available (octosuite.v{response.json()['tag_name']}). Exit Octosuite and run '{green_bold}pip install --upgrade octosuite{white}' to download and install the update.")


# Author info
def author():
    xprint(f"{white}Richard Mwewa (Ritchie){reset}")
    for key, value in author_dict.items():
        xprint(f"{white}├─ {key}:{reset} {value}")


# About program
def about():
    xprint(f"""
     {white_bold}OCTOSUITE © 2022 Richard Mwewa{reset}
        
An advanced and lightning fast framework for gathering open-source intelligence on GitHub users and organizations.
With over 20+ features, Octosuite only runs on 2 external dependencies, and returns the gathered intelligence in a highly readable format.

'_This is how you gather GitHub OSINT like a god:fire:_'

{white_bold}Read the wiki:{reset} https://github.com/rly0nheart/octosuite/wiki
{white_bold}GitHub REST API documentation:{reset} https://docs.github.com/rest
""")


# Close session 	
def exitSession():
    xprint(f"{SignVar.prompt} This will close the current session, continue? (Y/n) ", end="")
    prompt = input().lower()
    if prompt == 'y':
        logging.info(logRoller.sessionClosed.format(datetime.now()))
        xprint(f"{SignVar.info} {logRoller.sessionClosed.format(datetime.now())}")
        exit()
    else:
        pass


# Clear screen    
def clearScreen():
    """
    We use 'cls' on Windows machines to clear the screen,
    otherwise, we use 'clear'
    """
    if sys.platform.lower().startswith("win"):
        os.system('cls')
    else:
        subprocess.run(['clear'], shell=False)


# Show version information
def versionInfo():
    # Yes... the changelog is hard coded lol
    xprint(f"""
{white_bold}Whats new in v{version_tag}?{reset}
[ {green}fixed{reset}  ] [ Errno 22 ] Invalid argument (on Windows machines)
[ {green}fixed{reset}  ] [ Error 2 ] The system cannot find the file specified (on Windows machines)
""")
