import json
import os
import boto3
from aws_lambda_powertools.utilities.validation import validator
from aws_lambda_powertools.utilities.validation import SchemaValidationError
from melon.layers.common.utilities import get_dynamo_item, get_logger, upload_to_s3
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
        category_type_jp = format_data["category_type_jp"]

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
    
        section_formats = []
    
        # システムプロンプト文章を生成
        system_prompt = generate_system_prompt(
            title=title,
            category_type_jp=category_type_jp,
            formulas_schema=formulas_schema_json,
            graphs_schema=graphs_schema_json,
            tables_schema=table_schema_json
        )
        
        for section in sections:
            section_title = section.get('title_name', '')
            print(section_title)
            
            # プロンプトを配列に追加
            section_formats.append(section)
            
        # SQSにメッセージを送信
        # sqs.send_message(
        #     QueueUrl=sqs_queue_url,
        #     MessageBody=json.dumps({
        #         'title': title,
        #         'prompt': prompts
        #     })
        # )

        prompts = {
            "title" : title,
            "system_prompt" : system_prompt,
            "section_formats" : section_formats
        } 
        
        upload_to_s3(bucket_name="fake-thesis-bucket",object_key="prompts.json",data=json.dumps(prompts, ensure_ascii=False))

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

def generate_system_prompt(title, category_type_jp, formulas_schema, graphs_schema, tables_schema):
    """
    生成AIに送るプロンプト文章を生成する関数
    """
    system_prompt = f"""
あなたはタイトルから面白くユーモアのある偽の論文を構成する専門家です。それぞれのセクション毎のフォーマットオブジェクトを内容として添付します。
これから各セクションフォーマット毎に分割して生成をリクエストしますが、論文として論理的に一貫性があるように考慮してください。
それでは以下指示に従いながら添付したセクションのフォーマットオブジェクト内に追記し、レスポンスとして追記したオブジェクト形式をJSONパース可能なテキストのみで返却してください。

### 要件 
- 各サブセクションそれぞれに必ず以下のプロパティを追加してください。: "text", "graphs", "tables", "formulas"。
- 論文全体として必ず２つ以上グラフ、数式、表を含めてください。
- "text" プロパティには偽論文のタイトルとサブセクションの"title_name"を考慮した学術論文風の文章を記載してください。文字数は長めに設定し、改行コードや段落を適切に含めてください。
- 偽の内容であることを活かしつつ、論文にリアルさを持たせることを目的とし、閲覧者が興味を惹かれるようなユーモアある面白い内容にしてください。
- 各サブセクションにグラフ、表、数式が必要な場合、"text" 内に挿入位置を示す識別子を含めてください。（例: [INSERT_FORMULA_HOGEHOGE]とするとFORMULA_HOGEHOGEというidを持つ数式データの挿入という意味、数式を表す場合はFORMULA_大文字英数字、グラフを表す場合はGRAPH_大文字英数字、表を表す場合はTABLE_大文字英数字　として大文字英数字は各セクション間で重複がないようにランダムにしてください）
- 必ずしもサブセクション毎にグラフ、表、数式を含める必要はありません。サブセクションの内容に応じて適切に選択してください。挿入する場合必ず挿入識別子を含めた"text"と同じサブセクション内の"graphs"、"tables"、"formulas"それぞれに詳細なデータを以下の各jsonスキーマを厳格に満たすように設定し、各idを"text"内の識別子とリンクさせてください。必要ない場合でも、空の配列としてgraphs,tables,formulasプロパティを含めてください。
- 例えば1つ目のサブセクションの"text"で"[INSERT_FORMULA_HOGEHOGE]"とすると、必ずそのサブセクション内のformulasプロパティにデータを設定してください。
- グラフ、表、数式を含める場合は"text"内でそのデータに言及してください。形式は下記jsonスキーマを必ず遵守すること。
- グラフ、表、数式データをgraphs,tables,formulas内に定義したならば"text"内に挿入位置を示す識別子を必ず入れてください。挿入位置識別子がなくgraphs,formulas,tablesにデータを入れることは許可しません。
- 必ずタイトルとセクションとサブセクションに合うように内容を構成し一貫性のある論文にしてください。
- レスポンスは JSON パース可能な文字列のみで、セクションフォーマット1オブジェクトに追記した形で出力してください。
- 返却されたレスポンスの内容をそのままjsonにパースするので絶対に前後に不要な「```json」 などの文章を入れてレスポンスすることは許可しません。回答の出力は必ずjsonデータのみであることに注意してください。

### 偽論文タイトル
{title}

### 論文のカテゴリ
{category_type_jp}

### 各データのjsonスキーマ
#### Formulas Schema
{formulas_schema}

#### Graphs Schema
{graphs_schema}

#### Tables Schema
{tables_schema}

"""

    ### section object
    return system_prompt