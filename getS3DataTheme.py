import json
import boto3
import csv
from datetime import datetime, timezone

def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    bucket_name = 'data-morocco'

    # Extracting theme and dataset names from the event
    theme = event['queryStringParameters']['theme']
    objects = s3_client.list_objects_v2(
            Bucket=bucket_name, 
            Prefix=f"csv_data/{theme}/" 
        )
        
    try:
        datasets = []
    
        for obj in objects['Contents']:
            key = obj['Key']
            last_modified = obj['LastModified'].astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
            size = obj['Size']
            dataset = key.split('/')[-1].split('.')[0]
    
            dataset_meta = {
                "Name": dataset,
                "LastModified": last_modified,
                "Size": size
            }
    
            datasets.append(dataset_meta)
    
        return {
          "statusCode": 200,
          "body": json.dumps(datasets)   
        }

    except s3_client.exceptions.NoSuchKey:
        return {
            'statusCode': 404,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps('File not found')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(str(e))
        }
