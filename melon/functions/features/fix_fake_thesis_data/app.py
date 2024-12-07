import json

from aws_lambda_powertools import Logger

from anthropic_client import AnthropicClient
from utilities import read_schema_jsons

logger = Logger(service_name="fix_fake_thesis_data")

# 生成AI リクエストインスタンス生成
# client = AnthropicClient()  

@logger.inject_lambda_context(log_event=False)
def lambda_handler(event, context):
    """
    修正を促す生成AIリクエストを実行するLambda関数。
    """
    title = event.get("title")
    abstract = event.get("abstract")
    workflow_id = event.get("workflow_id")
    sections_format = event.get("sections_format")
    validation_error = event.get("validation_error")

    logger.info(validation_error)

    cause = json.loads(validation_error.get('Cause'))

    error_messages = cause['errorMessage']

    # 修正リクエストと処理を行う    
    # response_graphs, response_tables, response_formulas = [], [], []

    # for section in sections_format:
    #     for sub_section in section.get('sub_sections', []):
    #         response_graphs.extend(sub_section.get('graphs', []))
    #         response_tables.extend(sub_section.get('tables', []))
    #         response_formulas.extend(sub_section.get('formulas', []))

    # # スキーマファイルを読み込み
    # formulas_schema_json, tables_schema_json, graphs_schema_json = read_schema_jsons()


    return {
        'statusCode': 200,
        'body': {
            "workflow_id" : workflow_id,
            "title" : title,
            "abstract" : abstract,
            "sections_format" : sections_format,
        }
    }