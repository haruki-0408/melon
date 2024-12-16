import io
import boto3
import base64
import os
from utilities import put_item_to_dynamodb
from aws_lambda_powertools import Logger, Tracer

FONT_PATH = '/opt/python/fonts/ipaexm.ttf'  # フォントパスを設定
S3_BUCKET = os.environ.get("S3_BUCKET")

logger = Logger()

tracer = Tracer()

@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler

def lambda_handler(event, context):
    try:
        item = {
            "workflow_id": "xef2mkov",
            "state_name#timestamp": "convert_to_pdf#2024-12-04T01:30:27.375296+00:00",
            "status": "success",
            "error_details": None,
            "execution_id": "test",
        }
        put_item_to_dynamodb(table_name="melon_dev_workflow_progress_management_table", item=item)
    except Exception as e:
        logger.exception(f"Error: {e}")
        raise e
    