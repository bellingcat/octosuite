#!usr/bin/python

import os
import csv 
import sys
import json
import logging
import getpass
import requests
import platform
import subprocess
from pprint import pprint
from datetime import datetime
from octosuite.helper import Help
from octosuite.colors import Color
from octosuite.banner import Banner
from octosuite.sign_vars import SignVar
from octosuite.log_roller import logRoller
from octosuite.csv_loggers import csvLogger


global endpoint
global path_attrs
global path_attr_dict
global org_attrs
global org_attr_dict
global repo_attrs
global repo_attr_dict
global repo_releases_attrs
global repo_releases_attr_dict
global profile_attrs
global profile_attr_dict
global user_attrs
global user_attr_dict
global topic_attrs
global topic_attr_dict
global gists_attrs
global gists_attr_dict
global issue_attrs
global issue_attr_dict
global repo_issues_attrs
global repo_issues_attr_dict
global user_orgs_attrs
global user_orgs_attr_dict
global author_dict


# API endpoint
endpoint = 'https://api.github.com'
# Path attribute
path_attrs =['size','type','path','sha','html_url']
# Path attribute dictionary
path_attr_dict = {'size': 'Size (bytes)',
                  'type': 'Type',
                  'path': 'Path',
                  'sha': 'SHA',
                  'html_url': 'URL'}
                                             
                                             
# Organization attributes
org_attrs = ['avatar_url','login','id','node_id','email','description','blog','location','followers','following','twitter_username','public_gists','public_repos','type','is_verified','has_organization_projects','has_repository_projects','created_at','updated_at']
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
repo_attrs = ['id','description','forks','stargazers_count','watchers','license','default_branch','visibility','language','open_issues','topics','homepage','clone_url','ssh_url','fork','allow_forking','private','archived','has_downloads','has_issues','has_pages','has_projects','has_wiki','pushed_at','created_at','updated_at']
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
repo_releases_attrs = ['id', 'node_id','tag_name','target_commitish','assets','draft','prerelease','created_at','published_at']
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
profile_attrs = ['avatar_url','login','id','node_id','bio','blog','location','followers','following','twitter_username','public_gists','public_repos','company','hireable','site_admin','created_at','updated_at']
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
user_attrs = ['avatar_url','id','node_id','gravatar_id','site_admin','type','html_url']
# User attribute dictionary
user_attr_dict = {'avatar_url': 'Profile Photo',
                  'id': 'ID',
                  'node_id': 'Node ID',
                  'gravatar_id': 'Gravatar ID',
                  'site_admin': 'Is site admin?',
                  'type': 'Account type',
                  'html_url': 'URL'}
                                         
                                         
# Topic atrributes
topic_attrs = ['score','curated','featured','display_name','created_by','created_at','updated_at']
# Topic attribute dictionary
topic_attr_dict = {'score': 'Score',
                   'curated': 'Curated',
                   'featured': 'Featured',
                   'display_name': 'Display name',
                   'created_by': 'Created by',
                   'created_at': 'Created at',
                   'updated_at': 'Updated at'}
                                               
        
# Gists attributes
gists_attrs = ['node_id','description','comments','files','git_push_url','public','truncated','updated_at']
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
issue_attrs = ['id','node_id','score','state','number','comments','milestone','assignee','assignees','labels','locked','draft','closed_at']
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
repo_issues_attrs = ['id','node_id','state', 'reactions','number','comments','milestone','assignee','active_lock_reason', 'author_association','assignees','labels','locked','closed_at','created_at','updated_at']
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
user_orgs_attrs = ['avatar_url','id','node_id','url','description']
user_orgs_attr_dict = {'avatar_url': 'Profile Photo',
                       'id': 'ID',
                       'node_id': 'Node ID',
                       'url': 'URL',
                       'description': 'About'}
                                               
                                               
# Author dictionary
author_dict = {'Alias': 'rly0nheart',
               'Country': 'Zambia, Africa',
               'About.me': 'https://about.me/rly0nheart',
               'BuyMeACoffee': 'https://buymeacoffee.com/189381184'}
                          

