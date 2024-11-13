import json
import os
from aws_lambda_powertools.utilities.validation import validator
from aws_lambda_powertools.utilities.validation import SchemaValidationError
from utilities import get_dynamo_item, get_logger
import melon.functions.generate_prompt_parameters.schemas as schemas

logger = get_logger(service_name="get_fake_thesis_title_category_format")

@logger.inject_lambda_context(log_event=True)
@validator(inbound_schema=schemas.INPUT)
def lambda_handler(event, context):
    try:
        # イベントからタイトルとフォーマットを取得
        title = event.get("title")
        category_format = event.get("format")
        
        # フォーマットからカテゴリタイプとセクション情報を取得
        category_type_jp = category_format["category_type_jp"]
        sections = category_format["sections"]

        prompts = []

        # プロンプトを構築
        # セクションごとにプロンプトを生成
        for section in sections:
            section_title = section.get("title_name")
            for sub_section in section.get("sub_sections", []):
                sub_section_title = sub_section.get("title_name")
                
                # セクション・サブセクション単位のプロンプト作成
                prompt = (
                    f"以下の論文のサブセクション部分を作成してください:\n"
                    f"論文タイトル: {title}\n"
                    f"カテゴリ: {category_type_jp}\n"
                    f"セクション: {section_title}\n"
                    f"サブセクション: {sub_section_title}\n\n"
                    "必ず結果は下記サンプルに提示したJSON形式で提供してください:\n"
                    "- **text(string, required)**: 各サブセクションの詳細な説明文\n"
                    "- **figures(array, optional)**: 各サブセクションの text に関連する図（チャート、グラフ、画像など）に関する情報（生成するためのデータや形式を含む）\n"
                    "- **tables(array, optional)_**: 各サブセクションの  text に関連する表に関する情報（列名、行データなど）\n"
                    "- **formulas(array, optional)**: 各サブセクションの text に関連する数式\n"
                )

                # JSONレスポンスの構造を示すための例を構築
                example_json_structure = {
                        {
                            "title_name": section.get("title_name"),
                            "sub_sections": [
                                {
                                    "title_name": sub_section.get("title_name"),
                                    "text": "ここにサブセクションの詳細な内容を入力",
                                    "figures": [
                                        {
                                            "name": "figure_1",
                                            "type": "chart",
                                            "data": {
                                                "x": [1, 2, 3],
                                                "y": [10, 20, 30],
                                                "title": "Sample Chart"
                                            }
                                        },
                                        {
                                            "name": "figure_2",
                                            "type": "graph",
                                            "data": {
                                                "nodes": ["A", "B", "C"],
                                                "edges": [["A", "B"], ["B", "C"]],
                                                "title": "Sample Graph"
                                            }
                                        },
                                    ],
                                    "tables": ["ここに表に関する情報（列名、行データなど）を入力"],
                                    "formulas": ["ここに必要な数式を入力"]
                                }
                                for sub_section in section.get("sub_sections", [])
                            ]
                        }
                }

                # プロンプトにJSONの構造例を追加
                prompt += f"{json.dumps(example_json_structure, ensure_ascii=False, indent=2)}\n\n"

                # 各プロンプトをリストに追加
                prompts.append({
                    "section_title": section_title,
                    "sub_section_title": sub_section_title,
                    "prompt": prompt
                })

    except SchemaValidationError as e:
        logger.error(f"Schema validation failed: {e}")
        return {
            "statusCode": 400,
            "body": {"error": str(e)}
        }

    return {
        'statusCode': 200,
        'body': {
            'prompt': prompts
        }
    }    