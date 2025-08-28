import boto3
import uuid
from botocore.exceptions import ClientError

s3 = boto3.client('s3', region_name='us-east-1')
BUCKET_NAME = 'prima-tech-challenge-robert-2025'

def upload_avatar(file):
    file_key = f"{uuid.uuid4()}-{file.filename}"
    print(f"📤 Attempting to upload '{file.filename}' as '{file_key}' to bucket '{BUCKET_NAME}'")

    try:
        s3.upload_fileobj(
            file.file,
            BUCKET_NAME,
            file_key
        )
        print("Upload successful")
        return f"https://{BUCKET_NAME}.s3.amazonaws.com/{file_key}"

    except ClientError as e:
        error_message = e.response["Error"]
        print("S3 Upload Failed:", error_message)
        raise

    except Exception as e:
        print("Unexpected upload error:", str(e))
        raise

