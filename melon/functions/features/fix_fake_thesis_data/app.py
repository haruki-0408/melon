import json

from aws_lambda_powertools import Logger

from anthropic_client import AnthropicClient

logger = Logger(service_name="request_generative_ai_model_api")

# 生成AI リクエストインスタンス生成
client = AnthropicClient()  

@logger.inject_lambda_context(log_event=False)
def lambda_handler(event, context):
    """
    修正を促す生成AIリクエストを実行するLambda関数。
    """
    title = event.get("title")
    abstract = event.get("abstract")
    workflow_id = event.get("workflow_id")
    sections_format = event.get("sections_format")
    errors = event.get("errors")

    # 修正リクエストと処理を行う    

    return {
        'statusCode': 200,
        'body': {
            "workflow_id" : workflow_id,
            "title" : title,
            "abstract" : abstract,
            "serctions_format" : sections_format,
        }
    }