import json
from lambda_function import lambda_handler

# Sample event mimicking API Gateway query parameters
event = {
    "queryStringParameters": {
        "thematic_subfolder": "Agriculture",
        "file_name": "cheptel-2010-2021.csv",
    }
}

# Mimic Lambda context (can be an empty object for this test)
context = {}

# Invoke the Lambda function
response = lambda_handler(event, context)
print(json.dumps(response, indent=4))
