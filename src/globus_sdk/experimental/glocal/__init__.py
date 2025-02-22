"""
Experimental Module
(moto but for globus)

With glocal, you can run an in-memory version of Globus hosted services to aid in
testing.

glocal modules are updated on a best-effort basis with the intent of properly
emulating globus api behavior an in-memory context. There are no guarantees of total
accuracy or completeness.
As we encounter bugs and missing features, we will update glocal to address them but
some discrepancies may be intentionally omitted. The goal isn't to replace globus
services, just simulate their APIs.
"""

from .decorator import mock_globus

__all__ = (
    "mock_globus",
)
