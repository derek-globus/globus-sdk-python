import pytest

import globus_sdk

from globus_sdk.experimental.glocal import mock_globus


@pytest.fixture(autouse=True)
def setup():
    with mock_globus():
        yield

def test_flow_crud():
    flow_def_a = {
        "StartAt": "nothing",
        "States": {"nothing": {"Type": "Pass", "End": True}}
    }
    flow_def_b = {
        "StartAt": "something",
        "States": {"something": {"Type": "Fail", "End": True}}
    }

    flows = globus_sdk.FlowsClient()
    flow = flows.create_flow("Do Nothing", flow_def_a, {})
    flow_id = flow["id"]
    assert flows.get_flow(flow_id)["definition"] == flow_def_a

    flows.update_flow(flow_id, definition=flow_def_b)
    assert flows.get_flow(flow_id)["definition"] == flow_def_b

    flows.delete_flow(flow_id)

    with pytest.raises(globus_sdk.GlobusAPIError, match="404"):
        flows.get_flow(flow_id)
