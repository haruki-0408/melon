import json
import os
from aws_lambda_powertools import Logger
from pdf_generator import create_pdf_document
from utilities import upload_to_s3

LOGGER_SERVICE = "convert_to_pdf"
logger = Logger(service=LOGGER_SERVICE)

# 環境変数からS3バケット名を取得
S3_BUCKET = os.environ["S3_BUCKET"]


@logger.inject_lambda_context(log_event=False)
def lambda_handler(event, context):
    try:
        # 入力データの取得
        workflow_id = event.get("workflow_id")
        title = event.get("title")
        abstract = event.get("abstract")
        sections_format = event.get("sections_format")

        # PDFの生成
        pdf_data = create_pdf_document(workflow_id,title, abstract, sections_format, S3_BUCKET)

        # S3にアップロード
        object_key = f"{workflow_id}/fake_thesis.pdf"
        upload_to_s3(bucket_name=S3_BUCKET, object_key=object_key, data=pdf_data, content_type="application/pdf")

        # 成功レスポンスを返す
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "PDF successfully uploaded to S3"})
        }

    except Exception as e:
        error = {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "payload": event
        }
        logger.error(error)
        return {
            'statusCode': 500,
            'body': error
        }
