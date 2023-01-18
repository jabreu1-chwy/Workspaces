import boto3
import datetime
from botocore.exceptions import ClientError
import csv
import time

workspace_ids = []
regions = ["us-east-1", "us-west-2"]

# open csv and add workspace_id to list
with open(
    "/Users/jabreu1/Library/CloudStorage/OneDrive-Chewy.com,LLC/Documents/Workspaces/connection_status.csv",
    newline="",
    encoding="utf-8-sig",
) as inputfile:
    for row in csv.reader(inputfile):
        workspace_ids.append(row[0])


def paginate(method, **kwargs):
    client = method.__self__
    paginator = client.get_paginator(method.__name__)
    for page in paginator.paginate(**kwargs).result_key_iters():
        for result in page:
            yield result


processed_ws = []
terminated_list = []

for region in regions:
    client = boto3.client("workspaces", region_name=region)
    for id in workspace_ids:
        try:
            if id not in processed_ws:
                response = client.describe_workspaces_connection_status(
                    WorkspaceIds=[id]
                )
                # processed_ws.append(id)
                # print(json.dumps(response, default=str, indent=4))

                if len(response["WorkspacesConnectionStatus"]):
                    processed_ws.append(id)
                    if (
                        "LastKnownUserConnectionTimestamp"
                        in response["WorkspacesConnectionStatus"][0]
                    ):
                        last_known_connection_timestamp = str(
                            response["WorkspacesConnectionStatus"][0][
                                "LastKnownUserConnectionTimestamp"
                            ]
                        )

                        last_known_connection_datetime = datetime.datetime.strptime(
                            last_known_connection_timestamp, "%Y-%m-%d %H:%M:%S.%f%z"
                        )

                        current_date = datetime.datetime.now(
                            datetime.timezone.utc)

                        time_difference = current_date - last_known_connection_datetime

                        # check if time difference is greater than 30 days
                        if time_difference > datetime.timedelta(days=30):
                            print(
                                f"{id} | Last known connection is older than 30 days | {region}"
                            )
                            terminated_list.append(id)
                        else:
                            print(
                                f"{id} | Last known connection is not older than 30 days | {region}"
                            )
                            time.sleep(1)
                    else:
                        print(f"{id} | No login registered | {region}")
                        terminated_list.append(id)
                else:
                    print(f"{id} | Does not exist | {region}")
                    time.sleep(1)
        except ClientError as e:
            print(f"Client error: {e}")
        except Exception as e:
            print(f"Other error: {e}")
print(terminated_list)


# import boto3
# import datetime
# from botocore.exceptions import ClientError
# import csv
# import json
# import time

# workspace_ids = []
# regions = ["us-east-1", "us-west-2"]

# # open csv and add workspace_id to list
# with open(
#     "/Users/jabreu1/Library/CloudStorage/OneDrive-Chewy.com,LLC/Documents/Workspaces/connection_status.csv",
#     newline="",
#     encoding="utf-8-sig",
# ) as inputfile:
#     for row in csv.reader(inputfile):
#         workspace_ids.append(row[0])


# def paginate(method, **kwargs):
#     client = method.__self__
#     paginator = client.get_paginator(method.__name__)
#     for page in paginator.paginate(**kwargs).result_key_iters():
#         for result in page:
#             yield result


# processed_ws = []
# terminated_list = []

# for region in regions:
#     client = boto3.client("workspaces", region_name=region)
#     for id in workspace_ids:
#         try:
#             if id not in processed_ws:
#                 response = client.describe_workspaces_connection_status(
#                     WorkspaceIds=[id]
#                 )
#                 # processed_ws.append(id)
#                 # print(json.dumps(response, default=str, indent=4))

#                 if len(response["WorkspacesConnectionStatus"]):
#                     processed_ws.append(id)
#                     if (
#                         "LastKnownUserConnectionTimestamp"
#                         in response["WorkspacesConnectionStatus"][0]
#                     ):
#                         last_known_connection_timestamp = str(
#                             response["WorkspacesConnectionStatus"][0][
#                                 "LastKnownUserConnectionTimestamp"
#                             ]
#                         )

#                         last_known_connection_datetime = datetime.datetime.strptime(
#                             last_known_connection_timestamp, "%Y-%m-%d %H:%M:%S.%f%z"
#                         )

#                         current_date = datetime.datetime.now(datetime.timezone.utc)

#                         time_difference = current_date - last_known_connection_datetime

#                         # check if time difference is greater than 30 days
#                         if time_difference > datetime.timedelta(days=30):
#                             print(
#                                 f"{id} | Last known connection is older than 30 days | {region}"
#                             )
#                             terminated_list.append(id)
#                         else:
#                             print(
#                                 f"{id} | Last known connection is not older than 30 days | {region}"
#                             )
#                             time.sleep(1)
#                     else:
#                         print(f"{id} | No login registered | {region}")
#                         terminated_list.append(id)
#                 else:
#                     print(f"{id} | Does not exist | {region}")
#                     time.sleep(1)
#         except ClientError as e:
#             print(f"Client error: {e}")
#         except Exception as e:
#             print(f"Other error: {e}")
# print(terminated_list)
