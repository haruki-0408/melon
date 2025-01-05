import pytest
from aws_lambda_powertools.utilities.validation import SchemaValidationError
from functions.features.get_fake_thesis_title_category_format import app
from tests.unit.events.get_fake_thesis_title_category_format import (
    VALID_EVENT,
    INVALID_DATA_EVENT
)

# モックデータの定義
MOCK_DYNAMODB_RESPONSE = {
    'Item': {
        'category_type_en': 'validation',
        'category_type_jp': '検証',
        'sections': [
        {
          "sub_sections": [
            {
              "title_name": "目的と仮説"
            },
            {
              "title_name": "仮説や理論の背景"
            }
          ],
          "title_name": "はじめに"
        },
        {
          "sub_sections": [
            {
              "title_name": "実験の設計と実施方法"
            },
            {
              "title_name": "使用したツール・技術・データセット"
            }
          ],
          "title_name": "方法論"
        },
        {
          "sub_sections": [
            {
              "title_name": "実験結果の詳細"
            },
            {
              "title_name": "得られたデータの分析"
            }
          ],
          "title_name": "結果"
        },
        {
          "sub_sections": [
            {
              "title_name": "結果に対する解釈"
            },
            {
              "title_name": "仮説と実験結果の一致/不一致"
            },
            {
              "title_name": "実験の限界・誤差・改善点"
            }
          ],
          "title_name": "考察"
        },
        {
          "sub_sections": [
            {
              "title_name": "仮説の検証結果"
            },
            {
              "title_name": "今後の研究方向性"
            }
          ],
          "title_name": "結論"
        }
      ]
    }
}

@pytest.fixture
def mock_dynamodb(mocker):
    """DynamoDBのget_dynamo_item関数の正常系モック"""
    def mock_get_dynamo_item(*args, **kwargs):
        return MOCK_DYNAMODB_RESPONSE['Item']
    
    mocker.patch('utilities.get_dynamo_item', side_effect=mock_get_dynamo_item)

@pytest.fixture
def valid_event():
    return VALID_EVENT

@pytest.fixture
def invalid_data_event():
    return INVALID_DATA_EVENT

@pytest.fixture
def dynamodb_error(mocker):
    """DynamoDBのget_dynamo_item関数のエラーをモック化"""
    def mock_get_dynamo_item(*args, **kwargs):
        # utilities.pyのget_dynamo_itemの実装に合わせる
        response = {'Item': None}  # Itemキーが存在しない場合
        if 'Item' not in response:
            raise KeyError(f"アイテムが存在しません: {kwargs.get('key', '')}")
    
    # utilities.get_dynamo_itemをモック化
    mocker.patch('utilities.get_dynamo_item', side_effect=mock_get_dynamo_item)

@pytest.mark.success
def test_successful_format(valid_event, lambda_context, mock_event_recorder, mock_dynamodb):
    """正常系のフォーマット生成テスト"""
    response = app.lambda_handler(valid_event, lambda_context)
    
    assert response['statusCode'] == 200
    assert 'sections_format' in response['body']
    assert 'category_type_jp' in response['body']['sections_format']
    assert len(response['body']['sections_format']['sections']) > 0
    
    # モックデータと一致することを確認
    assert response['body']['sections_format'] == MOCK_DYNAMODB_RESPONSE['Item']
    
    # record_workflow_progress_eventに渡されるパラメータを検証
    assert mock_event_recorder.call_args.kwargs == {
        'workflow_id': valid_event['workflow_id'],
        'request_id': lambda_context.aws_request_id,
        'order': app.STATE_ORDER,
        'status': 'success',
        'state_name': app.STATE_NAME,
        'event_bus_name': app.WORKFLOW_EVENT_BUS_NAME
    }

@pytest.mark.validation_failed
def test_invalid_format(invalid_data_event, lambda_context, mock_event_recorder):
    """バリデーション異常系テスト"""
    with pytest.raises(SchemaValidationError):
        app.lambda_handler(invalid_data_event, lambda_context)
    
    # record_workflow_progress_eventに渡されるパラメータを検証
    assert mock_event_recorder.call_args.kwargs == {
        'workflow_id': invalid_data_event['workflow_id'],
        'request_id': lambda_context.aws_request_id,
        'order': app.STATE_ORDER,
        'status': 'validation-failed',
        'state_name': app.STATE_NAME,
        'event_bus_name': app.WORKFLOW_EVENT_BUS_NAME
    }

@pytest.mark.failed
def test_dynamodb_error(valid_event, lambda_context, mock_event_recorder, dynamodb_error):
    """DynamoDB接続エラーのテスト"""
    with pytest.raises(Exception) as exc_info:
        app.lambda_handler(valid_event, lambda_context)
    
    # KeyErrorがExceptionとして再スローされることを確認
    assert "アイテムが存在しません" in str(exc_info.value)
    
    # record_workflow_progress_eventに渡されるパラメータを検証
    assert mock_event_recorder.call_args.kwargs == {
        'workflow_id': valid_event['workflow_id'],
        'request_id': lambda_context.aws_request_id,
        'order': app.STATE_ORDER,
        'status': 'failed',
        'state_name': app.STATE_NAME,
        'event_bus_name': app.WORKFLOW_EVENT_BUS_NAME
    } 