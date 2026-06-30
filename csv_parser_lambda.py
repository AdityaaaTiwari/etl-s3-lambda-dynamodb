def lambda_handler(event, context):

    print("CSV Parser Lambda Triggered")

    print(event)

    return {
        "statusCode": 200,
        "body": "CSV File Processed Successfully"
    }