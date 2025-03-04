import typing as t
from io import BufferedReader

import requests

from .meta import RouteMetadata


_RouteRespBody = t.Union[
    str, BaseException, requests.Response, BufferedReader, bytes, None
]
RouteResp = t.Union[
    Exception,
    # (status_code, headers, body)
    t.Tuple[int, t.Mapping[str, str], _RouteRespBody],
]

RouteHandler = t.Callable[..., RouteResp]
CallbackFunction = t.Callable[[requests.PreparedRequest], RouteResp]

class AnnotatedHandler(t.Protocol):
    meta: RouteMetadata
    __call__: RouteHandler

