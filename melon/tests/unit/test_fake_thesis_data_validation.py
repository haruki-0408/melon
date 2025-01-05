import pytest
from aws_lambda_powertools.utilities.validation import SchemaValidationError
from functions.features.fake_thesis_data_validation import app
from tests.unit.events.fake_thesis_data_validation import (
    VALID_EVENT,
    INVALID_DATA_EVENT,
    ERROR_EVENT
)

# テストデータのフィクスチャ
@pytest.fixture
def valid_event():
    """正常系テスト用のイベントデータ"""
    return VALID_EVENT

@pytest.fixture
def invalid_latex_event():
    """LaTeXバリデーション異常系テスト用のイベントデータ"""
    return INVALID_DATA_EVENT

@pytest.fixture
def error_event():
    """その他の異常系テスト用のイベントデータ"""
    return ERROR_EVENT

# 正常系テスト
@pytest.mark.success
def test_successful_validation(valid_event, lambda_context, mock_event_recorder):
    """正常系のバリデーションテスト"""
    response = app.lambda_handler(valid_event, lambda_context)
    
    assert response['statusCode'] == 200
    assert 'graphs' in response['body']
    assert 'tables' in response['body']
    assert 'formulas' in response['body']
    
    # イベント送信の検証
    assert mock_event_recorder({
        'detail': {
            'workflow_id': valid_event['workflow_id'],
            'request_id': lambda_context.aws_request_id,
            'order': app.STATE_ORDER,
            'status': 'success',
            'state_name': app.STATE_NAME
        }
    })

# バリデーション異常系テスト
@pytest.mark.validation_failed
def test_invalid_latex_validation(invalid_latex_event, lambda_context, mock_event_recorder):
    """LaTeXバリデーション異常系テスト"""
    with pytest.raises(SchemaValidationError) as exc_info:
        app.lambda_handler(invalid_latex_event, lambda_context)
    
    assert "LaTeX" in str(exc_info.value)
    
    # イベント送信の検証
    assert mock_event_recorder({
        'detail': {
            'workflow_id': invalid_latex_event['workflow_id'],
            'request_id': lambda_context.aws_request_id,
            'order': app.STATE_ORDER,
            'status': 'validation-failed',
            'state_name': app.STATE_NAME
        }
    })

# その他の異常系テスト
@pytest.mark.failed
def test_general_error(error_event, lambda_context, mock_event_recorder):
    """一般的なエラーのテスト"""
    with pytest.raises(Exception):
        app.lambda_handler(error_event, lambda_context)
    
    # イベント送信の検証
    assert mock_event_recorder({
        'detail': {
            'workflow_id': error_event['workflow_id'],
            'request_id': lambda_context.aws_request_id,
            'order': app.STATE_ORDER,
            'status': 'failed',
            'state_name': app.STATE_NAME
        }
    })

# ユーティリティ関数のテスト
def test_validate_latex_code():
    """LaTeXコード検証関数のテスト"""
    valid_formulas = [
        {"id": "FORMULA_1", "latex_code": "E = mc^2"},
        {"id": "FORMULA_2", "latex_code": "\\frac{1}{2}"}
    ]
    
    invalid_formulas = [
        {"id": "FORMULA_3", "latex_code": "E = %^&$%^$^"},
        {"id": "FORMULA_4", "latex_code": "\\frac{1}{2"}
    ]
    
    assert not app.validate_latex_code(valid_formulas)
    
    errors = app.validate_latex_code(invalid_formulas)
    assert len(errors) == 2
    assert "FORMULA_3" in errors[0]
    assert "FORMULA_4" in errors[1] 