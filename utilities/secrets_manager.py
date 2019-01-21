'''
@file: secrets_manager.py
@author: Sukraat Ahluwalia

Class to interact and fetch secrets from AWS Secrets Manager
'''

import sys
sys.path.append("../")

import boto3

from botocore.exceptions import ClientError
from utilities import logutils

class secrets_manager:
    def __init__(self, secret_name, region):
        self.__aws_region = region
        self.__secret_name = secret_name
        self.__sm_logger = logutils("../logging/utilities_errs.log", "warn")


    def fetch_secrets(self):
        aws_session = boto3.session.Session()
        sm_client = aws_session.client(
            service_name='secretsmanager',
            region_name=self.__aws_region
        )

        try:
            awssm_response = sm_client.get_secret_value(SecretId=self.__secret_name)
        except ClientError as cl_err:
            '''
            Determine the correct error and log it into
            the log files with the current time
            '''
            sm_err_str = ""
            if cl_err.response['Error']['Code'] == 'DecryptionFailureException':
                sm_err_str = " Decryption Failure for Secrets Manager"
                raise cl_err
            elif cl_err.response['Error']['Code'] == 'ResourceNotFoundException':
                sm_err_str = " Resource Not Found Error for Secrets Manager"
            elif cl_err.response['Error']['Code'] == 'InvalidRequestException':
                sm_err_str = " Invalid Request to Secrets Manager"
            elif cl_err.response['Error']['Code'] == 'InvalidParameterException':
                sm_err_str = "Invalid Parameter Passed to Secrets Manager"
            else:
                sm_err_str = "Error Occurred for Secrets Manager "
            self.__sm_logger.set_message(sm_err_str)
        else:
            if 'SecretString' in awssm_response:
                secret_str = awssm_response['SecretString']

        return secret_str