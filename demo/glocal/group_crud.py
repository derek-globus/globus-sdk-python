import json

import globus_sdk

from globus_sdk.experimental.glocal import mock_globus


@mock_globus()
def test_groups():
    groups = globus_sdk.GroupsClient(transport_params={"max_retries": 0})

    print("Creating group...")
    group_id = groups.create_group({"name": "My Cool Group"})["id"]
    group_id_trunc = group_id[:6]
    print(f"Created '{group_id_trunc}' 👍.\n")

    print(f"Accessing group '{group_id_trunc}'...")
    group = groups.get_group(group_id)
    assert group["name"] == "My Cool Group"
    print(f"Got '{group_id_trunc}' 👍.")
    print(json.dumps(group._parsed_json, indent=2))
    print()

    print(f"Deleting group '{group_id_trunc}'...")
    groups.delete_group(group_id)
    print(f"Deleted '{group_id_trunc}' 🫠.\n")

    try:
        print(f"Accessing group '{group_id_trunc}'...")
        groups.get_group(group_id)
    except globus_sdk.GlobusAPIError as e:
        assert e.http_status == 404
        print(f"Group '{group_id_trunc}' not found 🫠.")


if __name__ == "__main__":
    test_groups()
