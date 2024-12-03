from aws_lambda_powertools import Logger
import os
import json
from datetime import datetime, timezone

from utilities import put_item_to_dynamodb

# envパラメータ
DYNAMO_DB_TABLE = os.environ["DYNAMO_DB_WORKFLOW_PROGRESS_TABLE"]

logger = Logger(service_name="workflow_progress_recorder")

@logger.inject_lambda_context(log_event=False)
def lambda_handler(event, context):
    """
    Step Functionsのステート結果をDynamoDB進捗管理テーブルに追加する汎用的なLambda関数
    """
    try:
        # Step Functionsからのイベントを解析
        workflow_id = event['workflow_id']  # ワークフローID
        state_name = event['state_name']    # ステート名
        status = event['status']           # 成功/失敗 ("SUCCEEDED" or "FAILED")
        start_time = event.get('start_time', None)  # ステートの開始時間
        end_time = event.get('end_time', None)      # ステートの終了時間
        duration = event.get('duration', 0)        # 実行時間 (ミリ秒)
        error_details = event.get('error_details', {})  # エラー詳細（失敗時）

        # 現在時刻をISO 8601形式で記録
        timestamp = datetime.now(timezone.utc).isoformat()  

        # DynamoDBに進捗情報を記録
        item = {
            'workflow_id': workflow_id,
            'state_name#timestamp': f"{state_name}#{timestamp}",
            'status': status,
            'start_time': start_time,
            'end_time': end_time,
            'duration': duration,
            'error_details': error_details
        }

        # 不要なNone値を削除
        item = {k: v for k, v in item.items() if v is not None}

        # DynamoDBに値を保存
        put_item_to_dynamodb(DYNAMO_DB_TABLE, item)

        return {
            'status_code': 200,
            'body': json.dumps({'message': 'Progress added successfully'})
        }

    except KeyError as e:
        logger.error(f"Missing required key in event: {str(e)}")
        return {
            'status_code': 400,
            'body': json.dumps({'error': f"Missing required key: {str(e)}"})
        }
    except Exception as e:
        logger.error(f"Failed to update DynamoDB: {str(e)}")
        return {
            'status_code': 500,
            'body': json.dumps({'error': str(e)})
        }
