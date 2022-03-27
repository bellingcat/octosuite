import os
import logging
import requests
import platform
import subprocess
import urllib.request
from tqdm import tqdm
from pprint import pprint
from lib import colors,banner
from datetime import datetime

class octosuite:
    def __init__(self):
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
        logging.info(f'Started new session on {platform.node()}')
        while True:
            if platform.system() == 'Windows':
            	subprocess.run(['cls'])
            else:
            	subprocess.run(['clear'],shell=False)
            	
            print(banner.banner)
            command = input(f'''{colors.white}┌─({colors.red}{platform.node()}{colors.white}@{colors.red}octosuite{colors.white})-[{colors.green}{os.getcwd()}{colors.white}]\n└─╼[{colors.green}:~{colors.white}]{colors.reset} ''')
            if command == 'orginfo':
            	self.org_info()
            elif command == 'userinfo':
            	self.user_profile()
            elif command == 'repoinfo':
            	self.repo_info()
            elif command == 'pathcontents':
            	self.path_contents()
            elif command == 'orgrepos':
            	self.org_repos()
            elif command == 'userrepos':
            	self.user_repos()
            elif command == 'usergists':
            	self.user_gists()
            elif command == 'userfollowers':
            	self.followers()
            elif command == 'userfollowing':
            	self.following()
            elif command == 'usersearch':
            	self.user_search()
            elif command == 'reposearch':
            	self.repo_search()
            elif command == 'topicsearch':
            	self.topic_search()
            elif command == 'issuesearch':
            	self.issue_search()
            elif command == 'commitsearch':
            	self.commits_search()
            elif command == 'update':
            	self.update()
            elif command == 'author':
            	self.author()
            elif command == 'help':
            	print(self.help())
            elif command == 'exit':
            	logging.info('Session terminated.')
            	exit(f'\n{colors.white}[{colors.red}-{colors.white}] Session terminated.{colors.reset}')
            else:
                print(f'\n{colors.white}[{colors.red}!{colors.white}] Unknown command: ‘{command}’{colors.reset}')
                logging.warning(f'Unknown command: ‘{command}’')
                   
            input(f'\n{colors.white}^ Press any key to continue{colors.reset} ')
            
            
    def org_info(self):
        organization = input(f'{colors.white}@{colors.green}Organization{colors.white} >> {colors.reset}')
        api = f'https://api.github.com/orgs/{organization}'
        response = requests.get(api)
        if response.status_code != 200:
        	print(f'\n{colors.white}[{colors.red}-{colors.white}] Organization @{organization} {colors.red}Not Found{colors.reset}')
        else:
        	response = response.json()
        	print(f"\n{colors.white}{response['name']}{colors.reset}")
        	for attr in self.org_attrs:
        		print(f'{colors.white}├─ {self.org_attr_dict[attr]}: {colors.green}{response[attr]}{colors.reset}')
        
                        
    # Fetching user information        
    def user_profile(self):
        username = input(f'{colors.white}@{colors.green}Username{colors.white} >> {colors.reset}')
        api = f'https://api.github.com/users/{username}'
        response = requests.get(api)
        if response.status_code != 200:
        	print(f'\n{colors.white}[{colors.red}-{colors.white}] User @{username} {colors.red}Not Found{colors.reset}')
        else:
        	response = response.json()
        	print(f"\n{colors.white}{response['name']}{colors.reset}")
        	for attr in self.profile_attrs:
        		print(f'{colors.white}├─ {self.profile_attr_dict[attr]}: {colors.green}{response[attr]}{colors.reset}')

        	        	
    # Fetching repository information   	
    def repo_info(self):
        username = input(f'{colors.white}@{colors.green}Owner-username{colors.white} >> {colors.reset}')
        repo_name = input(f'{colors.white}%{colors.green}reponame{colors.white} >> {colors.reset}')
        api = f'https://api.github.com/repos/{username}/{repo_name}'
        response = requests.get(api)
        if response.status_code != 200:
        	print(f'\n{colors.white}[{colors.red}-{colors.white}] Repository %{repo_name} {colors.red}Not Found{colors.reset}')
        else:
        	response = response.json()
        	print(f"\n{colors.white}{response['full_name']}{colors.reset}")
        	for attr in self.repo_attrs:
        	    print(f"{colors.white}├─ {self.repo_attr_dict[attr]}: {colors.green}{response[attr]}{colors.reset}")
            
    
    # Get path contents        
    def path_contents(self):
        username = input(f'{colors.white}@{colors.green}Owner-username{colors.white} >> {colors.reset}')
        repo_name = input(f'{colors.white}%{colors.green}reponame{colors.white} >> {colors.reset}')
        path_name = input(f'{colors.white}/path/name >>{colors.reset} ')
        api = f'https://api.github.com/repos/{username}/{repo_name}/contents/{path_name}'
        response = requests.get(api)
        if response.status_code != 200:
            print(f'\n{colors.white}[{colors.red}-{colors.white}] Information {colors.red}Not Found{colors.reset}')
        else:
        	response = response.json()
        	for item in response:
        	    print(f"\n{colors.white}{item['name']}{colors.reset}")
        	    for attr in self.path_attrs:
        	    	print(f'{colors.white}├─ {self.path_attr_dict[attr]}: {colors.green}{item[attr]}{colors.reset}')
            	
                       
    # Fetching organozation repositories        
    def org_repos(self):
        organization = input(f'{colors.white}@{colors.green}Organization{colors.white} >> {colors.reset}')
        api = f'https://api.github.com/orgs/{organization}/repos?per_page=100'
        response = requests.get(api)
        if response.status_code != 200:
            print(f'\n{colors.white}[{colors.red}-{colors.white}] Organization @{organization} {colors.red}Not Found{colors.reset}')
        else:
            response = response.json()
            for repo in response:
            	print(f"\n{colors.white}{repo['full_name']}{colors.reset}")
            	for attr in self.repo_attrs:
            		print(f"{colors.white}├─ {self.repo_attr_dict[attr]}: {colors.green}{repo[attr]}{colors.reset}")
            	print('\n')
         
               
    # Fetching user repositories        
    def user_repos(self):
        username = input(f'{colors.white}@{colors.green}Username{colors.white} >> {colors.reset}')
        api = f'https://api.github.com/users/{username}/repos?per_page=100'
        response = requests.get(api)
        if response.status_code != 200:
        	print(f'\n{colors.white}[{colors.red}-{colors.white}] User @{username} {colors.red}Not Found{colors.reset}')
        else:
        	response = response.json()
        	for repo in response:
        		print(f"\n{colors.white}{repo['full_name']}{colors.reset}")
        		for attr in self.repo_attrs:
        			print(f"{colors.white}├─ {self.repo_attr_dict[attr]}: {colors.green}{repo[attr]}{colors.reset}")
        		print('\n')        	    
        	
        	   	       	    
    # Fetching user's gists
    def user_gists(self):
        username = input(f'{colors.white}@{colors.green}Username{colors.white} >> {colors.reset}')
        api = f'https://api.github.com/users/{username}/gists'
        response = requests.get(api).json()
        if response == []:
        	print(f'{colors.white}[{colors.red}-{colors.white}]User @{username} does not have any active gists.{colors.reset}')
        else:
            for item in response:
            	print(f"\n{colors.white}{item['id']}{colors.reset}")
            	for attr in self.gists_attrs:
            		print(f"{colors.white}├─ {self.gists_attr_dict[attr]}: {colors.green}{item[attr]}{colors.reset}")
            	print('\n')    	
        
        	    	    
    # Fetching user's followera'    	    
    def followers(self):
        username = input(f'{colors.white}@{colors.green}Username{colors.white} >> {colors.reset}')
        api = f'https://api.github.com/users/{username}/followers?per_page=100'
        response = requests.get(api).json()
        if response == []:
        	print(f'\n{colors.white}[{colors.red}-{colors.white}]User @{username} does not have followers.{colors.reset}')
        else:
            for item in response:
            	print(f"\n{colors.white}@{item['login']}{colors.reset}")
            	for attr in self.user_attrs:
            		print(f"{colors.white}├─ {self.user_attr_dict[attr]}: {colors.green}{item[attr]}{colors.reset}")
            	print('\n')
            
                    
    # Checking whether or not user[A] follows user[B]            
    def following(self):
        user_a = input(f'{colors.white}@{colors.green}User[A]{colors.white} >> {colors.reset}')
        user_b = input(f'{colors.white}@{colors.green}User[B]{colors.white} >> {colors.reset}')
        api = f'https://api.github.com/users/{user_a}/following/{user_b}'
        response = requests.get(api)
        if response.status_code == 204:
        	print(f'{colors.white}[{colors.green}+{colors.white}] @{user_a} follows @{user_b}.{colors.reset}')
        else:
        	print(f'{colors.white}[{colors.red}-{colors.white}] @{user_a} does not follow @{user_b}.{colors.reset}')             
 
        	           	    
    # User search    	    
    def user_search(self):
        query = input(f'{colors.white}#{colors.green}Query{colors.white} >> {colors.reset}')
        api = f'https://api.github.com/search/users?q={query}&per_page=100'
        response = requests.get(api).json()
        for item in response['items']:
        	print(f"\n{colors.white}@{item['login']}{colors.reset}")
        	for attr in self.user_attrs:
        		print(f"{colors.white}├─ {self.user_attr_dict[attr]}: {colors.green}{item[attr]}{colors.reset}")
        	print('\n')
        		
       		
    # Repository search
    def repo_search(self):
        query = input(f'{colors.white}#{colors.green}Query{colors.white} >> {colors.reset}')
        api = f'https://api.github.com/search/repositories?q={query}&per_page=100'
        response = requests.get(api).json()
        for item in response['items']:
            print(f"\n{colors.white}{item['full_name']}{colors.reset}")
            for attr in self.repo_attrs:
                print(f"{colors.white}├─ {self.repo_attr_dict[attr]}: {colors.green}{item[attr]}{colors.reset}")
            print('\n')
                
                
    # Topics search
    def topic_search(self):
        query = input(f'{colors.white}#{colors.green}Query{colors.white} >> {colors.reset}')
        api = f'https://api.github.com/search/topics?q={query}&per_page=100'
        response = requests.get(api).json()
        for item in response['items']:
            print(f"\n{colors.white}{item['name']}{colors.reset}")
            for attr in self.topic_attrs:
                print(f"{colors.white}├─ {self.topic_attr_dict[attr]}: {colors.green}{item[attr]}{colors.reset}")
            print('\n')
                
                
    # Issue search
    def issue_search(self):
        query = input(f'{colors.white}#{colors.green}Query{colors.white} >> {colors.reset}')
        api = f'https://api.github.com/search/issues?q={query}&per_page=100'
        response = requests.get(api).json()
        for item in response['items']:
            print(f"\n{colors.white}{item['title']}{colors.reset}")
            for attr in self.issue_attrs:
                print(f"{colors.white}├─ {self.issue_attr_dict[attr]}: {colors.green}{item[attr]}{colors.reset}")
            print('\n')
            
            
    # Commits search
    def commits_search(self):
        query = input(f'{colors.white}#{colors.green}Query{colors.white} >> {colors.reset}')
        api = f'https://api.github.com/search/commits?q={query}&per_page=100'
        response = requests.get(api).json()
        n=0
        for item in response['items']:
        	n+=1
        	print(f'{colors.white}{n}.{colors.reset}')
        	pprint(item['commit'])
        	print('\n')
        		
    
    # Update program
    def update(self):
    	logging.info('Fetching updates...')
    	files_to_update = ['src/main.py','lib/banner.py','lib/colors.py','octosuite','LICENSE','README.md','requirements.txt']
    	for file in tqdm(files_to_update,desc=f'{colors.white}[{colors.green}*{colors.white}] Fetching updates...{colors.reset}'):
    		data = urllib.request.urlopen(f'https://raw.githubusercontent.com/rly0nheart/octosuite/master/{file}').read()
    		with open(file, 'wb') as code:
    			code.write(data)
    			code.close()
    	
    	logging.info('Update complete.')		
    	exit(f'\n{colors.white}[{colors.green}+{colors.white}] Update complete. Re-run octosuite.{colors.reset}')
    	
    	
    # Author info   
    def author(self):
        print(f'\n{colors.white}Richard Mwewa (Ritchie){colors.reset}')
        for key,value in self.author_dict.items():
        	print(f'{colors.white}├─ {key}: {colors.green}{value}{colors.reset}')
        	
        	
    def help(self):
    	help = '''
    	
usage:
   orginfo           -->    Get target organization info
   userinfo          -->    Get target user profile info
   repoinfo          -->    Get target repository info
   pathcontents      -->    Get contents of a specified path from a target repository
   orgrepos          -->    Get a list of repositories owned by a target organization
   userrepos         -->    Get a list of repositories owned by a target user
   usergists         -->    Get a list of gists owned by a target user
   userfollowers     -->    Get a list of the target's followers
   userfollowing     -->    Check whether or not User[A] follows User[B]
   usersearch        -->    Search user(s)
   reposearch        -->    Search repositor[y][ies]
   topicsearch       -->    Search topic(s)
   issuesearch       -->    Search issue(s)
   commitsearch      -->    Search commit(s)
   update            -->    Update octosuite
   author            -->    Show author info
   help              -->    Show usage/help
   exit              -->    Exit session
   '''
    	return help


# Set to automatically monitor and log network and user activity to .log folder
logging.basicConfig(filename=f'.logs/{datetime.now()}.log',format='[%(asctime)s] %(message)s',level=logging.DEBUG)
