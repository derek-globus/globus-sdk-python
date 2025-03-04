from __future__ import annotations

import typing as t

import dataclasses
import uuid

from globus_sdk import MissingType, MISSING


@dataclasses.dataclass
class Group:
    # TODO - verify if these are required
    # == Required ==
    name: str

    # == Optional ==
    description: str | None = None
    # Required for certain high assurance use-cases.
    enforce_session: bool = False
    group_type: t.Literal["regular", "plus"] = "regular"
    id: str = dataclasses.field(default_factory=lambda: str(uuid.uuid4()))
    my_memberships: list[GroupMembership] = dataclasses.field(default_factory=list)
    parent_id: str | None = None
    child_ids: list[str] | MissingType = MISSING
    policies: GroupPolicies = dataclasses.field(default_factory=lambda: GroupPolicies())
    # TODO - verify default
    session_limit: int = 28800
    # TODO - how are these computed?
    # Key is some sort of UUID
    session_timeouts: dict[str, GroupSessionTimeout] = dataclasses.field(default_factory=dict)
    subscription_id: str | None = None
    subscription_info: GroupSubscriptionInfo | None = None
    # TODO - verify default
    terms_and_conditions: str | None = None


@dataclasses.dataclass
class GroupMembership:
    group_id: str
    identity_id: str
    invite_email_address: str | None
    invite_time: str
    membership_fields: dict[str, str]
    role: str
    status: str
    status_reason: str
    updated: str
    username: str


@dataclasses.dataclass
class GroupMembershipFields:
    email: str
    name: str
    nonprofit: bool
    organization: str


@dataclasses.dataclass
class GroupPolicies:
    authentication_assurance_timeout: int = 28800
    # TODO - this is an enum
    group_members_visibility: str = "managers"
    # TODO - this is an enum
    group_visibility: str = "private"
    is_high_assurance: bool = False
    join_requests: bool = False
    signup_fields: list[str] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class GroupSessionTimeout:
    expire_time: str
    expires_in: int


@dataclasses.dataclass
class GroupSubscriptionInfo:
    ...
