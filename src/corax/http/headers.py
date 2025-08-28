from collections.abc import MutableMapping
from typing import Iterator

class Headers(MutableMapping):
    """
        A case-insensitive, multi-valued dictionary for HTTP headers.

        This class behaves like a standard dictionary but correctly handles
        the specific rules of HTTP headers, such as allowing multiple values
        for the same key (e.g., 'Set-Cookie').
    """
    def __init__(self) -> None:
        """
            Initializes a new, empty Headers object.
        """
        self.map: dict[str, list[str]] = {}

    def __getitem__(self, key: str) -> str:
        """
            Gets the first value for a given header key, case-insensitively.
        """
        key = key.lower()
        if key in self:
            return self.map[key][0]
        else:
            raise KeyError(f"Header '{key}' not found.")

    def get_all(self, key: str) -> list[str]:
        """
            Gets all values for a given header key as a list.
        """
        return self.map.get(key.lower(), [])

    def __setitem__(self, key: str, value: str) -> None:
        """
            Sets a header, replacing any existing values for that key.
        """
        self.map[key.lower()] = [value]

    def add(self, key: str, value: str) -> None:
        """
            Adds a value to a header, preserving any existing values.
        """
        key = key.lower()
        if key in self:
            self.map[key].append(value)
        else:
            self.map[key] = [value]

    def __delitem__(self, key: str) -> None:
        """
            Deletes a header and all of its associated values.
        """
        del self.map[key.lower()]

    def __contains__(self, key: object) -> bool:
        """
            Checks if a header key exists, case-insensitively.
        """
        if not isinstance(key, str):
            return False
        return str(key).lower() in self.map

    def __len__(self) -> int:
        """
            Returns the number of unique headers.
        """
        return len(self.map)

    def __iter__(self) -> Iterator:
        """
            Iterates over the header keys.
        """
        return iter(self.map)

    def get_headers(self) -> dict[str, list[str]]:
        """
            Returns a copy of the underlying headers dictionary.
        """
        return dict(self.map)
