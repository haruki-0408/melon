import json
import re
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.validation import validate, SchemaValidationError
from utilities import upload_to_s3

# スキーマファイルのパスを設定
FORMULAS_SCHEMA = '/opt/python/schemas/formulas_schema.json'
GRAPHS_SCHEMA = '/opt/python/schemas/graphs_schema.json'
TABLES_SCHEMA = '/opt/python/schemas/tables_schema.json'

LOGGER_SERVICE = "fake_thesis_data_validation"
logger = Logger(service=LOGGER_SERVICE)

@logger.inject_lambda_context(log_event=False)
def lambda_handler(event, context):
    """
    スキーマバリデーションを実行するLambda関数。

    Parameters:
    - event (dict): イベントデータ。
      - system_prompt (str): システムプロンプト。
      - response_format (list): 各セクションの生成AIレスポンス。

    Returns:
    - dict: バリデーション成功データ。
    """
    workflow_id = event.get("workflow_id")
    sections_format = event["sections_format"]

    response_graphs, response_tables, response_formulas = [], [], []

    for section in sections_format:
        for sub_section in section['sub_sections']:
            response_graphs.extend(sub_section['graphs'])
            response_tables.extend(sub_section['tables'])
            response_formulas.extend(sub_section['formulas'])

    # スキーマファイルを読み込む
    with open(FORMULAS_SCHEMA, 'r', encoding='utf-8') as f:
        formulas_schema_json = json.loads(f.read())
    with open(GRAPHS_SCHEMA, 'r', encoding='utf-8') as f:
        graphs_schema_json = json.loads(f.read())
    with open(TABLES_SCHEMA, 'r', encoding='utf-8') as f:
        table_schema_json = json.loads(f.read())

    try:
        validate(event={"formulas": response_formulas}, schema=formulas_schema_json)
        validate(event={"graphs": response_graphs}, schema=graphs_schema_json)
        validate(event={"tables": response_tables}, schema=table_schema_json)
    except SchemaValidationError as e:
        logger.exception()
        raise Exception(f"Schema validation failed: {str(e)}")

    # 仮S3データ保存
    upload_to_s3(bucket_name="fake-thesis-bucket",object_key=f"{workflow_id}/responses_graphs.json",data=json.dumps(response_graphs, ensure_ascii=False))
    upload_to_s3(bucket_name="fake-thesis-bucket",object_key=f"{workflow_id}/responses_tables.json",data=json.dumps(response_tables, ensure_ascii=False))
    upload_to_s3(bucket_name="fake-thesis-bucket",object_key=f"{workflow_id}/responses_formulas.json",data=json.dumps(response_formulas, ensure_ascii=False))

    return {
        'statusCode': 200,
        'body': {
            "graphs": response_graphs,
            "tables": response_tables,
            "formulas": response_formulas
        }
    }

# def extract_schemas(system_prompt):
#     """
#     システムプロンプトからFormulas Schema、Graphs Schema、Tables Schemaを抽出し、
#     JSON形式でパースして返す関数。

#     Parameters:
#     - system_prompt (str): システムプロンプトの文字列

#     Returns:
#     - tuple: (formulas_schema, graphs_schema, tables_schema)
#       各スキーマをJSON形式でパースしたオブジェクトを返す
#     """
#     # 正規表現パターン
#     schema_patterns = {
#         "formulas_schema": r"#### Formulas Schema\s*({.*?})\s*(?=####|$)",
#         "graphs_schema": r"#### Graphs Schema\s*({.*?})\s*(?=####|$)",
#         "tables_schema": r"#### Tables Schema\s*({.*?})\s*(?=####|$)",
#     }

#     # 抽出とパース
#     extracted_schemas = {}
#     for key, pattern in schema_patterns.items():
#         match = re.search(pattern, system_prompt, re.DOTALL)
#         if match:
#             schema_str = match.group(1).strip()  # マッチしたスキーマ部分を取得
            
#             # 改行や余分な空白を1つのスペースに変換
#             cleaned_text = re.sub(r"\s+", " ", schema_str.strip())  # 改行や余分な空白を1つのスペースに変換
#             extracted_schemas[key] = json.loads(cleaned_text)
#         else:
#             raise ValueError(f"{key} not found in the system prompt")

#     return (
#         extracted_schemas.get("formulas_schema"),
#         extracted_schemas.get("graphs_schema"),
#         extracted_schemas.get("tables_schema"),
#     )