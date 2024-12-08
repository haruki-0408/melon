import json
from aws_lambda_powertools import Logger
from anthropic_client import AnthropicClient
from utilities import read_schema_jsons

logger = Logger(service_name="fix_fake_thesis_data")

# 生成AI リクエストインスタンス生成
client = AnthropicClient()

@logger.inject_lambda_context(log_event=False)
def lambda_handler(event, context):
    """
    修正を促す生成AIリクエストを実行するLambda関数。
    """
    try:
        # イベント情報の取得
        retry_count = event.get("retry_count") #リトライ回数取得(表示用)
        title = event.get("title")
        abstract = event.get("abstract")
        workflow_id = event.get("workflow_id")
        sections_format = event.get("sections_format")
        validation_error = event.get("validation_error")

        # Validation Error 解析
        validation_error_data = json.loads(validation_error.get('Cause'))
        error_details = validation_error_data.get('errorMessage')  # 例: {"graphs": "エラーメッセージ"}

        print('====== retry_count ========')
        print(f"{retry_count}回目")

        print('====== error_details ========')
        logger.info(error_details)

        # スキーマファイルを読み込み
        formulas_schema_json, tables_schema_json, graphs_schema_json = read_schema_jsons()

        # 修正リクエストの準備
        target_data = {
            "graphs": extract_target_data(sections_format, "graphs"),
            "tables": extract_target_data(sections_format, "tables"),
            "formulas": extract_target_data(sections_format, "formulas")
        }

        print('====== target_data ========')
        logger.info(target_data)

        # プロンプト生成（対象スキーマのみ含める）
        system_prompt = generate_system_prompt(
            graphs_schema=graphs_schema_json if "graphs" in error_details else None,
            tables_schema=tables_schema_json if "tables" in error_details else None,
            formulas_schema=formulas_schema_json if "formulas" in error_details else None,
            error_details=error_details
        )
        messages = generate_messages(target_data)

        # 生成AIに修正リクエスト
        assistant_response = client.call_message_request(system_prompt=system_prompt, messages=messages)

        # 修正されたデータを反映
        fixed_data = json.loads(assistant_response)

        print('====== fixed_data ========')
        logger.info(fixed_data)

        fixed_sections_format = update_sections_format(sections_format, fixed_data)

        # 最終結果を返却
        return {
            'statusCode': 200,
            'body': {
                "workflow_id": workflow_id,
                "title": title,
                "abstract": abstract,
                "sections_format": fixed_sections_format,
            }
        }

    except Exception as e:
        error = {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "payload": event
        }
        logger.exception(error)
        raise e


def extract_target_data(sections_format, data_type):
    """
    該当する sections_format 内のデータを抽出する。
    """
    target_data = []
    for section in sections_format:
        for sub_section in section.get('sub_sections', []):
            for item in sub_section.get(data_type, []):
                target_data.append(item)
    return target_data

def generate_system_prompt(graphs_schema, tables_schema, formulas_schema, error_details):
    """
    修正依頼のための system_prompt を生成する（日本語）。
    対象スキーマのみプロンプトに含める。
    """
    schemas = []
    if graphs_schema:
        schemas.append(f"グラフのスキーマ:\n{json.dumps(graphs_schema, indent=2, ensure_ascii=False)}\n")
    if tables_schema:
        schemas.append(f"テーブルのスキーマ:\n{json.dumps(tables_schema, indent=2, ensure_ascii=False)}\n")
    if formulas_schema:
        schemas.append(f"数式のスキーマ:\n{json.dumps(formulas_schema, indent=2, ensure_ascii=False)}\n")

    return (
        f"あなたはデータバリデーションの専門家です。以下のスキーマに基づきデータを修正してください。\n\n"
        + "\n".join(schemas)
        + f"\n次のバリデーションエラーが発生しました:\n{json.dumps(error_details, indent=2, ensure_ascii=False)}\n\n"
        f"対象のデータをスキーマに適合するように修正してください。元のデータの内容を極力変更せず、バリデーションエラーを解消してください。\n"
        f"注意: 回答は必ずJSON形式で、余計な文章を含めないでください。"
    )

def generate_messages(target_data):
    """
    生成AIに送信するメッセージを生成する（日本語）。
    """
    user_message = (
        f"以下のデータをスキーマに基づき修正してください。\n\n"
        f"対象データ:\n{json.dumps(target_data, indent=2, ensure_ascii=False)}\n\n"
        f"注意: 修正が必要なデータのみをkeyにgraphs,tables,formulas,を含めて値を各修正データの配列のオブジェクト形式JSONとして返してください。修正データが無い場合は各データを空配列で返却するようにしてください。それ以外のデータは含めないでください。\n"
    )
    return [{"role": "user", "content": user_message}]


def update_sections_format(sections_format, fixed_data):
    """
    修正されたデータを sections_format に反映する。
    該当するデータを id で検索して更新する。

    Parameters:
    - sections_format: 元のセクションデータ
    - fixed_data: 修正済みデータ (例: {"graphs": [...], "tables": [...], "formulas": [...]})

    Returns:
    - 修正された sections_format
    """
    for data_type in ["graphs", "tables", "formulas"]:
        fixed_items = fixed_data.get(data_type, [])
        if not fixed_items:
            continue  # 修正データがない場合は次のデータタイプへ

        # 修正データを id をキーとする辞書に変換
        fixed_items_dict = {item['id']: item for item in fixed_items if 'id' in item}

        # sections_format 内の該当データを更新
        for section in sections_format:
            for sub_section in section.get('sub_sections', []):
                original_items = sub_section.get(data_type, [])
                for idx, original_item in enumerate(original_items):
                    item_id = original_item.get('id')  # 元データの id を取得
                    if item_id and item_id in fixed_items_dict:
                        # 該当する id のデータを更新
                        print(f"Updating {data_type} with id {item_id}")
                        sub_section[data_type][idx] = fixed_items_dict[item_id]  # 更新処理

    return sections_format


