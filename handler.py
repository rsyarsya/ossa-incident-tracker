import json
import logging
import os


def read_incidents(s3, bucket):
    items = []
    pages = s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix="incidents/")
    for page in pages:
        for obj in page.get("Contents", []):
            key = obj["Key"]
            if key.endswith(".json"):
                result = s3.get_object(Bucket=bucket, Key=key)
                with result["Body"] as stream:
                    items.append(json.load(stream))
    return items


def lambda_handler(event, context, *, s3=None):
    status = 404
    payload = {"error": "Route not found"}
    if event.get("rawPath") == "/incidents" and event["requestContext"]["http"]["method"] == "GET":
        try:
            if s3 is None:
                import boto3
                s3 = boto3.client("s3")
            payload = {"items": read_incidents(s3, os.environ["INCIDENT_BUCKET"])}
            status = 200
        except Exception:
            logging.exception("Failed to read incident data")
            status, payload = 500, {"error": "Unable to load incidents"}
    return {"statusCode": status, "headers": {"Content-Type": "application/json"},
            "body": json.dumps(payload)}
