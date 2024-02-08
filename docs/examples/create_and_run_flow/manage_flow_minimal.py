#!/usr/bin/env python

import argparse
import sys

import globus_sdk

# Tutorial client ID - replace this with your own native client
# Alternatively, run this script with the environment variable:
#   GLOBUS_CLIENT_ID=61338d24-54d5-408f-a10d-66c06b59f6d2
NATIVE_CLIENT_ID = "61338d24-54d5-408f-a10d-66c06b59f6d2"
session = globus_sdk.GlobusUserSession("my-simple-flow", client_id=NATIVE_CLIENT_ID)


def main(action, flow_id, title):
    try:
        if action == "create":
            if title is None:
                print("[ERROR] create requires --title")
                sys.exit(1)
            create_flow(title)
        elif action == "delete":
            if flow_id is None:
                print("[ERROR] delete requires --flow-id")
                sys.exit(1)
            delete_flow(flow_id)
        elif action == "list":
            list_flows()
        elif action == "run":
            if flow_id is None:
                print("[ERROR] run requires --flow-id")
                sys.exit(1)
            run_flow(flow_id)
        else:
            raise NotImplementedError()
    except globus_sdk.FlowsAPIError as e:
        print(f"API Error: {e.code} {e.message}")
        print(e.text)
        sys.exit(1)


def create_flow(title):
    flows_client = session.get_client(globus_sdk.FlowsClient)
    print(
        flows_client.create_flow(
            title=title,
            definition={
                "StartAt": "DoIt",
                "States": {
                    "DoIt": {
                        "Type": "Action",
                        "ActionUrl": "https://actions.globus.org/hello_world",
                        "Parameters": {
                            "echo_string": "Hello, Asynchronous World!",
                        },
                        "End": True,
                    }
                },
            },
            input_schema={},
            subtitle="A flow created by the SDK tutorial",
        )
    )


def delete_flow(flow_id):
    flows_client = session.get_client(globus_sdk.FlowsClient)
    print(flows_client.delete_flow(flow_id))


def list_flows():
    flows_client = session.get_client(globus_sdk.FlowsClient)
    for flow in flows_client.list_flows(filter_role="flow_owner"):
        print(f"title: {flow['title']}")
        print(f"id: {flow['id']}")
        print()


def run_flow(flow_id):
    flows_client = session.get_client(globus_sdk.SpecificFlowClient, flow_id)
    flows_client.run_flow({})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["create", "delete", "list", "run"])
    parser.add_argument("-f", "--flow-id", help="Flow ID for delete")
    parser.add_argument("-t", "--title", help="Name for create")
    args = parser.parse_args()
    main(args.action, args.flow_id, args.title)
