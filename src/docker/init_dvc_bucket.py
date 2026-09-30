import os
import time
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError, EndpointConnectionError

bucket = os.environ["DVC_BUCKET"]
s3 = boto3.client(
    "s3",
    endpoint_url="http://minio:9000",
    aws_access_key_id=os.environ["MINIO_ROOT_USER"],
    aws_secret_access_key=os.environ["MINIO_ROOT_PASSWORD"],
    region_name="us-east-1",
    config=Config(s3={"addressing_style": "path"}),
)

# waiting for MinIO
for _ in range(30):
    try:
        s3.list_buckets()
        break
    except (EndpointConnectionError, ClientError):
        time.sleep(2)
else:
    raise SystemExit("MinIO nem érhető el")

# Ignore existing bucket
try:
    s3.create_bucket(Bucket=bucket)
except ClientError as e:
    if e.response["Error"]["Code"] not in ("BucketAlreadyOwnedByYou", "BucketAlreadyExists"):
        raise

# dvc anonymous policy set none
try:
    s3.delete_bucket_policy(Bucket=bucket)
except ClientError as e:
    if e.response["Error"]["Code"] != "NoSuchBucketPolicy":
        raise

print(f"Bucket is ready: {bucket}\n")
