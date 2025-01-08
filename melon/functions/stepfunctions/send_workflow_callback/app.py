import json
import os
from aws_lambda_powertools import Logger, Tracer
import boto3
from utilities import record_workflow_progress_event

WORKFLOW_EVENT_BUS_NAME = os.environ["WORKFLOW_EVENT_BUS_NAME"]

# Step Functions クライアント
sfn_client = boto3.client('stepfunctions')

STATE_NAME = "callback-success-lambda"
STATE_ORDER = 8

logger = Logger()
tracer = Tracer()

@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def lambda_handler(event, context):
    """
    子ワークフローの結果を親ワークフローに返すLambda関数
    """

    workflow_id = event.get('workflow_id')
    print(f"WorkflowId: {workflow_id}")

    # デフォルトは成功
    error = None    
    response = None

    try:
        # Eventから必要な情報を取得
        task_token = event['task_token']  # コールバック用トークン
        status = event['status']         # 成功/失敗のステータス ("SUCCEEDED" or "FAILED")
        payload = event.get('payload', {}) # 結果データ (成功時)
        error_detail = event.get('error', {}) # エラー詳細 (失敗時)

        if status.upper() == "SUCCEEDED":
            # 成功時に親ワークフローに結果を送信
            logger.info(f"Sending success to parent workflow: {payload}")
            response = sfn_client.send_task_success(
                taskToken=task_token,
                output=json.dumps(payload) # 必ずJSON形式で送信
            )
        elif status.upper() == "FAILED":
            # 失敗時に親ワークフローにエラーを送信
            logger.info(f"Sending failure to parent workflow: {error_detail}")
            response = sfn_client.send_task_failure(
                taskToken=task_token,
                error=error_detail.get('Error'),
                cause=error_detail.get('Cause')
            )
        else:
            raise ValueError("Invalid status. Must be 'SUCCEEDED' or 'FAILED'.")

    except Exception as e:
        error = {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "payload": event
        }
        logger.exception(str(e))

        # 予期せぬエラーを親ワークフローに送信
        if response is None:
            response = sfn_client.send_task_failure(
                taskToken=task_token,
                error=error.get('error_type'),
                cause=error.get('error_message')
            )

    finally:
        # レスポンスをログに記録
        logger.info(f"Response from Step Functions: {response}")

        # EventBridgeに進捗イベントを送信 (ここまでのステータスが成功の場合のみEventBridgeに送信)
        if status.upper() == "SUCCEEDED":
            record_workflow_progress_event(
                workflow_id=workflow_id,
                request_id=context.aws_request_id,
                order=STATE_ORDER,
                status="success" if error is None else "failed",
                state_name=STATE_NAME,
                event_bus_name=WORKFLOW_EVENT_BUS_NAME
            )   
            
        # バリデーションエラーの最大回数を超えた場合
        elif error_detail.get("Error") == "MaxValidationRetryAttemptsExceededError":
            record_workflow_progress_event(
                workflow_id=workflow_id,
                request_id=context.aws_request_id,
                order=STATE_ORDER,
                status="failed",
                state_name=STATE_NAME,
                event_bus_name=WORKFLOW_EVENT_BUS_NAME
            )

        if error:   
            raise Exception(error)
        
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Callback sent successfully'})
    }
