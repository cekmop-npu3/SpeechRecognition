from __future__ import annotations as _

from aiohttp import ClientSession, FormData
from asyncio import sleep
from typing import Optional
from aiofiles import open as async_open
from os.path import exists
from json import dumps

from .utils import vkErrorHandler, VkApiException
from .annotations import *


__all__ = (
    'Asr',
)


class FileManager:
    @staticmethod
    async def _loadFromSource(url: str) -> bytes:
        async with ClientSession() as session:
            async with session.get(url) as response:
                return await response.read()

    @staticmethod
    async def _loadFromPath(path: str) -> bytes:
        async with async_open(path, 'rb') as file:
            return await file.read()

    @classmethod
    async def getBytes(cls, audio: File) -> bytes:
        if isinstance(audio, str):
            if exists(audio):
                return await cls._loadFromPath(audio)
            return await cls._loadFromSource(audio)
        return audio


class Service:
    def __init__(self, params: VkParams, model: Model) -> None:
        self.params = params
        self.model = model

    async def __call__(self, audio: File) -> Text:
        payload = await FileManager.getBytes(audio)
        uploadUrl = await self.getUploadUrl()
        audioObject = await self.uploadFile(uploadUrl, payload)
        taskId = await self.process(audioObject)
        return await self.pending(taskId)

    async def getUploadUrl(self) -> UploadUrl:
        async with ClientSession() as session:
            async with session.get(Endpoints.uploadUrl, params=self.params) as response:
                return vkErrorHandler(UploadUrlRsp(await response.json())).response

    async def uploadFile(self, uploadUrl: UploadUrl, payload: bytes) -> AudioObject:
        async with ClientSession() as session:
            async with session.post(uploadUrl.upload_url, data=FormData([('file', payload)])) as response:
                if (r := response.status) == ResponseStatus.tooLarge:
                    raise VkApiException(ResponseStatus[r].message)
                return AudioObject(model=self.model, audio=dumps(Audio(await response.json())))

    async def process(self, audioObject: AudioObject) -> TaskId:
        async with ClientSession() as session:
            async with session.post(Endpoints.processAudio, params=self.params, data=audioObject) as response:
                return vkErrorHandler(TaskIdRsp(await response.json())).response

    async def pending(self, taskId: TaskId) -> Text:
        async with ClientSession() as session:
            async with session.post(Endpoints.checkStatus, params=self.params, data=taskId) as response:
                await sleep(1)
                if (text := CheckStatus(await response.json()).response).status in BadStatus:
                    raise VkApiException(text.status)
                return text if text.status == TextStatus.finished else await self.pending(taskId)


class Asr:
    def __init__(self, accessToken: Optional[str] = None) -> None:
        self.__accessToken = accessToken

    async def _loadParams(self) -> VkParams:
        if not self.__accessToken:
            self.__accessToken = (await self._generateServiceToken()).access_token
        return VkParams(v='5.199', access_token=self.__accessToken)

    @staticmethod
    async def _generateServiceToken() -> ServiceToken:
        async with ClientSession() as session:
            async with session.get(Endpoints.serviceToken) as response:
                return ServiceTokenRsp(await response.json()).response[1]

    async def recognize(self, audio: File, model: Model) -> Text:
        return await Service(await self._loadParams(), model)(audio)
