import json
from aws_lambda_powertools import Logger
import boto3
from botocore.exceptions import ClientError

logger = Logger(service_name="send_workflow_callback")

# Step Functions クライアント
sfn_client = boto3.client('stepfunctions')

@logger.inject_lambda_context(log_event=False)
def lambda_handler(event, context):
    """
    子ワークフローの結果を親ワークフローに返すLambda関数（スネークケース対応）
    """
    try:
        # Eventから必要な情報を取得
        task_token = event['task_token']  # コールバック用トークン
        status = event['status']         # 成功/失敗のステータス ("SUCCEEDED" or "FAILED")
        payload = event.get('payload', {}) # 結果データ (成功時)
        error = event.get('error', {}) # エラー詳細 (失敗時)

        if status.upper() == "SUCCEEDED":
            # 成功時に親ワークフローに結果を送信
            logger.info(f"Sending success to parent workflow: {payload}")
            response = sfn_client.send_task_success(
                taskToken=task_token,
                output=json.dumps(payload) # 必ずJSON形式で送信
            )
        elif status.upper() == "FAILED":
            # 失敗時に親ワークフローにエラーを送信
            logger.info(f"Sending failure to parent workflow: {error}")
            response = sfn_client.send_task_failure(
                taskToken=task_token,
                error=error.get('error', 'UnknownError'),
                cause=error.get('cause', 'No cause provided')
            )
        else:
            raise ValueError("Invalid status. Must be 'SUCCEEDED' or 'FAILED'.")

        # レスポンスをログに記録
        logger.info(f"Response from Step Functions: {response}")
        return {
            'status_code': 200,
            'body': json.dumps({'message': 'Callback sent successfully'})
        }

    except Exception as e:
        error = {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "payload": event
        }
        logger.exception(error)

        raise e
