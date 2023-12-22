import json
import boto3
import csv

# Initialize S3 client
s3_client = boto3.client("s3")


def lambda_handler(event, context):
    # # Extract parameters from event object
    # query_params = event.get("queryStringParameters", {})
    # thematic_subfolder = query_params.get("thematic_subfolder")
    # file_name = query_params.get("file_name")

    # Extract path parameters from event object
    path_params = event.get("pathParameters", {})
    thematic_subfolder = path_params.get("themeName")
    file_name = path_params.get("datasetName")

    # Validate parameters
    if not thematic_subfolder or not file_name:
        return {
            "statusCode": 400,
            "body": json.dumps("Missing thematic_subfolder or file_name"),
        }

    # Define the bucket name and object key
    bucket_name = "data-morocco"
    file_key = f"csv_data/{thematic_subfolder}/{file_name}"

    try:
        # Get the object from S3
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        content = response["Body"].read().decode("utf-8")

        # Read the CSV file
        lines = content.split("\n")
        reader = csv.reader(lines)

        # Convert CSV to list
        data = list(reader)

        # Return data as JSON
        return {"statusCode": 200, "body": json.dumps(data)}

    except s3_client.exceptions.NoSuchKey:
        return {"statusCode": 404, "body": json.dumps("File not found")}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps(str(e))}
