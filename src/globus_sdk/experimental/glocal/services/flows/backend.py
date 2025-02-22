from __future__ import annotations

import dataclasses
import json

import typing as t


from globus_sdk.experimental.glocal.core import BaseBackend, http_route
from .data import Flow

if t.TYPE_CHECKING:
    from requests import PreparedRequest
    from globus_sdk.experimental.glocal.core import RouteResp


class FlowsBackend(BaseBackend):

    service_name = "flows"
    base_url = "https://flows.automate.globus.org/"

    def __init__(self):
        super().__init__()
        self._flows: dict[str, Flow] = {}

    @http_route("/flows", methods=["POST"])
    def create_flow(self, request: PreparedRequest) -> RouteResp:
        request_json = json.loads(request.body)
        flow = Flow(
            title=request_json["title"],
            definition=request_json["definition"],
            input_schema=request_json["input_schema"],
            subtitle=request_json.get("subtitle"),
            description=request_json.get("description"),
        )
        self._flows[flow.id] = flow

        response = dataclasses.asdict(flow)
        return 201, {}, json.dumps(response)


    @http_route("/flows", methods=["GET"])
    def list_flows(self) -> RouteResp:
        flows = [dataclasses.asdict(flow) for flow in self._flows.values()]
        return 200, {}, json.dumps({"flows": flows})


    @http_route("/flows/{flow_id}", methods=["GET"])
    def get_flow(self, flow_id: str) -> RouteResp:
        flow = self._flows.get(flow_id)
        if not flow:
            return 404, {}, json.dumps({"error": "Flow not found"})
        response = dataclasses.asdict(flow)
        return 200, {}, json.dumps(response)


    @http_route("/flows/{flow_id}", methods=["PUT"])
    def update_flow(self, request: PreparedRequest, flow_id: str) -> RouteResp:
        if flow_id not in self._flows:
            return 404, {}, json.dumps({"error": "Flow not found"})

        request_json = json.loads(request.body)
        updated_flow = dataclasses.replace(self._flows[flow_id], **request_json)
        self._flows[flow_id] = updated_flow

        return 200, {}, json.dumps(dataclasses.asdict(updated_flow))


    @http_route("/flows/{flow_id}", methods=["DELETE"])
    def delete_flow(self, flow_id: str) -> RouteResp:
        if flow_id in self._flows:
            del self._flows[flow_id]

        return 204, {}, ""




