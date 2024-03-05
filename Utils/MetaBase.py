from functools import partial
from typing import Any


class ReadOnly(type):

    class PreparedDict(dict):
        def __setitem__(self, key: str, value: Any) -> None:
            if not key.startswith('__'):
                setattr(ReadOnly, f'__{key}', value)
                setattr(ReadOnly, f'{key}', property(
                    fget=partial(ReadOnly.getItem, key),
                    fset=partial(ReadOnly.setItem, key)
                ))
            super().__setitem__(key, value)

    @staticmethod
    def getItem(key: str, _) -> Any:
        return getattr(ReadOnly, f'__{key}')

    @staticmethod
    def setItem(key: str, *_):
        raise AttributeError(f'Cannot reassign {key}')

    def __new__(mcs, name, bases, attrs) -> object:
        return super().__new__(mcs, name, bases, attrs)

    @classmethod
    def __prepare__(mcs, name, bases) -> PreparedDict:
        return mcs.PreparedDict()
