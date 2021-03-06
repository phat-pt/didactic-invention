import logging
import boto3
from botocore.exceptions import ClientError

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

dynamodb_client = boto3.client('dynamodb',endpoint_url="http://host.docker.internal:4566",\
     region_name = "ap-southeast-1")
s3_client= boto3.client('s3',endpoint_url="http://host.docker.internal:4566",\
     region_name = "ap-southeast-1")

COUNTING_TABLE = 'csv_count_table'


def _read_object(event):
    bucket = event['Records'][0]['s3']['bucket']['name']
    csv_file_name = event['Records'][0]['s3']['object']['key']
    csv_file = s3_client.get_object(Bucket = bucket, Key = csv_file_name)
    csv_content = csv_file['Body'].read().decode('utf8').count('\n')-1
    return csv_content

def _put_to_dynamodb(csv_file_count):
    dynamodb_client.put_item(
        TableName = COUNTING_TABLE,
        Item = {
            'row' : {
                'N' : str(csv_file_count)
            }
        }
    )
    LOGGER.info("Put to dynamodb")

def lambda_handler(event, context):
    LOGGER.info('Event structure: %s', event)
    try:
        csv_file_count = _read_object(event)
        _put_to_dynamodb(csv_file_count)
    except ClientError:
        LOGGER.error("Failed to put record to dynamodb")
