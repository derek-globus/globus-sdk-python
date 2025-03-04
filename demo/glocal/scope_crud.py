import json

import globus_sdk

from globus_sdk.experimental.glocal import mock_globus


@mock_globus()
def test_scopes():
    auth = globus_sdk.AuthClient(transport_params={"max_retries": 0})
    client_id = "00000000-0000-0000-0000-000000000000"

    print("Creating scope...")
    scope_id = auth.create_scope(
        client_id,
        "My Cool Scope",
        "This is a scope for my cool client",
        "my_cool_scope",
    )["id"]
    scope_id_trunc = scope_id[:6]
    print(f"Created '{scope_id_trunc}' 👍.\n")

    print(f"Accessing scope '{scope_id_trunc}'...")
    scope = auth.get_scope(scope_id)
    assert scope["name"] == "My Cool Scope"
    print(f"Got '{scope_id_trunc}' 👍.")
    print(json.dumps(scope._parsed_json, indent=2))
    print()

    print(f"Deleting scope '{scope_id}'...")
    auth.delete_scope(scope_id)
    print(f"Deleted '{scope_id_trunc}' 🫠.\n")

    try:
        print(f"Accessing scope '{scope_id_trunc}'...")
        auth.get_scope(scope_id)
    except globus_sdk.GlobusAPIError as e:
        assert e.http_status == 404
        print(f"Scope '{scope_id_trunc}' not found 🫠.")


if __name__ == "__main__":
    test_scopes()
