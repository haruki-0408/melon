import json
import time
import os
import requests
import random
import anthropic
from anthropic.types.beta.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.beta.messages.batch_create_params import Request

# envパラメータ
API_URL = os.environ["ANTHROPIC_API_URL"]
# API_KEY = os.environ["ANTHROPIC_API_KEY"]
API_MODEL = os.environ["ANTHROPIC_API_MODEL"]

client = anthropic.Anthropic(api_key = os.environ["ANTHROPIC_API_KEY"])

def lambda_handler(event, context):
    # eventパラメータ
    prompts = event.get("prompts")  

    # AnthropicAPI バッジリクエストを送信するための配列
    requests = []

    # 各プロンプトについて生成AI APIを呼び出し
    for prompt_info in prompts:
        section_title = prompt_info["section_title"]
        print(section_title)
        prompt = prompt_info["prompt"]

        # 生成AI API呼び出し（前の返答も含める）
        request = genearte_anthropic_message_batch_request(prompt)

        requests.append(request)
    
    # バッジリクエスト送信
    message_batch_id = create_anthropic_message_batch_request(requests=requests)
    
    # 成功するまでポーリング
    retrieve_anthropic_message_batch_request(message_batch_id=message_batch_id)

    # 結果取得
    results = get_result_anthropic_message_batch_request(results)

    # すべてのバッジリクエストをキャンセル
    # cancel_anthropic_message_batch_request()

    # 最終的なレスポンス
    return {
        'statusCode': 200,
        'body': 'cancel 成功'
    }

# Anthropic APIを呼び出す関数
# def call_anthropic_api(prompt_text, previous_response=None):
#     headers = {
#         "x-api-key": API_KEY,
#         "anthropic-version": "2023-06-01",
#         "anthropic-beta": "message-batches-2024-09-24",
#         "Content-Type": "application/json"
#     }

#     # 直前の返答を含めてプロンプトを構成
#     # input_prompt = prompt
#     # if previous_response:
#     #     input_prompt = f"{previous_response}\n\n{prompt}"

#     body = {
#         "model": API_MODEL,
#         "max_tokens": 4096,
#         "system" : "",
#         "temperature": 0.4,
#         "messages" : [
#             {
#                 "role" : "user",
#                 "content" : prompt_text
#             }
#         ]
#     }

#     # APIリクエストを送信し、エラーがあれば例外を発生
#     response = requests.post(API_URL, headers=headers, json=body, timeout=360)
#     response.raise_for_status()  # ステータスコードが200以外の場合、例外を発生させる
    
#     # 正常なレスポンスを返す
#     # print(response.json)
#     response_json = response.json()
    
#     text = response_json['content'][0]['text']

#     text_parsed = json.loads(text)
#     return text_parsed
    

# メッセージバッチリクエスト生成関数
def genearte_anthropic_message_batch_request(prompt):
    # カスタムID生成
    custom_id = "message_" + str(random.randint(1, 10000))

    request = Request(
        custom_id = custom_id,
        params = MessageCreateParamsNonStreaming(
            model = API_MODEL,
            max_tokens = 4096,
            system = "",
            temperature = 0.4,
            messages = [
                {
                    "role" : "user",
                    "content" : prompt
                }
            ]
        )
    )

    return request

# Anthropic メッセージバッチ作成APIを呼び出す関数
def create_anthropic_message_batch_request(requests):
    response = client.beta.messages.batches.create(requests=requests)
    # response = requests.post(, headers=headers, json=body, timeout=360)
    # response.raise_for_status()  # ステータスコードが200以外の場合、例外を発生させる
    
    # 正常なレスポンスを返す
    # print(response.json)
    # print(content)
    
    # text = response_json['content'][0]['text']

    # text_parsed = json.loads(text)
    return response.id

# Anthropic メッセージバッチ作成APIの進捗を確認する関数
def retrieve_anthropic_message_batch_request(message_batch_id):
    
    while True:
        response = client.beta.messages.batches.retrieve(message_batch_id)

        if response.processing_status == "ended":
            break
            
        print(f"Batch {message_batch_id} is still processing...")
        time.sleep(60)

    print(response)
    print(f"Batch {message_batch_id} is succeeded")

    return  


# Anthropic メッセージバッチ作成APIの結果を取得する関数
def get_result_anthropic_message_batch_request(message_batch_id):
    results = []
    # Stream results file in memory-efficient chunks, processing one at a time
    for result in client.beta.messages.batches.results(
        message_batch_id,
    ):
        results.appned(result)

    return results

# Anthropic メッセージバッチ作成APIをすべてキャンセルする関数
def cancel_anthropic_message_batch_request():
    for message_batch in client.beta.messages.batches.list(
        limit=20
    ):
        print('--- キャンセル前取得結果 ---')
        print(message_batch)
        cancel_message_batch = client.beta.messages.batches.cancel(
            message_batch_id=message_batch.id,
        )
        print('--- キャンセル結果 ---')
        print(cancel_message_batch)
        
    return 
