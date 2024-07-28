from typing import Any, overload, Mapping


__all__ = (
    'Object',
)


class CustomDict(dict):
    @overload
    def __init__(self, **kwargs) -> None: ...

    @overload
    def __init__(self, seq: dict[str, Any]) -> None: ...

    @overload
    def __init__(self, seq: list[tuple]) -> None: ...

    @overload
    def __call__(self, **kwargs) -> CustomDict: ...

    @overload
    def __call__(self, seq: dict[str, Any]) -> CustomDict: ...

    @overload
    def __call__(self, seq: list[tuple]) -> CustomDict: ...

    def __getattr__(self, item) -> Any: ...

    def __or__(self, other: Mapping) -> CustomDict: ...

    def __ror__(self, other: Mapping) -> CustomDict: ...


class Object(CustomDict): ...
