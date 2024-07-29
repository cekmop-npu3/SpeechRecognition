from typing import NoReturn, Optional, Union


__all__ = (
    'StatusCode',
    'Status'
)


class StatusCode:
    def __init__(self, status: int, message: Optional[str] = None) -> None:
        self._status = status
        self._message = message

    @property
    def status(self) -> int:
        return self._status

    @status.setter
    def status(self, value) -> NoReturn:
        raise AttributeError("Can't set attribute")

    @property
    def message(self) -> Optional[str]:
        return self._message

    @message.setter
    def message(self, value) -> NoReturn:
        raise AttributeError("Can't set attribute")

    def __eq__(self, other) -> bool:
        if isinstance(other, StatusCode):
            return self.status == other.status
        elif isinstance(other, int):
            return self.status == other
        elif isinstance(other, str):
            if other.isdigit():
                return self.status == int(other)
        raise TypeError(f'Object must be type of {self.__class__.__name__}, int or digit str, not {type(other)}')

    def __iter__(self) -> iter:
        return iter(self.__dict__.values())

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({", ".join([f"{key}={value}" for key, value in self.__dict__.items()])})'


class StatusMeta(type):
    def __new__(mcs, name, bases, attrs: dict) -> object:
        [attrs.__setitem__(key, StatusCode(value) if isinstance(value, int) else StatusCode(*value)) for key, value in attrs.items() if not key.startswith('__') and not hasattr(object, key)]
        return super().__new__(mcs, name, bases, attrs)

    def __getitem__(self, status: Union[StatusCode, int]) -> StatusCode:
        return list(filter(lambda x: x == status, (value for key, value in self.__dict__.items() if not key.startswith('__') and not hasattr(object, key))))[0]

    def __repr__(self) -> str:
        return f'{self.__name__}({", ".join([f"{key}={value}" for key, value in self.__dict__.items() if not key.startswith("__") and not hasattr(object, key)])})'


class Status(metaclass=StatusMeta):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError(f'Cannot instantiate {self.__class__.__name__} object')
