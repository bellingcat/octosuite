import json
import re
import ssl
import sys
import typing as t
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import certifi

from .cache import cache
from ..meta import __version__

BASE_URL = "https://api.github.com"
SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())

__all__ = ["BASE_URL", "GitHub"]


class GitHub:
    """Handles GitHub API requests with caching and response sanitisation."""

    def __init__(
        self,
        user_agent: str = (
            f"octosuite/{__version__} "
            f"(Python {sys.version.split()[0]}; "
            f"https://github.com/bellingcat/octosuite)"
        ),
    ):
        """
        Initialise the GitHub API client.

        :param user_agent: Custom User-Agent string for API requests.
        """

        self.user_agent = user_agent
        self.cache = cache

    def request(
        self, url: str, params: t.Optional[dict] = None
    ) -> tuple[int, t.Union[dict, list]]:
        """
        Send a GET request to the GitHub API.

        :param url: The API endpoint URL.
        :param params: Optional query parameters for the request.
        :return: Tuple of (status_code, parsed JSON body). The body is an empty dict if an error response is not JSON.
        """

        if params:
            url = f"{url}?{urlencode(params)}"

        request = Request(url=url, headers={"User-Agent": self.user_agent})
        try:
            with urlopen(request, context=SSL_CONTEXT) as response:
                return response.status, json.load(response)
        except HTTPError as error:
            with error:
                try:
                    return error.code, json.load(error)
                except ValueError:
                    return error.code, {}

    def get(
        self,
        url: str,
        params: t.Optional[dict] = None,
        use_cache: bool = True,
    ) -> t.Union[dict, list]:
        """
        Make a GET request to the GitHub API.

        :param url: The API endpoint URL.
        :param params: Optional query parameters for the request.
        :param use_cache: If True, use cached responses when available.
        :return: Dictionary or list of response data, or an empty list if the request fails.
        """

        if use_cache:
            cached = self.cache.get(url, params)
            if cached is not None:
                return cached

        status_code, data = self.request(url=url, params=params)

        if status_code == 200:
            sanitised = self.sanitise_response(response=data)

            # Cache the successful response
            if use_cache:
                self.cache.set(url, sanitised, params)

            return sanitised

        return []

    def is_valid_entity(
        self, _type: t.Literal["user", "org", "repo"], **kwargs
    ) -> bool:
        """
        Validate whether a GitHub entity exists.

        :param _type: Type of entity to validate ("user", "org", or "repo").
        :param kwargs: Entity identifiers (username for user/org, repo_owner and repo_name for repo).
        :return: True if the entity exists, False otherwise.
        """

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

            status_code, data = self.request(url=url)

            # Only cache if entity exists (status 200)
            if status_code == 200:
                sanitised = self.sanitise_response(data)
                self.cache.set(url, sanitised)
                return True

            return False
        except (OSError, ValueError):
            return False

    def sanitise_response(self, response: t.Union[dict, list]) -> t.Union[dict, list]:
        """
        Remove API URLs and null values from response data recursively.

        :param response: The response data to sanitise (dict or list).
        :return: Sanitised response with API URLs and null values removed.
        """

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
