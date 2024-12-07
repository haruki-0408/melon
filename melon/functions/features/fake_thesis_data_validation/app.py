import json
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.validation import validate, SchemaValidationError
from utilities import read_schema_jsons, upload_to_s3

LOGGER_SERVICE = "fake_thesis_data_validation"
logger = Logger(service=LOGGER_SERVICE)

@logger.inject_lambda_context(log_event=False)
def lambda_handler(event, context):
    """
    スキーマバリデーションを実行するLambda関数。
    すべてのバリデーションエラーを収集し、最後にまとめてエラーとしてスローする。
    """

    try:
        sections_format = event.get("sections_format")

        response_graphs, response_tables, response_formulas = [], [], []

        for section in sections_format:
            for sub_section in section.get('sub_sections', []):
                response_graphs.extend(sub_section.get('graphs', []))
                response_tables.extend(sub_section.get('tables', []))
                response_formulas.extend(sub_section.get('formulas', []))


        # スキーマファイルを読み込み
        formulas_schema_json, tables_schema_json, graphs_schema_json = read_schema_jsons()

        # バリデーション実行
        validation_errors = validate_responses(
            response_formulas, response_graphs, response_tables,
            formulas_schema_json, graphs_schema_json, tables_schema_json
        )

        # バリデーションエラーがあればまとめてスロー
        if validation_errors:
            logger.error(validation_errors)
            raise SchemaValidationError(validation_errors)

        # バリデーション成功時のレスポンス
        return {
            'statusCode': 200,
            'body': {
                "graphs": response_graphs,
                "tables": response_tables,
                "formulas": response_formulas
            }
        }

    except SchemaValidationError:
        # ここでは既に上で適切なエラーログを出しているため、再度の処理は不要
        raise
    except Exception as e:
        # 予期せぬ例外
        error = {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "payload": event
        }
        logger.exception(error)
        raise

def validate_responses(response_formulas, response_graphs, response_tables, 
                       formulas_schema_json, graphs_schema_json, tables_schema_json):
    """
    各種レスポンス（数式、グラフ、テーブル）を対応するスキーマでバリデーションし、
    エラーがあればカテゴリごとに辞書形式で返す。

    Parameters:
    - response_formulas (list): 数式データ
    - response_graphs (list): グラフデータ
    - response_tables (list): テーブルデータ
    - formulas_schema_json (dict): 数式スキーマ
    - graphs_schema_json (dict): グラフスキーマ
    - tables_schema_json (dict): テーブルスキーマ

    Returns:
    - dict: {"graphs": "エラーメッセージ", "tables": "エラーメッセージ", "formulas": "エラーメッセージ"}
    """
    validation_errors = {
        "formulas": None,
        "tables": None,
        "graphs": None
    }

    # 数式バリデーション
    try:
        validate(event={"formulas": response_formulas}, schema=formulas_schema_json)
    except SchemaValidationError as e:
        validation_errors["formulas"] = parse_validation_error("formulas", str(e))

    # テーブルバリデーション
    try:
        validate(event={"tables": response_tables}, schema=tables_schema_json)
    except SchemaValidationError as e:
        validation_errors["tables"] = parse_validation_error("tables", str(e))

    # グラフバリデーション
    try:
        validate(event={"graphs": response_graphs}, schema=graphs_schema_json)
    except SchemaValidationError as e:
        validation_errors["graphs"] = parse_validation_error("graphs", str(e))

    # 空でないエラーのみ残す
    return {k: v for k, v in validation_errors.items() if v is not None}


def parse_validation_error(category, error_message):
    """
    エラーメッセージから category をキー、message を値とする形式で返す。

    Parameters:
    - category (str): エラーのカテゴリ（例: "formulas", "graphs", "tables"）
    - error_message (str): SchemaValidationError のメッセージ

    Returns:
    - str: エラーメッセージ本文
    """
    # エラーメッセージ本文の抽出
    if "Error: " in error_message:
        return error_message.split("Error: ")[1].split(", Path:")[0]
    else:
        return error_message
