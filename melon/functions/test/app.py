import re
import json
import os
import io

def lambda_handler(event, context):
    try:
        system_prompt = event['system_prompt']
        formulas_schema, graphs_schema, tables_schema = extract_schemas(system_prompt)
        
        print(formulas_schema)
        print('------=---')
        print(graphs_schema)
        print(tables_schema)
    except ValueError as e:
        print("Error:", e)


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

