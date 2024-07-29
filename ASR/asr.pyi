from typing import Optional, overload, Annotated
from os import PathLike

from .types import Model, Text


__all__ = (
    'Asr',
)


class Asr:
    def __init__(self, accessToken: Optional[str] = None) -> None: ...

    @overload
    async def recognize(self, audio: bytes, model: Model) -> Text: ...

    @overload
    async def recognize(self, audio: Annotated[str, 'Url to file'], model: Model) -> Text: ...

    @overload
    async def recognize(self, audio: Annotated[PathLike, 'Path to local file'], model: Model) -> Text: ...