'''
pathFinder()
This function is responsible for creating/checking the availability of  the (.logs, output, downloads) folders,
enabling logging to automatically log network/user activity to a file,
and logging the start of a session.
'''
def pathFinder():
    '''
    Windows based machines
    Here we check the existence of 3 directories
    If the directories exist, we ignore them.
    If not, we create them.
    '''
    if sys.platform.lower().startswith(('win', 'darwin')):
        if os.path.exists('.logs'):
        	pass
        else:
        	subprocess.run(['mkdir','.logs'])
        	
        if os.path.exists('output'):
        	pass
        else:
        	subprocess.run(['mkdir','output'])
        	
        if os.path.exists('downloads'):
        	pass
        else:
        	subprocess.run(['mkdir','.downloads'])
    else:
        '''
        Here we do the same as above,
        except we are not creating on windows based machines
        '''
        if os.path.exists('.logs'):
        	pass
        else:
        	subprocess.run(['sudo','mkdir','.logs'], shell=False)
        	
        if os.path.exists('output'):
        	pass
        else:
        	subprocess.run(['sudo','mkdir','output'], shell=False)
        	
        if os.path.exists('downloads'):
            pass
        else:
        	subprocess.run(['sudo', 'mkdir', 'downloads'], shell=False)
        	
    '''
    Configure logging to log activities to a file, which will be named by the date and time a session was opened.
    '''
    now = datetime.now()
    now_formatted = now.strftime('%Y-%m-%d %H:%M:%S%p')
    logging.basicConfig(filename=f'.logs/{now_formatted}.log', format='[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S%p', level=logging.DEBUG)
    # Log the start of a session
    logging.info(logRoller.sessionOpened.format(platform.node(), getpass.getuser()))
    

'''
onStart()
This is the main function, responsible for mapping commands, calling other functions, and catching exceptions
'''
def onStart():
    pathFinder()
    # A list of tuples mapping commands to their functions
    command_map = [('org', Help.Org),
                    ('org:events', orgEvents),
                    ('org:profile', orgProfile),
                    ('org:repos', orgRepos),
                    ('org:member', orgMember),
                    ('repo', Help.Repo),
                    ('repo:pathcontents', pathContents),
                    ('repo:profile', repoProfile),
                    ('repo:contributors', repoContributors),
                    ('repo:stargazers', repoStargazers),
                    ('repo:forks', repoForks),
                    ('repo:issues', repoIssues),
                    ('repo:releases', repoReleases),
                    ('user', Help.User),
                    ('user:repos', userRepos),
                    ('user:gists', userGists),
                    ('user:orgs', userOrgs),
                    ('user:profile', userProfile),
                    ('user:events', userEvents),
                    ('user:followers', userFollowers),
                    ('user:follows', userFollows),
                    ('user:following', userFollowing),
                    ('user:subscriptions', userSubscriptions),
                    ('search', Help.Search),
                    ('search:users', userSearch),
                    ('search:repos', repoSearch),
                    ('search:topics', topicSearch),
                    ('search:issues', issueSearch),
                    ('search:commits', commitsSearch),
                    ('source', Help.Source),
                    ('source:tarball', downloadTarball),
                    ('source:zipball', downloadZipball),
                    ('logs', Help.Logs),
                    ('logs:view',viewLogs),
                    ('logs:read',readLog),
                    ('logs:delete',deleteLog),
                    ('help', Help.helpCommand),
                    ('help:version', Help.versionCommand),
                    ('help:source', Help.sourceCommand),
                    ('help:search', Help.searchCommand),
                    ('help:user',  Help.userCommand),
                    ('help:repo',  Help.repoCommand),
                    ('help:logs',  Help.logsCommand),
                    ('help:org',  Help.orgCommand),
                    ('author', author),
                    ('about', about),
                    ('clear',clearScreen),
                    ('version', Help.Version),
                    ('version:info', versionInfo),
                    ('version:check', versionCheck),
                    ('exit', exitSession)]
                             
                             
    print(Banner.nameLogo)
    '''
    Main loop keeps octosuite running, this will break if Octosuite detects a KeyboardInterrupt (Ctrl+C)
    or if the 'exit' command is entered.
    '''
    while True:
        try:
            command_input = input(f'''{Color.white}┌──({Color.red}{getpass.getuser()}{Color.white}@{Color.red}octosuite{Color.white})\n├──[{Color.green}~{os.getcwd()}{Color.white}]\n└╼{Color.reset} ''').lower()
            print('\n')
            '''
            Iterating over the command_map and check if the user input matches any command in it [command_map],
            if there's a match, we return its function. If no match is found, we ignore it.
            '''
            for command, function in command_map:
                if command_input == command:
                    function()
                    print('\n')
                else:
                    pass
        
        # This catches the KeyboardInterrupt exception (Ctrl+C)
        except KeyboardInterrupt:
            logging.warning(logRoller.Ctrl.format('Ctrl+C'))
            sys.stdout.write(f"{SignVar.warning} {logRoller.Ctrl}".format(f"{Color.red}Ctrl{Color.reset}+{Color.red}C{Color.reset}")+'\n');break
        
        # This initially catches all exceptions (except the KeyboardInterrupt)
        except Exception as e:
            logging.error(logRoller.Error.format(e))
            sys.stderr.write(f"{SignVar.error} {logRoller.Error}".format(f'{Color.red}{e}{Color.reset}')+'\n')  
                    
                      
