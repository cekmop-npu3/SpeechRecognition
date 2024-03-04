from aiohttp import ClientResponse, ClientResponseError
from typing import Callable, Literal, Optional, Any
from dataclasses import dataclass
from json import loads
from json.decoder import JSONDecodeError

from .MetaBase import ReadOnly


class ApiEndpoints(metaclass=ReadOnly):
    uploadServer = 'https://api.vk.com/method/asr.getUploadUrl'
    processFileObj = 'https://api.vk.com/method/asr.process'
    checkStatus = 'https://api.vk.com/method/asr.checkStatus'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                      '/121.0.0.0 Safari/537.36 OPR/107.0.0.0'
    }


class VkApiException(Exception):
    def __init__(self, message: Optional[str | dict]) -> None:
        super().__init__(message)


@dataclass(kw_only=True)
class Response:
    status: int
    json: Optional[dict]
    text: Optional[str]
    content: Optional[bytes]

    def __repr__(self) -> str:
        return f'Response({", ".join([f"{key}={value}" for key, value in list(filter(lambda item: item[1] is not None, self.__dict__.items()))])})'


async def responseHandler(response: ClientResponse, state: Literal['toJson', 'toText', 'toBytes']) -> Response:
    response_json, text, content = None, None, None
    match state:
        case 'toJson':
            try:
                response_json = await response.json()
            except ClientResponseError:
                try:
                    response_json = loads(text := await response.text())
                except JSONDecodeError:
                    pass
        case 'toText':
            text = await response.text()
        case 'toBytes':
            content = await response.read()
    return Response(json=response_json, text=text if text else None, content=content, status=response.status)


def errorHandler(state: Literal['toJson', 'toText', 'toBytes'] = None) -> Any:
    def outer(obj: Callable):
        async def wrapper(*args, **kwargs):
            response: Response = await obj(*args, **kwargs)
            if response.status < 400 and isinstance(response, Response):
                match state:
                    case 'toJson':
                        if r := response.json:
                            if r.get('error'):
                                raise VkApiException(r.get('error').get('error_msg'))
                            elif r.get('error_msg'):
                                raise VkApiException(r.get('error_msg'))
                            return r
                        raise VkApiException('Invalid json')
                    case 'toText':
                        return response.text
                    case 'toBytes':
                        return response.content
                    case None:
                        raise VkApiException('No state has been provided')
            raise VkApiException('Bad request')
        return wrapper
    return outer
