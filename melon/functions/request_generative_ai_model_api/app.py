import json
import time
import os
import random
import anthropic
from anthropic.types.beta.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.beta.messages.batch_create_params import Request
from utilities import upload_to_s3

# envパラメータ
API_URL = os.environ["ANTHROPIC_API_URL"]
API_MODEL = os.environ["ANTHROPIC_API_MODEL"]

client = anthropic.Anthropic(api_key = os.environ["ANTHROPIC_API_KEY"])

def lambda_handler(event, context):
    # eventパラメータ
    title = event.get("title")  
    system_prompt = event.get("system_prompt")  
    section_formats = event.get("section_formats")

    # 各プロンプトについて生成AI APIを呼び出し

    # 会話のやり取りを保持する配列
    response_format = []
    messages = []
    for section_format in section_formats:
        section_title = section_format["title_name"]
        print(section_title)
        
        # 各セクションのプロンプトを追加
        messages.append(
            {
                "role" : "user",
                "content" : [
                    {
                        "type" : "text",
                        "text" : json.dumps(section_format,ensure_ascii=False)
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

        try:
            # 生成AI API呼び出し（前の返答も含める）
            assistant_response = call_anthropic_api_message_request(system_prompt=system_prompt, messages=messages_to_send)
        except anthropic.APIConnectionError as e:
            print("The server could not be reached")
            print(e.__cause__)  # an underlying Exception, likely raised within httpx.
        except anthropic.RateLimitError as e:
            print("A 429 status code was received; we should back off a bit.")
        except anthropic.APIStatusError as e:
            print("Another non-200-range status code was received")
            print(e.status_code)
            print(e.response)
        

        response_format.append(json.loads(assistant_response))

        messages.append({
            "role" : "assistant",
            "content" : assistant_response
        })
    
    # 論文のまとめ要旨作成
    abstract_prompt = "生成してくれた各セクションを簡潔にまとめた論文の要旨文章をテキスト形式で作成してください。文字数は300文字以上で内容を簡潔にまとめたものにしてください。レスポンスは必ずjson形式でなく改行コードを含めたテキスト形式にしてください。" 
    abstract_response = call_anthropic_api_message_request(system_prompt=abstract_prompt, messages=[])
    print('--- 要旨 ---')
    print(abstract_response)
    print('------------')

    # 最終的なレスポンス
    response_graphs = []
    response_tables = []
    response_formulas = []

    for section in response_format:
        for sub_section in section['sub_sections']:
            response_graphs.extend(sub_section['graphs'])
            response_tables.extend(sub_section['tables'])
            response_formulas.extend(sub_section['formulas'])
    
    # 分かりやすいようにS3に保存
    upload_to_s3(bucket_name="fake-thesis-bucket",object_key="responses.json",data=json.dumps(response_format, ensure_ascii=False))
    upload_to_s3(bucket_name="fake-thesis-bucket",object_key="responses_graphs.json",data=json.dumps(response_graphs, ensure_ascii=False))
    upload_to_s3(bucket_name="fake-thesis-bucket",object_key="responses_tables.json",data=json.dumps(response_tables, ensure_ascii=False))
    upload_to_s3(bucket_name="fake-thesis-bucket",object_key="responses_formulas.json",data=json.dumps(response_formulas, ensure_ascii=False))

    return {
        'statusCode': 200,
        'body': {
            "title" : title,
            "graphs": response_graphs,
            "tables": response_tables,
            "abstract" : abstract_response,
            "formulas": response_formulas,
            "sections_format" : response_format
        }
    }

# Anthropic APIを呼び出す関数
def call_anthropic_api_message_request(system_prompt, messages):
    response = client.beta.prompt_caching.messages.create(
        model=API_MODEL,
        max_tokens=4096,
        system=[
            {
                "type": "text",
                "text": system_prompt,
                "cache_control": {"type": "ephemeral"}
            }
        ],
        messages=messages
    )
    print(response)
    print(f"Usage: {response.usage}")

    assistant_response = response.content[0].text
    
    return assistant_response
    

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
            temperature = 0.1,
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
