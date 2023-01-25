![logo](https://user-images.githubusercontent.com/74001397/175805580-fffc96d4-e0ef-48bb-a55c-80b2da3e714d.png)

A framework for gathering open-source intelligence on GitHub users, repositories and organizations

[![Upload Python Package](https://github.com/bellingcat/octosuite/actions/workflows/python-publish.yml/badge.svg)](https://github.com/bellingcat/octosuite/actions/workflows/python-publish.yml)
[![CodeQL](https://github.com/bellingcat/octosuite/actions/workflows/codeql.yml/badge.svg)](https://github.com/bellingcat/octosuite/actions/workflows/codeql.yml)
![GitHub](https://img.shields.io/github/license/bellingcat/octosuite?style=flat)
![PyPI](https://img.shields.io/pypi/v/octosuite?style=flat&logo=pypi)
![PyPI - Downloads](https://img.shields.io/pypi/dw/octosuite?style=flat&logo=pypi)
![PyPI - Status](https://img.shields.io/pypi/status/octosuite?style=flat&logo=pypi)
![GitHub repo size](https://img.shields.io/github/repo-size/bellingcat/octosuite?style=flat&logo=github)

> About
![2023-01-23_01-01](https://user-images.githubusercontent.com/74001397/213950701-44b3f98b-89e1-443a-abb5-1be8969b611f.png "Octosuite about")

> User profile
![2023-01-23_01-02](https://user-images.githubusercontent.com/74001397/213950792-0fcf3aef-4921-4701-84ee-0c7a6043c61b.png "User profile window")

> Organisation profile
![2023-01-23_01-03](https://user-images.githubusercontent.com/74001397/213950889-d034b432-2ef1-4118-8eff-946f8fb566f4.png)


# Wiki
[Refer to the Wiki](https://github.com/bellingcat/octosuite/wiki) for installation instructions, in addition to all other documentation.

# Features
- [x] Fetches an organization's profile information
- [x] Fetches an oganization's events
- [x] Returns an organization's repositories
- [x] Returns an organization's public members
- [x] Fetches a repository's information
- [x] Returns a repository's contributors
- [x] Returns a repository's languages
- [x] Fetches a repository's stargazers
- [x] Fetches a repository's forks
- [x] Fetches a repository's releases
- [x] Returns a list of files in a specified path of a repository
- [x] Fetches a user's profile information
- [x] Returns a user's gists
- [x] Returns organizations that a user owns/belongs to
- [x] Fetches a user's events
- [x] Fetches a list of users followed by the target
- [x] Fetches a user's followers
- [x] Checks if user A follows user B
- [x] Checks if  user is a public member of an organizations
- [x] Returns a user's subscriptions
- [x] Gets a user's subscriptions
- [x] Gets a user's events
- [x] Searches users
- [x] Searches repositories
- [x] Searches topics
- [x] Searches issues
- [x] Searches commits
- [x] Automatically logs network activity (.logs folder)
- [x] User can view, read and delete logs
- [x] All the above can be used with command-line arguments (PyPI Package only)
- [x] ...And more

**Used the following implementation from [Somdev Sangwan](https://github.com/s0md3v)'s [Zen](https://github.com/s0md3v/zen) to get an email from a username**
```python
def findReposFromUsername(username):
	response = get('https://api.github.com/users/%s/repos?per_page=100&sort=pushed' % username, auth=HTTPBasicAuth(uname, '')).text
	repos = re.findall(r'"full_name":"%s/(.*?)",.*?"fork":(.*?),' % username, response)
	nonForkedRepos = []
	for repo in repos:
		if repo[1] == 'false':
			nonForkedRepos.append(repo[0])
	return nonForkedRepos

def findEmailFromContributor(username, repo, contributor):
	response = get('https://github.com/%s/%s/commits?author=%s' % (username, repo, contributor), auth=HTTPBasicAuth(uname, '')).text
	latestCommit = re.search(r'href="/%s/%s/commit/(.*?)"' % (username, repo), response)
	if latestCommit:
		latestCommit = latestCommit.group(1)
	else:
		latestCommit = 'dummy'
	commitDetails = get('https://github.com/%s/%s/commit/%s.patch' % (username, repo, latestCommit), auth=HTTPBasicAuth(uname, '')).text
	email = re.search(r'<(.*)>', commitDetails)
	if email:
		email = email.group(1)
		if breach:
			jsonOutput[contributor] = {}
			jsonOutput[contributor]['email'] = email
		else:
			jsonOutput[contributor] = email
	return email

def findEmailFromUsername(username):
	repos = findReposFromUsername(username)
	for repo in repos:
		email = findEmailFromContributor(username, repo, username)
		if email:
			print (username + ' : ' + email)
			break
```
## Note
> Octosuite automatically logs network and user activity of each session, the logs are saved by date and time in the .logs folder


# License
![license](https://user-images.githubusercontent.com/74001397/137917929-2f2cdb0c-4d1d-4e4b-9f0d-e01589e027b5.png)

# Donations
If you like OctoSuite and would like to show support, you can Buy A Coffee for the developer using the button below

<a href="https://www.buymeacoffee.com/189381184" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

Your support will be much appreciated😊
