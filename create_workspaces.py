import boto3
import csv
from botocore.exceptions import ClientError
import time

client = boto3.client("workspaces", region_name="us-east-1")

with open(
    "/Users/jabreu1/Library/CloudStorage/OneDrive-Chewy.com,LLC/Documents/workspaces/create_workspaces.csv",
    "r",
) as f_input:
    csv_input = csv.DictReader(f_input)
    username = []

    for row in csv_input:
        username.append(row["username"])

created_workspaces = []
for user in username:
    try:
        response = client.create_workspaces(
            Workspaces=[
                {
                    "DirectoryId": "d-90677397c8",  # change as needed
                    "UserName": str(user),
                    "BundleId": "wsb-83j5dqqlr",  # change as needed
                    "VolumeEncryptionKey": "alias/aws/workspaces",
                    "UserVolumeEncryptionEnabled": True,
                    "RootVolumeEncryptionEnabled": True,
                    "WorkspaceProperties": {
                        "RunningMode": "AUTO_STOP",  # 'ALWAYS_ON' or 'AUTO_STOP'
                        "RunningModeAutoStopTimeoutInMinutes": 60,  # remove if 'ALWAYS_ON' is selected
                    },
                    "Tags": [
                        {"Key": "NAME", "Value": "Testing"},
                    ],
                },
            ]
        )
        if not len(response["FailedRequests"]) == 0:
            created_workspaces += 1
        else:
            print(
                f"Failed to create Workspace for: {user}")
            time.sleep(2)
    except ClientError as e:
        print(f"Create Error for {user}: {e}")
    except Exception as e:
        print(f"Another error for {user}| Error: {e}")
        print(response)

print(f"Sucessfully created {created_workspaces} Workspaces")