# Fetching organization info
def orgProfile():
    organization = input(f'{Color.white}--> @{Color.green}Organization{Color.white} (username){Color.reset} ')
    response = requests.get(f'{endpoint}/orgs/{organization}')
    if response.status_code == 404:
        sys.stdout.write(f"{SignVar.negative} {logRoller.orgNotFound.format(organization)}\n")
    elif response.status_code == 200:
        print(f"\n{Color.white}{response.json()['name']}{Color.reset}")
        for attr in org_attrs:
        	print(f'{Color.white}├─ {org_attr_dict[attr]}: {Color.green}{response.json()[attr]}{Color.reset}')
        csvLogger.logOrgProfile(response)
    else:
        pprint(response.json())
        
                        
# Fetching user information        
def userProfile():
    username = input(f'{Color.white}--> @{Color.green}Username{Color.reset} ')
    response = requests.get(f'{endpoint}/users/{username}')
    if response.status_code == 404:
        sys.stdout.write(f"{SignVar.negative} {logRoller.userNotFound.format(username)}\n")
    elif response.status_code == 200:
        print(f"\n{Color.white}{response.json()['name']}{Color.reset}")
        for attr in profile_attrs:
            print(f'{Color.white}├─ {profile_attr_dict[attr]}: {Color.green}{response.json()[attr]}{Color.reset}')
        csvLogger.logUserProfile(response)
    else:
        pprint(response.json())
            
        	        	
# Fetching repository information   	
def repoProfile():
    repo_name = input(f'{Color.white}--> %{Color.green}Repository{Color.reset} ')
    username = input(f'{Color.white}--> @{Color.green}Owner{Color.white} (username){Color.reset} ')
    response = requests.get(f'{endpoint}/repos/{username}/{repo_name}')
    if response.status_code == 404:
        sys.stdout.write(f"{SignVar.negative} {logRoller.repoOrUserNotFound.format(repo_name, username)}\n")
    elif response.status_code == 200:
        print(f"\n{Color.white}{response.json()['full_name']}{Color.reset}")
        for attr in repo_attrs:
            print(f"{Color.white}├─ {repo_attr_dict[attr]}: {Color.green}{response.json()[attr]}{Color.reset}")
        csvLogger.logRepoProfile(response)
    else:
        pprint(response.json())
            
    
# Get path contents        
def pathContents():
    repo_name = input(f'{Color.white}--> %{Color.green}Repository{Color.reset} ')
    username = input(f'{Color.white}--> @{Color.green}Owner{Color.white} (username){Color.reset} ')
    path_name = input(f'{Color.white}--> ~{Color.green}/path/name{Color.reset} ')
    response = requests.get(f'{endpoint}/repos/{username}/{repo_name}/contents/{path_name}')
    if response.status_code == 404:
        sys.stdout.write(f"{SignVar.negative} {logRoller.infoNotFound.format(repo_name, username, path_name)}\n")
    elif response.status_code == 200:
        for content in response.json():
            print(f"\n{Color.white}{content['name']}{Color.reset}")
            for attr in path_attrs:
            	print(f'{Color.white}├─ {path_attr_dict[attr]}: {Color.green}{content[attr]}{Color.reset}')
            csvLogger.logRepoPathContents(content, repo_name)
    else:
        pprint(response.json())
        	    	
        	    	
# repo contributors
def repoContributors():
    repo_name = input(f'{Color.white}--> %{Color.green}Repository{Color.reset} ')
    username = input(f'{Color.white}--> @{Color.green}Owner{Color.white} (username){Color.reset} ')
    limit = input(SignVar.prompt+logRoller.limitInput.format('contributors'))
    response = requests.get(f'{endpoint}/repos/{username}/{repo_name}/contributors?per_page={limit}')
    if response.status_code == 404:
        sys.stdout.write(f"{SignVar.negative} {logRoller.repoOrUserNotFound.format(repo_name, username)}\n")
    elif response.status_code == 200:
        for contributor in response.json():
            print(f"\n{Color.white}{contributor['login']}{Color.reset}")
            for attr in user_attrs:
                print(f'{Color.white}├─ {user_attr_dict[attr]}: {Color.green}{contributor[attr]}{Color.reset}')
            csvLogger.logRepoContributors(contributor, repo_name)
    else:
        pprint(response.json())
                
                
