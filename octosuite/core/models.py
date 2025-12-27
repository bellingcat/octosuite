from .api import Api, BASE_URL


api = Api()


class User:
    def __init__(self, name: str):

        self.name = name
        self.endpoint = f"{BASE_URL}/users/{name}"

    def profile(self) -> dict:
        profile = api.get(url=self.endpoint)
        return profile

    def repos(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        repos = api.get(url=f"{self.endpoint}/repos", params=params)
        return repos

    def subscriptions(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        subscriptions = api.get(url=f"{self.endpoint}/subscriptions", params=params)
        return subscriptions

    def starred(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        starred = api.get(url=f"{self.endpoint}/starred", params=params)
        return starred

    def followers(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        users = api.get(url=f"{self.endpoint}/followers", params=params)
        return users

    def following(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        users = api.get(url=f"{self.endpoint}/following", params=params)
        return users

    def follows(self, user: str) -> bool: ...

    def orgs(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        orgs = api.get(url=f"{self.endpoint}/orgs", params=params)
        return orgs

    def gists(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        gists = api.get(url=f"{self.endpoint}/gists", params=params)
        return gists

    def events(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        events = api.get(url=f"{self.endpoint}/events", params=params)
        return events

    def received_events(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        received_events = api.get(url=f"{self.endpoint}/received_events", params=params)
        return received_events


class Org:
    def __init__(self, name: str):

        self.name = name
        self.endpoint = f"{BASE_URL}/orgs/{name}"

    def profile(self) -> dict:
        profile = api.get(url=self.endpoint)
        return profile

    def repos(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        repos = api.get(url=f"{self.endpoint}/repos", params=params)
        return repos

    def events(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        events = api.get(url=f"{self.endpoint}/events", params=params)
        return events

    def hooks(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        hooks = api.get(url=f"{self.endpoint}/hooks", params=params)
        return hooks

    def issues(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        issues = api.get(url=f"{self.endpoint}/issues", params=params)
        return issues

    def members(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        members = api.get(url=f"{self.endpoint}/members", params=params)
        return members


class Repo:
    def __init__(self, name: str, owner: str):
        self.name = name
        self.owner = owner
        self.endpoint = f"{BASE_URL}/repos/{owner}/{name}"

    def profile(self) -> dict:
        profile = api.get(url=self.endpoint)
        return profile

    def forks(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        forks = api.get(url=f"{self.endpoint}/forks", params=params)
        return forks

    def issue_events(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        issue_events = api.get(url=f"{self.endpoint}/issue_events", params=params)
        return issue_events

    def events(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        events = api.get(url=f"{self.endpoint}/events", params=params)
        return events

    def assignees(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        assignees = api.get(url=f"{self.endpoint}/assignees", params=params)
        return assignees

    def branches(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        branches = api.get(url=f"{self.endpoint}/branches", params=params)
        return branches

    def tags(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        tags = api.get(url=f"{self.endpoint}/tags", params=params)
        return tags

    def languages(self) -> dict:
        languages = api.get(url=f"{self.endpoint}/languages")
        return languages

    def stargazers(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        stargazers = api.get(url=f"{self.endpoint}/stargazers", params=params)
        return stargazers

    def subscribers(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        subscribers = api.get(url=f"{self.endpoint}/subscribers", params=params)
        return subscribers

    def commits(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        commits = api.get(url=f"{self.endpoint}/commits", params=params)
        return commits

    def comments(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        comments = api.get(url=f"{self.endpoint}/comments", params=params)
        return comments

    def contents(self, path: str) -> list:
        contents = api.get(url=f"{self.endpoint}/contents/{path}")
        return contents

    def issues(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        issues = api.get(url=f"{self.endpoint}/issues", params=params)
        return issues

    def releases(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        releases = api.get(url=f"{self.endpoint}/releases", params=params)
        return releases

    def deployments(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        deployments = api.get(url=f"{self.endpoint}/deployments", params=params)
        return deployments

    def labels(self, page: int, per_page: int) -> list:
        params = {"page": page, "per_page": per_page}
        labels = api.get(url=f"{self.endpoint}/labels", params=params)
        return labels
