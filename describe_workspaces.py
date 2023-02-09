import boto3
import csv
import time
import datetime
import os

regions = ["us-east-1", "us-west-2"]
date_string = datetime.datetime.now().strftime("%Y-%m-%d")
file_name = f"AWS_Cleanup_{date_string}.csv"

directory = input("Enter the directory where you want to save the file: ")


def paginate(method, **kwargs):
    client = method.__self__
    paginator = client.get_paginator(method.__name__)
    for page in paginator.paginate(**kwargs).result_key_iters():
        for result in page:
            yield result


# Opens the CSV
with open(os.path.join(directory, file_name), 'w', newline='') as file:
    writer = csv.writer(file)

    writer.writerow(["WorkspaceId", "UserName", "Region"])

    for region in regions:
        workspaces = boto3.client("workspaces", region_name=region)
        for workspace in paginate(workspaces.describe_workspaces):
            # Write the workspace data as a row in the CSV file
            writer.writerow([workspace['WorkspaceId'],
                            workspace['UserName'], region])
