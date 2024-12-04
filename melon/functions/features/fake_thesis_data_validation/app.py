import json
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.validation import validate, SchemaValidationError
from utilities import upload_to_s3

# スキーマファイルのパスを設定
FORMULAS_SCHEMA = '/opt/python/schemas/formulas_schema.json'
GRAPHS_SCHEMA = '/opt/python/schemas/graphs_schema.json'
TABLES_SCHEMA = '/opt/python/schemas/tables_schema.json'

LOGGER_SERVICE = "fake_thesis_data_validation"
logger = Logger(service=LOGGER_SERVICE)

@logger.inject_lambda_context(log_event=False)
def lambda_handler(event, context):
    """
    スキーマバリデーションを実行するLambda関数。

    Parameters:
    - event (dict): イベントデータ。
      - system_prompt (str): システムプロンプト。
      - response_format (list): 各セクションの生成AIレスポンス。

    Returns:
    - dict: バリデーション成功データ。
    """
    title = event.get("title")
    abstract = event.get("abstract")
    workflow_id = event.get("workflow_id")
    sections_format = event.get("sections_format")

    response_graphs, response_tables, response_formulas = [], [], []

    for section in sections_format:
        for sub_section in section['sub_sections']:
            response_graphs.extend(sub_section['graphs'])
            response_tables.extend(sub_section['tables'])
            response_formulas.extend(sub_section['formulas'])

    # スキーマファイルを読み込む
    with open(FORMULAS_SCHEMA, 'r', encoding='utf-8') as f:
        formulas_schema_json = json.loads(f.read())
    with open(GRAPHS_SCHEMA, 'r', encoding='utf-8') as f:
        graphs_schema_json = json.loads(f.read())
    with open(TABLES_SCHEMA, 'r', encoding='utf-8') as f:
        table_schema_json = json.loads(f.read())

    try:
        validate(event={"formulas": response_formulas}, schema=formulas_schema_json)
        validate(event={"graphs": response_graphs}, schema=graphs_schema_json)
        validate(event={"tables": response_tables}, schema=table_schema_json)
    except SchemaValidationError as e:
        logger.exception(e)
        raise e
    except Exception as e:
        error = {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "payload": event
        }
        logger.exception(error)

        raise e
    

    # 仮S3データ保存
    # upload_to_s3(bucket_name="fake-thesis-bucket",object_key=f"{workflow_id}/responses_graphs.json",data=json.dumps(response_graphs, ensure_ascii=False))
    # upload_to_s3(bucket_name="fake-thesis-bucket",object_key=f"{workflow_id}/responses_tables.json",data=json.dumps(response_tables, ensure_ascii=False))
    # upload_to_s3(bucket_name="fake-thesis-bucket",object_key=f"{workflow_id}/responses_formulas.json",data=json.dumps(response_formulas, ensure_ascii=False))

    return {
        'statusCode': 200,
        'body': {
            "graphs": response_graphs,
            "tables": response_tables,
            "formulas": response_formulas
        }
    }