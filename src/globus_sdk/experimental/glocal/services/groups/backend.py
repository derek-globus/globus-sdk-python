from __future__ import annotations

import json
import typing as t
import requests

from globus_sdk.experimental.glocal.core import BaseBackend, api_route, DataManager
from .data import Group

if t.TYPE_CHECKING:
    from requests import PreparedRequest
    from globus_sdk.experimental.glocal.core import RouteResp

class GroupsBackend(BaseBackend):

    service_name = "groups"
    base_url = "https://groups.api.globus.org/v2/"

    def __init__(self):
        super().__init__()
        self._group_manager = DataManager(Group)
        self._groups: dict[str, Group] = {}

    # -- Group CRUD Ops --

    @api_route("/groups", methods=["POST"])
    def create_group(self, request: requests.PreparedRequest) -> RouteResp:
        try:
            group = self._group_manager.create(request)
        except TypeError:
            return 400, {}, "Invalid request body"

        self._groups[group.id] = group

        return 201, {}, self._group_manager.serialize(group)

    @api_route("/groups/my_groups", methods=["GET"])
    def list_groups(self) ->  RouteResp:
        groups = self._groups.values()
        groups_dict = [self._group_manager.to_dict(group) for group in groups]
        return 200, {}, json.dumps(groups_dict)

    @api_route("/groups/{group_id}", methods=["GET"])
    def get_group(self, group_id: str) ->  RouteResp:
        if group_id not in self._groups:
            return 404, {}, "Group not found"
        group = self._groups[group_id]

        return 200, {}, self._group_manager.serialize(group)

    @api_route("/subscription_info/{subscription_id}", methods=["GET"])
    def get_group_by_subscription_id(self, subscription_id: str) ->  RouteResp:
        pass

    @api_route("/groups/{group_id}", methods=["PUT"])
    def update_group(self, request: requests.PreparedRequest, group_id: str) -> RouteResp:
        if group_id in self._groups:
            # TODO - verify
            return 409, {}, "Group already exists"

        try:
            group = self._group_manager.create(request)
        except TypeError:
            return 400, {}, "Invalid request body"

        self._groups[group.id] = group
        return 200, {}, self._group_manager.serialize(group)


    @api_route("/groups/{group_id}", methods=["DELETE"])
    def delete_group(self, group_id: str) ->  RouteResp:
        group = self._groups.get(group_id)
        if group_id in self._groups:
            del self._groups[group_id]
        resp = self._group_manager.serialize(group) if group else ""

        return 200, {}, resp

    # -- Group Facet: Policy --

    @api_route("/groups/{group_id}/policies", methods=["PUT"])
    def set_group_policies(self, request: requests.PreparedRequest, group_id: str) -> RouteResp:
        pass

    @api_route("/groups/{group_id}/policies", methods=["GET"])
    def get_group_policies(self, group_id: str) -> RouteResp:
        pass

    # -- Group Facet: Membership Fields --

    @api_route("/groups/{group_id}/membership_fields", methods=["PUT"])
    def set_group_membership_fields(self, request: requests.PreparedRequest, group_id: str) -> RouteResp:
        pass

    @api_route("/groups/{group_id}/membership_fields", methods=["GET"])
    def get_group_membership_fields(self, group_id: str) -> RouteResp:
        pass

    # -- Group Membership Actions --

    @api_route("/groups/{group_id}", methods=["POST"])
    def batch_membership_action(self, request: requests.PreparedRequest, group_id: str) -> RouteResp:
        pass

    # -- Identity Preferences --

    @api_route("/preferences", methods=["PUT"])
    def set_identity_preferences(self, request: requests.PreparedRequest) -> RouteResp:
        pass

    @api_route("/preferences", methods=["GET"])
    def get_identity_preferences(self):
        pass
