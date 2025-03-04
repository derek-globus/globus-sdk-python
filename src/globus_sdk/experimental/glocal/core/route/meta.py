from __future__ import annotations

import dataclasses
import typing as t

import re
import urllib.parse


@dataclasses.dataclass(frozen=True)
class RouteMetadata:
    path: str | re.Pattern
    methods: t.Sequence[str]
    path_params: t.Sequence[str] = dataclasses.field(init=False, default_factory=tuple)

    def __post_init__(self):
        self._init_path_params(self.path)

    def _init_path_params(self, path: str | re.Pattern) -> None:
        """
        Extract path parameters from str path specifications.

        If path params are found:
          1. They will be stored in the `path_params` attribute as a tuple.
          2. The path will be compiled into a regex pattern for named-group matching.
        """
        if isinstance(path, str):
            path_params = _parse_path_params(path)
            if path_params:
                object.__setattr__(self, "path", _compile_path(path))
                object.__setattr__(self, "path_params", path_params)


def _parse_path_params(path: str) -> tuple[str, ...]:
    """
    Extract path parameters from a string-type route path specification.
    e.g., "/path/{p1}/{p2}" -> ["p1", "p2"]
    """
    return tuple(re.findall(r"{([^/]+)}", path))

def _compile_path(path: str) -> re.Pattern:
    """
    Compile a path string into a regex pattern, replacing path parameters with regex
    named-groups.
    e.g., "/path/{p1}/{p2}" -> Pattern("/path/(?P<p1>[^/]+)/(?P<p2>[^/]+)")
    """
    path = path.replace("{", "(?P<")
    path = path.replace("}", ">[^/]+)")
    return re.compile(path)

