#!/usr/bin/env python3

from typing import Union
from datetime import datetime, timedelta
import argparse

import boto3
from botocore.exceptions import ClientError


def check_s3_data(bucket_name: str, object_key: str) -> bool:
    """
    Determine whether bucket and object exist and you have permission to access them.
    """
    s3_client = boto3.client('s3')
    # Supplementary dict to determine which item (bucket or object) exception relates to.
    checked_item = {
        'type': 'bucket',
        'name': bucket_name
    }
    try:
        # Check whether bucket exist and authenticated user has permissions to access it
        s3_client.head_bucket(
            Bucket=bucket_name
        )
        # Check whether object in bucket exist and authenticated user has permissions to access it
        checked_item['type'], checked_item['name']= 'object', object_key
        s3_client.head_object(
            Bucket=bucket_name,
            Key=object_key
        )
        return True
    except ClientError as error:
        error_code = error.response['Error']['Code']
        item_type, item_name = checked_item['type'], checked_item['name']
        if error_code == '404':
            print(f'Error: {item_type.capitalize()} {item_name} does not exist')
        elif error_code == '403':
            print(f'Error: You do not have permission to access {item_name} {item_type}')
        else:
            print('Error: An error has occurred')
    return False


def create_presigned_url(bucket_name: str, object_name:str, expiration_time: str = 60) -> Union[str, None]:
    """
    Generate a presigned URL to share an S3 object.
    """
    s3_client = boto3.client('s3')
    # Expiration time in seconds
    expiration_time = expiration_time * 60
    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket_name,
                'Key': object_name
            },
            ExpiresIn=expiration_time
        )
    except ClientError as error:
        print(error)
        return None
    return response


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='The script generates S3 object presigned URL')
    parser.add_argument('-b', '--bucket', required=True, help='S3 bucket name')
    parser.add_argument('-o', '--object', required=True, help='S3 object key')
    parser.add_argument('-e', '--expires',
                        type=int,
                        default=60,
                        help='Number of minutes until the pre-signed URL expires (default 60 min)')
    args = parser.parse_args()

    # Get data from argparse
    s3_bucket_name = args.bucket
    s3_object_key = args.object
    # Expiration time in minutes - default 60 minutes
    url_expiration_time = args.expires

    # Check whether bucket and object exist and authenticated user has permissions to access them.
    s3_data_correct = check_s3_data(bucket_name=s3_bucket_name,
                                    object_key=s3_object_key)

    if s3_data_correct:
        url = create_presigned_url(bucket_name=s3_bucket_name,
                                   object_name=s3_object_key,
                                   expiration_time=url_expiration_time)
        valid_time = datetime.now() + timedelta(minutes=url_expiration_time)
        # Time in format: 28-Aug-2021 06:03:46
        valid_time_str = valid_time.strftime('%d-%b-%Y %H:%M:%S')
        print(f'URL = {url}')
        print(f'Valid until = {valid_time_str} ({url_expiration_time} minutes)')
