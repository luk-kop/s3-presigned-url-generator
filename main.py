import logging
from typing import Union

import boto3
from botocore.exceptions import ClientError


def check_bucket_exist(bucket_name: str) -> bool:
    """
    Checks whether the bucket exists.
    """
    buckets = get_buckets_list()
    if bucket_name in buckets:
        return True
    return False


def get_buckets_list() -> list:
    """
    Returns a list of all buckets owned by the authenticated sender of the request.
    """
    s3_client = boto3.client('s3')
    s3_buckets = s3_client.list_buckets()['Buckets']
    return [bucket.get('Name') for bucket in s3_buckets]


def create_presigned_url(bucket_name: str, object_name:str , expiration: str = 3600) -> Union[str, None]:
    """
    Generate a presigned URL to share an S3 object
    """
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={
                                                        'Bucket': bucket_name,
                                                        'Key': object_name
                                                    },
                                                    ExpiresIn=expiration)
    except ClientError as err:
        logging.error(err)
        return None
    return response


if __name__ == '__main__':

    s3_bucket_name = 'test-pre-bucket'
    s3_object_name = 'test-object'

    # Check if bucket exist for authenticated user
    bucket_exist = check_bucket_exist(bucket_name=s3_bucket_name)

    if bucket_exist:
        url = create_presigned_url(bucket_name=s3_bucket_name, object_name=s3_object_name)
        print(f'URL = {url}')
