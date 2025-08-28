import pytest
import boto3
from moto import mock_aws
from botocore.exceptions import ClientError
from app import db_utils

TABLE_NAME = "Users"


@pytest.fixture
def dynamodb_table():
    """Creates an in-memory DynamoDB table using moto's new mock_aws."""
    with mock_aws():
        # Create DynamoDB resource
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")

        # Create table schema
        table = dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {"AttributeName": "name", "KeyType": "HASH"},  # Partition key
            ],
            AttributeDefinitions=[
                {"AttributeName": "name", "AttributeType": "S"},
            ],
            BillingMode="PAY_PER_REQUEST",
        )

        # Wait until table exists
        table.meta.client.get_waiter("table_exists").wait(TableName=TABLE_NAME)

        # Inject moto's table into db_utils so code under test uses it
        db_utils.table = table

        yield table


def test_save_user_success(dynamodb_table):
    db_utils.save_user("John", "john@example.com", "http://avatar")
    result = dynamodb_table.scan()
    assert len(result["Items"]) == 1
    assert result["Items"][0]["name"] == "John"


def test_save_user_failure(dynamodb_table):
    # Simulate AWS error by deleting the table before calling save_user
    dynamodb_table.delete()
    with pytest.raises(ClientError):
        db_utils.save_user("error", "err@example.com", "http://avatar")


def test_get_all_users(dynamodb_table):
    dynamodb_table.put_item(Item={"name": "Jane", "email": "jane@example.com"})
    users = db_utils.get_all_users()
    assert users == [{"name": "Jane", "email": "jane@example.com"}]
