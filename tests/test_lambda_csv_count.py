import pytest
from unittest.mock import patch
from botocore.exceptions import ClientError
from src.lambda_csv_count import _read_object, _put_to_dynamodb, lambda_handler
from botocore.exceptions import ClientError
from src.lambda_csv_count import COUNTING_TABLE

@patch("src.lambda_csv_count.s3_client")
def test_read_object(s3_client_mock):
    event = {
    "Records": [
            {
            "eventVersion": "2.0",
            "eventSource": "aws:s3",
            "awsRegion": "us-west-2",
            "eventTime": "1970-01-01T00:00:00.000Z",
            "eventName": "ObjectCreated:Put",
            "userIdentity": {
                "principalId": "EXAMPLE"
            },
            "requestParameters": {
                "sourceIPAddress": "127.0.0.1"
            },
            "responseElements": {
                "x-amz-request-id": "EXAMPLE123456789",
                "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH"
            },
            "s3": {
                "s3SchemaVersion": "1.0",
                "configurationId": "testConfigRule",
                "bucket": {
                "name": "my-s3-bucket",
                "ownerIdentity": {
                    "principalId": "EXAMPLE"
                },
                "arn": "arn:aws:s3:::example-bucket"
                },
                "object": {
                "key": "record.csv",
                "size": 1024,
                "eTag": "0123456789abcdef0123456789abcdef",
                "sequencer": "0A1B2C3D4E5F678901"
                }
            }
            }
        ]
    }
    _read_object(event)
    s3_client_mock.get_object.assert_called_once_with(
        Bucket = "my-s3-bucket",
        Key = "record.csv"
    )

@patch("src.lambda_csv_count.dynamodb_client")
def test_put_to_dynamodb(dynamodb_client_mock):
    row_count = 3
    _put_to_dynamodb(row_count)
    dynamodb_client_mock.put_item.assert_called_once_with(
        TableName = COUNTING_TABLE,
        Item = {
            'row' : {
                'N' : str(row_count)
            }
        }
    )

@patch("src.lambda_csv_count._read_object")
@patch("src.lambda_csv_count._put_to_dynamodb")
def test_lambda_handler(_put_to_dynamodb_mock, _read_object_mock, ):
    _read_object_mock.return_value = 3
    lambda_handler({},{})
    _put_to_dynamodb_mock.assert_called_once_with(3)

@patch("src.lambda_csv_count._read_object")
@patch("src.lambda_csv_count._put_to_dynamodb")
def test_lambda_handler_failed(_put_to_dynamodb_mock, _read_object_mock, ):
    
    _read_object_mock.side_effect = ClientError(
        error_response= {'Error': {'Code' : 'Client Error', 'Message' : 'Client Get Object Failed'}},
        operation_name= 'GetObject'
    )
    _put_to_dynamodb_mock.side_effect = ClientError(
        error_response= {'Error': {'Code' : 'Client Error', 'Message' : 'Client Put Item Failed'}},
        operation_name= 'PutItem'
    )
    lambda_handler({},{})