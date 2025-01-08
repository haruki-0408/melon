import os
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.validation import validate
from aws_lambda_powertools.utilities.validation import SchemaValidationError
from aws_lambda_powertools import Tracer
from utilities import get_dynamo_item, record_workflow_progress_event
import schemas

# envパラメータ
DYNAMO_DB_CATEGORY_MASTER_TABLE = os.environ["DYNAMO_DB_CATEGORY_MASTER_TABLE"]
WORKFLOW_EVENT_BUS_NAME = os.environ["WORKFLOW_EVENT_BUS_NAME"]

STATE_NAME = "format-lambda"
STATE_ORDER = 2

logger = Logger()
tracer = Tracer()

@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def lambda_handler(event, context):
    """
    カテゴリマスタからカテゴリのフォーマットを取得するLambda関数
    """

    workflow_id = event.get('workflow_id')
    print(f"WorkflowId: {workflow_id}")
    
    # デフォルトは成功
    error = None
    
    try:
        # イベントバリデーション
        validate(event=event, schema=schemas.INPUT)

        # eventパラメータ
        fake_thesis_category_en =  event.get('category')
        format_data = get_dynamo_item(table_name=DYNAMO_DB_CATEGORY_MASTER_TABLE, key={"category_type_en": fake_thesis_category_en})
    except SchemaValidationError as e:
        error = {
            "error_type": "SchemaValidationError",
            "error_message": str(e)
        }
        logger.exception(str(e))
    except Exception as e:
        error = {
            "error_type": type(e).__name__,
            "error_message": str(e)
        }
        logger.exception(str(e))
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
            if error.get("error_type") == "SchemaValidationError":
                raise SchemaValidationError(error)
            else:
                raise Exception(error)
    
    # ユーザーに返却するレスポンス
    return {
        'statusCode': 200,
        'body': {
            'sections_format': format_data
        }
    }
