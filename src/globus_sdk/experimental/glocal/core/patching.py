from __future__ import annotations

import responses

from .backend import BaseBackend


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

    def patch_backend(self, backend: BaseBackend) -> None:
        base_url = backend.base_url
        for route in backend.http_routes():
            for method in route.methods:
                self._requests_mock.add_callback(
                    method=method,
                    url=route.get_url(base_url),
                    callback=route,
                )
        self._patched.append(backend)

    def __exit__(self, *args):
        for backend in self._patched:
            backend.close()
        self._requests_mock.stop()
        self._requests_mock.reset()