# repo stargazers
def repoStargazers():
    repo_name = input(f'{Color.white}--> %{Color.green}Repository{Color.reset} ')
    username = input(f'{Color.white}--> @{Color.green}Owner{Color.white} (username){Color.reset} ')
    limit = input(SignVar.prompt+logRoller.limitInput.format('repository stargazers'))
    response = requests.get(f'{endpoint}/repos/{username}/{repo_name}/stargazers?per_page={limit}')
    if response.status_code == 404:
        sys.stdout.write(f"{SignVar.negative} {logRoller.repoOrUserNotFound.format(repo_name, username)}\n")
    elif response.json() == {}:
        sys.stdout.write(f'{SignVar.negative} Repository ({repo_name}) does not have any stargazers.{Color.reset}\n')
    elif response.status_code == 200:
        for stargazer in response.json():
            print(f"\n{Color.white}{stargazer['login']}{Color.reset}")
            for attr in  user_attrs:
                print(f'{Color.white}├─ {user_attr_dict[attr]}: {Color.green}{stargazer[attr]}{Color.reset}')
            csvLogger.logRepoStargazers(stargazer, repo_name)
    else:
        pprint(response.json())
                    
                    
# repo forks
def repoForks():
    repo_name = input(f'{Color.white}--> %{Color.green}Repository{Color.reset} ')
    username = input(f'{Color.white}--> @{Color.green}Owner{Color.white} (username){Color.reset} ')
    limit = input(SignVar.prompt+logRoller.limitInput.format('repository forks'))
    response = requests.get(f'{endpoint}/repos/{username}/{repo_name}/forks?per_page={limit}')
    if response.status_code == 404:
        sys.stdout.write(f"{SignVar.negative} {logRoller.repoOrUserNotFound.format(repo_name, username)}\n")
    elif response.json() == {}:
        sys.stdout.write(f'{SignVar.negative} Repository ({repo_name}) does not have forks.{Color.reset}\n')
    elif response.status_code == 200:
        count = 0
        for fork in response.json():
            count += 1
            print(f"\n{Color.white}{fork['full_name']}{Color.reset}")
            for attr in  repo_attrs:
                print(f'{Color.white}├─ {repo_attr_dict[attr]}: {Color.green}{fork[attr]}{Color.reset}')
            csvLogger.logRepoForks(fork, count)
    else:
        pprint(response.json())


# Repo issues
def repoIssues():
    repo_name = input(f'{Color.white}--> %{Color.green}Repository{Color.reset} ')
    username = input(f'{Color.white}--> @{Color.green}Owner{Color.white} (username){Color.reset} ')
    limit = input(SignVar.prompt+logRoller.limitInput.format('repository issues'))
    response = requests.get(f'{endpoint}/repos/{username}/{repo_name}/issues?per_page={limit}')
    if response.status_code == 404:
        sys.stdout.write(f"{SignVar.negative} {logRoller.repoOrUserNotFound.format(repo_name, username)}\n")
    elif response.json() == []:
        sys.stdout.write(f'{SignVar.negative} Repository ({repo_name}) does not have open issues.{Color.reset}\n')
    elif response.status_code == 200:
    	for issue in response.json():
    	    print(f"\n{Color.white}{issue['title']}{Color.reset}")
    	    for attr in  repo_issues_attrs:
    	        print(f'{Color.white}├─ {repo_issues_attr_dict[attr]}: {Color.green}{issue[attr]}{Color.reset}')
    	    print(issue['body'])
    	    csvLogger.logRepoIssues(issue, repo_name)
    else:
        pprint(response.json())


# Repo releases
def repoReleases():
    repo_name = input(f'{Color.white}--> %{Color.green}Repository{Color.reset} ')
    username = input(f'{Color.white}--> @{Color.green}Owner{Color.white} (username){Color.reset} ')
    limit = input(SignVar.prompt+logRoller.limitInput.format('repository releases'))
    response = requests.get(f'{endpoint}/repos/{username}/{repo_name}/releases?per_page={limit}')
    if response.status_code == 404:
    	 sys.stdout.write(f"{SignVar.negative} {logRoller.repoOrUserNotFound.format(repo_name, username)}\n")
    elif response.json() == []:
        sys.stdout.write(f"{SignVar.negative} Repository ({repo_name}) does not have releases.{Color.reset}\n")
    elif response.status_code == 200:
        for release in response.json():
        	print(f"\n{Color.white}{release['name']}{Color.reset}")
        	for attr in repo_releases_attrs:
        	    print(f'{Color.white}├─ {repo_releases_attr_dict[attr]}: {Color.green}{release[attr]}{Color.reset}')
        	print(release['body'])
        	csvLogger.logRepoReleases(release, repo_name)
    else:
        pprint(response.json())
            	
                       
# Fetching organization repositories        
def orgRepos():
    organization = input(f'{Color.white}--> @{Color.green}Organization{Color.white} (username){Color.reset} ')
    limit = input(SignVar.prompt+logRoller.limitInput.format('organization repositories'))
    response = requests.get(f'{endpoint}/orgs/{organization}/repos?per_page={limit}')
    if response.status_code == 404:
        sys.stdout.write(f"{SignVar.negative} {logRoller.orgNotFound.format(organization)}\n")
    elif response.status_code == 200:
        for repository in response.json():
        	print(f"\n{Color.white}{repository['full_name']}{Color.reset}")
        	for attr in repo_attrs:
        		print(f"{Color.white}├─ {repo_attr_dict[attr]}: {Color.green}{repository[attr]}{Color.reset}")
        	csvLogger.logOrgRepos(repository, organization)
    else:
        pprint(response.json())
        
    
