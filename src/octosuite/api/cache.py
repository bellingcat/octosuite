import hashlib
import json

__all__ = ["cache"]


class ResponseCache:
    """Simple in-memory cache for API responses."""

    def __init__(self):
        """Initialise the ResponseCache with an empty cache dictionary."""

        self._cache = {}

    @staticmethod
    def _generate_key(url: str, params: dict = None) -> str:
        """
        Generate a unique cache key from URL and parameters.

        :param url: The URL to generate a key for.
        :param params: Optional dictionary of parameters to include in the key.
        :return: MD5 hash string representing the unique cache key.
        """

        cache_data = f"{url}:{json.dumps(params or {}, sort_keys=True)}"
        return hashlib.md5(cache_data.encode()).hexdigest()

    def get(self, url: str, params: dict = None):
        """
        Retrieve a cached response if it exists.

        :param url: The URL to retrieve cached data for.
        :param params: Optional dictionary of parameters used in the original request.
        :return: Cached response data if found, None otherwise.
        """

        key = self._generate_key(url, params)
        return self._cache.get(key)

    def set(self, url: str, data, params: dict = None):
        """
        Store a response in the cache.

        :param url: The URL to cache data for.
        :param data: The response data to cache.
        :param params: Optional dictionary of parameters used in the request.
        """

        key = self._generate_key(url, params)
        self._cache[key] = data

    def clear(self):
        """Clear all cached responses from memory."""
        self._cache.clear()

    def remove(self, url: str, params: dict = None):
        """
        Remove a specific cached response.

        :param url: The URL to remove cached data for.
        :param params: Optional dictionary of parameters used in the original request.
        """

        key = self._generate_key(url, params)
        self._cache.pop(key, None)


cache = ResponseCache()


def clear_cache():
    """Clear all cached API responses from the global cache instance."""

    cache.clear()
