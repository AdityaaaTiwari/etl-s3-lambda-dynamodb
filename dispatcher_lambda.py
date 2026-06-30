import json
import boto3

lambda_client = boto3.client("lambda")

def lambda_handler(event, context):

    record = event["Records"][0]
    key = record["s3"]["object"]["key"]

    if key.endswith(".txt"):
        target = "transit-etl-lambda"
        
    elif key.endswith(".csv"):
        target = "csv-parser-lambda"

    else:
        return {
            "statusCode": 400,
            "body": "Unsupported file type"
        }

    lambda_client.invoke(
        FunctionName=target,
        InvocationType="Event",
        Payload=json.dumps(event)
    )

    return {
        "statusCode": 200,
        "body": f"{target} triggered successfully"
    }