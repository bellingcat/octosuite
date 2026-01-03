import re
import sys
import typing as t

import requests
from requests import Response

from .cache import cache
from ..lib import __version__

BASE_URL = "https://api.github.com"

__all__ = ["BASE_URL", "GitHub"]


class GitHub:
    def __init__(
        self,
        user_agent: str = (
            f"octosuite/{__version__} "
            f"(Python {sys.version.split()[0]}; "
            f"https://github.com/bellingcat/octosuite) requests/{requests.__version__}"
        ),
    ):
        self.user_agent = user_agent
        self.cache = cache

    def get(
        self,
        url: str,
        params: t.Optional[dict] = None,
        return_response: bool = False,
        use_cache: bool = True,
    ) -> t.Union[dict, list, Response]:
        if use_cache and not return_response:
            cached = self.cache.get(url, params)
            if cached is not None:
                return cached

        response = requests.get(
            url=url, params=params, headers={"User-Agent": self.user_agent}
        )

        if return_response:
            return response

        if response.status_code == 200:
            sanitised = self.sanitise_response(response=response.json())

            # Cache the successful response
            if use_cache:
                self.cache.set(url, sanitised, params)

            return sanitised

        return []

    def is_valid_entity(
        self, _type: t.Literal["user", "org", "repo"], **kwargs
    ) -> bool:
        """Validate if a GitHub entity exists."""
        try:
            type_map = {
                "user": f"https://api.github.com/users/{kwargs.get('username')}",
                "org": f"https://api.github.com/orgs/{kwargs.get('username')}",
                "repo": f"https://api.github.com/repos/{kwargs.get('repo_owner')}/{kwargs.get('repo_name')}",
            }

            url = type_map[_type]

            # Check cache first
            cached = self.cache.get(url)
            if cached is not None:
                return True  # If cached, entity exists

            response = requests.get(url=url, headers={"User-Agent": self.user_agent})

            # Only cache if entity exists (status 200)
            if response.status_code == 200:
                sanitised = self.sanitise_response(response.json())
                self.cache.set(url, sanitised)
                return True

            return False
        except requests.RequestException:
            return False

    def sanitise_response(self, response: t.Union[dict, list]) -> t.Union[dict, list]:
        pattern = re.compile(r"https://api\.github\.com")

        if isinstance(response, list):
            return [self.sanitise_response(response=item) for item in response]

        if isinstance(response, dict):
            keys_to_remove = [
                key
                for key, value in response.items()
                if (isinstance(value, str) and pattern.search(value)) or value is None
            ]
            for key in keys_to_remove:
                response.pop(key)

            # Recursively clean nested dicts/lists
            for key, value in response.items():
                if isinstance(value, (dict, list)):
                    response[key] = self.sanitise_response(response=value)

        return response
