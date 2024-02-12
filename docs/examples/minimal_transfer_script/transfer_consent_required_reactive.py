import argparse

import globus_sdk

# Tutorial client ID - replace this with your own native client
# Alternatively, run this script with the environment variable:
#   GLOBUS_CLIENT_ID=61338d24-54d5-408f-a10d-66c06b59f6d2
NATIVE_CLIENT_ID = "61338d24-54d5-408f-a10d-66c06b59f6d2"
session = globus_sdk.UserProxySession("my-simple-transfer", client_id=NATIVE_CLIENT_ID)


def main(src, dst):
    # get an initial client to try with, which requires a login flow
    transfer_client = globus_sdk.TransferClient(session=session)

    session.run_login_flow()

    # create a Transfer task consisting of one or more items
    task_data = globus_sdk.TransferData(source_endpoint=src, destination_endpoint=dst)
    task_data.add_item(
        "/share/godata/file1.txt",  # source
        "/~/example-transfer-script-destination.txt",  # dest
    )

    task_doc = transfer_client.submit_transfer(task_data)
    task_id = task_doc["task_id"]
    print(f"submitted transfer, task_id={task_id}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("SRC")
    parser.add_argument("DST")
    args = parser.parse_args()
    main(args.SRC, args.DST)
