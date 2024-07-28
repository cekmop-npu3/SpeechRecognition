from __future__ import annotations as _

from typing import Any, Iterable, Optional


__all__ = (
    'Object',
)


def applyCustomDict(data: Any) -> Any:
    if isinstance(data, dict):
        return CustomDict({key: applyCustomDict(value) for key, value in data.items()})
    elif hasattr(data, '__iter__') and not isinstance(data, str):
        return data.__class__(map(applyCustomDict, data))
    return data


class CustomDict(dict):
    def __getattr__(self, item) -> Any:
        return self.get(item)

    def __setattr__(self, key, value) -> None:
        return self.__setitem__(key, value)

    def __setitem__(self, key, value) -> None:
        return super().__setitem__(key, applyCustomDict(value))

    def __init__(self, seq=None, **kwargs) -> None:
        super().__init__()
        [self.__setitem__(key, value) for key, value in (dict(seq) | kwargs if seq else kwargs).items()]

    def __call__(self, seq=None, **kwargs) -> CustomDict:
        [self.__setitem__(key, value) for key, value in (dict(seq) | kwargs if seq else kwargs).items()]
        return self

    def __hash__(self) -> hash:
        return hash(self.__dict__)

    def __or__(self, other) -> CustomDict | type(CustomDict):
        if isinstance(other, dict):
            return self(other)
        return type(self)

    def __ror__(self, other) -> CustomDict | type(CustomDict):
        if isinstance(other, dict):
            return self(other)
        return type(self)

    def update(self, seq=None, **kwargs) -> None:
        [self.__setitem__(key, value) for key, value in (dict(seq) | kwargs if seq else kwargs).items()]

    @classmethod
    def fromkeys(cls, iterable: Iterable, value: Optional[Any] = None) -> CustomDict:
        return CustomDict({item: value for item in iterable})

    def setdefault(self, key: str, default: Optional[Any] = None) -> Any:
        if key not in self:
            self.__setitem__(key, default)
        return self.get(key)


class ObjectMeta(type):
    def __new__(mcs, name, bases, attrs) -> CustomDict | Object:
        if not attrs.get('__check__'):
            return CustomDict
        return super().__new__(mcs, name, bases, attrs)


class Object(metaclass=ObjectMeta):
    __check__ = True

    def __init__(self, *args, **kwargs):
        raise NotImplementedError('Object class should be used via inheriting')
