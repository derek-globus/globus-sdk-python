from __future__ import annotations

import typing as t
from copy import deepcopy


class GlocalConfig(t.TypedDict, total=False):
    core: CoreConfig


class CoreConfig(t.TypedDict, total=False):
    service_blocklist: t.List[str]


def load_config(user_config: GlocalConfig | None = None) -> GlocalConfig:
    """
    Load a GlocalConfig from the user's configuration, filling in any missing values
        with defaults.
    """
    default_config = deepcopy(_DEFAULT_CONFIG)
    if user_config is None:
        return default_config

    for key, subconfig in default_config.items():
        if key in user_config:
            subconfig.update(user_config[key])

    return default_config


_DEFAULT_CONFIG = {
    "core": {
        "service_blocklist": [],
    }
}

