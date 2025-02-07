import json
import os
from aws_lambda_powertools import Logger, Tracer
from pdf_generator import create_pdf_document
from utilities import upload_to_s3, record_workflow_progress_event

WORKFLOW_EVENT_BUS_NAME = os.environ["WORKFLOW_EVENT_BUS_NAME"]
S3_BUCKET = os.environ["S3_BUCKET"]

STATE_NAME = "pdf-format-lambda"
STATE_ORDER = 12

logger = Logger()
tracer = Tracer()

@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def lambda_handler(event, context):
    """
    論文データをPDFに変換するLambda関数
    """
    workflow_id = event.get("workflow_id")
    print(f"WorkflowId: {workflow_id}")
    
    # デフォルトは成功
    error = None    

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

    except Exception as e:
        error = {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "payload": event
        }
        logger.exception(error)

    finally:
        # EventBridgeに進捗イベントを送信
        record_workflow_progress_event(
            workflow_id=workflow_id,
            request_id=context.aws_request_id,
            order=STATE_ORDER,
            status="success" if error is None else "failed",
            state_name=STATE_NAME,
            event_bus_name=WORKFLOW_EVENT_BUS_NAME
        )

        if error:
            raise Exception(error)

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "PDF successfully uploaded to S3"})
    }