# organization events        
def orgEvents():
    organization = input(f"{Color.white}--> @{Color.green}Organization{Color.white} (username){Color.reset} ")
    limit = input(SignVar.prompt+logRoller.limitInput.format('organization events'))
    response = requests.get(f'{endpoint}/orgs/{organization}/events?per_page={limit}')
    if response.status_code == 404:
        sys.stdout.write(f"{SignVar.negative} {logRoller.orgNotFound.format(organization)}\n")
    elif response.status_code == 200:
        for event in response.json():
        	print(f"\n{Color.white}{event['id']}{Color.reset}")
        	print(f"{Color.white}├─ Type: {Color.green}{event['type']}{Color.reset}\n{Color.white}├─ Created at: {Color.green}{event['created_at']}{Color.reset}")
        	pprint(event['payload'])
        csvLogger.logOrgEvents(event, organization)
    else:
        pprint(response.json())
            	
    
# organization member        	
def orgMember():
    organization = input(f"{Color.white}--> @{Color.green}Organization{Color.white} (username){Color.reset} ")
    username = input(f'{Color.white}--> @{Color.green}Username{Color.reset} ')
    response = requests.get(f'{endpoint}/orgs/{organization}/public_members/{username}')
    if response.status_code == 204:
        sys.stdout.write(f"{SignVar.positive} User ({username}) is a public member of the organization ({organization}){Color.reset}\n")
    else:
    	sys.stdout.write(f"{SignVar.negative} {response.json()['message']}{Color.reset}\n")
    	
        	           
# Fetching user repositories        
def userRepos():
    username = input(f'{Color.white}--> @{Color.green}Username{Color.reset} ')
    limit = input(SignVar.prompt+logRoller.limitInput.format('repositories'))
    response = requests.get(f'{endpoint}/users/{username}/repos?per_page={limit}')
    if response.status_code == 404:
    	sys.stdout.write(f"{SignVar.negative} {logRoller.userNotFound.format(username)}\n")
    elif response.status_code == 200:
    	for repository in response.json():
    		print(f"\n{Color.white}{repository['full_name']}{Color.reset}")
    		for attr in repo_attrs:
    			print(f"{Color.white}├─ {repo_attr_dict[attr]}: {Color.green}{repository[attr]}{Color.reset}")
    		csvLogger.logUserRepos(repository, username)
    else:
        pprint(response.json())
        	
        	   	       	    
# Fetching user's gists
def userGists():
    username = input(f'{Color.white}--> @{Color.green}Username{Color.reset} ')
    limit = input(f'{SignVar.prompt+logRoller.limitInput.format("gists")}')
    response = requests.get(f'{endpoint}/users/{username}/gists?per_page={limit}')
    #pprint(response.json())
    if response.json() == []:
    	sys.stdout.write(f'{SignVar.negative} User does not have gists.{Color.reset}\n')
    elif response.status_code == 404:
    	sys.stdout.write(f"{SignVar.negative} {logRoller.userNotFound.format(username)}\n")
    elif response.status_code == 200:
        for gist in response.json():
        	print(f"\n{Color.white}{gist['id']}{Color.reset}")
        	for attr in gists_attrs:
        		print(f"{Color.white}├─ {gists_attr_dict[attr]}: {Color.green}{gist[attr]}{Color.reset}")
        	csvLogger.logUserGists(gist)
    else:
        pprint(response.json())
        		
        	
    
# Fetching a list of organizations that a user owns or belongs to        	
def userOrgs():
    username = input(f'{Color.white}--> @{Color.green}Username{Color.reset} ')
    limit = input(SignVar.prompt+logRoller.limitInput.format('user organizations'))
    response = requests.get(f'{endpoint}/users/{username}/orgs?per_page={limit}')
    if response.json() == []:
        sys.stdout.write(f'{SignVar.negative} User ({username}) does not (belong to/own) any organizations.{Color.reset}\n')
    elif response.status_code == 404:
        sys.stdout.write(f"{SignVar.negative} {logRoller.userNotFound.format(username)}\n")
    elif response.status_code == 200:
    	for organization in response.json():
    	    print(f'\n{Color.white}{organization["login"]}{Color.reset}')
    	    for attr in user_orgs_attrs:
    	        print(f'{Color.white}├─ {user_orgs_attr_dict[attr]}: {Color.green}{organization[attr]}{Color.reset}')
    	    csvLogger.logUserOrgs(organization, username)
    else:
        pprint(response.json())
        	    
        	    
