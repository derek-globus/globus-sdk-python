
from ..core import BaseBackend
from .flows import FlowsBackend


_backends = {
    backend.service_name: backend
    for backend in (FlowsBackend,)
}

def load_backends(blocklist: list[str]) -> tuple[BaseBackend, ...]:
    """
    Load all globus backends.
    Any service in the blocklist will not be loaded.
    """
    backends = []
    for service_name, backend_cls in _backends.items():
        if service_name in blocklist:
            continue
        backends.append(backend_cls())

    return tuple(backends)

__all__ = (
    "load_backends",
)
