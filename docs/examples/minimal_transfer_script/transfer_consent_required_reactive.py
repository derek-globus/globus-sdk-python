import argparse

import globus_sdk

# Tutorial client ID - replace this with your own native client
# Alternatively, run this script with the environment variable:
#   GLOBUS_CLIENT_ID=61338d24-54d5-408f-a10d-66c06b59f6d2
NATIVE_CLIENT_ID = "61338d24-54d5-408f-a10d-66c06b59f6d2"
session = globus_sdk.UserProxySession("my-simple-transfer", client_id=NATIVE_CLIENT_ID)


def main(src, dst):
    # get an initial client to try with, which requires a login flow
    transfer_client = session.get_client(globus_sdk.TransferClient)

    # create a Transfer task consisting of one or more items
    task_data = globus_sdk.TransferData(source_endpoint=src, destination_endpoint=dst)
    task_data.add_item(
        "/share/godata/file1.txt",  # source
        "/~/example-transfer-script-destination.txt",  # dest
    )

    try:
        do_submit(transfer_client, task_data)
    except globus_sdk.TransferAPIError as err:
        # if the error is something other than consent_required, reraise it,
        # exiting the script with an error message
        if not err.info.consent_required:
            raise

        # we now know that the error is a ConsentRequired
        # print an explanatory message and do the login flow again
        print(
            "Encountered a ConsentRequired error.\n"
            "You must login a second time to grant consents.\n\n"
        )

        # Note that this call will initiate a new login flow (prompting for the
        # newly discovered scopes)
        transfer_client = session.get_client(
            globus_sdk.TransferClient,
            additional_auth_requirements=globus_sdk.AuthRequirements(
                scopes=err.info.consent_required.required_scopes
            ),
        )

        # finally, try the submission a second time, this time with no error
        # handling
        do_submit(transfer_client, task_data)


def do_submit(client, task_data):
    """
    define the submission step -- we will use it twice below
    """
    task_doc = client.submit_transfer(task_data)
    task_id = task_doc["task_id"]
    print(f"submitted transfer, task_id={task_id}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("SRC")
    parser.add_argument("DST")
    args = parser.parse_args()
    main(args.SRC, args.DST)
