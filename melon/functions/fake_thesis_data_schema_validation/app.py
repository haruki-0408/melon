import json
import re
from aws_lambda_powertools.utilities.validation import validate, SchemaValidationError
from utilities import extract_schemas

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
    system_prompt = event["system_prompt"]
    response_format = event["response_format"]

    response_graphs, response_tables, response_formulas = [], [], []

    for section in response_format:
        for sub_section in section['sub_sections']:
            response_graphs.extend(sub_section['graphs'])
            response_tables.extend(sub_section['tables'])
            response_formulas.extend(sub_section['formulas'])

    formulas_schema, graphs_schema, tables_schema = extract_schemas(system_prompt)

    try:
        validate(event={"formulas": response_formulas}, schema=formulas_schema)
        validate(event={"graphs": response_graphs}, schema=graphs_schema)
        validate(event={"tables": response_tables}, schema=tables_schema)
    except SchemaValidationError as e:
        raise Exception(f"Schema validation failed: {str(e)}")

    return {
        "response_graphs": response_graphs,
        "response_tables": response_tables,
        "response_formulas": response_formulas
    }

def extract_schemas(system_prompt):
    """
    システムプロンプトからFormulas Schema、Graphs Schema、Tables Schemaを抽出し、
    JSON形式でパースして返す関数。

    Parameters:
    - system_prompt (str): システムプロンプトの文字列

    Returns:
    - tuple: (formulas_schema, graphs_schema, tables_schema)
      各スキーマをJSON形式でパースしたオブジェクトを返す
    """
    # 正規表現パターン
    schema_patterns = {
        "formulas_schema": r"#### Formulas Schema\s*({.*?})\s*(?=####|$)",
        "graphs_schema": r"#### Graphs Schema\s*({.*?})\s*(?=####|$)",
        "tables_schema": r"#### Tables Schema\s*({.*?})\s*(?=####|$)",
    }

    # 抽出とパース
    extracted_schemas = {}
    for key, pattern in schema_patterns.items():
        match = re.search(pattern, system_prompt, re.DOTALL)
        if match:
            schema_str = match.group(1).strip()  # マッチしたスキーマ部分を取得
            
            # 改行や余分な空白を1つのスペースに変換
            cleaned_text = re.sub(r"\s+", " ", schema_str.strip())  # 改行や余分な空白を1つのスペースに変換
            extracted_schemas[key] = json.loads(cleaned_text)
        else:
            raise ValueError(f"{key} not found in the system prompt")

    return (
        extracted_schemas.get("formulas_schema"),
        extracted_schemas.get("graphs_schema"),
        extracted_schemas.get("tables_schema"),
    )