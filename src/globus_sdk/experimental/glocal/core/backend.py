from __future__ import annotations

import functools
import inspect
import json
import re

import typing as t
import urllib.parse
from io import BufferedReader
import requests

from .route import RouteMetadata, AnnotatedHandler, RouteResp, api_route




class BaseBackend:

    # [Required Class Attribute] The name of the service implemented by this backend.
    # e.g., "flows"
    service_name: str = "_base"

    # [Required Class Attribute] The url prefix; prepended to any route registrations.
    # e.g., "https://flows.automate.globus.org/"
    base_url: str = "_base"

    def __init__(self) -> None:
        for attr in ("service_name", "base_url"):
            if getattr(self, attr) == "_base":
                msg = f"Missing required class attribute: `{attr}` in {type(self)}"
                raise NotImplementedError(msg)

    @property
    def api_handlers(self) -> t.Iterator[AnnotatedHandler]:
        for attr in dir(self):
            item = getattr(self, attr)
            meta = getattr(item, "meta", None)
            if isinstance(meta, RouteMetadata):
                yield item

        # Default fallback route for unimplemented service routes.
        # Responses prefers earlier-registered routes; so this must be added last.
        # TODO - is this possible?
        #  We'll probably need to use a custom registry if we want fallback responses (maybe just moto's?)
        #  https://github.com/getmoto/moto/blob/master/moto/core/responses_custom_registry.py
        # yield _NOT_IMPLEMENTED_ROUTE


    def close(self) -> None:
        pass


_ALL_METHODS = (
    "GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS", "TRACE", "CONNECT"
)


@api_route(re.compile(".*"), _ALL_METHODS)
def _NOT_IMPLEMENTED_ROUTE() -> RouteResp:
    """
    A standard route registered on every backend.
    Gives control over the default "unimplemented" response structure.
    """
    return 501, {}, json.dumps({"Error": "Not Implemented"})
