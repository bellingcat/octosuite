from typing import Union, Literal

from octosuite.data import Event, Account, Repository, User, Organisation, Gist


def parse_profile(
    profile: dict, profile_type: Literal["user", "org", "repo"]
) -> Union[User, Organisation, Repository]:
    type_mapping: dict = {
        "user": User(
            name=profile.get("name"),
            username=profile.get("login"),
            bio=profile.get("bio"),
            email=profile.get("email"),
            id=profile.get("id"),
            node_id=profile.get("node_id"),
            avatar_url=profile.get("avatar_url"),
            blog=profile.get("blog"),
            location=profile.get("location"),
            followers=profile.get("followers"),
            following=profile.get("following"),
            twitter_x_username=profile.get("twitter_username"),
            public_gists=profile.get("public_gists"),
            public_repositories=profile.get("public_repos"),
            organisation=profile.get("company"),
            is_open_to_work=profile.get("hireable"),
            is_site_admin=profile.get("site_admin"),
            profile_url=profile.get("html_url"),
            joined_at=profile.get("created_at"),
            update_at=profile.get("updated_at"),
        ),
        "org": Organisation(
            name=profile.get("name"),
            login=profile.get("login"),
            id=profile.get("id"),
            node_id=profile.get("node_id"),
            avatar_url=profile.get("avatar_url"),
            email=profile.get("email"),
            about=profile.get("description"),
            blog=profile.get("blog"),
            location=profile.get("location"),
            followers=profile.get("followers"),
            following=profile.get("following"),
            twitter_x_username=profile.get("twitter_username"),
            public_repositories=profile.get("public_repos"),
            public_gists=profile.get("public_gists"),
            type=profile.get("type"),
            is_verified=profile.get("is_verified"),
            has_organisation_projects=profile.get("has_organization_projects"),
            has_repository_projects=profile.get("has_repository_projects"),
            url=profile.get("html_url"),
            created_at=profile.get("created_at"),
            updated_at=profile.get("updated_at"),
        ),
        "repo": Repository(
            name=profile.get("full_name"),
            id=profile.get("id"),
            node_id=profile.get("node_id"),
            description=profile.get("description"),
            stars=profile.get("stargazers_count"),
            forks=profile.get("forks"),
            watchers=profile.get("watchers"),
            default_branch=profile.get("default_branch"),
            language=profile.get("language"),
            open_issues=profile.get("open_issues"),
            homepage=profile.get("homepage"),
            license=profile.get("license"),
            topics=profile.get("topics"),
            is_fork=profile.get("fork"),
            allow_forking=profile.get("allow_forking"),
            is_archived=profile.get("archived"),
            is_template=profile.get("is_template"),
            has_wiki=profile.get("has_wiki"),
            has_pages=profile.get("has_pages"),
            has_projects=profile.get("has_projects"),
            has_issues=profile.get("has_issues"),
            has_downloads=profile.get("has_downloads"),
            clone_url=profile.get("clone_url"),
            ssh_url=profile.get("ssh_url"),
            pushed_at=profile.get("pushed_at"),
            created_at=profile.get("created_at"),
            updated_at=profile.get("updated_at"),
        ),
    }

    if "node_id" in profile:
        return type_mapping.get(profile_type)


def parse_repos(repos: list[dict]) -> list[Repository]:
    repos_list: list = []
    for repo in repos:
        repos_list.append(
            Repository(
                name=repo.get("full_name"),
                id=repo.get("id"),
                node_id=repo.get("node_id"),
                description=repo.get("description"),
                stars=repo.get("stargazers_count"),
                forks=repo.get("forks"),
                watchers=repo.get("watchers"),
                default_branch=repo.get("default_branch"),
                language=repo.get("language"),
                open_issues=repo.get("open_issues"),
                homepage=repo.get("homepage"),
                license=repo.get("license"),
                topics=repo.get("topics"),
                is_fork=repo.get("fork"),
                allow_forking=repo.get("allow_forking"),
                is_archived=repo.get("archived"),
                is_template=repo.get("is_template"),
                has_wiki=repo.get("has_wiki"),
                has_pages=repo.get("has_pages"),
                has_projects=repo.get("has_projects"),
                has_issues=repo.get("has_issues"),
                has_downloads=repo.get("has_downloads"),
                clone_url=repo.get("clone_url"),
                ssh_url=repo.get("ssh_url"),
                pushed_at=repo.get("pushed_at"),
                created_at=repo.get("created_at"),
                updated_at=repo.get("updated_at"),
            )
        )
    return repos_list


def parse_accounts(accounts: list[dict]) -> list[Account]:
    accounts_list: list = []
    for account in accounts:
        accounts_list.append(
            Account(
                username=account.get("login"),
                id=account.get("id"),
                node_id=account.get("node_id"),
                gravatar_id=account.get("gravatar_id"),
                avatar_url=account.get("avatar_url"),
                is_site_admin=account.get("site_admin"),
                type=account.get("type"),
                profile_url=account.get("html_url"),
            )
        )

    return accounts_list


def parse_events(events: list[dict]) -> list[Event]:
    events_list: list = []
    for event in events:
        events_list.append(
            Event(
                type=event.get("type"),
                repository=event.get("repo").get("name"),
                actor=event.get("actor").get("login"),
                created_at=event.get("created_at"),
            )
        )

    return events_list


def parse_gists(gists: list[dict]) -> list[Gist]:
    gists_list: list = []
    for gist in gists:
        gists_list.append(
            Gist(
                id=gist.get("id"),
                node_id=gist.get("node_id"),
                files=gist.get("files"),
                description=gist.get("description"),
                comments=gist.get("comments"),
                created_at=gist.get("created_at"),
                updated_at=gist.get("updated_at"),
            )
        )

    return gists_list