# Fetching a users events 
def userEvents():
    username = input(f'{Color.white}--> @{Color.green}Username{Color.reset} ')
    limit = input(SignVar.prompt+logRoller.limitInput.format('events'))
    response = requests.get(f'{endpoint}/users/{username}/events/public?per_page={limit}')
    if response.status_code == 404:
        sys.stdout.write(f"{SignVar.negative} {logRoller.userNotFound.format(username)}\n")
    elif response.status_code == 200:
        for event in response.json():
        	print(f"\n{Color.white}{event['id']}{Color.reset}")
        	print(f"{Color.white}├─ Actor: {Color.green}{event['actor']['login']}{Color.reset}")
        	print(f"{Color.white}├─ Type: {Color.green}{event['type']}{Color.green}")
        	print(f"{Color.white}├─ Repository: {Color.green}{event['repo']['name']}{Color.reset}")
        	print(f"{Color.white}├─ Created at: {Color.green}{event['created_at']}{Color.reset}")
        	pprint(event['payload'])
        	csvLogger.logUserEvents(event)
    else:
        pprint(response.json())
            	
            	
# Fetching a target user's subscriptions 
def userSubscriptions():
    username = input(f'{Color.white}--> @{Color.green}Username{Color.reset} ')
    limit = input(SignVar.prompt+logRoller.limitInput.format('user subscriptions'))
    response = requests.get(f'{endpoint}/users/{username}/subscriptions?per_page={limit}')
    if response.json() == []:
    	print(f"{SignVar.negative} User does not have any subscriptions.{Color.reset}\n")
    elif response.status_code == 404:
        sys.stdout.write(f"{SignVar.negative} {logRoller.userNotFound.format(username)}\n")
    elif response.status_code == 200:
    	for repository in response.json():
    		print(f"\n{Color.white}{repository['full_name']}{Color.reset}")
    		for attr in repo_attrs:
    			print(f"{Color.white}├─ {repo_attr_dict[attr]}: {Color.green}{repository[attr]}{Color.reset}")
    		csvLogger.logUserSubscriptions(repository, username)
    else:
        pprint(response.json())
        

# Fetching a list of users the target follows        
def userFollowing():
    username = input(f'{Color.white}--> @{Color.green}Username{Color.reset} ')
    limit = input(SignVar.prompt+logRoller.limitInput.format('user\' following'))
    response = requests.get(f'{endpoint}/users/{username}/following?per_page={limit}')
    if response.json() == []:
    	sys.stdout.write(f'{SignVar.negative} User ({username})does not follow anyone.{Color.reset}')
    elif response.status_code == 404:
    	sys.stdout.write(f"{SignVar.negative} {logRoller.userNotFound.format(username)}\n")
    elif response.status_code == 200:
        for user in response.json():
        	print(f"\n{Color.white}@{user['login']}{Color.reset}")
        	for attr in user_attrs:
        		print(f"{Color.white}├─ {user_attr_dict[attr]}: {Color.green}{user[attr]}{Color.reset}")
        	csvLogger.logUserFollowing(user, username)
    else:
        pprint(response.json())
    
    	    	    
# Fetching user's followera'    	    
def userFollowers():
    username = input(f'{Color.white}--> @{Color.green}Username{Color.reset} ')
    limit = input(SignVar.prompt+logRoller.limitInput.format('user followers'))
    response = requests.get(f'{endpoint}/users/{username}/followers?per_page={limit}')
    if response.json() == []:
    	sys.stdout.write(f'{SignVar.negative} User ({username})does not have followers.{Color.reset}')
    elif response.status_code == 404:
    	sys.stdout.write(f"{SignVar.negative} {logRoller.userNotFound.format(username)}\n")
    elif response.status_code == 200:
        for follower in response.json():
        	print(f"\n{Color.white}@{follower['login']}{Color.reset}")
        	for attr in user_attrs:
        		print(f"{Color.white}├─ {user_attr_dict[attr]}: {Color.green}{follower[attr]}{Color.reset}")
        	csvLogger.logUserFollowers(follower, username)
    else:
        pprint(response.json())
            
                    
# Checking whether or not user[A] follows user[B]            
def userFollows():
    user_a = input(f'{Color.white}--> @{Color.green}user{Color.white}(A) (username){Color.reset} ')
    user_b = input(f'{Color.white}--> @{Color.green}user{Color.white}(B) (username){Color.reset} ')
    response = requests.get(f'{endpoint}/users/{user_a}/following/{user_b}')
    if response.status_code == 204:
        sys.stdout.write(f'{SignVar.positive} @{user_a} FOLLOWS @{user_b}{Color.reset}\n')
    else:
    	sys.stdout.write(f'{SignVar.negative} @{user_a} DOES NOT FOLLOW @{user_b}{Color.reset}\n')   
 
 
