from __future__ import annotations

import functools
import inspect
import re

import typing as t
import urllib.parse
from io import BufferedReader

if t.TYPE_CHECKING:
    from requests import PreparedRequest, Response

    _RouteRespBody = t.Union[
        str, BaseException, Response, BufferedReader, bytes, None
    ]
    RouteResp = t.Union[
        Exception,
        # (status_code, headers, body)
        t.Tuple[int, t.Mapping[str, str], _RouteRespBody],
    ]

    RouteHandler = t.Callable[..., RouteResp]
    CallbackFunction = t.Callable[[PreparedRequest], RouteResp]


class BaseBackend:

    # The backend service name.
    # This is how a backend is identified; for instance, in config.
    # e.g., "flows"
    service_name: str = "_base"

    # A url prefix for all registered routes
    # e.g., "https://flows.automate.globus.org/"
    base_url: str = "_base"

    def __init__(self) -> None:
        for attr in ("service_name", "base_url"):
            if getattr(self, attr) == "_base":
                msg = f"Missing required class attribute: `{attr}` in {type(self)}"
                raise NotImplementedError(msg)

        for route in self.http_routes():
            route.bind(self)

    def http_routes(self) -> t.Iterator[HttpRoute]:
        for attr in dir(self):
            item = getattr(self, attr)
            if isinstance(item, HttpRoute):
                yield item

    def close(self) -> None:
        pass


def http_route(
    path: str, methods: t.Sequence[str]
) -> t.Callable[[RouteHandler], HttpRoute]:
    """
    Decorator to define an HTTP route on a backend service.
    """

    def decorator(handler: RouteHandler) -> HttpRoute:
        route = HttpRoute(path, list(methods), handler)
        functools.wraps(handler)(route)

        return route

    return decorator



class HttpRoute:
    """
    Callable object wrapping an route handler with metadata about the route.

    If the route wraps an instance method, the instance should be bound to the route
    using the `bind` method.
    """

    def __init__(self, path: str, methods: t.List[str], handler: RouteHandler) -> None:
        self.path = path
        self.methods = methods
        self._handler = handler

        self._path_params = re.findall(r"{([^/]+)}", path)
        self._path_patt_str = path.replace("{", "(?P<").replace("}", ">[^/]+)")
        self._path_patt = re.compile(self._path_patt_str) if self._path_params else None

        self._instance: object | None = None


    def __call__(self, request: PreparedRequest) -> RouteResp:
        event: t.Dict[str, t.Any] = self._extract_path_params(request)
        if "request" in inspect.signature(self._handler).parameters:
            event["request"] = request

        if self._instance:
            return self._handler(self._instance, **event)
        else:
            return self._handler(**event)

    def bind(self, instance: object) -> None:
        """
        Bind a route handler to an instance to support Routes as an instance method.
        This will be supplied to the `_handler` as a first "self" parameter.
        """
        self._instance = instance

    def _extract_path_params(self, request: PreparedRequest) -> t.Dict[str, str]:
        """
        Load any path parameters from the request URL.
        If the route has no path parameters, this will return an empty dict.
        """
        if self._path_patt:
            match = self._path_patt.match(request.path_url)
            return {param: match.group(param) for param in self._path_params}
        return {}

    def get_url(self, base_url: str) -> str | re.Pattern:
        if not self._path_params:
            return urllib.parse.urljoin(base_url, self.path)

        url = urllib.parse.urljoin(base_url, self._path_patt_str)
        return re.compile(url)

    def __repr__(self):
        return f"<HttpRoute {self.methods} {self.path}>"
