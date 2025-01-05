import pytest
from aws_lambda_powertools.utilities.validation import SchemaValidationError
from functions.features.generate_prompt_parameters import app
from tests.unit.events.generate_prompt_parameters import (
    VALID_EVENT,
    INVALID_DATA_EVENT,
    ERROR_EVENT
)

@pytest.fixture
def valid_event():
    return VALID_EVENT

@pytest.fixture
def invalid_data_event():
    return INVALID_DATA_EVENT

@pytest.fixture
def error_event():
    return ERROR_EVENT

@pytest.mark.success
def test_successful_prompt_generation(valid_event, lambda_context, mock_event_recorder):
    """正常系のプロンプト生成テスト"""
    response = app.lambda_handler(valid_event, lambda_context)
    
    assert response['statusCode'] == 200
    assert 'system_prompt' in response['body']
    assert valid_event['title'] in response['body']['system_prompt']
    assert valid_event['sections_format']['category_type_jp'] in response['body']['system_prompt']
    
    assert mock_event_recorder({
        'detail': {
            'workflow_id': valid_event['workflow_id'],
            'request_id': lambda_context.aws_request_id,
            'order': app.STATE_ORDER,
            'status': 'success',
            'state_name': app.STATE_NAME
        }
    })

@pytest.mark.validation_failed
def test_invalid_prompt_parameters(invalid_data_event, lambda_context, mock_event_recorder):
    """イベントカテゴリータイプのバリデーション異常系テスト"""
    with pytest.raises(SchemaValidationError):
        app.lambda_handler(invalid_data_event, lambda_context)
    
    assert mock_event_recorder({
        'detail': {
            'workflow_id': invalid_data_event['workflow_id'],
            'request_id': lambda_context.aws_request_id,
            'order': app.STATE_ORDER,
            'status': 'failed',
            'state_name': app.STATE_NAME
        }
    })

@pytest.mark.failed
def test_general_error(error_event, lambda_context, mock_event_recorder):
    """一般的なエラーのテスト"""
    with pytest.raises(Exception):
        app.lambda_handler(error_event, lambda_context)
    
    assert mock_event_recorder({
        'detail': {
            'workflow_id': error_event['workflow_id'],
            'request_id': lambda_context.aws_request_id,
            'order': app.STATE_ORDER,
            'status': 'failed',
            'state_name': app.STATE_NAME
        }
    }) 