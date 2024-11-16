import json
import os
import boto3
from aws_lambda_powertools.utilities.validation import validator
from aws_lambda_powertools.utilities.validation import SchemaValidationError
from utilities import get_dynamo_item, get_logger
import event_schemas as event_schemas

# スキーマファイルのパスを設定
SCHEMAS_DIR = os.path.join(os.path.dirname(__file__), 'schemas')
FORMULAS_SCHEMA = os.path.join(SCHEMAS_DIR, 'formulas_schema.json')
GRAPHS_SCHEMA = os.path.join(SCHEMAS_DIR, 'graphs_schema.json')
TABLES_SCHEMA = os.path.join(SCHEMAS_DIR, 'tables_schema.json')

# SQSクライアントを初期化
sqs = boto3.client('sqs')

logger = get_logger(service_name="get_fake_thesis_title_category_format")

@logger.inject_lambda_context(log_event=True)
@validator(inbound_schema=event_schemas.INPUT)
def lambda_handler(event, context):
    """
    各セクションごとに生成AIに送るプロンプト文章を作成し、SQSキューに送信するLambda関数
    """
    try:
        # タイトルとフォーマットを取得
        title = event.get('title', '')
        format_data = event.get('format', {})
        sections = format_data.get('sections', [])
        
        # スキーマファイルを読み込む
        with open(FORMULAS_SCHEMA, 'r', encoding='utf-8') as f:
            formulas_schema_json = f.read()
        with open(GRAPHS_SCHEMA, 'r', encoding='utf-8') as f:
            graphs_schema_json = f.read()
        with open(TABLES_SCHEMA, 'r', encoding='utf-8') as f:
            table_schema_json = f.read()
    
        # SQSキューのURLを取得（環境変数から取得する場合）
        # sqs_queue_url = os.environ.get('SQS_QUEUE_URL')
        # if not sqs_queue_url:
        #     raise ValueError('SQS_QUEUE_URL環境変数が設定されていません')
    
        prompts = []
    
        for section in sections:
            section_title = section.get('title_name', '')
            print(section_title)
            
            # プロンプト文章を生成
            prompt = generate_prompt(
                title=title,
                section_object=section,
                formulas_schema=formulas_schema_json,
                graphs_schema=graphs_schema_json,
                tables_schema=table_schema_json
            )
            
            # プロンプトを配列に追加
            prompts.append({
                'section_title': section_title,
                'prompt': prompt
            })
            
            # SQSにメッセージを送信
            # sqs.send_message(
            #     QueueUrl=sqs_queue_url,
            #     MessageBody=json.dumps({
            #         'title': title,
            #         'prompt': prompts
            #     })
            # )
        
        f = open('prompts.json', 'w')

        f.write(prompts)

        f.close()

        return {
            'statusCode': 200,
            'body': "Success"
        }
    
    except Exception as e:
        error = {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "payload": event
        }
        logger.error(error)
        return {
            'statusCode': 500,
            'body': error
        }

def generate_prompt(title, section_object, formulas_schema, graphs_schema, tables_schema):
    """
    生成AIに送るプロンプト文章を生成する関数
    """
    prompt = f"""
以下のオブジェクト形式は偽の論文を構成するそれぞれのセクションオブジェクトの１つです。
以下指示に従いながらオブジェクト内に追記し、レスポンスとして追記したオブジェクト形式をJSONパース可能なテキストのみで返却してください。

### 要件
- 各サブセクションそれぞれに必ず以下のプロパティを追加してください。: "text", "graphs", "tables", "formulas"。
- "text" は偽論文のタイトルとサブセクションの"title_name"を考慮した学術論文風の文章にしてください。文字数は長めに設定し、改行コードや段落を適切に含めてください。嘘の論文ですが、読者が納得するような説得力のある内容にしてください。
- 各サブセクションにグラフ、表、数式が必要な場合、"text" 内に挿入位置を示す識別子を含めてください（例: [INSERT_FORMULA_1]とするとFORMULA_1というidを持つ数式データの挿入という意味）。
- 必ずしもグラフ、表、数式を含める必要はありません。サブセクションの内容に応じて適切に選択してください。挿入する場合は、"graphs"、"tables"、"formulas"それぞれに実際使用するデータの値を以下のjsonスキーマを厳格に満たすように設定し、各idを"text"内の識別子とリンクさせてください。必要ない場合でも、空の配列としてこれらのキーを含めてください。
- グラフ、表、数式を含める場合は"text"にてそのデータを言及するような内容を必ず含めてください。
- レスポンスは JSON パース可能な文字列で、セクション1オブジェクトとして出力してください。
- 嘘論文をそれっぽく見せるというコンセプトなので全体的に信憑性が高い学術論文のように作成してください。

### section object
{section_object}

### 偽論文タイトル
{title}

### スキーマ
#### Formulas Schema
{formulas_schema}

#### Graphs Schema
{graphs_schema}

#### Tables Schema
{tables_schema}

"""

    return prompt