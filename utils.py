"""General-purpose helpers for the data-toolkit project."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator, Mapping, Sequence
from typing import Any, Hashable, TypeVar

T = TypeVar("T")
K = TypeVar("K", bound=Hashable)
_MISSING = object()


def chunked(iterable: Iterable[T], size: int) -> Iterator[tuple[T, ...]]:
    """Yield items from an iterable in fixed-size chunks.

    The final chunk may contain fewer than ``size`` items.

    Args:
        iterable: Source values to divide into chunks.
        size: Maximum number of items per chunk. Must be positive.

    Yields:
        Tuples containing up to ``size`` source items.

    Raises:
        ValueError: If ``size`` is less than one.
    """
    if size < 1:
        raise ValueError("size must be greater than zero")

    chunk: list[T] = []
    for item in iterable:
        chunk.append(item)
        if len(chunk) == size:
            yield tuple(chunk)
            chunk.clear()

    if chunk:
        yield tuple(chunk)


def flatten_mapping(
    mapping: Mapping[str, Any],
    *,
    separator: str = ".",
    parent_key: str = "",
) -> dict[str, Any]:
    """Flatten a nested string-keyed mapping into a single-level dictionary.

    Args:
        mapping: Mapping whose nested mapping values should be flattened.
        separator: Text inserted between adjacent key components.
        parent_key: Optional prefix applied to every generated key.

    Returns:
        A dictionary containing flattened keys and original leaf values.

    Raises:
        ValueError: If ``separator`` is empty or flattened keys collide.
    """
    if not separator:
        raise ValueError("separator must not be empty")

    flattened: dict[str, Any] = {}
    pending: list[tuple[str, Mapping[str, Any]]] = [(parent_key, mapping)]

    while pending:
        prefix, current = pending.pop()
        for key, value in current.items():
            if not isinstance(key, str):
                raise TypeError("all mapping keys must be strings")

            combined_key = separator.join(part for part in (prefix, key) if part)
            if isinstance(value, Mapping) and value:
                pending.append((combined_key, value))
                continue

            if combined_key in flattened:
                raise ValueError(f"flattened key collision: {combined_key!r}")
            flattened[combined_key] = dict(value) if isinstance(value, Mapping) else value

    return flattened


def get_path(
    data: Any,
    path: Iterable[str | int],
    default: Any = _MISSING,
) -> Any:
    """Retrieve a value from nested mappings and sequences.

    String path components address mapping keys, while integer components can
    address either mapping keys or sequence indexes. Strings and bytes are not
    treated as indexable sequences.

    Args:
        data: Nested value to traverse.
        path: Ordered mapping keys or sequence indexes.
        default: Value returned when traversal fails. If omitted, failure
            raises an exception.

    Returns:
        The value found at the requested path, or ``default`` when supplied.

    Raises:
        KeyError: If a mapping key is missing and no default is supplied.
        IndexError: If a sequence index is invalid and no default is supplied.
        TypeError: If a component cannot be applied and no default is supplied.
    """
    current = data

    for component in path:
        try:
            if isinstance(current, Mapping):
                current = current[component]
            elif (
                isinstance(current, Sequence)
                and not isinstance(current, (str, bytes, bytearray))
                and isinstance(component, int)
            ):
                current = current[component]
            else:
                raise TypeError(
                    f"cannot apply path component {component!r} to "
                    f"{type(current).__name__}"
                )
        except (KeyError, IndexError, TypeError):
            if default is not _MISSING:
                return default
            raise

    return current


def unique_by(
    iterable: Iterable[T],
    key: Callable[[T], K] | None = None,
) -> list[T]:
    """Return unique items while preserving their first-seen order.

    Args:
        iterable: Source values from which duplicates are removed.
        key: Optional function producing a hashable identity for each item.
            When omitted, each item itself must be hashable.

    Returns:
        A list containing the first item for every unique identity.

    Raises:
        TypeError: If an item or generated identity is not hashable.
    """
    seen: set[Hashable] = set()
    result: list[T] = []

    for item in iterable:
        identity: Hashable = key(item) if key is not None else item  # type: ignore[assignment]
        if identity not in seen:
            seen.add(identity)
            result.append(item)

    return result