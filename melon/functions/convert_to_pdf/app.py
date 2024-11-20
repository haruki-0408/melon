import json
import os
from pdf_generator import create_pdf_document
from utilities import get_logger, upload_to_s3

logger = get_logger(service_name="convert_to_pdf")

# 環境変数からS3バケット名を取得
S3_BUCKET = os.environ["S3_BUCKET"]
OBJECT_KEY = "fake_thesis.pdf"

@logger.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    try:
        # 入力データの取得
        title = event.get("title")
        abstract = event.get("abstract")
        sections_format = event.get("sections_format")

        # PDFの生成
        pdf_data = create_pdf_document(title, abstract, sections_format, S3_BUCKET)

        # S3にアップロード
        upload_to_s3(bucket_name=S3_BUCKET, object_key=OBJECT_KEY, data=pdf_data, content_type="application/pdf")

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
