import hashlib
import json

__all__ = ["cache"]


class ResponseCache:
    """Simple in-memory cache for API responses."""

    def __init__(self):
        self._cache = {}

    @staticmethod
    def _generate_key(url: str, params: dict = None) -> str:
        """Generate a unique cache key from URL and params."""
        cache_data = f"{url}:{json.dumps(params or {}, sort_keys=True)}"
        return hashlib.md5(cache_data.encode()).hexdigest()

    def get(self, url: str, params: dict = None):
        """Get cached response."""
        key = self._generate_key(url, params)
        return self._cache.get(key)

    def set(self, url: str, data, params: dict = None):
        """Cache a response."""
        key = self._generate_key(url, params)
        self._cache[key] = data

    def clear(self):
        """Clear all cached responses."""
        self._cache.clear()

    def remove(self, url: str, params: dict = None):
        """Remove a specific cached response."""
        key = self._generate_key(url, params)
        self._cache.pop(key, None)


cache = ResponseCache()


def clear_cache():
    """Clear all cached API responses."""
    cache.clear()
