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
        result = event.get('result', {}) # 結果データ (成功時)
        error_details = event.get('error_details', {}) # エラー詳細 (失敗時)

        if status.upper() == "SUCCEEDED":
            # 成功時に親ワークフローに結果を送信
            logger.info(f"Sending success to parent workflow: {result}")
            response = sfn_client.send_task_success(
                taskToken=task_token,
                output=json.dumps(result) # 必ずJSON形式で送信
            )
        elif status.upper() == "FAILED":
            # 失敗時に親ワークフローにエラーを送信
            logger.info(f"Sending failure to parent workflow: {error_details}")
            response = sfn_client.send_task_failure(
                taskToken=task_token,
                error=error_details.get('error', 'UnknownError'),
                cause=error_details.get('cause', 'No cause provided')
            )
        else:
            raise ValueError("Invalid status. Must be 'SUCCEEDED' or 'FAILED'.")

        # レスポンスをログに記録
        logger.info(f"Response from Step Functions: {response}")
        return {
            'status_code': 200,
            'body': json.dumps({'message': 'Callback sent successfully'})
        }

    except KeyError as e:
        logger.exception(f"Missing required key in event: {str(e)}")
        return {
            'status_code': 400,
            'body': json.dumps({'error': f"Missing required key: {str(e)}"})
        }
    except ClientError as e:
        logger.exception(f"Failed to send callback to Step Functions: {e.response['Error']['Message']}")
        return {
            'status_code': 500,
            'body': json.dumps({'error': e.response['Error']['Message']})
        }
    except Exception as e:
        logger.exception(f"Unexpected error: {str(e)}")
        return {
            'status_code': 500,
            'body': json.dumps({'error': str(e)})
        }