# User search    	    
def userSearch():
    query = input(f'{Color.white}--> @{Color.green}Query{Color.white} (eg. john){Color.reset} ')
    limit = input(SignVar.prompt+logRoller.limitInput.format('user search'))
    response = requests.get(f'{endpoint}/search/users?q={query}&per_page={limit}').json()
    for user in response['items']:
    	print(f"\n{Color.white}@{user['login']}{Color.reset}")
    	for attr in user_attrs:
    		print(f"{Color.white}├─ {user_attr_dict[attr]}: {Color.green}{user[attr]}{Color.reset}")
    	csvLogger.logUserSearch(user, query)
        		
       		
# Repository search
def repoSearch():
    query = input(f'{Color.white}--> %{Color.green}Query{Color.white} (eg. git){Color.reset} ')
    limit = input(SignVar.prompt+logRoller.limitInput.format('repositor[y][ies] search'))
    response = requests.get(f'{endpoint}/search/repositories?q={query}&per_page={limit}').json()
    for repository in response['items']:
        print(f"\n{Color.white}{repository['full_name']}{Color.reset}")
        for attr in repo_attrs:
            print(f"{Color.white}├─ {repo_attr_dict[attr]}: {Color.green}{repository[attr]}{Color.reset}")
        csvLogger.logRepoSearch(repository, query)
            
            
# Topics search
def topicSearch():
    query = input(f'{Color.white}--> #{Color.green}Query{Color.white} (eg. osint){Color.reset} ')
    limit = input(SignVar.prompt+logRoller.limitInput.format('topic(s) search'))
    response = requests.get(f'{endpoint}/search/topics?q={query}&per_page={limit}').json()
    for topic in response['items']:
        print(f"\n{Color.white}{topic['name']}{Color.reset}")
        for attr in topic_attrs:
            print(f"{Color.white}├─ {topic_attr_dict[attr]}: {Color.green}{topic[attr]}{Color.reset}")
        csvLogger.logTopicSearch(topic, query)
        
            
# Issue search
def issueSearch():
    query = input(f'{Color.white}--> !{Color.green}Query{Color.white} (eg. error){Color.reset} ')
    limit = input(SignVar.prompt+logRoller.limitInput.format('issue(s) search'))
    response = requests.get(f'{endpoint}/search/issues?q={query}&per_page={limit}').json()
    for issue in response['items']:
        print(f"\n\n{Color.white}{issue['title']}{Color.reset}")
        for attr in repo_issues_attrs:
            print(f"{Color.white}├─ {repo_issues_attr_dict[attr]}: {Color.green}{issue[attr]}{Color.reset}")
        print(issue['body'])
        csvLogger.logIssueSearch(issue, query)
            

# Commits search
def commitsSearch():
    query = input(f'{Color.white}--> :{Color.green}Query{Color.white} (eg. filename:index.php){Color.reset} ')
    limit = input(SignVar.prompt+logRoller.limitInput.format('commit(s) search'))
    response = requests.get(f'{endpoint}/search/commits?q={query}&per_page={limit}').json()
    for commit in response['items']:
    	print(f"\n{Color.white}{commit['commit']['tree']['sha']}{Color.reset}")
    	print(f"{Color.white}├─ Author: {commit['commit']['author']['name']}{Color.reset}")
    	print(f"{Color.white}├─ Username: {Color.green}{commit['author']['login']}{Color.reset}")
    	print(f"{Color.white}├─ Email: {Color.green}{commit['commit']['author']['email']}{Color.reset}")
    	print(f"{Color.white}├─ Commiter: {Color.green}{commit['commit']['committer']['name']}{Color.reset}")
    	print(f"{Color.white}├─ Repository: {Color.green}{commit['repository']['full_name']}{Color.reset}")
    	print(f"{Color.white}├─ URL: {Color.green}{commit['html_url']}{Color.reset}")
    	pprint(commit['commit']['message'])
    	csvLogger.logCommitsSearch(commit, query)
    	
    
# View octosuite log files    	
def viewLogs():
    logging.info(logRoller.viewingLogs)
    logs = os.listdir('.logs')
    print(f'''{Color.white}
Log                               Size{Color.reset}
---                               ---------''')
    for log in logs:
        print(f"{log}\t ",os.path.getsize(".logs/"+log),"bytes")
    

# Read a specified log file    
def readLog():
    log_file = input(f"{Color.white}--> .log date (eg. 2022-04-27 10:09:36AM){Color.reset} ")
    with open(f'.logs/{log_file}.log', 'r') as log:
        logging.info(logRoller.readingLog.format(log_file))
        print("\n"+log.read())
        
        
