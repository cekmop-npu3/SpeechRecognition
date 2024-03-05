from aiohttp import ClientSession, FormData
from aiofiles import open as aio_open
from asyncio import sleep, run
from os import PathLike
from os.path import exists
from typing import Literal
from json import dumps

from Utils import (
    Singleton,
    ApiEndpoints,
    basicVkHandler,
    responseHandler,
    UploadUrl,
    Response,
    Audio,
    TaskId,
    VkApiException,
    Status
)


class SpeechRecognition(metaclass=Singleton):
    def __init__(self, access_token: str, vk_api_version: str | int = '5.199') -> None:
        self.auth = {'access_token': access_token, 'v': vk_api_version}

    @basicVkHandler
    async def uploadServer(self) -> UploadUrl | Response:
        async with ClientSession() as session:
            async with session.post(
                url=ApiEndpoints.uploadServer,
                data=self.auth
            ) as response:
                return await responseHandler(response, 'toJson')

    @staticmethod
    @basicVkHandler
    async def loadAudioFromSource(source: str) -> bytes | Response:
        async with ClientSession() as session:
            async with session.get(
                url=source,
                headers=ApiEndpoints.headers
            ) as response:
                return await responseHandler(response, 'toBytes')

    @basicVkHandler
    async def uploadAudio(self, upload_url: UploadUrl, audio: str | bytes | PathLike) -> Audio | Response:
        if isinstance(audio, str):
            if exists(audio):
                async with aio_open(audio, 'rb') as file:
                    audio = await file.read()
            elif audio.startswith('http'):
                audio = await self.loadAudioFromSource(audio)
            else:
                raise VkApiException('No such file')
        async with ClientSession() as session:
            async with session.post(
                url=upload_url.get('upload_url'),
                data=((new := FormData()).add_field('file', audio), new)[1]
            ) as response:
                return await responseHandler(response, 'toJson')

    @basicVkHandler
    async def taskId(self, audio: Audio, recognition_mode: Literal['neutral', 'spontaneous'] = 'spontaneous') -> TaskId | Response:
        async with ClientSession() as session:
            async with session.post(
                url=ApiEndpoints.processFileObj,
                data=self.auth | {'audio': dumps(audio), 'model': recognition_mode}
            ) as response:
                return await responseHandler(response, 'toJson')

    @basicVkHandler
    async def status(self, task_id: TaskId) -> Status | Response:
        async with ClientSession() as session:
            async with session.post(
                url=ApiEndpoints.checkStatus,
                data=self.auth | dict(task_id)
            ) as response:
                return await responseHandler(response, 'toJson')

    async def pending(self, task_id: TaskId) -> Status:
        if (status := (r := await self.status(task_id)).get('status')) in ('internal_error', 'transcoding_error', 'recognition_error'):
            raise VkApiException(status)
        await sleep(1)
        return r if status == 'finished' else await self.pending(task_id)

    async def recognize(self, audio: str | bytes | PathLike, recognition_mode: Literal['neutral', 'spontaneous'] = 'spontaneous') -> str:
        return (await self.pending(await self.taskId(await self.uploadAudio(await self.uploadServer(), audio), recognition_mode))).get('text')
