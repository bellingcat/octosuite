from requests import exceptions

from .github import GitHub, BASE_URL

github = GitHub()

__all__ = ["User", "Org", "Repo", "Search"]


class GitHubEntity:
    """
    Base class for GitHub entities with common functionality."""

    def __init__(self, source: str):
        """
        Initialise a GitHub entity.

        :param source: The source identifier for the entity.
        """

        self.endpoint = None
        self.source = source

    def exists(self) -> tuple[bool, dict]:
        """
        Check if the entity exists on GitHub.

        :return: Tuple of (exists, response_data) where exists is True if the entity is found.
        """
        # Check cache first
        cached = github.cache.get(self.endpoint)
        if cached is not None:
            return True, cached

        try:
            response = github.get(url=self.endpoint, return_response=True)

            if response.status_code == 200:
                data = response.json()
                # Sanitise the data
                sanitised = github.sanitise_response(data)
                # Cache the sanitised response
                github.cache.set(self.endpoint, sanitised)
                return True, sanitised

            return False, response.json()
        except exceptions.RequestException:
            return False, {}


class User(GitHubEntity):
    """Represents a GitHub user with methods to query user data."""

    def __init__(self, name: str):
        """
        Initialise a User instance.

        :param name: The GitHub username.
        """

        super().__init__(source=name)
        self.name = name
        self.endpoint = f"{BASE_URL}/users/{name}"

    def profile(self) -> dict:
        """
        Retrieve the user's profile information.

        :return: Dictionary containing user profile data.
        """

        profile = github.get(url=self.endpoint)
        return profile

    def repos(self, page: int, per_page: int) -> list:
        """
        Retrieve the user's public repositories.

        :param page: Page number for pagination.
        :param per_page: Number of results per page.
        :return: List of repository dictionaries.
        """

        params = {"page": page, "per_page": per_page}
        repos = github.get(url=f"{self.endpoint}/repos", params=params)
        return repos

    def subscriptions(self, page: int, per_page: int) -> list:
        """
        Retrieve repositories the user is subscribed to.

        :param page: Page number for pagination.
        :param per_page: Number of results per page.
        :return: List of repository subscription dictionaries.
        """

        params = {"page": page, "per_page": per_page}
        subscriptions = github.get(url=f"{self.endpoint}/subscriptions", params=params)
        return subscriptions

    def starred(self, page: int, per_page: int) -> list:
        """
        Retrieve repositories the user has starred.

        :param page: Page number for pagination.
        :param per_page: Number of results per page.
        :return: List of starred repository dictionaries.
        """

        params = {"page": page, "per_page": per_page}
        starred = github.get(url=f"{self.endpoint}/starred", params=params)
        return starred

    def followers(self, page: int, per_page: int) -> list:
        """
        Retrieve the user's followers.

        :param page: Page number for pagination.
        :param per_page: Number of results per page.
        :return: List of follower user dictionaries.
        """

        params = {"page": page, "per_page": per_page}
        users = github.get(url=f"{self.endpoint}/followers", params=params)
        return users

    def following(self, page: int, per_page: int) -> list:
        """
        Retrieve users that this user is following.

        :param page: Page number for pagination.
        :param per_page: Number of results per page.
        :return: List of followed user dictionaries.
        """

        params = {"page": page, "per_page": per_page}
        users = github.get(url=f"{self.endpoint}/following", params=params)
        return users

    def follows(self, user: str) -> bool:
        """Check if this user follows another user.

        :param user: The username to check.
        :return: True if this user follows the specified user.
        """
        ...

    def orgs(self, page: int, per_page: int) -> list:
        """
        Retrieve organisations the user belongs to.

        :param page: Page number for pagination.
        :param per_page: Number of results per page.
        :return: List of organisation dictionaries.
        """

        params = {"page": page, "per_page": per_page}
        orgs = github.get(url=f"{self.endpoint}/orgs", params=params)
        return orgs

    def gists(self, page: int, per_page: int) -> list:
        """
        Retrieve the user's gists.

        :param page: Page number for pagination.
        :param per_page: Number of results per page.
        :return: List of gist dictionaries.
        """

        params = {"page": page, "per_page": per_page}
        gists = github.get(url=f"{self.endpoint}/gists", params=params)
        return gists

    def events(self, page: int, per_page: int) -> list:
        """
        Retrieve the user's public events.

        :param page: Page number for pagination.
        :param per_page: Number of results per page.
        :return: List of event dictionaries.
        """

        params = {"page": page, "per_page": per_page}
        events = github.get(url=f"{self.endpoint}/events", params=params)
        return events

    def received_events(self, page: int, per_page: int) -> list:
        """
        Retrieve events received by the user.

        :param page: Page number for pagination.
        :param per_page: Number of results per page.
        :return: List of received event dictionaries.
        """

        params = {"page": page, "per_page": per_page}
        received_events = github.get(
            url=f"{self.endpoint}/received_events", params=params
        )
        return received_events


