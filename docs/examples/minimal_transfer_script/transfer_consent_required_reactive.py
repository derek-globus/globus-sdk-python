import argparse

import globus_sdk
from globus_sdk.scopes import TransferScopes

# Tutorial client ID - replace this with your own native client
CLIENT_ID = "61338d24-54d5-408f-a10d-66c06b59f6d2"
auth_client = globus_sdk.NativeAppAuthClient(CLIENT_ID)


def main(src, dst):
    # Get an initial client to try with. This requires a login flow.
    transfer_client = login_and_get_transfer_client()

    # Create a transfer task consisting of one or more items.
    task_data = globus_sdk.TransferData(source_endpoint=src, destination_endpoint=dst)
    task_data.add_item(
        "/share/godata/file1.txt",  # source
        "/~/example-transfer-script-destination.txt",  # dest
    )

    try:
        do_submit(transfer_client, task_data)
    except globus_sdk.TransferAPIError as err:
        # If the error is something other than consent_required, reraise it,
        # exiting the script with an error message
        if not err.info.consent_required:
            raise

        # We now know that the error is a ConsentRequired
        # Print an explanatory message and do the login flow again
        print(
            "Encountered a ConsentRequired error.\n"
            "You must login a second time to grant consents.\n\n"
        )
        transfer_client = login_and_get_transfer_client(
            scopes=err.info.consent_required.required_scopes
        )

        # Finally, try the submission a second time, this time with no error handling
        do_submit(transfer_client, task_data)


def login_and_get_transfer_client(*, scopes=TransferScopes.all):
    """
    we will need to do the login flow potentially twice, so define it as a
    function

    we default to using the Transfer "all" scope, but it is settable here
    look at the ConsentRequired handler below for how this is used
    """
    auth_client.oauth2_start_flow(requested_scopes=scopes)
    authorize_url = auth_client.oauth2_get_authorize_url()
    print(f"Please go to this URL and login:\n\n{authorize_url}\n")

    auth_code = input("Please enter the code here: ").strip()
    tokens = auth_client.oauth2_exchange_code_for_tokens(auth_code)
    transfer_tokens = tokens.by_resource_server["transfer.api.globus.org"]

    # return the TransferClient object, as the result of doing a login
    return globus_sdk.TransferClient(
        authorizer=globus_sdk.AccessTokenAuthorizer(transfer_tokens["access_token"])
    )


def do_submit(client, task_data):
    """Submit a transfer request (defined as a distinct function for reuse)."""
    task_doc = client.submit_transfer(task_data)
    task_id = task_doc["task_id"]
    print(f"submitted transfer, task_id={task_id}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("SRC")
    parser.add_argument("DST")
    args = parser.parse_args()
    main(args.SRC, args.DST)
