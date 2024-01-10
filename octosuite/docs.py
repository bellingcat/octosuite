# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

import os
from datetime import date

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


AUTHOR: str = "Richard Mwewa"
ABOUT_AUTHOR: str = "https://rly0nheart.github.io"

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


class Version:
    major: str = "4"
    minor: str = "0"
    patch: str = "0"
    full: str = f"{major}.{minor}"


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


DESCRIPTION: str = f"""
# OctoSuite CLI {Version.full}
> An **All-In-One** framework for gathering **OSINT** on GitHub entities."""

# -------------------------------------------------------------------------------------- #

EPILOG: str = f"""
# Copyright © {date.today().year} [{AUTHOR}]({ABOUT_AUTHOR})

```
GNU General Public License v3 (GPLv3)

OctoSuite is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OctoSuite is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with OctoSuite If not, see <https://www.gnu.org/licenses/>. 
```
"""

# -------------------------------------------------------------------------------------- #

USER_EXAMPLES: str = """
# Examples
## Get a User's Profile
```
octosuite user torvalds --profile
```

## Get Emails from a User's PushEvents
```
octosuite user torvalds --emails
```

## Get a User's Public Repositories
```
octosuite user torvalds --repos
```

## Get a User's Public Gists
```
octosuite user torvalds --gists
```

## Get a User's Organisations
```
octosuite user torvalds --orgs
```

## Get a User's Public Events
```
octosuite user torvalds --events
```

## Get a User's Starred Repositories
```
octosuite user torvalds --starred
```

## Check if User follows a Second Specified User
```
octosuite user torvalds --follows --secondary-user SECONDARY_USERNAME
```

## Get a User's Followers
```
octosuite user torvalds --followers
```

## Get Accounts followed by User
```
octosuite user torvalds --following
```

## Check If Target Follows The Specified User
```
octosuite user wang920509 --follows torvalds
```
"""

# -------------------------------------------------------------------------------------- #

ORG_EXAMPLES: str = """
# Examples
## Get an Organisation's Profile
```
octosuite org github --profile
```

## Get an Organisation's Public Repositories
```
octosuite org github --repos
```

## Get an Organisation's Public Events
```
octosuite org github --events
```

## Get an Organisation's Public Members
```
octosuite org github --members
```

## CHeck If User Is a Public Member of the Target Organisation
```
octosuite org DROPCitizenShip --is-member torvalds
```
"""

# -------------------------------------------------------------------------------------- #

REPO_EXAMPLES: str = """
# Examples
## Get a Repository's profile
```
octosuite repo linux torvalds --profile
```

## Get a Repository's Forks
```
octosuite repo linux torvalds --forks
```

## Get a Repository's Stargazers
```
octosuite repo linux torvalds --stargazers
```

## Get a Repository's Contents (from root directory)
```
octosuite repo linux torvalds --contents
```

## Get a Repository's Contents (from a specified directory)
```
octosuite repo linux torvalds --contents kernel
```
"""

# -------------------------------------------------------------------------------------- #

SEARCH_EXAMPLES: str = """
# Examples
## Search Users
```
octosuite search QUERY --users
```

## Search Issues
```
octosuite search QUERY --issues
```

## Search Topics
```
octosuite search QUERY --topics
```

## Search Commits
```
octosuite search QUERY --commits
```
"""

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

# Construct path to the program's directory
PROGRAM_DATA_DIRECTORY: str = os.path.expanduser(os.path.join("~", "octosuite-data"))

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #