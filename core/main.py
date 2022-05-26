'''
            OCTOSUITE Advanced Github OSINT Framework
                     Copyright (C) 2022  Richard Mwewa

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
'''

import os
import sys
import logging
import getpass
import requests
import platform
import subprocess
from tqdm import tqdm
from pprint import pprint
from utilities.misc import Banner
from utilities.helper import Help
from utilities.colors import Color
from datetime import datetime


# logMsg
# This class is where the main notification strings/messages are held,
# and are being used in two different cases (they're beig used by logging to be written to log files, and being printed out to the screen).
class logMsg:
    Ctrl = 'Session terminated with (Ctrl+C).'
    Error = 'Session terminated on error: {}'
    sessionStart = 'Started new session on {}:{}'
    sessionClosed = 'Session closed with (exit) command.'
    fileDeleted = 'Deleted log: {}'
    readingFile = 'Reading log: {}'
    viewingLogs = 'Viewing logs...'
    checkingUpdates = 'Checking for update(s)...'
    installingUpdates = 'Installing update(s)...'
    installedUpdates = '{} Update(s) installed.'


# firstBlood
# *I couldn't think of a good name for this.*
# The firstBlood is responsible for creating/checking the availability of the .logs folder
# and enabling logging to automatically log network/user activity to a file.
class firstBlood:
    # If .logs folder exists, we ignore (pass)
    if os.path.exists('.logs'):
        pass
    else:
        # Creating the .logs directory
        # If the current system is Windows based, we run mkdir command (without sudo?)
        # Else we run the mkdir command (with sudo)
        # As of writing, I have absolutely no idea if Windows users also use sudo to run commands as root/admin
        if sys.platform.lower().startswith(('win','darwin')):
            subprocess.run(['mkdir','.logs'])
        else:
            subprocess.run(['sudo','mkdir','.logs'],shell=False)
            
    # Set to automatically monitor and log network and user activity into the .logs folder
    now = datetime.now()
    now_formatted = now.strftime('%Y-%m-%d %H:%M:%S%p')
    logging.basicConfig(filename=f'.logs/{now_formatted}.log',format='[%(asctime)s] [%(levelname)s] %(message)s',datefmt='%Y-%m-%d %H:%M:%S%p',level=logging.DEBUG)


# Attributes
# *Even here, I couldn't think of a good name.*
# The Attributes class holds the signs/symbols that show what a notification in OctoSuite might be all about.
# This might not be very important or necessary in some cases, but I think it's better to know the severerity of the notifications you get in a program.
class Attributes:
	prompt = f'\n{Color.white}[{Color.green}?{Color.white}]{Color.reset}'
	warning = f'\n{Color.white}[{Color.red}!{Color.white}]{Color.reset}'
	error = f'\n{Color.white}[{Color.red}x{Color.white}]{Color.reset}'
	positive = f'\n{Color.white}[{Color.green}+{Color.white}]{Color.reset}'
	negative = f'\n{Color.white}[{Color.red}-{Color.white}]{Color.reset}'
	info = f'\n{Color.white}[{Color.green}*{Color.white}]{Color.reset}'


