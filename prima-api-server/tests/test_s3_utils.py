import io
import uuid
import pytest
import boto3
from moto import mock_aws
from botocore.exceptions import ClientError
from app import s3_utils

BUCKET_NAME = "test-bucket"


@pytest.fixture
def s3_bucket():
    """Creates an in-memory S3 bucket using moto's new mock_aws."""
    with mock_aws():
        # Create S3 client & bucket
        s3_client = boto3.client("s3", region_name="us-east-1")
        s3_client.create_bucket(Bucket=BUCKET_NAME)

        # Inject moto's S3 client into s3_utils so code under test uses it
        s3_utils.s3 = s3_client
        s3_utils.BUCKET_NAME = BUCKET_NAME

        yield s3_client


def test_upload_avatar_success(s3_bucket, monkeypatch):
    # Make UUID deterministic for predictable file naming
    monkeypatch.setattr(uuid, "uuid4", lambda: "fixed-uuid")

    class FileObj:
        filename = "avatar.png"
        file = io.BytesIO(b"image-bytes")

    url = s3_utils.upload_avatar(FileObj())

    # Check the uploaded file exists in moto S3
    key = "fixed-uuid-avatar.png"
    contents = s3_bucket.list_objects_v2(Bucket=BUCKET_NAME).get("Contents", [])
    assert key in [obj["Key"] for obj in contents]

    # Verify file contents
    resp = s3_bucket.get_object(Bucket=BUCKET_NAME, Key=key)
    assert resp["Body"].read() == b"image-bytes"
    assert key in url


def test_upload_avatar_failure(s3_bucket):
    # Change to a non-existent bucket to trigger ClientError
    s3_utils.BUCKET_NAME = "fail-bucket"

    class FileObj:
        filename = "avatar.png"
        file = io.BytesIO(b"image-bytes")

    with pytest.raises(ClientError):
        s3_utils.upload_avatar(FileObj())
