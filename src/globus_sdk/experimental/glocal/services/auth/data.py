from __future__ import annotations

import dataclasses
import uuid


@dataclasses.dataclass
class Scope:
    client: str
    scope_string: str
    name: str
    description: str = ""
    dependent_scopes: list[DependentScope] = dataclasses.field(default_factory=list)
    advertised: bool = False
    allows_refresh_token: bool = True
    id: str = dataclasses.field(init=False, default_factory=lambda: str(uuid.uuid4()))


@dataclasses.dataclass
class DependentScope:
    scope: str
    optional: bool
    requires_refresh_token: bool
