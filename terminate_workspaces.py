import boto3
import time
import csv
from botocore.exceptions import ClientError


regions = ["us-east-1", "us-west-2"]

term_list = []
with open(
    "/Users/jabreu1/Library/CloudStorage/OneDrive-Chewy.com,LLC/Documents/Workspaces/terminate_workspaces.csv",
    newline="",
    encoding="utf-8-sig",
) as inputfile:
    for row in csv.reader(inputfile):
        term_list.append(row[0])

termed_count = 0
for region in regions:
    workspaces = boto3.client("workspaces", region_name=region)
    for entry in term_list:
        try:
            response = workspaces.terminate_workspaces(
                TerminateWorkspaceRequests=[
                    {"WorkspaceId": str(entry)},
                ]
            )
            if not len(response["FailedRequests"]) == 0:
                print(
                    f"Failed to terminate WorkspaceId: {response['FailedRequests']['WorkspaceId']} | {response['FailedRequests']['ErrorMessage']} {region}")
                time.sleep(2)
            else:
                print(f"Successfully terminated WorkspaceId: {entry}")
                termed_count += 1
        except ClientError as e:
            print(
                f"Term Error for WorkspaceId: {entry} in region {region}: | Error: {e}")
        except Exception as e:
            print(f"Another error with {entry} in region {region}| Error: {e}")

print(f"Sucessfully terminated {termed_count} Workspaces")

