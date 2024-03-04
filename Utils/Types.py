from typing import TypedDict, Literal, NotRequired


__all__ = (
    'UploadUrl',
    'Audio',
    'TaskId',
    'Pending'
)


class UploadUrlBase(TypedDict):
    upload_url: str


class UploadUrl(TypedDict):
    response: UploadUrlBase


class Meta(TypedDict):
    duration: str
    size: str
    type: Literal['ogg', 'wav', 'mp3']


class Audio(TypedDict):
    sha: str
    secret: str
    meta: Meta
    hash: str
    server: str
    user_id: NotRequired[int]
    request_id: str
    app_id: int


class TaskIdRaw(TypedDict):
    task_id: str


class TaskId(TypedDict):
    response: TaskIdRaw


class PendingRaw(TypedDict):
    id: str
    status: Literal['processing', 'finished', 'internal_error', 'transcoding_error', 'recognition_error']
    text: str


class Pending(TypedDict):
    response: PendingRaw
