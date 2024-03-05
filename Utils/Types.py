from typing import TypedDict, Literal, NotRequired


__all__ = (
    'ServiceToken',
    'UploadUrl',
    'Audio',
    'TaskId',
    'Status'
)


class ServiceToken(TypedDict):
    access_token: str


class UploadUrl(TypedDict):
    upload_url: str


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


class TaskId(TypedDict):
    task_id: str


class Status(TypedDict):
    id: str
    status: Literal['processing', 'finished', 'internal_error', 'transcoding_error', 'recognition_error']
    text: str