class Org(GitHubEntity):
    """Represents a GitHub organisation with methods to query organisation data."""

    def __init__(self, name: str):
        """
        Initialise an Org instance.

        :param name: The GitHub organisation name.
        """

        super().__init__(source=name)
        self.name = name
        self.endpoint = f"{BASE_URL}/orgs/{name}"

    def profile(self) -> dict:
        """
        Retrieve the organisation's profile information.

        :return: Dictionary containing organisation profile data.
        """

        profile = github.get(url=self.endpoint)
        return profile

    def repos(self, page: int, per_page: int) -> list:
        """
        Retrieve the organisation's public repositories.

        :param page: Page number for pagination.
        :param per_page: Number of results per page.
        :return: List of repository dictionaries.
        """

        params = {"page": page, "per_page": per_page}
        repos = github.get(url=f"{self.endpoint}/repos", params=params)
        return repos

    def events(self, page: int, per_page: int) -> list:
        """
        Retrieve the organisation's public events.

        :param page: Page number for pagination.
        :param per_page: Number of results per page.
        :return: List of event dictionaries.
        """

        params = {"page": page, "per_page": per_page}
        events = github.get(url=f"{self.endpoint}/events", params=params)
        return events

    def hooks(self, page: int, per_page: int) -> list:
        """
        Retrieve the organisation's webhooks.

        :param page: Page number for pagination.
        :param per_page: Number of results per page.
        :return: List of webhook dictionaries.
        """

        params = {"page": page, "per_page": per_page}
        hooks = github.get(url=f"{self.endpoint}/hooks", params=params)
        return hooks

    def issues(self, page: int, per_page: int) -> list:
        """
        Retrieve the organisation's issues.

        :param page: Page number for pagination.
        :param per_page: Number of results per page.
        :return: List of issue dictionaries.
        """

        params = {"page": page, "per_page": per_page}
        issues = github.get(url=f"{self.endpoint}/issues", params=params)
        return issues

    def members(self, page: int, per_page: int) -> list:
        """
        Retrieve the organisation's public members.

        :param page: Page number for pagination.
        :param per_page: Number of results per page.
        :return: List of member user dictionaries.
        """

        params = {"page": page, "per_page": per_page}
        members = github.get(url=f"{self.endpoint}/members", params=params)
        return members


