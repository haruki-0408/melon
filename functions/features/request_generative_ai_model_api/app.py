import json
import os
from aws_lambda_powertools import Logger, Tracer
from anthropic_client import AnthropicClient
from utilities import record_workflow_progress_event

# envパラメータ
WORKFLOW_EVENT_BUS_NAME = os.environ["WORKFLOW_EVENT_BUS_NAME"]

STATE_NAME = "ai-request-lambda"
STATE_ORDER = 5

# 生成AI リクエストインスタンス生成
client = AnthropicClient()  

logger = Logger()
tracer = Tracer()

@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def lambda_handler(event, context):
    """
    生成AIモデルAPIにリクエストを送信するLambda関数
    """

    workflow_id = event.get('workflow_id')
    print(f"WorkflowId: {workflow_id}")
    
    # デフォルトは成功
    error = None

    try:
        # eventパラメータ
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
            is_last = (idx == len(sections) - 1)

            # 各セクションのプロンプトを準備
            content_text = json.dumps(section, ensure_ascii=False)

            # 最終セクションの場合、締めくくりの言葉を追加
            if is_last:
                closing_statement = "フォーマット内のテキストの最終行にこの研究の結論をまとめるような締めの文章を作成してフォーマット内に挿入してほしいです。\n"
                # closing_statement += "[優先事項]さらにあえてこのセクションではgraphs, tables, formulas データのスキーマバリデーションが引っかかるようにわざとデータをスキーマに合わないようにしてほしいです。回答レスポンスは必ずjsonのみでコメントなどは挿入しないでください"
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
            
            print("==== assistant_response ====")
            logger.info(assistant_response)

            response_format.append(json.loads(assistant_response))

            messages.append({
                "role" : "assistant",
                "content" : assistant_response
            })
        
        # 論文のまとめ要旨作成
        abstract_prompt = "生成してくれた各セクションを簡潔にまとめた論文の要旨文章をテキスト形式で作成してください。文字数は300文字以上600文字以下で内容を簡潔にまとめたものにしてください。レスポンスは必ずjson形式でなく改行コードを含めたテキスト形式にしてください。" 
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
        
        print("==== abstract_response ====")
        logger.info(abstract_response)
        
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
            raise Exception(error)

    return {
        'statusCode': 200,
        'body': {
            "workflow_id" : workflow_id,
            "title" : title,
            "abstract" : abstract_response,
            "sections_format" : response_format
        }
    }
