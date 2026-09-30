import os
import time
import boto3
from typing import Any
from botocore.client import Config
from botocore.exceptions import ClientError, EndpointConnectionError


class MinIO:
    def access_to_s3(self) -> Any:
        s3: Any = boto3.client(
            "s3",
            endpoint_url="http://minio:9000",
            aws_access_key_id=os.environ["MINIO_ROOT_USER"],
            aws_secret_access_key=os.environ["MINIO_ROOT_PASSWORD"],
            region_name="us-east-1",
            config=Config(s3={"addressing_style": "path"}),
        )
        return s3

    def waiting_for_minio(self, s3: Any):
        for _ in range(30):
            try:
                s3.list_buckets()
                break
            except (EndpointConnectionError, ClientError):
                time.sleep(2)
        else:
            raise SystemExit("Cannot access the MinIO")

    def create_s3_bucket(self, s3: Any, bucket: Any):
        "Ignore existing bucket"
        try:
            s3.create_bucket(Bucket=bucket)
        except ClientError as e:
            if e.response["Error"]["Code"] not in (
               "BucketAlreadyOwnedByYou", "BucketAlreadyExists"):
                raise

    def set_anon_policy(self, s3: Any, bucket: Any):
        try:
            s3.delete_bucket_policy(Bucket=bucket)
        except ClientError as e:
            if e.response["Error"]["Code"] != "NoSuchBucketPolicy":
                raise


def main():
    dvc_bucket: str = os.environ["DVC_BUCKET"]
    mlflow_bucket: str = os.environ["MLFLOW_BUCKET"]
    buckets: list[str] = [dvc_bucket, mlflow_bucket]
    minio = MinIO()
    s3_access = minio.access_to_s3()
    minio.waiting_for_minio(s3_access)

    for bucket in buckets:
        minio.create_s3_bucket(s3_access, bucket)
        minio.set_anon_policy(s3_access, bucket)
        print(f"Bucket is ready: {bucket}")

    print(f"Buckets are ready: {buckets}")


if __name__ == "__main__":
    main()
