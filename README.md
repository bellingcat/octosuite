![octosuite](https://raw.githubusercontent.com/bellingcat/octosuite/refs/heads/master/img/octosuite.png)

Terminal-based toolkit for GitHub data analysis.

![PyPI - Version](https://img.shields.io/pypi/v/octosuite)
![PyPI - Downloads](https://img.shields.io/pepy/dt/octosuite)
![Code Size](https://img.shields.io/github/languages/code-size/bellingcat/octosuite)
![Release Date](https://img.shields.io/github/release-date/bellingcat/octosuite)
![Build Status](https://img.shields.io/github/actions/workflow/status/bellingcat/octosuite/python-publish.yml)
![License](https://img.shields.io/github/license/bellingcat/octosuite)

```shell
$ octosuite user torvalds
```

```python
from pprint import pprint
import octosuite

exists, profile = octosuite.User(name="torvalds")

if exists:
    pprint(profile)
```

## Installation

```bash
pip install octosuite
```

## Usage

### TUI (Interactive)

Launch the interactive terminal interface:

```bash
octosuite -t/--tui
```

Navigate using arrow keys and Enter to select options.

### CLI

Query GitHub data directly from the command line:

```bash
# User data
octosuite user torvalds
octosuite user torvalds --repos --page 1 --per-page 50
octosuite user torvalds --followers --json

# Repository data
octosuite repo torvalds/linux
octosuite repo torvalds/linux --commits
octosuite repo torvalds/linux --stargazers --export ./data

# Organisation data
octosuite org github
octosuite org github --members --json

# Search
octosuite search "machine learning" --repos
octosuite search "python cli" --users --json
```

**Common options:**

- `--page` - Page number (default: 1)
- `--per-page` - Results per page, max 100 (default: 100)
- `--json` - Output as JSON
- `--export DIR` - Export to directory

Run `octosuite <command> --help` for available data type flags.

### Library

Use octosuite in your Python projects:

```python
from octosuite import User, Repo, Org, Search

# Get user data
user = User("torvalds")
exists, profile = user.exists()
if exists:
    repos = user.repos(page=1, per_page=100)
    followers = user.followers(page=1, per_page=50)

# Get repository data
repo = Repo(name="linux", owner="torvalds")
exists, profile = repo.exists()
if exists:
    commits = repo.commits(page=1, per_page=100)
    languages = repo.languages()

# Get organisation data
org = Org("github")
exists, profile = org.exists()
if exists:
    members = org.members(page=1, per_page=100)

# Search GitHub
search = Search(query="machine learning", page=1, per_page=50)
results = search.repos()
```

## Features

<details>
<summary><strong>Data Types</strong></summary>

**User:** profile, repos, subscriptions, starred, followers, following, orgs, gists, events, received_events

**Repository:** profile, forks, issue_events, events, assignees, branches, tags, languages, stargazers, subscribers,
commits, comments, issues, releases, deployments, labels

**Organisation:** profile, repos, events, hooks, issues, members

**Search:** repos, users, commits, issues, topics

</details>

<details>
<summary><strong>Export Formats</strong></summary>

- JSON
- CSV
- HTML

</details>

## Licence

MIT Licence. See the [LICENCE](https://raw.githubusercontent.com/bellingcat/octosuite/refs/heads/master/LICENSE) file
for details.
