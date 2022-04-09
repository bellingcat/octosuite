![Screenshot_2022-03-17_10-12-53](https://user-images.githubusercontent.com/74001397/158868105-b5aba7e8-7342-4268-bd7a-6d6ae0bdae5a.png)


![OS](https://img.shields.io/badge/OS-GNU%2FLinux-red?style=for-the-badge&logo=Linux)
![OS](https://img.shields.io/badge/OS-Windows-blue?style=for-the-badge&logo=Windows)
![OS](https://img.shields.io/badge/OS-Mac-blue?style=for-the-badge&logo=apple)
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/rly0nheart/octosuite?style=for-the-badge&logo=github)
![GitHub commits since latest release (by date)](https://img.shields.io/github/commits-since/rly0nheart/octosuite/1.5.0?style=for-the-badge)
![GitHub last commit](https://img.shields.io/github/last-commit/rly0nheart/octosuite?style=for-the-badge)
![GitHub](https://img.shields.io/github/license/rly0nheart/octosuite?style=for-the-badge&logo=github)
![GitHub repo size](https://img.shields.io/github/repo-size/rly0nheart/octosuite?style=for-the-badge&logo=github)

> *Simply gather OSINT on Github users and organizations like a god🔥*

# FEATURES
- [x] Fetches organization info
- [x] Fetches user info
- [x] Fetches repository info
- [x] Returns contents of a path from a repository
- [x] Returns a list of repos owned by an organization
- [x] Returns a list of repos owned by a user
- [x] Returns a list of gists owned by a user
- [x] Returns a list of a user's followers
- [x] Checks whether user A follows user B
- [x] Searches users
- [x] Searches repositories
- [x] Searches topics
- [x] Searches issues
- [x] Searches commits
- [x] Easily updates with the 'update' command
- [x] Automatically logs network activity (.logs folder)

# INSTALLATION
**clone project**:

```
git clone https://github.com/rly0nheart/octosuite.git
```

```
cd octosuite
```

```
pip install -r requirements.txt
```

# USAGE
**Linux**:
```
sudo chmod +x octosuite
```

```
sudo ./octosuite
```

**Windows**:
```
python3 octosuite
```

**Mac**:
```
python3 octosuite
```

# AVAILABLE COMMANDS
| Command         | Usage|
| ------------- |:---------:|
| ``orginfo`` | *get organization info*  |
| ``userinfo`` | *get user profile info*  |
| ``repoinfo`` | *get repository info*  |
| ``pathcontents``  | *get contents of a path from a specified repository* |
| ``orgrepos``      | *get a list of repositories owned by a specified organization* |
| ``userrepos``  | *get a list of repositories owned by a specified user* |
| ``usergists``  |  *get a list of gists owned by a specified user* |
| ``userfollowers``  |  *get a list of a user's followers* |
| ``userfollowing`` | *check whether user A follows user B* |
| ``usersearch`` | *search user(s)* |
| ``reposearch`` | *search repositor(y)(ies)* |
| ``topicsearch`` | *search topics(s)* |
| ``issuesearch`` | *search issue(s)* |
| ``commitsearch`` | *search commit(s)* |
| ``update`` | *update octosuite* |
| ``changelog`` | *show changelog* |
| ``author`` | *show author info* |
| ``help`` | *show usage/help* |
| ``exit`` | *exit session* |


# NOTE
* *octosuite automatically logs network and minor user activity. The logs are saved by date and time in .logs folder*
* *Although octosuite was developed to work on **Mac**, **Windows**, or any **Linux** *Distribution*, it has only been tested on **Termux** *and* **Kali Linux***

# LICENSE
![license](https://user-images.githubusercontent.com/74001397/137917929-2f2cdb0c-4d1d-4e4b-9f0d-e01589e027b5.png)

# ABOUT AUTHOR
[About.me](https://about.me/rly0nheart)
