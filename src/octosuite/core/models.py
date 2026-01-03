from requests import exceptions

from .github import GitHub, BASE_URL

github = GitHub()

__all__ = ["User", "Org", "Repo", "Search"]


class GitHubEntity:
    """Base class for GitHub entities with common functionality."""

    def __init__(self, source: str):
        self.endpoint = None
        self.source = source

    def exists(self) -> bool:
        """Check if the entity exists on GitHub."""
        try:
            response = github.get(url=self.endpoint, return_response=True)
            return response.status_code == 200
        except exceptions.RequestException as err:
            return False


class User(GitHubEntity):
    def __init__(self, name: str):
        super().__init__(source=name)
        self.name = name
        self.endpoint = f"{BASE_URL}/users/{name}"

    def profile(self) -> dict:
        profile = github.get(url=self.endpoint)
        return profile

    def repos(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        repos = github.get(url=f"{self.endpoint}/repos", params=params)
        return repos

    def subscriptions(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        subscriptions = github.get(url=f"{self.endpoint}/subscriptions", params=params)
        return subscriptions

    def starred(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        starred = github.get(url=f"{self.endpoint}/starred", params=params)
        return starred

    def followers(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        users = github.get(url=f"{self.endpoint}/followers", params=params)
        return users

    def following(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        users = github.get(url=f"{self.endpoint}/following", params=params)
        return users

    def follows(self, user: str) -> bool: ...

    def orgs(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        orgs = github.get(url=f"{self.endpoint}/orgs", params=params)
        return orgs

    def gists(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        gists = github.get(url=f"{self.endpoint}/gists", params=params)
        return gists

    def events(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        events = github.get(url=f"{self.endpoint}/events", params=params)
        return events

    def received_events(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        received_events = github.get(
            url=f"{self.endpoint}/received_events", params=params
        )
        return received_events


class Org(GitHubEntity):
    def __init__(self, name: str):
        super().__init__(source=name)
        self.name = name
        self.endpoint = f"{BASE_URL}/orgs/{name}"

    def profile(self) -> dict:
        profile = github.get(url=self.endpoint)
        return profile

    def repos(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        repos = github.get(url=f"{self.endpoint}/repos", params=params)
        return repos

    def events(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        events = github.get(url=f"{self.endpoint}/events", params=params)
        return events

    def hooks(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        hooks = github.get(url=f"{self.endpoint}/hooks", params=params)
        return hooks

    def issues(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        issues = github.get(url=f"{self.endpoint}/issues", params=params)
        return issues

    def members(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        members = github.get(url=f"{self.endpoint}/members", params=params)
        return members


class Repo(GitHubEntity):
    def __init__(self, name: str, owner: str):
        super().__init__(source=f"{owner}/{name}")
        self.name = name
        self.owner = owner
        self.endpoint = f"{BASE_URL}/repos/{owner}/{name}"

    def profile(self) -> dict:
        profile = github.get(url=self.endpoint)
        return profile

    def forks(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        forks = github.get(url=f"{self.endpoint}/forks", params=params)
        return forks

    def issue_events(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        issue_events = github.get(url=f"{self.endpoint}/issue_events", params=params)
        return issue_events

    def events(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        events = github.get(url=f"{self.endpoint}/events", params=params)
        return events

    def assignees(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        assignees = github.get(url=f"{self.endpoint}/assignees", params=params)
        return assignees

    def branches(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        branches = github.get(url=f"{self.endpoint}/branches", params=params)
        return branches

    def tags(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        tags = github.get(url=f"{self.endpoint}/tags", params=params)
        return tags

    def languages(self) -> dict:
        languages = github.get(url=f"{self.endpoint}/languages")
        return languages

    def stargazers(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        stargazers = github.get(url=f"{self.endpoint}/stargazers", params=params)
        return stargazers

    def subscribers(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        subscribers = github.get(url=f"{self.endpoint}/subscribers", params=params)
        return subscribers

    def commits(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        commits = github.get(url=f"{self.endpoint}/commits", params=params)
        return commits

    def comments(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        comments = github.get(url=f"{self.endpoint}/comments", params=params)
        return comments

    def contents(self, path: str) -> list:
        contents = github.get(url=f"{self.endpoint}/contents/{path}")
        return contents

    def issues(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        issues = github.get(url=f"{self.endpoint}/issues", params=params)
        return issues

    def releases(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        releases = github.get(url=f"{self.endpoint}/releases", params=params)
        return releases

    def deployments(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        deployments = github.get(url=f"{self.endpoint}/deployments", params=params)
        return deployments

    def labels(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        labels = github.get(url=f"{self.endpoint}/labels", params=params)
        return labels


class Search:
    def __init__(self, query: str, page: int, per_page: int):
        self.query = query
        self.page = page
        self.per_page = per_page
        self.endpoint = f"{BASE_URL}/search"
        self.params = {"q": query, "page": page, "per_page": per_page}

    def repos(self) -> list:
        repos = github.get(url=f"{self.endpoint}/repositories", params=self.params)
        return repos

    def users(self) -> list:
        users = github.get(url=f"{self.endpoint}/users", params=self.params)
        return users

    def commits(self) -> list:
        commits = github.get(url=f"{self.endpoint}/commits", params=self.params)
        return commits

    def issues(self) -> list:
        issues = github.get(url=f"{self.endpoint}/issues", params=self.params)
        return issues

    def topics(self) -> list:
        topics = github.get(url=f"{self.endpoint}/topics", params=self.params)
        return topics
