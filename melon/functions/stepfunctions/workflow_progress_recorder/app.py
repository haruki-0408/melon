from aws_lambda_powertools import Logger, Tracer
import os
import json
from utilities import record_workflow_progress

# envパラメータ
DYNAMO_DB_WORKFLOW_PROGRESS_TABLE = os.environ["DYNAMO_DB_WORKFLOW_PROGRESS_TABLE"]  # DynamoDBのテーブル名

logger = Logger()
tracer = Tracer()

@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def lambda_handler(event, context):
    """
    進捗をDynamoDBに保存し更新する関数
    """
    try:
        # 進捗を記録
        record_workflow_progress(
            table_name=DYNAMO_DB_WORKFLOW_PROGRESS_TABLE,
            workflow_id=event['workflow_id'],
            request_id=event['request_id'],
            order=event['order'],
            status=event['status'],
            state_name=event['state_name']
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
