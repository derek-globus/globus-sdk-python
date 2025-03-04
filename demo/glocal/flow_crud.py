import json

import globus_sdk

from globus_sdk.experimental.glocal import mock_globus


@mock_globus()
def test_flows():
    flows = globus_sdk.FlowsClient(transport_params={"max_retries": 0})

    print("Creating Flow...")
    flow_id = create_flow(flows)
    flow_id_trunc = flow_id[:6]
    print(f"Created '{flow_id_trunc}' 👍.\n")

    print(f"Updating flow '{flow_id_trunc}'...")
    update_flow(flows, flow_id)
    print(f"Updated '{flow_id_trunc}' 👍.\n")

    print(f"Accessing flow '{flow_id_trunc}'...")
    flow = flows.get_flow(flow_id)
    assert flow["title"] == "Do Something"
    print(f"Got '{flow_id_trunc}' 👍.")
    print(json.dumps(flow._parsed_json, indent=2))
    print()

    print(f"Deleting flow '{flow_id_trunc}'...")
    flows.delete_flow(flow_id)
    print(f"Deleted '{flow_id_trunc}' 🫠.\n")

    try:
        print(f"Accessing flow '{flow_id_trunc}'...")
        flows.get_flow(flow_id)
    except globus_sdk.GlobusAPIError as e:
        assert e.http_status == 404
        print(f"Flow '{flow_id_trunc}' not found 🫠.")


def create_flow(flows: globus_sdk.FlowsClient) -> str:
    flow_resp = flows.create_flow(
        title="Do Nothing",
        definition={
            "StartAt": "nothing",
            "States": {"nothing": {"Type": "Pass", "End": True}}
        },
        input_schema={"type": "null"}
    )
    return flow_resp["id"]


def update_flow(flows: globus_sdk.FlowsClient, flow_id: str):
    flows.update_flow(
        flow_id,
        title="Do Something",
        definition={
            "StartAt": "something",
            "States": {"something": {"Type": "Fail", "End": True}}
        },
        input_schema={"type": "object"}
    )


def delete_flow(flows: globus_sdk.FlowsClient, flow_id: str):
    print(f"Deleting Flow with ID: {flow_id}")
    flows.delete_flow(flow_id)
    print("Flow deleted.")


if __name__ == "__main__":
    test_flows()
