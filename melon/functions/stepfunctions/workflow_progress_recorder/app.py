from aws_lambda_powertools import Logger, Tracer
import os
import json
from utilities import put_item_to_dynamodb
from datetime import datetime, timezone, timedelta
# envパラメータ
DYNAMO_DB_WORKFLOW_PROGRESS_TABLE = os.environ["DYNAMO_DB_WORKFLOW_PROGRESS_TABLE"]  # DynamoDBのテーブル名

logger = Logger()
tracer = Tracer()
JST = timezone(timedelta(hours=+9), 'JST')

@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def lambda_handler(event, context):
    """
    進捗をDynamoDBに保存し更新する関数
    """
    try:
        workflow_id = event['workflow_id']
        request_id = event['request_id']
        order = event['order']
        status = event['status']
        state_name = event['state_name']

        # JSTのタイムスタンプを取得
        timestamp = datetime.now(JST).isoformat()

        item = {
            'workflow_id': workflow_id,
            'timestamp#order': timestamp + '#' + str(order),
            'state_name': state_name,
            'status': status,
            'request_id': request_id
        }

        # DynamoDBに保存
        put_item_to_dynamodb(
            TableName=DYNAMO_DB_WORKFLOW_PROGRESS_TABLE,
            Item=item
        )

        return {
            'status_code': 200,
            'body': json.dumps({'message': 'Progress recorded successfully'})
        }
    except Exception as e:
        error = {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "payload": event
        }
        logger.exception(error)
        raise e