# Delete a specified log file    
def deleteLog():
    log_file = input(f"{Color.white}--> .log date (eg. 2022-04-27 10:09:36AM){Color.reset} ")
    if sys.platform.lower().startswith(('win','darwin')):
        subprocess.run(['del',f'.logs\{log_file}.log'])
    else:
        subprocess.run(['sudo','rm',f'.logs/{log_file}.log'],shell=False)
        
    logging.info(logRoller.deletedLog.format(log_file))
    sys.stdout.write(f"{SignVar.positive} {logRoller.deletedLog.format(log_file)}\n")
        
        
# Downloading release tarball
def downloadTarball():
    logging.info(logRoller.fileDownloading.format(f'octosuite.v{Banner.versionTag}.tar'))
    sys.stdout.write(SignVar.info+' '+logRoller.fileDownloading.format(f'octosuite.v{Banner.versionTag}.tar')+'...\n')
    data = requests.get(f'{endpoint}/repos/rly0nheart/octosuite/tarball/{Banner.versionTag}')
    if data.status_code == 404:
    	logging.info(logRoller.tagNotFound.format(Banner.versionTag))
    	sys.stdout.write(f'{SignVar.negative} {logRoller.tagNotFound.format(Banner.versionTag)}\n')
    else:
        with open(f'downloads/octosuite.v{Banner.versionTag}.tar', 'wb') as file:
            file.write(data.content)
            file.close()
            
        logging.info(logRoller.fileDownloaded.format(f'octosuite.v{Banner.versionTag}.tar'))
        sys.stdout.write(SignVar.positive+' '+logRoller.fileDownloaded.format(f'octosuite.v{Banner.versionTag}.tar'))


# Downloading release zipball
def downloadZipball():
    logging.info(logRoller.fileDownloading.format(f'octosuite.v{Banner.versionTag}.zip'))
    sys.stdout.write(SignVar.info+' '+logRoller.fileDownloading.format(f'octosuite.v{Banner.versionTag}.zip')+'...\n')
    data = requests.get(f'{endpoint}/repos/rly0nheart/octosuite/zipball/{Banner.versionTag}')
    if data.status_code == 404:
    	logging.info(logRoller.tagNotFound.format(Banner.versionTag))
    	sys.sdtout.write(f'{SignVar.negative} {logRoller.tagNotFound.format(Banner.versionTag)}\n')
    else:
        with open(f'downloads/octosuite.v{Banner.versionTag}.zip', 'wb') as file:
            file.write(data.content)
            file.close()
            
        logging.info(logRoller.fileDownloaded.format(f'octosuite.v{Banner.versionTag}.zip'))
        sys.stdout.write(SignVar.positive+' '+logRoller.fileDownloaded.format(f'octosuite.v{Banner.versionTag}.zip'))

    	
def versionCheck():
    response = requests.get(f"{endpoint}/repos/rly0nheart/octosuite/releases/latest")
    if response.json()['tag_name'] == Banner.versionTag:
        sys.stdout.write(f"{SignVar.positive} Octosuite is up to date. Check again soon :)\n")
    else:
    	sys.stdout.write(f"{SignVar.info} A new release is available (octosuite.v{response.json()['tag_name']}). Exit Octosuite and run '{Color.green}pip install --upgrade octosuite{Color.white}' to download and install the update.{Color.reset}\n")
    	
    	
# Author info
def author():
    print(f'{Color.white}Richard Mwewa (Ritchie){Color.reset}')
    for key,value in author_dict.items():
    	print(f'{Color.white}├─ {key}: {Color.green}{value}{Color.reset}')


def about():
    sys.stdout.write('''
     OCTOSUITE © 2022 Richard Mwewa
        
An advanced and lightning fast framework for gathering open-source intelligence on GitHub users and organizations.

Read the wiki: https://github.com/rly0nheart/octosuite/wiki
GitHub REST API documentation: https://docs.github.com/rest
''')
    
    
# Close session 	
def exitSession():
    prompt = input(f'{SignVar.prompt} This will close the current session, continue? (Y/n) ').lower()
    if prompt == 'y':
        logging.info(logRoller.sessionClosed.format('exit'))
        sys.stdout.write(f"{SignVar.info} {logRoller.sessionClosed.format(datetime.now())}\n");exit()
    else:
        pass
    

# Clear screen    
def clearScreen():
    '''
    We use 'cls' on Windows machines to clear the screen,
    otherwise, we use 'clear'
    '''
    if sys.platform.lower().startswith(('win','darwin')):
        subprocess.run(['cls'])
    else:
        subprocess.run(['clear'],shell=False)
        
        
# Show version information
def versionInfo():
	'''
    Yes... the changelog is hard coded
	It's actually frustrating having to change this everytime I publish a new release lol
    '''
	sys.stdout.write(f'''
OCTOSUITE.v{Banner.versionTag}

What's changed?
{'='*15}
[fix] error in source commands (source:tarball, source:zipball) 
''')
