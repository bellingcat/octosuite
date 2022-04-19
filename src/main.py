'''
            octosuite Advanced Github OSINT Framework
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
import requests
import platform
import subprocess
from tqdm import tqdm
from pprint import pprint
from lib.banner import banner
from datetime import datetime
from lib.colors import red, white, green, green_bg, white_bg, red_bg, reset

class octosuite:
    def __init__(self):
        # A list of tuples, mapping commands to their respective functionalities
        self.commands_base = [('info:org', self.org_info),
                                                   ('info:user', self.user_profile),
                                                   ('info:repo', self.repo_info),
                                                   ('path:contents', self.path_contents),
                                                   ('repos:org', self.org_repos),
                                                   ('repos:user', self.user_repos),
                                                   ('user:gists', self.user_gists),
                                                   ('user:followers', self.followers),
                                                   ('user:following', self.following),
                                                   ('search:users', self.user_search),
                                                   ('search:repos', self.repo_search),
                                                   ('search:topics', self.topic_search),
                                                   ('search:issues', self.issue_search),
                                                   ('search:commits', self.commits_search),
                                                   ('update', self.update),
                                                   ('changelog', self.changelog),
                                                   ('info:dev', self.author),
                                                   ('help', self.help),
                                                   ('exit', self.exit_session)]
                                                   
                                                   
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
        self.repo_attrs = ['id','description','forks','allow_forking','fork','stargazers_count','watchers','license','default_branch','visibility','language','open_issues','topics','homepage','clone_url','ssh_url','private','archived','has_downloads','has_issues','has_pages','has_projects','has_wiki','pushed_at','created_at','updated_at']
        # Repository attribute dictionary
        self.repo_attr_dict = {'id': 'ID#',
                                              'description': 'About',
                                              'forks': 'Forks',
                                              'allow_forking': 'Is forkable?',
                                              'fork': 'Is fork?',
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
                                               
                                               
        # Author dictionary
        self.author_dict = {'Alias': 'rly0nheart',
                                         'Country': 'Zambia, Africa',
                                         'About.me': 'https://about.me/rly0nheart'}    
 
               
    def on_start(self):
        # Start new session
        logging.info(f'Started new session on {platform.node()}:{os.getlogin()}')
        
        # Use 'cls' to clear screen on Windows based machines
        # Otherwise, use 'clear'
        while True:
            if sys.platform.lower().startswith(('win','darwin')):
                subprocess.run(['cls'])
            else:
            	subprocess.run(['clear'],shell=False)
            	
            print(banner)
            command_input = input(f'''{white}┌───({red}{os.getlogin()}{white}@{red}octosuite{white})-[{green}{os.getcwd()}{white}]\n└─╼[{green}:~{white}]{reset} ''')        
            # Looping through the commands base to check if the user input command matches any command in the commands base, and return its functionality
            # If no match is found, we ignore it
            for command, functionality in self.commands_base:
                if command == command_input:
                	functionality()
                else:
                    pass
                    
            input(f'\n{white}[{green} ? {white}] Press {white_bg}any key{reset}{white} to continue{reset} ')
            
            
    def org_info(self):
        organization = input(f'\n{white}[{white_bg}@Organization{reset}{white}] (username){reset} ')
        api = f'https://api.github.com/orgs/{organization}'
        response = requests.get(api)
        if response.status_code != 200:
        	print(f'\n{white}[{red}-{white}] Organization @{organization} {red_bg}Not Found{reset}')
        else:
        	response = response.json()
        	print(f"\n{white}{response['name']}{reset}")
        	for attr in self.org_attrs:
        		print(f'{white}├─ {self.org_attr_dict[attr]}: {green}{response[attr]}{reset}')
        
                        
    # Fetching user information        
    def user_profile(self):
        username = input(f'\n{white}[{white_bg}@Username{reset}{white}]{reset} ')
        api = f'https://api.github.com/users/{username}'
        response = requests.get(api)
        if response.status_code != 200:
        	print(f'\n{white}[{red} - {white}] User @{username} {red_bg}Not Found{reset}')
        else:
        	response = response.json()
        	print(f"\n{white}{response['name']}{reset}")
        	for attr in self.profile_attrs:
        		print(f'{white}├─ {self.profile_attr_dict[attr]}: {green}{response[attr]}{reset}')

        	        	
    # Fetching repository information   	
    def repo_info(self):
        repo_name = input(f'\n{white}[{white_bg}%reponame{reset}{white}]{reset} ')
        username = input(f'{white}[{white_bg}@Owner{reset}{white}] (username){reset} ')
        api = f'https://api.github.com/repos/{username}/{repo_name}'
        response = requests.get(api)
        if response.status_code != 200:
        	print(f'\n{white}[{red} - {white}] Repository %{repo_name} or user @{username} {red_bg}Not Found{reset}')
        else:
        	response = response.json()
        	print(f"\n{white}{response['full_name']}{reset}")
        	for attr in self.repo_attrs:
        	    print(f"{white}├─ {self.repo_attr_dict[attr]}: {green}{response[attr]}{reset}")
            
    
    # Get path contents        
    def path_contents(self):
        username = input(f'\n{white}[{white_bg}@Owner{reset}{white}] (username){reset} ')
        repo_name = input(f'{white}[{white_bg}%reponame{reset}{white}]{reset} ')
        path_name = input(f'{white}[{white_bg}/path/name{reset}{white}]{reset} ')
        api = f'https://api.github.com/repos/{username}/{repo_name}/contents/{path_name}'
        response = requests.get(api)
        if response.status_code != 200:
            print(f'\n{white}[{red} - {white}] Information {red_bg}Not Found{reset}')
        else:
        	response = response.json()
        	for item in response:
        	    print(f"\n{white}{item['name']}{reset}")
        	    for attr in self.path_attrs:
        	    	print(f'{white}├─ {self.path_attr_dict[attr]}: {green}{item[attr]}{reset}')
            	
                       
    # Fetching organozation repositories        
    def org_repos(self):
        organization = input(f'\n{white}[{white_bg}@Organization{reset}{white}] (username){reset} ')
        api = f'https://api.github.com/orgs/{organization}/repos?per_page=100'
        response = requests.get(api)
        if response.status_code != 200:
            print(f'\n{white}[{red} - {white}] Organization @{organization} {red_bg}Not Found{reset}')
        else:
            response = response.json()
            for repo in response:
            	print(f"\n{white}{repo['full_name']}{reset}")
            	for attr in self.repo_attrs:
            		print(f"{white}├─ {self.repo_attr_dict[attr]}: {green}{repo[attr]}{reset}")
            	print('\n')
         
               
    # Fetching user repositories        
    def user_repos(self):
        username = input(f'\n{white}[{white_bg}@Username{reset}{white}]{reset} ')
        api = f'https://api.github.com/users/{username}/repos?per_page=100'
        response = requests.get(api)
        if response.status_code != 200:
        	print(f'\n{white}[{red} - {white}] User @{username} {red_bg}Not Found{reset}')
        else:
        	response = response.json()
        	for repo in response:
        		print(f"\n{white}{repo['full_name']}{reset}")
        		for attr in self.repo_attrs:
        			print(f"{white}├─ {self.repo_attr_dict[attr]}: {green}{repo[attr]}{reset}")
        		print('\n')        	    
        	
        	   	       	    
    # Fetching user's gists
    def user_gists(self):
        username = input(f'\n{white}[{white_bg}@Username{reset}{white}]{reset} ')
        api = f'https://api.github.com/users/{username}/gists'
        response = requests.get(api).json()
        if response == []:
        	print(f'\n{white}[{red} - {white}] User @{username} {red_bg}does not{reset}{white} have any active gists.{reset}')
        elif "Not Found" in response['message']:
        	print(f'\n{white}[{red} - {white}] User @{username} {red_bg}Not Found{reset}')
        else:
            for item in response:
            	print(f"\n{white}{item['id']}{reset}")
            	for attr in self.gists_attrs:
            		print(f"{white}├─ {self.gists_attr_dict[attr]}: {green}{item[attr]}{reset}")
            	print('\n')    	
        
        	    	    
    # Fetching user's followera'    	    
    def followers(self):
        username = input(f'\n{white}[{white_bg}@Username{reset}{white}]{reset} ')
        api = f'https://api.github.com/users/{username}/followers?per_page=100'
        response = requests.get(api).json()
        if response == []:
        	print(f'\n{white}[{red} - {white}]User @{username} {red_bg}does not{reset}{white} have followers.{reset}')
        elif "Not Found" in response['message']:
        	print(f'\n{white}[{red} - {white}] User @{username} {red_bg}Not Found{reset}')
        else:
            for item in response:
            	print(f"\n{white}@{item['login']}{reset}")
            	for attr in self.user_attrs:
            		print(f"{white}├─ {self.user_attr_dict[attr]}: {green}{item[attr]}{reset}")
            	print('\n')
            
                    
    # Checking whether or not user[A] follows user[B]            
    def following(self):
        user_a = input(f'\n{white}[{white_bg}@User A{reset}{white}] (username){reset} ')
        user_b = input(f'{white}[{white_bg}@User B{reset}{white}] (username){reset} ')
        api = f'https://api.github.com/users/{user_a}/following/{user_b}'
        response = requests.get(api)
        if response.status_code == 204:
        	print(f'\n{white}[{green} + {white}] @{user_a} {green_bg}follows{reset}{white} @{user_b}.{reset}')
        else:
        	print(f'\n{white}[{red} - {white}] @{user_a} {red_bg}does not{reset}{white} follow @{user_b}.{reset}')             
 
        	           	    
    # User search    	    
    def user_search(self):
        query = input(f'\n{white}[{white_bg}#@Query{reset}{white}]{reset} ')
        api = f'https://api.github.com/search/users?q={query}&per_page=100'
        response = requests.get(api).json()
        for item in response['items']:
        	print(f"\n{white}@{item['login']}{reset}")
        	for attr in self.user_attrs:
        		print(f"{white}├─ {self.user_attr_dict[attr]}: {green}{item[attr]}{reset}")
        	print('\n')
        		
       		
    # Repository search
    def repo_search(self):
        query = input(f'\n{white}[{white_bg}#%Query{reset}{white}]{reset} ')
        api = f'https://api.github.com/search/repositories?q={query}&per_page=100'
        response = requests.get(api).json()
        for item in response['items']:
            print(f"\n{white}{item['full_name']}{reset}")
            for attr in self.repo_attrs:
                print(f"{white}├─ {self.repo_attr_dict[attr]}: {green}{item[attr]}{reset}")
            print('\n')
                
                
    # Topics search
    def topic_search(self):
        query = input(f'\n{white}[{white_bg}##Query{reset}{white}]{reset} ')
        api = f'https://api.github.com/search/topics?q={query}&per_page=100'
        response = requests.get(api).json()
        for item in response['items']:
            print(f"\n{white}{item['name']}{reset}")
            for attr in self.topic_attrs:
                print(f"{white}├─ {self.topic_attr_dict[attr]}: {green}{item[attr]}{reset}")
            print('\n')
                
                
    # Issue search
    def issue_search(self):
        query = input(f'\n{white}[{white_bg}#!Query{reset}{white}]{reset} ')
        api = f'https://api.github.com/search/issues?q={query}&per_page=100'
        response = requests.get(api).json()
        for item in response['items']:
            print(f"\n{white}{item['title']}{reset}")
            for attr in self.issue_attrs:
                print(f"{white}├─ {self.issue_attr_dict[attr]}: {green}{item[attr]}{reset}")
            print('\n')
            
            
    # Commits search
    def commits_search(self):
        query = input(f'\n{white}[{white_bg}#:Query{reset}{white}]{reset} ')
        api = f'https://api.github.com/search/commits?q={query}&per_page=100'
        response = requests.get(api).json()
        number=0
        for item in response['items']:
        	number+=1
        	print(f'{white}{number}.{reset}')
        	pprint(item['commit'])
        	print('\n')
        		
    
    # Update program
    def update(self):
    	logging.info('Updating...')
    	files_to_update = ['src/main.py','lib/banner.py','lib/colors.py','octosuite','.github/dependabot.yml','.github/ISSUE_TEMPLATE/bug_report.md','.github/ISSUE_TEMPLATE/feature_request.md','.github/ISSUE_TEMPLATE/config.yml','LICENSE','README.md','requirements.txt']
    	for file in tqdm(files_to_update,desc=f'{white}[{green} * {white}] Updating{reset}'):
    		data = requests.get(f'https://raw.githubusercontent.com/rly0nheart/octosuite/master/{file}')
    		with open(file, 'wb') as code:
    			code.write(data.content)
    			code.close()
    	
    	logging.info('Update complete.')		
    	exit(f'{white}[{green} + {white}] {green_bg}Updated{reset}{white} successfully. Re-run octosuite.{reset}')
    	
    	
    # Show changelog
    def changelog(self):
    	# lol yes the changelog is hard coded
    	changelog_text = f'''
    	
     {red_bg}v1.6.0-stable [CHANGELOG]{reset}
     • Minor improvements and bug fixes
     {red_bg}                         {reset}
     '''
    	print(changelog_text)
    	
    	
    # Author info   
    def author(self):
        print(f'\n{white}Richard Mwewa (Ritchie){reset}')
        for key,value in self.author_dict.items():
        	print(f'{white}├─ {key}: {green}{value}{reset}')
        	
        	
    def exit_session(self):
        logging.info('Session closed with \'exit\' command.')
        exit(f'\n{white}[{green} ! {white}] Session closed with {white_bg}exit{reset}{white} command.{reset}')
        	
        	
    def help(self):
    	help = f'''

   {red_bg}[COMMAND]                 [DESCRIPTION]               {reset}
   info:org                  Get target organization info
   info:user                 Get target user profile info
   info:repo                 Get target repository info
   info:dev                  Show developer's info
   path:contents             Get contents of a specified path from a target repository
   repos:org                 Get a list of repositories owned by a target organization
   repos:user                Get a list of repositories owned by a target user
   user:gists                Get a list of gists owned by a target user
   user:followers            Get a list of the target's followers
   user:following            Check whether or not User[A] follows User[B]
   search:users              Search user(s)
   search:repos              Search repositor[y][ies]
   search:topics             Search topic(s)
   search:issues             Search issue(s)
   search:commits            Search commit(s)
   update                    Update octosuite
   changelog                 Show changelog
   help                      Show usage/help
   exit                      Exit session
   {red_bg}                                                      {reset}
   '''
    	print(help)


# If .logs folder exists, pass
if os.path.exists('.logs'):
	pass
	
else:
	# Creating the .logs directory
	# If the current system is Windows based, we run mkdir command without sudo
	# Else we run the mkdir command with sudo
	if sys.platform.lower().startswith(('win','darwin')):
		subprocess.run(['mkdir','.logs'])
	else:
		subprocess.run(['sudo','mkdir','.logs'],shell=False)
		
# Set to automatically monitor and log network and user activity into the .logs folder
logging.basicConfig(filename=f'.logs/{datetime.now()}.log',format='[%(asctime)s] [%(levelname)s] %(message)s',datefmt='%Y-%m-%d %H:%M:%S%p',level=logging.DEBUG)
