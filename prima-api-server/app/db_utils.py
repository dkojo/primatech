import boto3
from botocore.exceptions import ClientError

dynamo = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamo.Table('users')

def save_user(name, email, avatar_url):
    try:
        table.put_item(Item={"name": name, "email": email, "avatar_url": avatar_url})
    except ClientError as e:
        print("DynamoDB PutItem error:", e)
        raise

def get_all_users():
    try:
        response = table.scan()
        return response.get("Items", [])
    except ClientError as e:
        print("DynamoDB Scan error:", e)
        raise

