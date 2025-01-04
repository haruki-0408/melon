import json
import pytest
import boto3
from moto import mock_dynamodb, mock_events
from unittest.mock import patch, MagicMock
from aws_lambda_powertools.utilities.validation import SchemaValidationError
from functions.features.fake_thesis_data_validation import app

# テスト用の共通フィクスチャ
@pytest.fixture(scope="function")
def aws_credentials():
    """
    モックAWS認証情報を提供するフィクスチャ
    scope="function": 各テスト関数ごとに新しいフィクスチャを作成
    """
    import os
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "ap-northeast-1"

@pytest.fixture(scope="function")
def dynamodb(aws_credentials):
    """
    DynamoDBのモックを提供するフィクスチャ
    aws_credentials: 依存するフィクスチャ
    """
    with mock_dynamodb():
        yield boto3.client("dynamodb")

@pytest.fixture(scope="function")
def eventbridge(aws_credentials):
    """
    EventBridgeのモックを提供するフィクスチャ
    aws_credentials: 依存するフィクスチャ
    """
    with mock_events():
        yield boto3.client("events")

# テストデータのフィクスチャ
@pytest.fixture
def valid_event():
    """
    正常系テスト用のイベントデータ
    """
    return {
        "workflow_id": "test-workflow",
        "sections_format": [
            {
                "sub_sections": [
                    {
                        "graphs": [{"id": "GRAPH_1", "type": "line"}],
                        "tables": [{"id": "TABLE_1", "headers": ["A", "B"]}],
                        "formulas": [{"id": "FORMULA_1", "latex_code": "E = mc^2"}]
                    }
                ]
            }
        ]
    }

@pytest.fixture
def invalid_latex_event():
    """
    異常系テスト用のイベントデータ（不正なLaTeX）
    """
    return {
        "workflow_id": "test-workflow",
        "sections_format": [
            {
                "sub_sections": [
                    {
                        "formulas": [{"id": "FORMULA_1", "latex_code": "E = %^&$%^$^"}]
                    }
                ]
            }
        ]
    }

@pytest.fixture
def lambda_context():
    """
    Lambda実行コンテキストのモック
    """
    context = MagicMock()
    context.aws_request_id = "test-request-id"
    return context

# テストケース
@mock_events  # EventBridgeをモック化
def test_successful_validation(valid_event, lambda_context):
    """
    正常系のバリデーションテスト
    
    テスト内容：
    1. 有効なイベントデータでLambdaを実行
    2. レスポンスの構造を確認
    3. EventBridgeへの進捗イベント送信を確認
    """
    with patch('functions.features.fake_thesis_data_validation.app.record_workflow_progress_event') as mock_record:
        response = app.lambda_handler(valid_event, lambda_context)
        
        # レスポンスの検証
        assert response['statusCode'] == 200
        assert 'graphs' in response['body']
        assert 'tables' in response['body']
        assert 'formulas' in response['body']
        
        # 進捗イベントの送信確認
        mock_record.assert_called_once_with(
            workflow_id=valid_event['workflow_id'],
            request_id=lambda_context.aws_request_id,
            order=app.STATE_ORDER,
            status="success",
            state_name=app.STATE_NAME,
            event_bus_name=app.WORKFLOW_EVENT_BUS_NAME
        )

@mock_events
def test_invalid_latex_validation(invalid_latex_event, lambda_context):
    """
    LaTeXバリデーションエラーのテスト
    
    テスト内容：
    1. 不正なLaTeXコードを含むイベントでLambdaを実行
    2. 適切な例外が発生することを確認
    3. エラー時の進捗イベント送信を確認
    """
    with patch('functions.features.fake_thesis_data_validation.app.record_workflow_progress_event') as mock_record:
        with pytest.raises(SchemaValidationError) as exc_info:
            app.lambda_handler(invalid_latex_event, lambda_context)
        
        # エラーメッセージの検証
        assert "LaTeX" in str(exc_info.value)
        
        # エラー時の進捗イベント送信確認
        mock_record.assert_called_once_with(
            workflow_id=invalid_latex_event['workflow_id'],
            request_id=lambda_context.aws_request_id,
            order=app.STATE_ORDER,
            status="validation-failed",
            state_name=app.STATE_NAME,
            event_bus_name=app.WORKFLOW_EVENT_BUS_NAME
        )

# ユーティリティ関数のテスト
def test_validate_latex_code():
    """
    LaTeXコード検証関数のテスト
    
    テスト内容：
    1. 正常なLaTeXコードの検証
    2. 不正なLaTeXコードの検証
    """
    valid_formulas = [
        {"id": "FORMULA_1", "latex_code": "E = mc^2"},
        {"id": "FORMULA_2", "latex_code": "\\frac{1}{2}"}
    ]
    
    invalid_formulas = [
        {"id": "FORMULA_3", "latex_code": "E = %^&$%^$^"},
        {"id": "FORMULA_4", "latex_code": "\\frac{1}{2"}
    ]
    
    # 正常系テスト
    assert not app.validate_latex_code(valid_formulas)
    
    # 異常系テスト
    errors = app.validate_latex_code(invalid_formulas)
    assert len(errors) == 2
    assert "FORMULA_3" in errors[0]
    assert "FORMULA_4" in errors[1]

def test_parse_validation_error():
    """バリデーションエラーメッセージのパース関数のテスト"""
    error_message = "Error: Invalid format, Path: $.formulas[0]"
    parsed = app.parse_validation_error(error_message)
    assert parsed == "Invalid format"
    
    # エラーメッセージの形式が異なる場合
    different_format = "Something went wrong"
    assert app.parse_validation_error(different_format) == different_format 