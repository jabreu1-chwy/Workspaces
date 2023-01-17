import boto3
import csv
import time

regions = ["us-east-1", "us-west-2"]

# To use a CSV list, un-comment the below
# ws_list = []
# with open(
#     "/Users/jabreu1/Library/CloudStorage/OneDrive-Chewy.com,LLC/Documents/Workspaces/describe_workspaces.csv",
#     newline="",
#     encoding="utf-8-sig",
# ) as inputfile:
#     for row in csv.reader(inputfile):
#         ws_list.append(row[0])


def paginate(method, **kwargs):
    client = method.__self__
    paginator = client.get_paginator(method.__name__)
    for page in paginator.paginate(**kwargs).result_key_iters():
        for result in page:
            yield result


for region in regions:
    workspaces = boto3.client("workspaces", region_name=region)
    # for entry in ws_list:
    for workspace in paginate(
            workspaces.describe_workspaces):

        print(
            f"{workspace['WorkspaceId']} | {workspace['UserName']} | {workspace['State']} | {workspace['WorkspaceProperties']['RunningMode']} | {workspace['WorkspaceProperties']['ComputeTypeName']} | {region} ")
        time.sleep(1)
