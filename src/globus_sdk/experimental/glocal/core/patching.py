from __future__ import annotations

import inspect
import typing as t

import functools
import re
from urllib.parse import urljoin

import requests
import responses

from .backend import BaseBackend
from .route import RouteMetadata, RouteResp
from .route.decorator import AnnotatedHandler


class ResponsesPatcher:
    """
    A context manager for patching globus backends using the `responses` library.

    On __exit__, any patched backends will have their `close` method called and the
    `responses` mock will be stopped and reset.
    """

    def __init__(self, requests_mock: responses.RequestsMock | None = None) -> None:
        self._requests_mock = requests_mock or responses._default_mock
        self._patched: list[BaseBackend] = []

    def __enter__(self):
        self._requests_mock.start()
        return self

    def __exit__(self, *args):
        for backend in self._patched:
            backend.close()
        self._requests_mock.stop()
        self._requests_mock.reset()

    def patch_backend(self, backend: BaseBackend) -> None:
        for handler in backend.api_handlers:
            url = self._build_url(backend, handler.meta)
            for method in handler.meta.methods:
                route = functools.partial(_handle_request, handler)
                self._requests_mock.add_callback(url=url, method=method, callback=route)


    @classmethod
    def _build_url(cls, backend: BaseBackend, meta: RouteMetadata) -> str | re.Pattern:
        if isinstance(meta.path, re.Pattern):
            url_pattern = _append_path(backend.base_url, meta.path.pattern)
            return re.compile(url_pattern)

        return _append_path(backend.base_url, meta.path)


def _append_path(base_url: str, path: str) -> str:
    if path.startswith("/"):
        path = path[1:]
    return urljoin(base_url, path[1:] if path.startswith("/") else path)


def _handle_request(
    handler: AnnotatedHandler,
    request: requests.PreparedRequest,
) -> RouteResp:
    kwargs: dict[str, t.Any] = _extract_path_params(handler, request)
    if "request" in inspect.signature(handler).parameters:
        kwargs["request"] = request

    return handler(**kwargs)

def _extract_path_params(
    handler: AnnotatedHandler,
    request: requests.PreparedRequest,
) -> dict[str, str]:
    """
    Load path parameters from the request URL.
    If the route has no path parameters, this will return an empty dict.
    """
    path = handler.meta.path
    if isinstance(path, re.Pattern):
        # TODO - request.path_url sort of assumes that the part we want to strip is
        #   just a domain. This is an issue for apis like groups that have a /v2/
        #   prefix.
        match = path.search(request.path_url)
        return {param: match.group(param) for param in handler.meta.path_params}
    return {}
