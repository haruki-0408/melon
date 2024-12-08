import json
from aws_lambda_powertools import Logger, Tracer
import os
from utilities import upload_to_s3

S3_BUCKET = os.environ.get("S3_BUCKET")

logger = Logger()

tracer = Tracer()

@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def lambda_handler(event, context):
    """
    イベントで渡されたLaTeX数式とその説明をS3に保存するLambda関数
    """
    try:
        # イベントから数式の配列を取得
        workflow_id = event.get('workflow_id')
        formulas = event.get('formulas')
        
        if not formulas:
            raise Exception("No formulas data provided in event")
        if not S3_BUCKET:
            raise Exception("No S3 Bucket provided in the environ.")

        metadata_keys = []
        for eq in formulas:
            id = eq.get('id')
            latex_code = eq.get('latex_code')
            description = eq.get('description', '')
            parameters = eq.get('parameters', [])

            # 入力の検証・サニタイズが必要

            # 数式のメタデータをS3に保存
            metadata_key = f'{workflow_id}/formulas/{id}_metadata.json'

            metadata_keys.append(metadata_key)
            
            metadata = {
                'description': description,
                'parameters': parameters,
                'latex_code': latex_code
            }

            upload_to_s3(S3_BUCKET, metadata_key,json.dumps(metadata, ensure_ascii=False))
            # s3.put_object(
            #     Bucket=S3_BUCKET,
            #     Key=metadata_key,
            #     Body=json.dumps(metadata, ensure_ascii=False),
            #     ContentType='application/json'
            # )

        return {
            'statusCode': 200,
            'body': metadata_keys
        }

    except Exception as e:
        error = {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "payload": event
        }
        logger.exception(error)
        raise e
