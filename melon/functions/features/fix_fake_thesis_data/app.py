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

    Parameters:
    - event (dict): イベントデータ。
      - system_prompt (str): システムプロンプト。
      - messages (list): 現在までの会話履歴。
      - error_details (str): バリデーションエラー詳細メッセージ。

    Returns:
    - dict: 修正版レスポンス。
    """
    system_prompt = event["system_prompt"]
    messages = event["messages"]
    error_details = event["error_details"]

    correction_prompt = f"以下のエラーを修正してください: {error_details}. 修正版を提供してください。"
    messages.append({
        "role": "user",
        "content": [{"type": "text", "text": correction_prompt}]
    })

    assistant_response = client.call_message_request(system_prompt=system_prompt, messages=messages)            

    response_format = json.loads(assistant_response)
    messages.append({"role": "assistant", "content": assistant_response})

    return {
        "response_format": response_format,
        "messages": messages
    }