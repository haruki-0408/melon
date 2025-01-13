import pytest
import boto3
from moto import mock_aws
import json
from unittest.mock import patch

@pytest.fixture(scope="function")
def aws_services():
    """AWS サービスのモックを提供する基本フィクスチャ"""
    with mock_aws():
        services = {
            'dynamodb': boto3.client('dynamodb'),
            'events': boto3.client('events'),
            's3': boto3.client('s3'),
            'lambda': boto3.client('lambda'),
            'stepfunctions': boto3.client('stepfunctions')
        }
        
        # EventBridgeバスを作成
        services['events'].create_event_bus(Name="test-bus")
        
        yield services

@pytest.fixture(scope="function")
def lambda_context():
    """Lambda実行コンテキストのモック"""
    class LambdaContext:
        def __init__(self):
            self.aws_request_id = "test-request-id"
            self.function_name = "test-function"
            self.memory_limit_in_mb = 128
            self.invoked_function_arn = "arn:aws:lambda:eu-west-1:123456789012:function:test"
            self.log_group_name = "/aws/lambda/test"
            self.log_stream_name = "2020/01/01/[$LATEST]xxx"
    return LambdaContext()

@pytest.fixture(scope="function")
def mock_event_recorder(mocker):
    """record_workflow_progress_eventのモック化"""
    mock = mocker.patch('utilities.record_workflow_progress_event')
    return mock