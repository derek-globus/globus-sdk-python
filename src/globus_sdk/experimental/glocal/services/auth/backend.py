import json
from urllib.parse import urlparse, parse_qs

import requests

from .data import Scope
from globus_sdk.experimental.glocal.core import BaseBackend, api_route, RouteResp, \
    DataManager


class AuthBackend(BaseBackend):

    service_name = "auth"
    base_url = "https://auth.globus.org/v2/api/"

    def __init__(self):
        super().__init__()
        self._scope_manager = DataManager(Scope)
        self._scopes: dict[str, Scope] = {}
        self._scopes_by_string: dict[str, Scope] = {}


    @api_route("/clients/{client_id}/scopes", methods=["POST"])
    def create_scope(self, request: requests.PreparedRequest, client_id: str) -> RouteResp:
        try:
            scope_body = json.loads(request.body)["scope"]
            scope_suffix = scope_body.get("scope_suffix")
            del scope_body["scope_suffix"]
            scope_body["scope_string"] = f"https://auth.globus.org/scopes/{client_id}/{scope_suffix}"
            scope_body["client"] = client_id

            scope = Scope(**scope_body)
        except TypeError as e:
            return 400, {}, "Invalid request body"
        self._scopes[scope.id] = scope
        self._scopes_by_string[scope.scope_string] = scope
        return 201, {}, self._scope_manager.serialize(scope)

    @api_route("/scopes", methods=["GET"])
    def list_scopes(self, request: requests.PreparedRequest):
        query_params = parse_qs(urlparse(request.url).query)

        filter_ids = query_params.get("ids", [])
        filter_strings = query_params.get("scope_strings", [])

        scopes = self._scopes.values()
        if filter_ids or filter_strings:
            scopes = [
                scope for scope in scopes
                if scope.id in filter_ids or scope.scope_string in filter_strings
            ]

        resp = [self._scope_manager.to_dict(scope) for scope in scopes]
        return 200, {}, json.dumps({"scopes": resp})

    @api_route("/scopes/{scope_id}", methods=["GET"])
    def get_scope(self, scope_id: str) -> RouteResp:
        scope = self._scopes.get(scope_id)
        if not scope:
            return 404, {}, "Scope not found"
        return 200, {}, self._scope_manager.serialize(scope)

    @api_route("/scopes/{scope_id}", methods=["PUT"])
    def update_scope(self, request: requests.PreparedRequest, scope_id: str) -> RouteResp:
        scope = self._scopes.get(scope_id)
        if not scope:
            return 404, {}, "Scope not found"
        try:
            scope = self._scope_manager.update(request, scope)
        except TypeError:
            return 400, {}, "Invalid request body"
        self._scopes[scope.id] = scope
        self._scopes_by_string[scope.scope_string] = scope
        return 200, {}, self._scope_manager.serialize(scope)

    @api_route("/scopes/{scope_id}", methods=["DELETE"])
    def delete_scope(self, scope_id: str) -> RouteResp:
        scope = self._scopes.get(scope_id)
        if scope_id in self._scopes:
            del self._scopes[scope_id]
            del self._scopes_by_string[scope.scope_string]

        resp = self._scope_manager.serialize(scope) if scope else ""
        return 200, {}, resp
