import typing as t

from ..core import BaseBackend

from .auth import AuthBackend
from .compute import ComputeBackend
from .flows import FlowsBackend
from .groups import GroupsBackend
from .search import SearchBackend
from .timers import TimersBackend
from .transfer import TransferBackend


_BACKENDS = (
    AuthBackend,
    ComputeBackend,
    FlowsBackend,
    GroupsBackend,
    SearchBackend,
    TimersBackend,
    TransferBackend,
)


def load_backends(blocklist: list[str]) -> t.Iterator[BaseBackend]:
    """
    Load all globus backends.
    Any service in the blocklist will not be loaded.
    """
    for backend_cls in _BACKENDS:
        if backend_cls.service_name not in blocklist:
            yield backend_cls()

__all__ = (
    "load_backends",
)
