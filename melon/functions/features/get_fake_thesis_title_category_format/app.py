import os
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.validation import validator
from aws_lambda_powertools.utilities.validation import SchemaValidationError
from utilities import get_dynamo_item
import schemas

# envパラメータ
DYNAMO_DB_CATEGORY_MASTER_TABLE = os.environ["DYNAMO_DB_CATEGORY_MASTER_TABLE"]

LOGGER_SERVICE = "get_fake_thesis_title_category_format"
logger = Logger(service=LOGGER_SERVICE)

@logger.inject_lambda_context(log_event=True)
@validator(inbound_schema=schemas.INPUT)
def lambda_handler(event, context):
    # eventパラメータ
    fake_thesis_category_en =  event.get('category')
    
    try:
        format = get_dynamo_item(table_name=DYNAMO_DB_CATEGORY_MASTER_TABLE, key={"category_type_en": fake_thesis_category_en})

    except SchemaValidationError as e:
        logger.exception(f"Schema validation failed: {e}")
        raise e
    except Exception as e:
        error = {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "payload": event
        }
        logger.exception(error)
        raise e

    # ユーザーに返却するレスポンス
    return {
        'statusCode': 200,
        'body': {
            'sections_format': format
        }
    }