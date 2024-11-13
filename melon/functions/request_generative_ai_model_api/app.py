import json
import os
import requests

# envパラメータ
API_URL = os.environ["ANTHROPIC_API_URL"]
API_KEY = os.environ["ANTHROPIC_API_KEY"]
API_MODEL = os.environ["ANTHROPIC_API_MODEL"]

def lambda_handler(event, context):
    # eventパラメータ
    prompts = event.get(prompts)  

    # 結果を格納するためのリスト
    results = []
    previous_response_text = None  # 直前の返答を格納する変数

    # 各プロンプトについて生成AI APIを呼び出し
    for prompt_info in prompts:
        section_title = prompt_info["section_title"]
        sub_section_title = prompt_info["sub_section_title"]
        prompt = prompt_info["prompt"]

        # 生成AI API呼び出し（前の返答も含める）
        response = call_anthropic_api(prompt, previous_response_text)
        generated_text = response.get("text", "")

        # 直前の返答テキストを更新
        previous_response_text = generated_text

        # 各セクションのレスポンスを統合
        results.append({
            "section_title": section_title,
            "sub_section_title": sub_section_title,
            "response": response  # text, figures, tables, formulasのデータ
        })

    # 最終的なレスポンス
    return {
        'statusCode': 200,
        'body': json.dumps(results, ensure_ascii=False)
    }

# Anthropic APIを呼び出す関数
def call_anthropic_api(prompt, previous_response=None):
    headers = {
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json"
    }

    # 直前の返答を含めてプロンプトを構成
    input_prompt = prompt
    if previous_response:
        input_prompt = f"{previous_response}\n\n{prompt}"

    body = {
        "model": API_MODEL,
        "max_tokens": 4096,
        "system" : "",
        "temperature": 0.7,
        "messages" : messages,
    }

    # APIリクエストを送信し、エラーがあれば例外を発生
    response = requests.post(API_URL, headers=headers, json=body, timeout=300)
    response.raise_for_status()  # ステータスコードが200以外の場合、例外を発生させる
    
    # 正常なレスポンスを返す
    return response.json()