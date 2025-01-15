from aws_lambda_powertools import Logger, Tracer
import os
import json
import requests

# envパラメータ
NEXTJS_API_ENDPOINT = os.environ["NEXTJS_API_ENDPOINT"]  # Next.jsのAPIエンドポイントのベースURL

logger = Logger()
tracer = Tracer()

@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def lambda_handler(event, context):
    """
    DynamoDB Streamからのイベントを受け取り、
    Next.jsのSSEエンドポイントに進捗情報を送信するLambda関数
    """
    try:
        # DynamoDB Streamからのレコードを処理
        for record in event['Records']:
            # INSERT または MODIFY イベントのみ処理
            if record['eventName'] in ['INSERT', 'MODIFY']:
                # DynamoDBのNewImageから項目を取得
                new_image = record['dynamodb']['NewImage']
                
                # DynamoDBのデータ形式を通常の辞書形式に変換
                item = {
                    'workflow_id': new_image['workflow_id']['S'],
                    'timestamp#order': new_image['timestamp#order']['S'],
                    'state_name': new_image['state_name']['S'],
                    'request_id': new_image.get('request_id', {}).get('S', None),
                    'status': new_image['status']['S']
                }

                # Next.jsのSSEエンドポイントにPOSTリクエストを送信
                sse_endpoint = f"{NEXTJS_API_ENDPOINT}/api/notify"
                response = requests.post(
                    sse_endpoint,
                    json=item,
                    headers={'Content-Type': 'application/json'}
                )
                
                if response.status_code != 200:
                    logger.error(f"Failed to send data to SSE endpoint: {response.text}")
                    raise Exception("Failed to send data to SSE endpoint")

        return {
            'status_code': 200,
            'body': json.dumps({'message': 'Progress notifications sent successfully'})
        }
    except Exception as e:
        error = {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "payload": event
        }
        logger.exception(error)
        raise e