class Repo(GitHubEntity):
    """Represents a GitHub repository with methods to query repository data."""

    def __init__(self, name: str, owner: str):
        """
        Initialise a Repo instance.

        :param name: The repository name.
        :param owner: The repository owner's username.
        """

        super().__init__(source=f"{owner}/{name}")
        self.name = name
        self.owner = owner
        self.endpoint = f"{BASE_URL}/repos/{owner}/{name}"

    def profile(self) -> dict:
        """
        Retrieve the repository's information.

        :return: Dictionary containing repository data.
        """

        profile = github.get(url=self.endpoint)
        return profile

    def forks(self, page: int, per_page: int) -> list:
        """
        Retrieve the repository's forks.

        :param page: Page number for pagination.
        :param per_page: Number of results per page.
        :return: List of fork repository dictionaries.
        """

        params = {"page": page, "per_page": per_page}
        forks = github.get(url=f"{self.endpoint}/forks", params=params)
        return forks

    def issue_events(self, page: int, per_page: int) -> list:
        """
        Retrieve the repository's issue events.

        :param page: Page number for pagination.
        :param per_page: Number of results per page.
        :return: List of issue event dictionaries.
        """

        params = {"page": page, "per_page": per_page}
        issue_events = github.get(url=f"{self.endpoint}/issue_events", params=params)
        return issue_events

    def events(self, page: int, per_page: int) -> list:
        """
        Retrieve the repository's events.

        :param page: Page number for pagination.
        :param per_page: Number of results per page.
        :return: List of event dictionaries.
        """

        params = {"page": page, "per_page": per_page}
        events = github.get(url=f"{self.endpoint}/events", params=params)
        return events

    def assignees(self, page: int, per_page: int) -> list:
        """
        Retrieve the repository's available assignees.

        :param page: Page number for pagination.
        :param per_page: Number of results per page.
        :return: List of assignee user dictionaries.
        """

        params = {"page": page, "per_page": per_page}
        assignees = github.get(url=f"{self.endpoint}/assignees", params=params)
        return assignees

    def branches(self, page: int, per_page: int) -> list:
        """
        Retrieve the repository's branches.

        :param page: Page number for pagination.
        :param per_page: Number of results per page.
        :return: List of branch dictionaries.
        """

        params = {"page": page, "per_page": per_page}
        branches = github.get(url=f"{self.endpoint}/branches", params=params)
        return branches

    def tags(self, page: int, per_page: int) -> list:
        """
        Retrieve the repository's tags.

        :param page: Page number for pagination.
        :param per_page: Number of results per page.
        :return: List of tag dictionaries.
        """

        params = {"page": page, "per_page": per_page}
        tags = github.get(url=f"{self.endpoint}/tags", params=params)
        return tags

    def languages(self) -> dict:
        """
        Retrieve the programming languages used in the repository.

        :return: Dictionary mapping language names to bytes of code.
        """

        languages = github.get(url=f"{self.endpoint}/languages")
        return languages

    def stargazers(self, page: int, per_page: int) -> list:
        """
        Retrieve users who have starred the repository.

        :param page: Page number for pagination.
        :param per_page: Number of results per page.
        :return: List of stargazer user dictionaries.
        """

        params = {"page": page, "per_page": per_page}
        stargazers = github.get(url=f"{self.endpoint}/stargazers", params=params)
        return stargazers

    def subscribers(self, page: int, per_page: int) -> list:
        """
        Retrieve users subscribed to the repository.

        :param page: Page number for pagination.
        :param per_page: Number of results per page.
        :return: List of subscriber user dictionaries.
        """

        params = {"page": page, "per_page": per_page}
        subscribers = github.get(url=f"{self.endpoint}/subscribers", params=params)
        return subscribers

    def commits(self, page: int, per_page: int) -> list:
        """
        Retrieve the repository's commits.

        :param page: Page number for pagination.
        :param per_page: Number of results per page.
        :return: List of commit dictionaries.
        """

        params = {"page": page, "per_page": per_page}
        commits = github.get(url=f"{self.endpoint}/commits", params=params)
        return commits

    def comments(self, page: int, per_page: int) -> list:
        """
        Retrieve the repository's commit comments.

        :param page: Page number for pagination.
        :param per_page: Number of results per page.
        :return: List of comment dictionaries.
        """

        params = {"page": page, "per_page": per_page}
        comments = github.get(url=f"{self.endpoint}/comments", params=params)
        return comments

    def contents(self, path: str) -> list:
        """
        Retrieve the contents of a file or directory in the repository.

        :param path: Path to the file or directory.
        :return: List of content item dictionaries.
        """

        contents = github.get(url=f"{self.endpoint}/contents/{path}")
        return contents

    def issues(self, page: int, per_page: int) -> list:
        """
        Retrieve the repository's issues.

        :param page: Page number for pagination.
        :param per_page: Number of results per page.
        :return: List of issue dictionaries.
        """

        params = {"page": page, "per_page": per_page}
        issues = github.get(url=f"{self.endpoint}/issues", params=params)
        return issues

    def releases(self, page: int, per_page: int) -> list:
        """
        Retrieve the repository's releases.

        :param page: Page number for pagination.
        :param per_page: Number of results per page.
        :return: List of release dictionaries.
        """

        params = {"page": page, "per_page": per_page}
        releases = github.get(url=f"{self.endpoint}/releases", params=params)
        return releases

    def deployments(self, page: int, per_page: int) -> list:
        """
        Retrieve the repository's deployments.

        :param page: Page number for pagination.
        :param per_page: Number of results per page.
        :return: List of deployment dictionaries.
        """

        params = {"page": page, "per_page": per_page}
        deployments = github.get(url=f"{self.endpoint}/deployments", params=params)
        return deployments

    def labels(self, page: int, per_page: int) -> list:
        """
        Retrieve the repository's labels.

        :param page: Page number for pagination.
        :param per_page: Number of results per page.
        :return: List of label dictionaries.
        """

        params = {"page": page, "per_page": per_page}
        labels = github.get(url=f"{self.endpoint}/labels", params=params)
        return labels


class Search:
    """Provides methods to search GitHub for various entity types."""

    def __init__(self, query: str, page: int, per_page: int):
        """
        Initialise a Search instance.

        :param query: The search query string.
        :param page: Page number for pagination.
        :param per_page: Number of results per page.
        """

        self.query = query
        self.page = page
        self.per_page = per_page
        self.endpoint = f"{BASE_URL}/search"
        self.params = {"q": query, "page": page, "per_page": per_page}

    def repos(self) -> list:
        """
        Search for repositories matching the query.

        :return: List of repository search result dictionaries.
        """

        repos = github.get(url=f"{self.endpoint}/repositories", params=self.params)
        return repos

    def users(self) -> list:
        """
        Search for users matching the query.

        :return: List of user search result dictionaries.
        """

        users = github.get(url=f"{self.endpoint}/users", params=self.params)
        return users

    def commits(self) -> list:
        """
        Search for commits matching the query.

        :return: List of commit search result dictionaries.
        """

        commits = github.get(url=f"{self.endpoint}/commits", params=self.params)
        return commits

    def issues(self) -> list:
        """
        Search for issues and pull requests matching the query.

        :return: List of issue search result dictionaries.
        """

        issues = github.get(url=f"{self.endpoint}/issues", params=self.params)
        return issues

    def topics(self) -> list:
        """
        Search for topics matching the query.

        :return: List of topic search result dictionaries.
        """

        topics = github.get(url=f"{self.endpoint}/topics", params=self.params)
        return topics
