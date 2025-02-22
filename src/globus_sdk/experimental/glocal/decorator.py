import contextlib
import typing as t

import responses

from .core import ResponsesPatcher, load_config, GlocalConfig
from .services import load_backends


@contextlib.contextmanager
def mock_globus(
    config: GlocalConfig | None = None,
    *,
    requests_mock: responses.RequestsMock | None = None,
) -> t.Iterator[None]:
    config = load_config(config)

    with ResponsesPatcher(requests_mock) as patcher:
        for backend in load_backends(config["core"]["service_blocklist"]):
            patcher.patch_backend(backend)
        yield







