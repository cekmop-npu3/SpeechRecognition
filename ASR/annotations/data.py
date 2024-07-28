from os import PathLike
from typing import Union, TypeAlias, Annotated, Literal

from ASR.utils import ReadOnly
from ASR.javascript import Object


__all__ = (
    'File',
    'Model',
    'BadStatus',
    'Endpoints',
    'VkParams',
    'ServiceToken',
    'ServiceTokenRsp',
    'UploadUrl',
    'UploadUrlRsp',
    'Meta',
    'Audio',
    'AudioObject',
    'TaskId',
    'TaskIdRsp',
    'Text',
    'CheckStatus'
)


File: TypeAlias = Union[bytes, Annotated[str, 'Url to file'], Annotated[PathLike, 'Path to local file']]
Model: TypeAlias = Literal['neutral', 'spontaneous']

BadStatus = ('internal_error', 'transcoding_error', 'recognition_error')


class Endpoints(ReadOnly):
    serviceToken = 'https://api.vk.com/method/restore.getAccessToken?v=5.83'
    uploadUrl = 'https://api.vk.com/method/asr.getUploadUrl'
    processAudio = 'https://api.vk.com/method/asr.process'
    checkStatus = 'https://api.vk.com/method/asr.checkStatus'


class VkParams(Object):
    v: str
    access_token: str


"""ServiceTokenRsp entities"""


class ServiceToken(Object):
    access_token: str


class ServiceTokenRsp(Object):
    response: list[Union[int, ServiceToken]]


"""UploadUrlRsp entities"""


class UploadUrl(Object):
    upload_url: str


class UploadUrlRsp(Object):
    response: UploadUrl


"""AudioObject entities"""


class Meta(Object):
    duration: str
    size: str
    type: Literal['mp3', 'ogg', 'wav']


class Audio(Object):
    sha: str
    secret: str
    meta: Meta
    hash: str
    server: str
    request_id: str
    app_id: int


class AudioObject(Object):
    audio: Audio
    model: Model


"""TaskId entities"""


class TaskId(Object):
    task_id: str


class TaskIdRsp(Object):
    response: TaskId


"""Status entities"""


class Text(Object):
    id: str
    status: Literal['processing', 'finished', 'internal_error', 'transcoding_error', 'recognition_error']
    text: str


class CheckStatus(Object):
    response: Text
