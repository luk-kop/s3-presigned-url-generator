# S3 presigned URL generator

[![Python 3.8.5](https://img.shields.io/badge/python-3.8.5-blue.svg)](https://www.python.org/downloads/release/python-377/)
[![Boto3](https://img.shields.io/badge/Boto3-1.18.30-blue.svg)](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

> The **S3 presigned URL generator** is a simple script that allows you to quickly generate an **presigned URL** for an object in a selected S3 bucket. 
> This way you can temporarily grant access to private object (file) to user who does not have AWS credentials or permission to access it.


## Features
- When executing the script, the following arguments must be provided:
  - bucket name;
  - object key;
  - URL validity time in minutes (optional).
- Before generating the URL, the script verifies if the S3 bucket and object exist.
- The script also checks whether user has permissions to access S3 bucket and object.
- As a result of invoking the script you will get the presigned URL for the specified object and the URL expiration date.

## Requirements
- Python third party packages: [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- Before using the script, you need to set up valid authentication credentials for your AWS account (with programmatic access) using either the IAM Management Console or the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html) tool.
- A presigned URL should be generated by an AWS user who has access to the specified object.

## Installation with venv
The script can be build and run locally with virtualenv tool. Run following commands in order to create virtual environment and install the required packages.
```bash
$ virtualenv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```

## Running the script
- You can start the script using the following command:
  ```bash
  (venv) $ python presign_url.py --bucket your-bucket-name --object your-object-key --expires 10
  
  # You should get the similar output:
  URL = https://your-bucket-name.s3.amazonaws.com/your-object-key?AWSAccessKeyId=AKIAXX1234QWERTYUI09&Signature=abcDE1fGHIj2K3lmNoPQ%4RSTuWxy%5Z&Expires=1630601368
  Valid until = 02-Sep-2021 18:49:28 (10 minutes)
  ```
- For detailed help, use the following command:
    ```bash
    (venv) $ python presign_url.py --help
    ```