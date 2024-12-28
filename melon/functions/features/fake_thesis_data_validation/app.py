import os
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.validation import validate, SchemaValidationError
from utilities import read_schema_jsons, record_workflow_progress_event

# envパラメータ
WORKFLOW_EVENT_BUS_NAME = os.environ["WORKFLOW_EVENT_BUS_NAME"]

STATE_NAME = "validation-lambda"
STATE_ORDER = 6

logger = Logger()
tracer = Tracer()

@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def lambda_handler(event, context):
    """
    スキーマバリデーションを実行するLambda関数。
    すべてのバリデーションエラーを収集し、最後にまとめてエラーとしてスローする。
    """

    workflow_id = event.get('workflow_id')
    print(f"WorkflowId: {workflow_id}")
    
    # デフォルトは成功
    error = None

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

    except SchemaValidationError:
        # ここでは既に上で適切なエラーログを出しているため、再度の処理は不要
        # raise
        error = {
            "error_type": "SchemaValidationError",
            "error_message": str(e),
            "payload": event
        }
    except Exception as e:
        # 予期せぬ例外
        error = {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "payload": event
        }

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
            logger.exception(error)
            if error.get("error_type") == "SchemaValidationError":
                raise SchemaValidationError(error)
            else:
                raise Exception(error)

    # ユーザーに返却するレスポンス
    return {
        'statusCode': 200,
        'body': {
            'graphs': response_graphs,
            'tables': response_tables,
            'formulas': response_formulas
        }
    }

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
