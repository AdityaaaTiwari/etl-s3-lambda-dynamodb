import json
import boto3
import csv
import io
from datetime import datetime

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

TABLE_NAME = "clean_records"


def lambda_handler(event, context):

    table = dynamodb.Table(TABLE_NAME)

    total_records = 0
    inserted_records = 0
    rejected_records = 0

    try:
        bucket = event["Records"][0]["s3"]["bucket"]["name"]
        key = event["Records"][0]["s3"]["object"]["key"]

        response = s3.get_object(Bucket=bucket, Key=key)
        content = response["Body"].read().decode("utf-8")

        csv_reader = csv.DictReader(io.StringIO(content))

        with table.batch_writer() as batch:

            for row in csv_reader:

                total_records += 1

                stop_id = row.get("stop_id", "").strip()
                stop_name = row.get("stop_name", "").strip().title()
                stop_code = row.get("stop_code", "").strip()
                stop_lat = row.get("stop_lat", "").strip()
                stop_lon = row.get("stop_lon", "").strip()

                if not stop_id or not stop_name:
                    rejected_records += 1
                    continue

                batch.put_item(
                    Item={
                        "record_id": stop_id,
                        "stop_code": stop_code,
                        "stop_name": stop_name,
                        "stop_lat": stop_lat,
                        "stop_lon": stop_lon,
                        "processed_at": datetime.utcnow().isoformat()
                    }
                )

                inserted_records += 1

        print("========== ETL SUMMARY ==========")
        print(f"Total Records : {total_records}")
        print(f"Inserted      : {inserted_records}")
        print(f"Rejected      : {rejected_records}")
        print("=================================")

        return {
            "statusCode": 200,
            "body": json.dumps("ETL completed successfully")
        }

    except Exception as e:
        print("ERROR:", str(e))

        return {
            "statusCode": 500,
            "body": json.dumps(str(e))
        }