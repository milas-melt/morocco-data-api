import json
import boto3
import csv


def lambda_handler(event, context):
    s3_client = boto3.client("s3")
    bucket_name = "data-morocco"

    # Extracting theme and dataset names from the event
    theme = event["queryStringParameters"]["theme"]
    dataset = event["queryStringParameters"]["dataset"]
    file_key = f"csv_data/{theme}/{dataset}.csv"

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
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(data),
        }

    except s3_client.exceptions.NoSuchKey:
        return {
            "statusCode": 404,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps("File not found"),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(str(e)),
        }
