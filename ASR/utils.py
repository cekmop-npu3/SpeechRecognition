from typing import Any, TypeVar


__all__ = (
    'Response',
    'ReadOnly',
    'VkApiException',
    'vkErrorHandler'
)


Response = TypeVar('Response')


class ReadOnlyMeta(type):
    class Attr:
        def __init__(self, value: Any) -> None:
            self.value = value

        def __get__(self, instance, owner) -> Any:
            return self.value

        def __set__(self, instance, value):
            raise AttributeError("Can't set attribute")

    def __new__(mcs, name, bases, attrs) -> object:
        new_attrs = {}
        for key, value in attrs.items():
            if not key.startswith('__'):
                value = mcs.Attr(value)
            new_attrs[key] = value
        return super().__new__(mcs, name, bases, new_attrs)

    def __setattr__(cls, key, value) -> None:
        if hasattr(cls, key):
            raise AttributeError("Can't set attribute")
        super().__setattr__(key, value)


class ReadOnly(metaclass=ReadOnlyMeta):
    pass


class VkApiException(Exception):
    pass


def vkErrorHandler(rsp: Response) -> Response:
    if r := rsp.error:
        raise VkApiException(r.error_msg)
    elif r := rsp.error_msg:
        raise VkApiException(r)
    return rsp
