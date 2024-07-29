from typing import Optional, Union


__all__ = (
    'StatusCode',
    'Status'
)


class StatusCode:
    status: int
    message: Optional[str]

    def __init__(self, status: int, message: Optional[str] = None) -> None: ...


class Status:
    def __class_getitem__(cls, status: Union[StatusCode, int]) -> StatusCode: ...
