from __future__ import annotations

import dataclasses
import uuid

import typing as t


@dataclasses.dataclass
class Flow:
    title: str
    definition: dict[str, t.Any]
    input_schema: dict[str, t.Any]
    subtitle: str | None = None
    description: str | None = None
    id: str = dataclasses.field(default_factory=lambda: str(uuid.uuid4()))

    def as_dict(self) -> dict[str, t.Any]:
        return dataclasses.asdict(self)
