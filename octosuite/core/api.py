import re
import typing as t

import requests

BASE_URL = "https://api.github.com"


class Api:
    def __init__(self): ...

    def get(self, url: str, params: t.Optional[dict] = None) -> t.Union[dict, list]:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return self._sanitise_response(response=response.json())

    def _sanitise_response(self, response: t.Union[dict, list]) -> t.Union[dict, list]:
        pattern = re.compile(r"https://api\.github\.com")

        if isinstance(response, list):
            return [self._sanitise_response(response=item) for item in response]

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
                    response[key] = self._sanitise_response(response=value)

        return response
