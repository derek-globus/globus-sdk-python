import inspect
import re
import typing as t

# Do we need to move this into a t.TYPE_CHECKING block for import speed?
import requests

from .meta import RouteMetadata
from .typing_ import RouteHandler, RouteResp


class AnnotatedHandler(t.Protocol):
    meta: RouteMetadata
    __call__: RouteHandler


def api_route(
    path: str | re.Pattern, methods: t.Sequence[str]
) -> t.Callable[[RouteHandler], AnnotatedHandler]:
    """
    Annotate a route handler method with a `meta` attribute containing RouteMetadata.

    Example
    >>> class MyApi:
    >>>    @api_route("/path/{p1}", ["GET"])
    >>>    def my_route(self, request: requests.PreparedRequest, p1: int) -> RouteResp:
    >>>        return 200, {}, "Hello World"

    :param path: The path to match for this route. Can contain path parameters in the
      form {param1} or be a compiled regex Pattern, but not both.
    :param methods: The HTTP methods to match for this route.
    """
    def decorator(handler: RouteHandler) -> AnnotatedHandler:
        if inspect.ismethod(handler):
            # Instance methods don't allow for setting arbitrary attributes like `meta`.
            raise TypeError(
                f"Invalid annotation target: {handler!r}. "
                "'@api_route' cannot be used on instance-bound methods."
            )
        if not callable(handler):
            raise TypeError(
                f"Invalid annotation target: {handler!r}. "
                "'@api_route' can only be used on callables."
            )

        handler.meta = RouteMetadata(path, methods)
        return handler

    return decorator
