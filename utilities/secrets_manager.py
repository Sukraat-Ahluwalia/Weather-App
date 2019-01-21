'''
@file: secrets_manager.py
@author: Sukraat Ahluwalia

Class to connect to and fetch secrets from AWS Secrets Manager
'''

import sys
sys.path.append("../")

import boto3

from botocore.exceptions import ClientError
from utilities.logutils import logutils

class secrets_manager:
    '''
    Constructor

    Variables -

    __aws_region    The region specified in the AWS API
    __secret_name   The secret name under which the credentials
                    have been stored
    __sm_logger     The logging object for this class
    '''
    def __init__(self, secret_name, region):
        self.__aws_region = region
        self.__secret_name = secret_name
        self.__sm_logger = logutils("../logging/utilities_errs.log", 40)


    '''
    Method to fetch the secrets from secrets manager
    
    :@return A JSON string representing the secrets. In case of failure
             the method returns an empty string.
    '''
    def fetch_secrets(self):
        # Initialize an AWS Session with secrets manager as the service
        aws_session = boto3.session.Session()
        sm_client = aws_session.client(
            service_name='secretsmanager',
            region_name=self.__aws_region
        )

        # connect to secrets manager with the secret name
        # In case of failure log the failure in the file
        # with logging level set to ERROR( integer code: 40)
        # In case of success return the JSON string.
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