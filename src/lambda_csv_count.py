"""Parsing json to csv and parquet"""
import logging
import boto3

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

dynamodb_client = boto3.client('dynamodb',endpoint_url="http://host.docker.internal:4566",\
     region_name = "ap-southeast-1")
s3_client= boto3.client('s3',endpoint_url="http://host.docker.internal:4566",\
     region_name = "ap-southeast-1")

COUNTING_TABLE = 'csv_count_table'


def _read_object(event):
    """Read json object files"""
    bucket = event['Records'][0]['s3']['bucket']['name']
    csv_file_name = event['Records'][0]['s3']['object']['key']
    csv_file = s3_client.get_object(Bucket = bucket, Key = csv_file_name)
    csv_content = csv_file['Body'].read()
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
    """Main function"""
    LOGGER.info('Event structure: %s', event)
    csv_file_count = _read_object(event).decode('utf8').count('\n')-1
    LOGGER.info(str(csv_file_count))
    _put_to_dynamodb(csv_file_count)
