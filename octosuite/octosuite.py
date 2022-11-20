#!usr/bin/python

import os 
import sys
import shutil
import logging
import getpass
import requests
import platform
from rich.text import Text
from rich.tree import Tree
from rich.table import Table
from datetime import datetime
from rich import print as xprint
from octosuite.helper import Help
from octosuite.sign_vars import SignVar
from octosuite.log_roller import logRoller
from octosuite.csv_loggers import csvLogger
from octosuite.banner import name_logo, version_tag
from octosuite.colors import red, white, green, white_bold, green_bold, header_title, reset


class Octosuite:
    def __init__(self):
        # API endpoint
        self.endpoint = 'https://api.github.com'
        
        # A list of tuples mapping commands to their methods
        self.command_map = [("exit", self.exitSession),
                   ("clear", self.clearScreen),
                   ("about", self.about),
                   ("author", self.author),
                   ("help", Help.helpCommand),
                   ("help:source", Help.sourceCommand),
                   ("help:search", Help.searchCommand),
                   ("help:user", Help.userCommand),
                   ("help:repo", Help.repoCommand),
                   ("help:logs", Help.logsCommand),
                   ("help:csv", Help.csvCommand),
                   ("help:org", Help.orgCommand),
                   ("source", Help.Source),
                   ("source:tarball", self.downloadTarball),
                   ("source:zipball", self.downloadZipball),
                   ("org", Help.Org),
                   ("org:events", self.orgEvents),
                   ("org:profile", self.orgProfile),
                   ("org:repos", self.orgRepos),
                   ("org:member", self.orgMember),
                   ("repo", Help.Repo),
                   ("repo:path_contents", self.pathContents),
                   ("repo:profile", self.repoProfile),
                   ("repo:contributors", self.repoContributors),
                   ("repo:stargazers", self.repoStargazers),
                   ("repo:forks", self.repoForks),
                   ("repo:issues", self.repoIssues),
                   ("repo:releases", self.repoReleases),
                   ("user", Help.User),
                   ("user:repos", self.userRepos),
                   ("user:gists", self.userGists),
                   ("user:orgs", self.userOrgs),
                   ("user:profile", self.userProfile),
                   ("user:events", self.userEvents),
                   ("user:followers", self.userFollowers),
                   ("user:follows", self.userFollows),
                   ("user:following", self.userFollowing),
                   ("user:subscriptions", self.userSubscriptions),
                   ("search", Help.Search),
                   ("search:users", self.userSearch),
                   ("search:repos", self.repoSearch),
                   ("search:topics", self.topicSearch),
                   ("search:issues", self.issueSearch),
                   ("search:commits", self.commitsSearch),
                   ("logs", Help.Logs),
                   ("logs:view", self.viewLogs),
                   ("logs:read", self.readLog),
                   ("logs:delete", self.deleteLog),
                   ("logs:clear", self.clearLogs),
                   ("csv", Help.Csv),
                   ("csv:view", self.viewCsv),
                   ("csv:read", self.readCsv),
                   ("csv:delete", self.deleteCsv),
                   ("csv:clear", self.clearCsv)]

        # Path attribute
        self.path_attrs = ['size', 'type', 'path', 'sha', 'html_url']
        # Path attribute dictionary
        self.path_attr_dict = {'size': 'Size (bytes)',
                  'type': 'Type',
                  'path': 'Path',
                  'sha': 'SHA',
                  'html_url': 'URL'}
                  
                  
        # Organization attributes
        self.org_attrs = ['avatar_url', 'login', 'id', 'node_id', 'email', 'description', 'blog', 'location', 'followers',
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
        self.repo_attrs = ['id', 'description', 'forks', 'stargazers_count', 'watchers', 'license', 'default_branch', 'visibility',
              'language', 'open_issues', 'topics', 'homepage', 'clone_url', 'ssh_url', 'fork', 'allow_forking',
              'private', 'archived', 'has_downloads', 'has_issues', 'has_pages', 'has_projects', 'has_wiki',
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
        self.repo_releases_attrs = ['id', 'node_id', 'tag_name', 'target_commitish', 'assets', 'draft', 'prerelease', 'created_at',
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
        self.profile_attrs = ['avatar_url', 'login', 'id', 'node_id', 'bio', 'blog', 'location', 'followers', 'following',
                 'twitter_username', 'public_gists', 'public_repos', 'company', 'hireable', 'site_admin', 'created_at',
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
                  
                  
        # Topic atrributes
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
        self.gists_attrs = ['node_id', 'description', 'comments', 'files', 'git_push_url', 'public', 'truncated', 'updated_at']
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
        self.issue_attrs = ['id', 'node_id', 'score', 'state', 'number', 'comments', 'milestone', 'assignee', 'assignees', 'labels',
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
                     'active_lock_reason', 'author_association', 'assignees', 'labels', 'locked', 'closed_at',
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
               
               
    """
    pathFinder()
    This method is responsible for creating/checking the availability of  the (.logs, output, downloads) folders,
    enabling logging to automatically log network/user activity to a file,
    and logging the start of a session.
    """
    def pathFinder(self):
        """
        Check 3 directories (.logs, output, downloads) on startup
        If they exist, ignore, otherwise, create them
        """
        directory_list = ['.logs', 'output', 'downloads']
        for directory in directory_list:
            os.makedirs(directory, exist_ok=True)
                  
          
    """
    Configure logging and check for updates
    """
    def configure_logging(self):
        """
        Configure logging to log activities to a file, which will be named by the date and time a session was opened.
        """
        now = datetime.now()
        now_formatted = now.strftime("%Y-%m-%d %H-%M-%S%p")
        logging.basicConfig(filename=f".logs/{now_formatted}.log", format="[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S%p", level=logging.DEBUG)
        # Log the start of a session
        logging.info(logRoller.sessionOpened.format(platform.node(), getpass.getuser()))
              
          
    """
    Check for updates
    """      
    def check_updates(self):
        response = requests.get("https://api.github.com/repos/bellingcat/octosuite/releases/latest").json()
        if response['tag_name'] == version_tag:
            """
            Ignore if the program is up to date
            """
            pass
        else:
            xprint(f"{SignVar.info} A new release of Octosuite is available ({response['tag_name']}). Run 'pip install --upgrade octosuite' to get the updates.\n")
                  
                  
    """
    onStart()
    This is the main method, responsible for mapping commands, calling other methods, and catching exceptions
    """
    def onStart(self):
        self.pathFinder()
        self.clearScreen()
        self.configure_logging()
        self.check_updates()
        xprint(name_logo)
              
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
            for command, method in self.command_map:
                if command_input == command:
                    method()
                    print("\n")
                else:
                    pass
                
                
    # Fetching organization info
    def orgProfile(self):
        xprint(f"{white}>> @{green}Organization {white}(username){reset} ", end="")
        organization = input()
        response = requests.get(f"{self.endpoint}/orgs/{organization}")
        if response.status_code == 404:
            xprint(f"{SignVar.negative} {logRoller.orgNotFound.format(organization)}")
        elif response.status_code == 200:
            org_profile_tree = Tree("\n" + response.json()['name'])
            for attr in self.org_attrs:
                org_profile_tree.add(f"{self.org_attr_dict[attr]}: {response.json()[attr]}")
            xprint(org_profile_tree)
            csvLogger.logOrgProfile(response)
        else:
            xprint(response.json())
            
            
    # Fetching user information
    def userProfile(self):
        xprint(f"{white}>> @{green}Username{reset} ", end="")
        username = input()
        response = requests.get(f"{self.endpoint}/users/{username}")
        if response.status_code == 404:
            xprint(f"{SignVar.negative} {logRoller.userNotFound.format(username)}")
        elif response.status_code == 200:
            user_profile_tree = Tree("\n" + response.json()['name'])
            for attr in self.profile_attrs:
                user_profile_tree.add(f"{self.profile_attr_dict[attr]}: {response.json()[attr]}")
            xprint(user_profile_tree)
            csvLogger.logUserProfile(response)
        else:
            xprint(response.json())
            
            
    # Fetching repository information
    def repoProfile(self):
        xprint(f"{white}>> %{green}Repository{reset} ", end="")
        repo_name = input()
        xprint(f"{white}>> @{green}Owner{white} (username) ", end="")
        username = input()
        response = requests.get(f"{self.endpoint}/repos/{username}/{repo_name}")
        if response.status_code == 404:
            xprint(f"{SignVar.negative} {logRoller.repoOrUserNotFound.format(repo_name, username)}")
        elif response.status_code == 200:
            repo_profile_tree = Tree("\n" + response.json()['full_name'])
            for attr in self.repo_attrs:
                repo_profile_tree.add(f"{self.repo_attr_dict[attr]}: {response.json()[attr]}")
            xprint(repo_profile_tree)
            csvLogger.logRepoProfile(response)
        else:
            xprint(response.json())
            
            
    # Get path contents
    def pathContents(self):
        xprint(f"{white}>> %{green}Repository{reset} ", end="")
        repo_name = input()
        xprint(f"{white}>> @{green}Owner{white} (username) ", end="")
        username = input()
        xprint(f"{white}>> ~{green}/path/name{reset} ", end="")
        path_name = input()
        response = requests.get(f"{self.endpoint}/repos/{username}/{repo_name}/contents/{path_name}")
        if response.status_code == 404:
            xprint(f"{SignVar.negative} {logRoller.infoNotFound.format(repo_name, username, path_name)}")
        elif response.status_code == 200:
            for content_count, content in enumerate(response.json(), start=1):
                path_contents_tree = Tree("\n" + content['name'])
                for attr in self.path_attrs:
                    path_contents_tree.add(f"{self.path_attr_dict[attr]}: {content[attr]}")
                xprint(path_contents_tree)
                csvLogger.logRepoPathContents(content, repo_name)
            xprint(SignVar.info, f"Found {content_count} file(s) in {repo_name}/{path_name}.")
        else:
            xprint(response.json())
            
            
    # repo contributors
    def repoContributors(self):
        xprint(f"{white}>> %{green}Repository{reset} ", end="")
        repo_name = input()
        xprint(f"{white}>> @{green}Owner{white} (username) ", end="")
        username = input()
        xprint(SignVar.prompt, logRoller.limitInput.format("contributors"), end="")
        limit = int(input())
        response = requests.get(f"{self.endpoint}/repos/{username}/{repo_name}/contributors?per_page={limit}")
        if response.status_code == 404:
            xprint(f"{SignVar.negative} {logRoller.repoOrUserNotFound.format(repo_name, username)}")
        elif response.status_code == 200:
            for contributor in response.json():
                contributor_tree = Tree("\n" + contributor['login'])
                for attr in self.user_attrs:
                    contributor_tree.add(f"{self.user_attr_dict[attr]}: {contributor[attr]}")
                xprint(contributor_tree)
                csvLogger.logRepoContributors(contributor, repo_name)
            else:
                xprint(response.json())
                
                
    # repo stargazers
    def repoStargazers(self):
        xprint(f"{white}>> %{green}Repository{reset} ", end="")
        repo_name = input()
        xprint(f"{white}>> @{green}Owner{white} (username){reset} ", end="")
        username = input()
        xprint(SignVar.prompt, logRoller.limitInput.format("repository stargazers"), end="")
        limit = int(input())
        response = requests.get(f"{self.endpoint}/repos/{username}/{repo_name}/stargazers?per_page={limit}")
        if response.status_code == 404:
            xprint(f"{SignVar.negative} {logRoller.repoOrUserNotFound.format(repo_name, username)}")
        elif response.json() == {}:
            xprint(f"{SignVar.negative} Repository does not have any stargazers -> ({repo_name})")
        elif response.status_code == 200:
            for stargazer in response.json():
                stargazer_tree = Tree("\n" + stargazer['login'])
                for attr in self.user_attrs:
                    stargazer_tree.add(f"{self.user_attr_dict[attr]}: {stargazer[attr]}")
                xprint(stargazer_tree)
                csvLogger.logRepoStargazers(stargazer, repo_name)
        else:
            xprint(response.json())
            
            
    # repo forks
    def repoForks(self):
        xprint(f"{white}>> %{green}Repository{reset} ", end="")
        repo_name = input()
        xprint(f"{white}>> @{green}Owner{white} (username){reset} ", end="")
        username = input()
        xprint(SignVar.prompt, logRoller.limitInput.format("repository forks"), end="")
        limit = int(input())
        response = requests.get(f"{self.endpoint}/repos/{username}/{repo_name}/forks?per_page={limit}")
        if response.status_code == 404:
            xprint(f"{SignVar.negative} {logRoller.repoOrUserNotFound.format(repo_name, username)}")
        elif response.json() == {}:
            xprint(f"{SignVar.negative} Repository does not have forks -> ({repo_name})")
        elif response.status_code == 200:
            for count, fork in enumerate(response.json()):
                fork_tree = Tree("\n" + fork['full_name'])
                for attr in self.repo_attrs:
                    fork_tree.add(f"{self.repo_attr_dict[attr]}: {fork[attr]}")
                xprint(fork_tree)
                csvLogger.logRepoForks(fork, count)
        else:
            xprint(response.json())
            
    # Repo issues
    def repoIssues(self):
        xprint(f"{white}>> %{green}Repository{reset} ", end="")
        repo_name = input()
        xprint(f"{white}>> @{green}Owner{white} (username){reset} ", end="")
        username = input()
        xprint(SignVar.prompt, logRoller.limitInput.format("repository issues"), end="")
        limit = int(input())
        response = requests.get(f"{self.endpoint}/repos/{username}/{repo_name}/issues?per_page={limit}")
        if response.status_code == 404:
            xprint(f"{SignVar.negative} {logRoller.repoOrUserNotFound.format(repo_name, username)}")
        elif response.json() == []:
            xprint(f"{SignVar.negative} Repository does not have open issues -> ({repo_name})")
        elif response.status_code == 200:
            for issue in response.json():
                issues_tree = Tree("\n" + issue['title'])
                for attr in self.repo_issues_attrs:
                    issues_tree.add(f"{self.repo_issues_attr_dict[attr]}: {issue[attr]}")
                xprint(issues_tree)
                xprint(issue['body'])
                csvLogger.logRepoIssues(issue, repo_name)
        else:
            xprint(response.json())
            
            
    # Repo releases
    def repoReleases(self):
        xprint(f"{white}>> %{green}Repository{reset} ", end="")
        repo_name = input()
        xprint(f"{white}>> @{green}Owner{white} (username){reset} ", end="")
        username = input()
        xprint(SignVar.prompt, logRoller.limitInput.format("repository releases"), end="")
        limit = int(input())
        response = requests.get(f"{self.endpoint}/repos/{username}/{repo_name}/releases?per_page={limit}")
        if response.status_code == 404:
            xprint(f"{SignVar.negative} {logRoller.repoOrUserNotFound.format(repo_name, username)}")
        elif response.json() == []:
            xprint(f"{SignVar.negative} Repository does not have releases -> ({repo_name})")
        elif response.status_code == 200:
            for release in response.json():
                releases_tree = Tree("\n" + release['name'])
                for attr in self.repo_releases_attrs:
                    releases_tree.add(f"{self.repo_releases_attr_dict[attr]}: {release[attr]}")
                xprint(releases_tree)
                xprint(release['body'])
            csvLogger.logRepoReleases(release, repo_name)
        else:
            xprint(response.json())
            
            
    # Fetching organization repositories
    def orgRepos(self):
        xprint(f"{white}>> @{green}Organization{white} (username){reset} ", end="")
        organization = input()
        xprint(SignVar.prompt, logRoller.limitInput.format("organization repositories"), end="")
        limit = int(input())
        response = requests.get(f"{self.endpoint}/orgs/{organization}/repos?per_page={limit}")
        if response.status_code == 404:
            xprint(f"{SignVar.negative} {logRoller.orgNotFound.format(organization)}")
        elif response.status_code == 200:
            for repository in response.json():
                repos_tree = Tree("\n" + repository['full_name'])
                for attr in self.repo_attrs:
                    repos_tree.add(f"{self.repo_attr_dict[attr]}: {repository[attr]}")
                xprint(repos_tree)
                csvLogger.logOrgRepos(repository, organization)
        else:
            xprint(response.json())
            
            
    # organization events
    def orgEvents(self):
        xprint(f"{white}>> @{green}Organization{white} (username){reset} ", end="")
        organization = input()
        xprint(SignVar.prompt, logRoller.limitInput.format("organization repositories"), end="")
        limit = int(input())
        response = requests.get(f"{self.endpoint}/orgs/{organization}/events?per_page={limit}")
        if response.status_code == 404:
            xprint(f"{SignVar.negative} {logRoller.orgNotFound.format(organization)}")
        elif response.status_code == 200:
            for event in response.json():
                events_tree = Tree("\n" + event['id'])
                events_tree.add(f"Type: {event['type']}")
                events_tree.add(f"Created at: {event['created_at']}")
            xprint(events_tree)
            xprint(event['payload'])
            csvLogger.logOrgEvents(event, organization)
        else:
            xprint(response.json())
            
            
    # organization member
    def orgMember(self):
        xprint(f"{white}>> @{green}Organization{white} (username){reset} ", end="")
        organization = input()
        xprint(f"{white}>> @{green}Username{reset} ", end="")
        username = input()
        response = requests.get(f"{self.endpoint}/orgs/{organization}/public_members/{username}")
        if response.status_code == 204:
            xprint(f"{SignVar.positive} User ({username}) is a public member of the organization -> ({organization})")
        else:
            xprint(f"{SignVar.negative} {response.json()['message']}")
            
            
    # Fetching user repositories
    def userRepos(self):
        xprint(f"{white}>> @{green}Username{reset} ", end="")
        username = input()
        xprint(SignVar.prompt, logRoller.limitInput.format("repositories"), end="")
        limit = int(input())
        response = requests.get(f"{self.endpoint}/users/{username}/repos?per_page={limit}")
        if response.status_code == 404:
            xprint(f"{SignVar.negative} {logRoller.userNotFound.format(username)}")
        elif response.status_code == 200:
            for repository in response.json():
                repos_tree = Tree("\n" + repository['full_name'])
                for attr in self.repo_attrs:
                    repos_tree.add(f"{self.repo_attr_dict[attr]}: {repository[attr]}")
                xprint(repos_tree)
                csvLogger.logUserRepos(repository, username)
            else:
                xprint(response.json())
                
                
    # Fetching user's gists
    def userGists(self):
        xprint(f"{white}>> @{green}Username{reset} ", end="")
        username = input()
        xprint(SignVar.prompt, logRoller.limitInput.format('gists'), end="")
        limit = int(input())
        response = requests.get(f"{self.endpoint}/users/{username}/gists?per_page={limit}")
        if response.json() == []:
            xprint(f"{SignVar.negative} User does not have gists.")
        elif response.status_code == 404:
            xprint(f"{SignVar.negative} {logRoller.userNotFound.format(username)}")
        elif response.status_code == 200:
            for gist in response.json():
                gists_tree = Tree("\n" + gist['id'])
                for attr in self.gists_attrs:
                    gists_tree.add(f"{self.gists_attr_dict[attr]}: {gist[attr]}")
                xprint(gists_tree)
                csvLogger.logUserGists(gist)
        else:
            xprint(response.json())
            
            
    # Fetching a list of organizations that a user owns or belongs to
    def userOrgs(self):
        xprint(f"{white}>> @{green}Username{reset} ", end="")
        username = input()
        xprint(SignVar.prompt, logRoller.limitInput.format("user organizations"), end="")
        limit = int(input())
        response = requests.get(f"{self.endpoint}/users/{username}/orgs?per_page={limit}")
        if response.json() == []:
            xprint(f"{SignVar.negative} User ({username}) does not (belong to/own) any organizations.")
        elif response.status_code == 404:
            xprint(f"{SignVar.negative} {logRoller.userNotFound.format(username)}")
        elif response.status_code == 200:
            for organization in response.json():
                org_tree = Tree("\n" + organization['login'])
                for attr in self.user_orgs_attrs:
                    org_tree.add(f"{self.user_orgs_attr_dict[attr]}: {organization[attr]}")
                xprint(org_tree)
                csvLogger.logUserOrgs(organization, username)
        else:
            xprint(response.json())
            
            
    # Fetching a users events 
    def userEvents(self):
        xprint(f"{white}>> @{green}Username{reset} ", end="")
        username = input()
        xprint(SignVar.prompt, logRoller.limitInput.format("events"), end="")
        limit = int(input())
        response = requests.get(f"{self.endpoint}/users/{username}/events/public?per_page={limit}")
        if response.status_code == 404:
            xprint(f"{SignVar.negative} {logRoller.userNotFound.format(username)}")
        elif response.status_code == 200:
            for event in response.json():
                events_tree = Tree("\n" + event['id'])
                events_tree.add(f"Actor: {event['actor']['login']}")
                events_tree.add(f"Type: {event['type']}")
                events_tree.add(f"Repository: {event['repo']['name']}")
                events_tree.add(f"Created at: {event['created_at']}")
                xprint(events_tree)
                xprint(event['payload'])
                csvLogger.logUserEvents(event)
        else:
            xprint(response.json())
            
            
    # Fetching a target user's subscriptions
    def userSubscriptions(self):
        xprint(f"{white}>> @{green}Username{reset} ", end="")
        username = input().lower()
        xprint(SignVar.prompt, logRoller.limitInput.format("user subscriptions"), end="")
        limit = int(input())
        response = requests.get(f"{self.endpoint}/users/{username}/subscriptions?per_page={limit}")
        if response.json() == []:
            xprint(f"{SignVar.negative} User does not have any subscriptions.")
        elif response.status_code == 404:
            xprint(f"{SignVar.negative} {logRoller.userNotFound.format(username)}")
        elif response.status_code == 200:
            for repository in response.json():
                subscriptions_tree =Tree("\n" + repository['full_name'])
                for attr in self.repo_attrs:
                    subscriptions_tree.add(f"{self.repo_attr_dict[attr]}: {repository[attr]}")
                xprint(subscriptions_tree)
                csvLogger.logUserSubscriptions(repository, username)
        else:
            xprint(response.json())
            
            
    # Fetching a list of users the target follows        
    def userFollowing(self):
        xprint(f"{white}>> @{green}Username{reset} ", end="")
        username = input().lower()
        xprint(SignVar.prompt, logRoller.limitInput.format("user' following"), end="")
        limit = int(input())
        response = requests.get(f"{self.endpoint}/users/{username}/following?per_page={limit}")
        if response.json() == []:
            xprint(f"{SignVar.negative} User ({username})does not follow anyone.")
        elif response.status_code == 404:
            xprint(f"{SignVar.negative} {logRoller.userNotFound.format(username)}")
        elif response.status_code == 200:
            for user in response.json():
                following_tree = Tree("\n" + user['login'])
                for attr in self.user_attrs:
                    following_tree.add(f"{self.user_attr_dict[attr]}: {user[attr]}")
                xprint(following_tree)
                csvLogger.logUserFollowing(user, username)
        else:
            xprint(response.json())
            
            
    # Fetching user's followers
    def userFollowers(self):
        xprint(f"{white}>> @{green}Username{reset} ", end="")
        username = input().lower()
        xprint(SignVar.prompt, logRoller.limitInput.format("user followers"), end="")
        limit = int(input())
        response = requests.get(f"{self.endpoint}/users/{username}/followers?per_page={limit}")
        if response.json() == []:
            xprint(f"{SignVar.negative} User ({username})does not have followers.")
        elif response.status_code == 404:
            xprint(f"{SignVar.negative} {logRoller.userNotFound.format(username)}")
        elif response.status_code == 200:
            for follower in response.json():
                followers_tree = Tree("\n" + follower['login'])
                for attr in self.user_attrs:
                    followers_tree.add(f"{self.user_attr_dict[attr]}: {follower[attr]}")
                xprint(followers_tree)
                csvLogger.logUserFollowers(follower, username)
        else:
            xprint(response.json())
            
            
    # Checking whether user[A] follows user[B]
    def userFollows(self):
        xprint(f"{white}>> @{green}user{white}(A) (username){reset} ", end="")
        user_a = input()
        xprint(f"{white}>> @{green}user{white}(B) (username){reset} ", end="")
        user_b = input()
        response = requests.get(f"{self.endpoint}/users/{user_a}/following/{user_b}")
        if response.status_code == 204:
            xprint(f"{SignVar.positive} @{user_a} FOLLOWS @{user_b}")
        else:
            xprint(f"{SignVar.negative} @{user_a} DOES NOT FOLLOW @{user_b}")
            
            
    # User search
    def userSearch(self):
        xprint(f"{white}>> @{green}Query{white} (eg. john){reset} ", end="")
        query = input()
        xprint(SignVar.prompt, logRoller.limitInput.format("user search"), end="")
        limit = int(input())
        response = requests.get(f"{self.endpoint}/search/users?q={query}&per_page={limit}").json()
        for user in response['items']:
            user_search_tree = Tree("\n" + user['login'])
            for attr in self.user_attrs:
                user_search_tree.add(f"{self.user_attr_dict[attr]}: {user[attr]}")
            xprint(user_search_tree)
            csvLogger.logUserSearch(user, query)
            
            
    # Repository search
    def repoSearch(self):
        xprint(f"{white}>> %{green}Query{white} (eg. git){reset} ", end="")
        query = input()
        xprint(SignVar.prompt, logRoller.limitInput.format("repositor[y][ies] search"), end="")
        limit = int(input())
        response = requests.get(f"{self.endpoint}/search/repositories?q={query}&per_page={limit}").json()
        for repository in response['items']:
            repo_search_tree = Tree("\n" + repository['full_name'])
            for attr in self.repo_attrs:
                repo_search_tree.add(f"{self.repo_attr_dict[attr]}: {repository[attr]}")
            xprint(repo_search_tree)
            csvLogger.logRepoSearch(repository, query)
            
            
    # Topics search
    def topicSearch(self):
        xprint(f"{white}>> #{green}Query{white} (eg. osint){reset} ", end="")
        query = input()
        xprint(SignVar.prompt, logRoller.limitInput.format("topic(s) search"), end="")
        limit = int(input())
        response = requests.get(f"{self.endpoint}/search/topics?q={query}&per_page={limit}").json()
        for topic in response['items']:
            topic_search_tree = Tree("\n" + topic['name'])
            for attr in self.topic_attrs:
                topic_search_tree.add(f"{self.topic_attr_dict[attr]}: {topic[attr]}")
            xprint(topic_search_tree)
            csvLogger.logTopicSearch(topic, query)
            
            
    # Issue search
    def issueSearch(self):
        xprint(f"{white}>> !{green}Query{white} (eg. error){reset} ", end="")
        query = input()
        xprint(SignVar.prompt, logRoller.limitInput.format("issue(s) search"), end="")
        limit = int(input())
        response = requests.get(f"{self.endpoint}/search/issues?q={query}&per_page={limit}").json()
        for issue in response['items']:
            issue_search_tree = Tree("\n" + issue['title'])
            for attr in self.repo_issues_attrs:
                issue_search_tree.add(f"{self.repo_issues_attr_dict[attr]}: {issue[attr]}")
            xprint(issue_search_tree)
            xprint(issue['body'])
        csvLogger.logIssueSearch(issue, query)
        
        
    # Commits search
    def commitsSearch(self):
        xprint(f"{white}>> :{green}Query{white} (eg. filename:index.php){reset} ", end="")
        query = input()
        xprint(SignVar.prompt, logRoller.limitInput.format("commit(s) search"), end="")
        limit = int(input())
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
            csvLogger.logCommitsSearch(commit, query)
            
            
    # View csv files
    def viewCsv(self):
        logging.info(logRoller.viewingCsv)
        csv_files = os.listdir("output")
        csv_table = Table(show_header=True, header_style=header_title)
        csv_table.add_column("CSV", style="dim")
        csv_table.add_column("Size (bytes)")
        for csv_file in csv_files:
            csv_table.add_row(str(csv_file), str(os.path.getsize("output/" + csv_file)))
        xprint(csv_table)
        
        
    # Read a specified csv file    
    def readCsv(self):
        xprint(f"{white}>> {green}.csv {reset}(filename) ", end="")
        csv_file = input()
        with open(os.path.join("output", csv_file + ".csv"), "r") as file:
            logging.info(logRoller.readingCsv.format(csv_file))
            text = Text(file.read())
            xprint(text)
            # xprint("\n" + file.read())
            
            
    # Delete a specified csv file
    def deleteCsv(self):
        xprint(f"{white}>> {green}.csv {reset}filename{reset} ", end="")
        csv_file = input()
        os.remove(os.path.join("output", csv_file))
        logging.info(logRoller.deletedCsv.format(csv_file))
        xprint(f"{SignVar.positive} {logRoller.deletedCsv.format(csv_file)}")
                    
                    
    # Clear csv
    def clearCsv(self):
        xprint(f"{SignVar.prompt} This will clear all {len(os.listdir('output'))} csv files, continue? (y/n) ", end="")
        prompt = input().lower()
        if prompt == "y":
            shutil.rmtree("output", ignore_errors=True)
            xprint(f"{SignVar.info} CSV files cleared successfully!")
        else:
            pass
                    
        
    # View octosuite log files
    def viewLogs(self):
        logging.info(logRoller.viewingLogs)
        logs = os.listdir(".logs")
        logs_table = Table(show_header=True, header_style=header_title)
        logs_table.add_column("Log", style="dim")
        logs_table.add_column("Size (bytes)")
        for log in logs:
            logs_table.add_row(str(log), str(os.path.getsize(".logs/" + log)))
        xprint(logs_table)
        
        
    # Read a specified log file
    def readLog(self):
        xprint(f"{white}>> {green}.log date{reset} (eg. 2022-04-27 10:09:36AM) ", end="")
        log_file = input()
        with open(os.path.join(".logs", log_file + ".log"), "r") as log:
            logging.info(logRoller.readingLog.format(log_file))
            xprint("\n" + log.read())
            
            
    # Delete a specified log file
    def deleteLog(self):
        xprint(f"{white}>> {green}.log date{reset} (eg. 2022-04-27 10:09:36AM) ", end="")
        log_file = input()
        os.remove(os.path.join(".logs", log_file))
        logging.info(logRoller.deletedLog.format(log_file))
        xprint(f"{SignVar.positive} {logRoller.deletedLog.format(log_file)}")
        
        
    # Clear logs
    def clearLogs(self):
        xprint(f"{SignVar.prompt} This will clear all {len(os.listdir('.logs'))} logs and close the current session, continue? (y/n) ", end="")
        prompt = input().lower()
        if prompt == "y":
            shutil.rmtree(".logs", ignore_errors=True)
            xprint(f"{SignVar.info} Logs cleared successfully!")
            xprint(f"{SignVar.info} {logRoller.sessionClosed.format(datetime.now())}")
            exit()
        else:
            pass
        
        
    # Downloading release tarball
    def downloadTarball(self):
        logging.info(logRoller.fileDownloading.format(f"octosuite.v{version_tag}.tar"))
        xprint(SignVar.info, logRoller.fileDownloading.format(f"octosuite.v{version_tag}.tar"))
        data = requests.get(f"{self.endpoint}/repos/bellingcat/octosuite/tarball/{version_tag}")
        with open(os.path.join("downloads", f"octosuite.v{version_tag}.tar"), "wb") as file:
            file.write(data.content)
            file.close()
            
        logging.info(logRoller.fileDownloaded.format(f"octosuite.v{version_tag}.tar"))
        xprint(SignVar.positive, logRoller.fileDownloaded.format(f"octosuite.v{version_tag}.tar"))
        
        
    # Downloading release zipball
    def downloadZipball(self):
        logging.info(logRoller.fileDownloading.format(f"octosuite.v{version_tag}.zip"))
        xprint(SignVar.info, logRoller.fileDownloading.format(f"octosuite.v{version_tag}.zip"))
        data = requests.get(f"{self.endpoint}/repos/rly0nheart/octosuite/zipball/{version_tag}")
        with open(os.path.join("downloads", f"octosuite.v{version_tag}.zip"), "wb") as file:
            file.write(data.content)
            file.close()
            
        logging.info(logRoller.fileDownloaded.format(f"octosuite.v{version_tag}.zip"))
        xprint(SignVar.positive, logRoller.fileDownloaded.format(f"octosuite.v{version_tag}.zip"))
        
        
    # Author info
    def author(self):
        author_tree = Tree(f"{white}Richard Mwewa (Ritchie){reset}")
        for author_key, author_value in self.author_dict.items(self):
            author_tree.add(f"{white}{author_key}:{reset} {author_value}")
        xprint(author_tree)
        
        
    # About program
    def about(self):
        about_text = Text(f"""
        OCTOSUITE © 2022 Richard Mwewa
        
An advanced and lightning fast framework for gathering open-source intelligence on GitHub users and organizations.
With over 20+ features, Octosuite only runs on 2 external dependencies, and returns the gathered intelligence in a highly readable format.


Whats new in v{version_tag}?
[fixed] Minor fixes
[improved] Removed width from tables, so that they can auto adjust
[added] Added the 'log:clear' command, which will be used to clear all logs
[added] Added the 'csv:clear' command, which will be used to clear all csv files

Read the wiki: https://github.com/bellingcat/octosuite/wiki
GitHub REST API documentation: https://docs.github.com/rest
""")
        xprint(about_text)

    
    # Close session
    def exitSession(self):
        xprint(f"{SignVar.prompt} This will close the current session, continue? (Y/n) ", end="")
        prompt = input().lower()
        if prompt == 'y':
            logging.info(logRoller.sessionClosed.format(datetime.now()))
            xprint(f"{SignVar.info} {logRoller.sessionClosed.format(datetime.now())}")
            exit()
        else:
            pass
        
    
    # Clear screen    
    def clearScreen(self):
        """
        using 'cls' on Windows machines to clear the screen,
        otherwise, use 'clear'
        """
        if sys.platform.lower().startswith("win"):
            os.system('cls')
        else:
            os.system('clear')
            