# Octosuite
# This class is the backbone of the program.
# It holds all important methods/information for the program.
class Octosuite:
    def __init__(self):
        firstBlood()
        # A list of tuples, mapping commands to their respective functionalities
        self.commands_map = [('org:events', self.orgEvents),
                             ('org:profile', self.orgProfile),
                             ('org:repos', self.orgRepos),
                             ('org:member', self.orgMember),
                             ('repo:pathcontents', self.pathContents),
                             ('repo:profile', self.repoProfile),
                             ('repo:contributors', self.repoContributors),
                             ('repo:languages', self.repoLanguages),
                             ('repo:stargazers', self.repoStargazers),
                             ('repo:forks', self.repoForks),
                             ('repo:releases', self.repoReleases),
                             ('user:repos', self.userRepos),
                             ('user:gists', self.userGists),
                             ('user:orgs', self.userOrgs),
                             ('user:profile', self.userProfile),
                             ('user:events', self.userEvents),
                             ('user:followers', self.userFollowers),
                             ('user:following', self.userFollowing),
                             ('user:subscriptions', self.userSubscriptions),
                             ('search:users', self.userSearch),
                             ('search:repos', self.repoSearch),
                             ('search:topics', self.topicSearch),
                             ('search:issues', self.issueSearch),
                             ('search:commits', self.commitsSearch),
                             ('logs:view',self.viewLogs),
                             ('logs:read',self.readLog),
                             ('logs:delete',self.deleteLog),
                             ('update:check', self.checkUpdate),
                             ('update:install', self.installUpdate),
                             ('help', Help.helpCommand),
                             ('help:search', Help.searchCommand),
                             ('help:user',  Help.userCommand),
                             ('help:repo',  Help.repoCommand),
                             ('help:logs',  Help.logsCommand),
                             ('help:org',  Help.orgCommand),
                             ('help:update', Help.updateCommand),
                             ('author', self.author),
                             ('about', self.about),
                             ('clear',self.clearScreen),
                             ('version', self.versionInfo),
                             ('exit', self.exitSession)]
                                                   
                                                   
        # Path attribute
        self.path_attrs =['size','type','path','sha','html_url']
        # Path attribute dictionary
        self.path_attr_dict = {'size': 'Size (bytes)',
                               'type': 'Type',
                               'path': 'Path',
                               'sha': 'SHA',
                               'html_url': 'URL'}
                                             
                                             
        # Organization attributes
        self.org_attrs = ['avatar_url','login','id','node_id','email','description','blog','location','followers','following','twitter_username','public_gists','public_repos','type','is_verified','has_organization_projects','has_repository_projects','created_at','updated_at']
        # Organization attribute dictionary
        self.org_attr_dict = {'avatar_url': 'Profile Photo',
                              'login': 'Username',
                              'id': 'ID#',
                              'node_id': 'Node ID',
                              'email': 'Email',
                              'description': 'About',
                              'location': 'Location',
                              'blog': 'Blog',
                              'followers': 'Followers',
                              'following': 'Following',
                              'twitter_username': 'Twitter Handle',
                              'public_gists': 'Gists (public)',
                              'public_repos': 'Repositories (public)',
                              'type': 'Account type',
                              'is_verified': 'Is verified?',
                              'has_organization_projects': 'Has organization projects?',
                              'has_repository_projects': 'Has repository projects?',
                              'created_at': 'Created at',
                              'updated_at': 'Updated at'}
                                           
                                           
        # Repository attributes
        self.repo_attrs = ['id','description','forks','stargazers_count','watchers','license','default_branch','visibility','language','open_issues','topics','homepage','clone_url','ssh_url','fork','allow_forking','private','archived','has_downloads','has_issues','has_pages','has_projects','has_wiki','pushed_at','created_at','updated_at']
        # Repository attribute dictionary
        self.repo_attr_dict = {'id': 'ID#',
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
        self.repo_releases_attrs = ['node_id','tag_name','target_commitish','assets','draft','prerelease','created_at','published_at']
        # Repo releases attribute dictionary
        self.repo_releases_attr_dict = {'node_id': 'Node ID',
                                        'tag_name': 'Tag',
                                        'target_commitish': 'Branch',
                                        'assets': 'Assets',
                                        'draft': 'Is draft?',
                                        'prerelease': 'Is prerelease?',
                                        'created_at': 'Created at',
                                        'published_at': 'Published at'}
                                              
                                              
        # Profile attributes
        self.profile_attrs = ['avatar_url','login','id','node_id','bio','blog','location','followers','following','twitter_username','public_gists','public_repos','company','hireable','site_admin','created_at','updated_at']
        # Profile attribute dictionary                                      
        self.profile_attr_dict = {'avatar_url': 'Profile Photo',
                                  'login': 'Username',
                                  'id': 'ID#',
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
        self.user_attrs = ['avatar_url','id','node_id','gravatar_id','site_admin','type','html_url']
        # User attribute dictionary
        self.user_attr_dict = {'avatar_url': 'Profile Photo',
                               'id': 'ID#',
                               'node_id': 'Node ID',
                               'gravatar_id': 'Gravatar ID',
                               'site_admin': 'Is site admin?',
                               'type': 'Account type',
                               'html_url': 'URL'}
                                             
                                         
        # Topic atrributes                                 
        self.topic_attrs = ['score','curated','featured','display_name','created_by','created_at','updated_at']
        # Topic attribute dictionary
        self.topic_attr_dict = {'score': 'Score',
                                'curated': 'Curated',
                                'featured': 'Featured',
                                'display_name': 'Display Name',
                                'created_by': 'Created by',
                                'created_at': 'Created at',
                                'updated_at': 'Updated at'}
                                               
        
        # Gists attributes                                       
        self.gists_attrs = ['node_id','description','comments','files','git_push_url','public','truncated','updated_at']
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
        self.issue_attrs = ['id','node_id','score','state','number','comments','milestone','assignee','assignees','labels','locked','draft','closed_at','body']
        # Issue attribute dict
        self.issue_attr_dict = {'id': 'ID#',
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
                                'created_at': 'Created at',
                                'body': 'Body'}
                                               
                                               
        # User organizations attributes
        self.user_orgs_attrs = ['avatar_url','id','node_id','url','description']
        self.user_orgs_attr_dict = {'avatar_url': 'Profile Photo',
                                    'id': 'ID#',
                                    'node_id': 'Node ID',
                                    'url': 'URL',
                                    'description': 'About'}
                                               
                                               
        # Author dictionary
        self.author_dict = {'Alias': 'rly0nheart',
                            'Country': 'Zambia, Africa',
                            'About.me': 'https://about.me/rly0nheart',
                            'BuyMeACoffee': 'https://buymeacoffee.com/189381184'}

        # About dictionary 
        self.about_dict = {'Version': Banner.versionTag,'Category': 'Open Source Intelligence'}

 
               
    def onStart(self):
        # Log the beginning of a session
        logging.info(logMsg.sessionStart.format(platform.node(), getpass.getuser()))
        
        # Use 'cls' to clear screen on Windows based machines
        # Otherwise, use 'clear'
        while True:
            command_input = input(f'''\n{Color.white}┌──({Color.red}{getpass.getuser()}{Color.white}@{Color.red}octosuite{Color.white})-[{Color.green}{os.getcwd()}{Color.white}]\n└╼[{Color.green}:_{Color.white}]{Color.reset} ''')        
            # Looping through the commands base to check if the user input command matches any command in the commands base, and return its functionality
            # If no match is found, we ignore it
            for command, functionality in self.commands_map:
                if command_input.lower() == command:
                	functionality()
                else:
                    pass
  	
                      
    # Fetching organization info        
    def orgProfile(self):
        organization = input(f'\n{Color.white}--> @{Color.green}organization{Color.white} (username){Color.reset} ')
        response = requests.get(f'https://api.github.com/orgs/{organization}')
        if response.status_code == 404:
        	print(f"{Attributes.negative} Organization {response.json()['message']}{Color.reset}")
        else:
        	print(f"\n{Color.white}{response.json()['name']}{Color.reset}")
        	for attr in self.org_attrs:
        		print(f'{Color.white}├─ {self.org_attr_dict[attr]}: {Color.green}{response.json()[attr]}{Color.reset}')
        
                        
    # Fetching user information        
    def userProfile(self):
        username = input(f'\n{Color.white}--> @{Color.green}username{Color.reset} ')
        response = requests.get(f'https://api.github.com/users/{username}')
        if response.status_code == 404:
        	print(f"{Attributes.negative} User {response.json()['message']}{Color.reset}")
        else:
        	print(f"\n{Color.white}{response.json()['name']}{Color.reset}")
        	for attr in self.profile_attrs:
        		print(f'{Color.white}├─ {self.profile_attr_dict[attr]}: {Color.green}{response.json()[attr]}{Color.reset}')

        	        	
    # Fetching repository information   	
    def repoProfile(self):
        repo_name = input(f'\n{Color.white}--> %{Color.green}reponame{Color.reset} ')
        username = input(f'{Color.white}--> @{Color.green}owner{Color.white} (username){Color.reset} ')
        response = requests.get(f'https://api.github.com/repos/{username}/{repo_name}')
        if response.status_code == 404:
        	print(f"{Attributes.negative} Repository or user {response.json()['message']}{Color.reset}")
        else:
        	print(f"\n{Color.white}{response.json()['full_name']}{Color.reset}")
        	for attr in self.repo_attrs:
        	    print(f"{Color.white}├─ {self.repo_attr_dict[attr]}: {Color.green}{response.json()[attr]}{Color.reset}")
            
    
    # Get path contents        
    def pathContents(self):
        repo_name = input(f'\n{Color.white}--> %{Color.green}reponame{Color.reset} ')
        username = input(f'{Color.white}--> @{Color.green}owner{Color.white} (username){Color.reset} ')
        path_name = input(f'{Color.white}--> ~{Color.green}/path/name{Color.reset} ')
        response = requests.get(f'https://api.github.com/repos/{username}/{repo_name}/contents/{path_name}')
        if response.status_code == 404:
            print(f"{Attributes.negative} Information {response.json()['message']}{Color.reset}")
        else:
        	for item in response.json():
        	    print(f"\n{Color.white}{item['name']}{Color.reset}")
        	    for attr in self.path_attrs:
        	    	print(f'{Color.white}├─ {self.path_attr_dict[attr]}: {Color.green}{item[attr]}{Color.reset}')
        	    	
        	    	
    # repo contributors
    def repoContributors(self):
        repo_name = input(f'\n{Color.white}--> %{Color.green}reponame{Color.reset} ')
        username = input(f'{Color.white}--> @{Color.green}owner{Color.white} (username){Color.reset} ')
        response = requests.get(f'https://api.github.com/repos/{username}/{repo_name}/contributors')
        if response.status_code == 404:
            print(f"{Attributes.negative} Repository or user {response.json()['message']}{Color.reset}")
        else:
            for item in response.json():
                print(f"\n{Color.white}{item['login']}{Color.reset}")
                for attr in self.user_attrs:
                	print(f'{Color.white}├─ {self.user_attr_dict[attr]}: {Color.green}{item[attr]}{Color.reset}')
                	
                	
    # repo downloads
    def repoLanguages(self):
        repo_name = input(f'\n{Color.white}--> %{Color.green}reponame{Color.reset} ')
        username = input(f'{Color.white}--> @{Color.green}owner{Color.white} (username){Color.reset} ')
        response = requests.get(f'https://api.github.com/repos/{username}/{repo_name}/languages')
        if response.status_code == 404:
            print(f"{Attributes.negative} Repository or user {response.json()['message']}{Color.reset}")
        elif response.json() == {}:
            print(f'{Attributes.negative} Repository has no supported language(s){Color.reset}')
        else:
            for language in response.json():
                print(language)
                
                
    # repo stargazers
    def repoStargazers(self):
        repo_name = input(f'\n{Color.white}--> %{Color.green}reponame{Color.reset} ')
        username = input(f'{Color.white}--> @{Color.green}owner{Color.white} (username){Color.reset} ')
        response = requests.get(f'https://api.github.com/repos/{username}/{repo_name}/stargazers')
        if response.status_code == 404:
            print(f"{Attributes.negative} Repository or user {response.json()['message']}{Color.reset}")
        elif response.json() == {}:
            print(f'{Attributes.negative} Repository does not have stargazers.{Color.reset}')
        else:
            for item in response.json():
                print(f"\n{Color.white}{item['login']}{Color.reset}")
                for attr in  self.user_attrs:
                    print(f'{Color.white}├─ {self.user_attr_dict[attr]}: {Color.green}{item[attr]}{Color.reset}')
                    
                    
    # repo forks
    def repoForks(self):
        repo_name = input(f'\n{Color.white}--> %{Color.green}reponame{Color.reset} ')
        username = input(f'{Color.white}--> @{Color.green}owner{Color.white} (username){Color.reset} ')
        response = requests.get(f'https://api.github.com/repos/{username}/{repo_name}/forks')
        if response.status_code == 404:
            print(f"{Attributes.negative} Repository or user {response.json()['message']}{Color.reset}")
        elif response.json() == {}:
            print(f'{Attributes.negative} Repository does not have forks.{Color.reset}')
        else:
            for item in response.json():
                print(f"\n{Color.white}{item['full_name']}{Color.reset}")
                for attr in  self.repo_attrs:
                    print(f'{Color.white}├─ {self.repo_attr_dict[attr]}: {Color.green}{item[attr]}{Color.reset}')


    # Repo releases
    def repoReleases(self):
        repo_name = input(f'\n{Color.white}--> %{Color.green}reponame{Color.reset} ')
        username = input(f'{Color.white}--> @{Color.green}owner{Color.white} (username){Color.reset} ')
        response = requests.get(f'https://api.github.com/repos/{username}/{repo_name}/releases')
        if response.status_code == 404:
        	print(f"{Attributes.negative} Repository or user not found{Color.reset}")
        elif response.json() == []:
            print(f"\n{Attributes.negative} Repository does not have releases{Color.reset}")
        else:
            for item in response.json():
            	print(f"\n{Color.white}{item['name']}{Color.reset}")
            	for attr in self.repo_releases_attrs:
            	    print(f'{Color.white}├─ {self.repo_releases_attr_dict[attr]}: {Color.green}{item[attr]}{Color.reset}')
            	print(item['body'])
            	
                       
    # Fetching organization repositories        
    def orgRepos(self):
        organization = input(f'\n{Color.white}--> @{Color.green}organization{Color.white} (username){Color.reset} ')
        response = requests.get(f'https://api.github.com/orgs/{organization}/repos?per_page=100')
        if response.status_code == 404:
            print(f"{Attributes.negative} Organization {response.json()['message']}{Color.reset}")
        else:
            for repo in response.json():
            	print(f"\n{Color.white}{repo['full_name']}{Color.reset}")
            	for attr in self.repo_attrs:
            		print(f"{Color.white}├─ {self.repo_attr_dict[attr]}: {Color.green}{repo[attr]}{Color.reset}")
            
    
    # organization events        
    def orgEvents(self):
        organization = input(f"\n{Color.white}--> @{Color.green}organization{Color.white} (username){Color.reset} ")
        response = requests.get(f'https://api.github.com/orgs/{organization}/events')
        if response.status_code == 404:
            print(f"{Attributes.negative} Organization {response.json()['message']}{Color.reset}")
        else:
            for item in response.json():
            	print(f"\n{Color.white}{item['id']}{Color.reset}")
            	print(f"{Color.white}├─ Type: {Color.green}{item['type']}{Color.reset}\n{Color.white}├─ Created at: {Color.green}{item['created_at']}{Color.green}")
            	pprint(item['payload'])
            	print(f"{Color.reset}\n")
            	
    
    # organization member        	
    def orgMember(self):
        organization = input(f"\n{Color.white}--> @{Color.green}organization{Color.white} (username){Color.reset} ")
        username = input(f'{Color.white}--> @{Color.green}username{Color.reset} ')
        response = requests.get(f'https://api.github.com/orgs/{organization}/public_members/{username}')
        if response.status_code == 204:
            print(f"{Attributes.positive} User is a public member of the organization{Color.reset}")
        else:
        	print(f"{Attributes.negative} {response.json()['message']}{Color.reset}")
        	
        	           
    # Fetching user repositories        
    def userRepos(self):
        username = input(f'\n{Color.white}--> @{Color.green}username{Color.reset} ')
        response = requests.get(f'https://api.github.com/users/{username}/repos?per_page=100')
        if response.status_code == 404:
        	print(f"{Attributes.negative} User {response.json()['message']}{Color.reset}")
        else:
        	for repo in response.json():
        		print(f"\n{Color.white}{repo['full_name']}{Color.reset}")
        		for attr in self.repo_attrs:
        			print(f"{Color.white}├─ {self.repo_attr_dict[attr]}: {Color.green}{repo[attr]}{Color.reset}")	    
        	
        	   	       	    
    # Fetching user's gists
    def userGists(self):
        username = input(f'\n{Color.white}--> @{Color.green}username{Color.reset} ')
        response = requests.get(f'https://api.github.com/users/{username}/gists')
        if response.json() == []:
        	print(f'{Attributes.negative} User does not have any active gists{Color.reset}')
        elif response.status_code == 404:
        	print(f"{Attributes.negative} User {response.json()['message']}{Color.reset}")
        else:
            for item in response.json():
            	print(f"\n{Color.white}{item['id']}{Color.reset}")
            	for attr in self.gists_attrs:
            		print(f"{Color.white}├─ {self.gists_attr_dict[attr]}: {Color.green}{item[attr]}{Color.reset}")
            	
    
    # Fetching a list of organizations that a user owns or belongs to        	
    def userOrgs(self):
        username = input(f'\n{Color.white}--> @{Color.green}username{Color.reset} ')
        response = requests.get(f'https://api.github.com/users/{username}/orgs')
        if response.json() == []:
            print(f'{Attributes.negative} User does not belong to or own any organizations.{Color.reset}')
        elif response.status_code == 404:
            print(f"{Attributes.negative} User {response.json()['message']}{Color.reset}")
        else:
        	for item in response.json():
        	    print(f'\n{Color.white}{item["login"]}{Color.reset}')
        	    for attr in self.user_orgs_attrs:
        	        print(f'{Color.white}├─ {self.user_orgs_attr_dict[attr]}: {Color.green}{item[attr]}{Color.reset}')
        	    
        	    
    # Fetching a users events 
    def userEvents(self):
        username = input(f'\n{Color.white}--> @{Color.green}username{Color.reset} ')
        response = requests.get(f'https://api.github.com/users/{username}/events/public')
        if response.status_code == 404:
            print(f"{Attributes.negative} User {response.json()['message']}{Color.reset}")
        else:
            for item in response.json():
            	print(f"\n{Color.white}{item['id']}{Color.reset}")
            	print(f"{Color.white}├─ Type: {Color.green}{item['type']}{Color.reset}\n{Color.white}├─ Created at: {Color.green}{item['created_at']}{Color.green}")
            	pprint(item['payload'])
            	print(reset)
            	
            	
    # Fetching a target user's subscriptions 
    def userSubscriptions(self):
        username = input(f'\n{Color.white}--> @{Color.green}username{Color.reset} ')
        response = requests.get(f'https://api.github.com/users/{username}/subscriptions')
        if response.json() == []:
        	print(f"{Attributes.negative} User does not have any subscriptions.{Color.reset}")
        elif response.status_code == 404:
            print(f"{Attributes.negative} User {response.json()['message']}{Color.reset}")
        else:
        	for item in response.json():
        		print(f"\n{Color.white}{item['full_name']}{Color.reset}")
        		for attr in self.repo_attrs:
        			print(f"{Color.white}├─ {self.repo_attr_dict[attr]}: {Color.green}{item[attr]}{Color.reset}")
        
        	    	    
    # Fetching user's followera'    	    
    def userFollowers(self):
        username = input(f'\n{Color.white}--> @{Color.green}username{Color.reset} ')
        response = requests.get(f'https://api.github.com/users/{username}/followers?per_page=100')
        if response.json() == []:
        	print(f'{Attributes.negative} User does not have followers.{Color.reset}')
        elif response.status_code == 404:
        	print(f"{Attributes.negative} User {response.json()['message']}{Color.reset}")
        else:
            for item in response.json():
            	print(f"\n{Color.white}@{item['login']}{Color.reset}")
            	for attr in self.user_attrs:
            		print(f"{Color.white}├─ {self.user_attr_dict[attr]}: {Color.green}{item[attr]}{Color.reset}")
            
                    
    # Checking whether or not user[A] follows user[B]            
    def userFollowing(self):
        user_a = input(f'\n{Color.white}--> @{Color.green}user{Color.white}[A] (username){Color.reset} ')
        user_b = input(f'{Color.white}--> @{Color.green}user{Color.white}[B] (username){Color.reset} ')
        response = requests.get(f'https://api.github.com/users/{user_a}/following/{user_b}')
        if response.status_code == 204:
        	print(f'{Attributes.positive} @{user_a} follows @{user_b}{Color.reset}')
        else:
        	print(f'{Attributes.negative} @{user_a} does not follow @{user_b}{Color.reset}')   
 
        	           	    
    # User search    	    
    def userSearch(self):
        query = input(f'\n{Color.white}--> @{Color.green}query{Color.white} (eg. john){Color.reset} ')
        response = requests.get(f'https://api.github.com/search/users?q={query}&per_page=100').json()
        for item in response['items']:
        	print(f"\n{Color.white}@{item['login']}{Color.reset}")
        	for attr in self.user_attrs:
        		print(f"{Color.white}├─ {self.user_attr_dict[attr]}: {Color.green}{item[attr]}{Color.reset}")
        		
       		
    # Repository search
    def repoSearch(self):
        query = input(f'\n{Color.white}--> %{Color.green}query{Color.white} (eg. git){Color.reset} ')
        response = requests.get(f'https://api.github.com/search/repositories?q={query}&per_page=100').json()
        for item in response['items']:
            print(f"\n{Color.white}{item['full_name']}{Color.reset}")
            for attr in self.repo_attrs:
                print(f"{Color.white}├─ {self.repo_attr_dict[attr]}: {Color.green}{item[attr]}{Color.reset}")
                
                
    # Topics search
    def topicSearch(self):
        query = input(f'\n{Color.white}--> #{Color.green}query{Color.white} (eg. osint){Color.reset} ')
        response = requests.get(f'https://api.github.com/search/topics?q={query}&per_page=100').json()
        for item in response['items']:
            print(f"\n{Color.white}{item['name']}{Color.reset}")
            for attr in self.topic_attrs:
                print(f"{Color.white}├─ {self.topic_attr_dict[attr]}: {Color.green}{item[attr]}{Color.reset}")
                
                
    # Issue search
    def issueSearch(self):
        query = input(f'\n{Color.white}--> !{Color.green}query{Color.white} (eg. error){Color.reset} ')
        response = requests.get(f'https://api.github.com/search/issues?q={query}&per_page=100').json()
        for item in response['items']:
            print(f"\n{Color.white}{item['title']}{Color.reset}")
            for attr in self.issue_attrs:
                print(f"{Color.white}├─ {self.issue_attr_dict[attr]}: {Color.green}{item[attr]}{Color.reset}")
            
            
    # Commits search
    def commitsSearch(self):
        query = input(f'\n{Color.white}--> :{Color.green}query{Color.white} (eg. filename:index.php){Color.reset} ')
        response = requests.get(f'https://api.github.com/search/commits?q={query}&per_page=100').json()
        number=0
        for item in response['items']:
        	number+=1
        	print(f'\n{Color.white}-> {number}.{Color.reset}')
        	pprint(item['commit'])
        	
    
    # View octosuite log files    	
    def viewLogs(self):
        logging.info(logMsg.viewingLogs)
        logs = os.listdir('.logs')
        print(f'''\n{Color.white}Log                               Size{Color.reset}
---                               ---------''')
        for log in logs:
            print(f"{log}\t ",os.path.getsize(".logs/"+log),"bytes")
        
    
    # Delete a specified log file    
    def deleteLog(self):
        log_file = input(f"\n{Color.white}--> logfile (eg. 2022-04-27 10:09:36AM.log){Color.reset} ")
        if sys.platform.lower().startswith(('win','darwin')):
            subprocess.run(['del',f'{os.getcwd()}/.logs/{log_file}'])
        else:
            subprocess.run(['sudo','rm',f'.logs/{log_file}'],shell=False)
        
        logging.info(logMsg.fileDeleted.format(log_file))
        print(Attributes.positive, logMsg.fileDeleted)
        
    
    # Read a specified log file    
    def readLog(self):
        log_file = input(f"\n{Color.white}--> logfile (eg. 2022-04-27 10:09:36AM.log){Color.reset} ")
        with open(f'.logs/{log_file}', 'r') as log:
            logging.info(logMsg.readingFile.format(log_file))
            print("\n"+log.read())
        		
    
    # Update program
    def installUpdate(self):
    	files_to_update = ['core/main.py','utilities/helper.py','utilities/misc.py','utilities/colors.py','octosuite','.github/dependabot.yml','.github/ISSUE_TEMPLATE/bug_report.md','.github/ISSUE_TEMPLATE/feature_request.md','.github/ISSUE_TEMPLATE/config.yml','LICENSE','README.md','requirements.txt']
    	logging.info(logMsg.installingUpdates)
    	for file in tqdm(files_to_update,desc = logMsg.installingUpdates):
    		data = requests.get(f'https://raw.githubusercontent.com/rly0nheart/octosuite/master/{file}')
    		with open(file, 'wb') as code:
    			code.write(data.content)
    			code.close()
    	
    	logging.info(logMsg.installedUpdates.format(len(files_to_update)))		
    	print(Attributes.positive, logMsg.installedUpdates.format(len(files_to_update)));exit()
    	
    	
    def checkUpdate(self):
        logging.info(logMsg.checkingUpdates)
        response = requests.get("https://api.github.com/repos/rly0nheart/octosuite/releases/latest")
        if response.json()['tag_name'] == Banner.versionTag:
            print(f"{Attributes.positive} OctoSuite is up to date. Check again soon :)")
        else:
        	print(f"{Attributes.info} A new release is available ({response.json()['tag_name']}). Use command {Color.green}update:install{Color.white} to download and install the updates.{Color.reset}")
    	
    	
    # Show version information
    def versionInfo(self):
    	# Yes... the changelog is actually hard coded
    	# It's actually frustrating having to change this everytime I publish a new release lol
    	print(f'''
Tag: {Banner.versionTag}
Released at: 2022-05-25 11:05AM
{'-'*31}

What's changed?
{'-'*15}
[✓] Fixed a bug in issue #2''')
    	
    	
    # Author info
    def author(self):
        print(f'\n{Color.white}Richard Mwewa (Ritchie){Color.reset}')
        for key,value in self.author_dict.items():
        	print(f'{Color.white}├─ {key}: {Color.green}{value}{Color.reset}')


    def about(self):
        print('''
     OCTOSUITE (C) 2022 Richard Mwewa
        
is an advanced and lightning fast framework for gathering open-source intelligence on GitHub users and organizations.''')

        	     
    # Close session 	
    def exitSession(self):
        logging.info(logMsg.sessionClosed)
        print(Attributes.info, logMsg.sessionClosed);exit()
        
    
    def clearScreen(self):
        if sys.platform.lower().startswith(('win','darwin')):
            subprocess.run(['cls'])
        else:
            subprocess.run(['clear'],shell=False)
