"""General-purpose helpers for working with data collections."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable, Iterable, Iterator, Mapping
from typing import Any, Hashable, TypeVar

T = TypeVar("T")
K = TypeVar("K", bound=Hashable)


def chunked(items: Iterable[T], size: int) -> Iterator[list[T]]:
    """Yield items in lists containing at most ``size`` elements.

    Args:
        items: Values to divide into chunks.
        size: Maximum number of elements per chunk. Must be positive.

    Yields:
        Lists of up to ``size`` elements, preserving input order.

    Raises:
        ValueError: If ``size`` is not a positive integer.
    """
    if isinstance(size, bool) or not isinstance(size, int) or size <= 0:
        raise ValueError("size must be a positive integer")

    chunk: list[T] = []
    for item in items:
        chunk.append(item)
        if len(chunk) == size:
            yield chunk
            chunk = []

    if chunk:
        yield chunk


def unique(
    items: Iterable[T],
    key: Callable[[T], Hashable] | None = None,
) -> list[T]:
    """Return unique items while preserving their first-seen order.

    Args:
        items: Values to deduplicate.
        key: Optional function that returns a hashable identity for each item.

    Returns:
        A list containing the first item associated with each unique identity.

    Raises:
        TypeError: If an item, or the value returned by ``key``, is unhashable.
    """
    seen: set[Hashable] = set()
    result: list[T] = []

    for item in items:
        identity = key(item) if key is not None else item
        if identity not in seen:
            seen.add(identity)
            result.append(item)

    return result


def group_by(items: Iterable[T], key: Callable[[T], K]) -> dict[K, list[T]]:
    """Group items by a key while preserving their input order.

    Args:
        items: Values to group.
        key: Function that returns a hashable group key for each item.

    Returns:
        A dictionary mapping each key to its corresponding ordered items.
    """
    groups: defaultdict[K, list[T]] = defaultdict(list)
    for item in items:
        groups[key(item)].append(item)
    return dict(groups)


def deep_get(
    data: Mapping[str, Any],
    path: str | Iterable[str],
    default: Any = None,
    *,
    separator: str = ".",
) -> Any:
    """Retrieve a value from nested mappings without raising ``KeyError``.

    Args:
        data: Root mapping to search.
        path: Dot-separated path or iterable of individual string keys.
        default: Value returned when a key is absent or an intermediate value
            is not a mapping.
        separator: Delimiter used when ``path`` is a string.

    Returns:
        The nested value when found; otherwise ``default``.

    Raises:
        ValueError: If ``separator`` is empty or the path contains an empty key.
        TypeError: If a path component is not a string.
    """
    if not separator:
        raise ValueError("separator must not be empty")

    keys = path.split(separator) if isinstance(path, str) else tuple(path)
    if any(not isinstance(key, str) for key in keys):
        raise TypeError("path components must be strings")
    if any(not key for key in keys):
        raise ValueError("path components must not be empty")

    current: Any = data
    for key in keys:
        if not isinstance(current, Mapping) or key not in current:
            return default
        current = current[key]

    return current