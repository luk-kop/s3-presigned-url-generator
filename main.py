from typing import Union

import boto3
from botocore.exceptions import ClientError


def check_bucket(bucket_name: str) -> bool:
    """
    Determine whether a bucket exists and you have permission to access it.
    """
    s3_client = boto3.client('s3')
    try:
        response = s3_client.head_bucket(Bucket=bucket_name)
        return True
    except ClientError as error:
        error_code = error.response['Error']['Code']
        if error_code == '404':
            print(f'Bucket {bucket_name} does not exist')
        elif error_code == '403':
            print(f'You do not have permission to access {bucket_name} bucket')
        else:
            print('An error has occurred')
    return False


def check_object(bucket_name: str, object_key: str) -> bool:
    """
    Determine whether a object exists and you have permission to access it.
    """
    s3_client = boto3.client('s3')
    try:
        response = s3_client.head_object(
            Bucket=bucket_name,
            Key=object_key
        )
        return True
    except ClientError as error:
        print(error)
        error_code = error.response['Error']['Code']
        if error_code == '404':
            print(f'Object {object_key} does not exist')
        elif error_code == '403':
            print(f'You do not have permission to access {object_key} object')
        else:
            print('An error has occurred')
    return False


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
    except ClientError as error:
        print(error)
        return None
    return response


if __name__ == '__main__':

    s3_bucket_name = 'test-pre-bucket'
    s3_object_name = 'test-object'

    # Check whether bucket exist and authenticated user has permissions to access it
    bucket_exist = check_bucket(bucket_name=s3_bucket_name)
    object_exist = check_object(bucket_name=s3_bucket_name, object_key=s3_object_name)

    if bucket_exist and object_exist:
        url = create_presigned_url(bucket_name=s3_bucket_name, object_name=s3_object_name)
        print(f'URL = {url}')
