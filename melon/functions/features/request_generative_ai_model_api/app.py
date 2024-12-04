import json
from aws_lambda_powertools import Logger
from anthropic_client import AnthropicClient
from utilities import upload_to_s3

logger = Logger(service_name="request_generative_ai_model_api")

# 生成AI リクエストインスタンス生成
client = AnthropicClient()  

@logger.inject_lambda_context(log_event=False)
def lambda_handler(event, context):
    try:
        # eventパラメータ
        workflow_id = event.get("workflow_id")
        title = event.get("title")  
        system_prompt = event.get("system_prompt")  
        sections_format = event.get("sections_format")
        sections = sections_format.get("sections")

        # 生成AIからのレスポンスを保持するリスト
        response_format = []

        # 会話のやり取りを保持するリスト
        messages = []
        for idx, section in enumerate(sections):
            section_title = section["title_name"]
            print(f"====== セクション: {section_title} ======")

            # 最後のセクションかどうかを判定
            is_last = (idx == len(sections_format) - 1)

            # 各セクションのプロンプトを準備
            content_text = json.dumps(section, ensure_ascii=False)

            # 最終セクションの場合、締めくくりの言葉を追加
            if is_last:
                closing_statement = "フォーマット内のテキストの最終行にこの研究の結論をまとめるような締めの文章を作成してフォーマット内に挿入してほしいです。"
                content_text += f"\n\n{closing_statement}"

            # プロンプトを追加
            messages.append(
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": content_text
                        }
                    ]
                }
            )

            # 最近2件のユーザーメッセージのみキャッシュコントロールを有効化する
            result = []
            user_turns_processed = 0
            for message in reversed(messages):
                if message["role"] == "user" and user_turns_processed < 2:
                    result.append({
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": message["content"][0]["text"],
                                "cache_control": {"type": "ephemeral"}
                            }
                        ]
                    })
                    user_turns_processed += 1
                else:
                    result.append(message)

            # 順番を下に戻す
            messages_to_send = list(reversed(result))

            # 生成AI API呼び出し（前の返答も含める）
            assistant_response = client.call_message_request(system_prompt=system_prompt, messages=messages_to_send)            

            response_format.append(json.loads(assistant_response))

            messages.append({
                "role" : "assistant",
                "content" : assistant_response
            })
        
        # 論文のまとめ要旨作成
        abstract_prompt = "生成してくれた各セクションを簡潔にまとめた論文の要旨文章をテキスト形式で作成してください。文字数は300文字以上600文字以下で内容を簡潔にまとめたものにしてください。レスポンスは必ずjson形式でなく改行コードを含めたテキスト形式にしてください。" 
        print(f"====== 要旨 ======")
        messages.append(
            {
                "role" : "user",
                "content" : [
                    {
                        "type" : "text",
                        "text" : abstract_prompt
                    }
                ]
            }
        )

        abstract_response = client.call_message_request(system_prompt=abstract_prompt, messages=messages)
        
        # 分かりやすいようにS3に保存
        # upload_to_s3(bucket_name="fake-thesis-bucket",object_key=f"{workflow_id}/responses.json",data=json.dumps({
        #     "title" : title,
        #     "abstract" : abstract_response,
        #     "sections_format" : response_format
        # }, ensure_ascii=False))

    # except anthropic.APIConnectionError as e:
    #     logger.exception("The server could not be reached")

    #     return {
    #         'statusCode': 500,
    #         'body': e   
    #     }
    # except anthropic.RateLimitError as e:
    #     logger.exception("A 429 status code was received; we should back off a bit.")

    #     return {
    #         'statusCode': 429,
    #         'body': e
    #     }
    except Exception as e:
        error = {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "payload": event
        }
        logger.exception(error)

        raise e

    return {
        'statusCode': 200,
        'body': {
            "workflow_id" : workflow_id,
            "title" : title,
            "abstract" : abstract_response,
            "sections_format" : response_format
        }
    }
