from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.validation import validate
from aws_lambda_powertools.utilities.validation import SchemaValidationError
import event_schemas as event_schemas
import os
from utilities import read_schema_jsons, record_workflow_progress_event

WORKFLOW_EVENT_BUS_NAME = os.environ["WORKFLOW_EVENT_BUS_NAME"]

STATE_NAME = "prompt-lambda"
STATE_ORDER = 3

logger = Logger()
tracer = Tracer()

@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def lambda_handler(event, context):
    """
    各セクションごとに生成AIに送るプロンプト文章を作成し、SQSキューに送信するLambda関数
    """

    workflow_id = event.get('workflow_id')
    print(f"WorkflowId: {workflow_id}")

    # デフォルトは成功
    error = None

    try:
        # イベントバリデーション
        validate(event=event, schema=event_schemas.INPUT)

        # タイトルとフォーマットを取得
        title = event.get('title', '')
        sections_format = event.get('sections_format', {})
        category_type_jp = sections_format["category_type_jp"]

        # スキーマファイルを読み込み
        formulas_schema_json, tables_schema_json, graphs_schema_json = read_schema_jsons()
    
        sections_format = []
    
        # システムプロンプト文章を生成
        system_prompt = generate_system_prompt(
            title=title,
            category_type_jp=category_type_jp,
            formulas_schema=formulas_schema_json,
            graphs_schema=graphs_schema_json,
            tables_schema=tables_schema_json
        )

        return {
            'statusCode': 200,
            'body': {
                "system_prompt" : system_prompt,
            }
        }
    except SchemaValidationError as e:
        error = {
            "error_type": "SchemaValidationError",
            "error_message": str(e)
        }
        logger.exception(str(e))
        
    except Exception as e:
        error = {
            "error_type": type(e).__name__,
            "error_message": str(e)
        }
        logger.exception(str(e))

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
            if error.get("error_type") == "SchemaValidationError":
                raise SchemaValidationError(error)
            else:
                raise Exception(error)

def generate_system_prompt(title, category_type_jp, formulas_schema, graphs_schema, tables_schema):
    """
    生成AIに送るプロンプト文章を生成する関数
    """
    system_prompt = f"""
あなたはタイトルから面白くユーモアのある嘘の論文を構成する専門家・作家です。論文のセクション毎のフォーマットオブジェクトを内容として添付します。
以下指示に従いながら添付したセクションのフォーマットオブジェクト内に追記し、レスポンスとして追記したオブジェクト形式を必ずJSONパース可能なテキストのみで返却してください。

# 要件(必ず遵守すること)

### 文章に関して
- "text" プロパティには嘘論文のタイトルとサブセクションの"title_name"を考慮したユーモアで説得力のある文章を記載してください。文字数は長めに設定し、改行コードや段落を適切に含めてください。
- 嘘の内容であることを活かしつつ、閲覧者が興味を惹かれるようにユーモアある面白い内容にすることにこだわってください。
- 内容に関しては必ずタイトルとセクションとサブセクションに合うように構成し一貫性のある論文にしてください。

### データに関して
- 各サブセクションにグラフ、表、数式が必要な場合、"text"と同じサブセクション内の"graphs"、"tables"、"formulas"それぞれに詳細なデータを以下の参照データの各JSONスキーマを厳格に確実に満たすように慎重に設定してください。この時スキーマオブジェクト内の各idは後述する"text"内の識別子とリンクさせてください。データを挿入しない場合でも、空の配列としてgraphs,tables,formulasプロパティを必ず含めてください。
- 必ずしもサブセクション毎にグラフ、表、数式を含める必要はありません。データを入れると不自然なセクションで不必要にデータを含めないでください。データを含めるかどうかはセクションとサブセクションの内容に応じて適切に選択してください。
- サブセクションにデータを含める場合その"text"内に挿入位置を示す識別子を含めてください。具体例: [INSERT_FORMULA_HOGEHOGE]とするとFORMULA_HOGEHOGEというidを持つ数式データの挿入という意味になります。数式を表す場合はデータのidをFORMULA_大文字英数字、グラフを表す場合はGRAPH_大文字英数字、表を表す場合はTABLE_大文字英数字 として大文字英数字は示したいデータに関連した名称をつける、各セクション間で必ず重複がないように注意してください。
- 例えば1つ目のサブセクションの"text"で"[INSERT_FORMULA_HOGEHOGE]"とすると、必ずそのサブセクション内のformulasプロパティに "id" : "FORMULA_HOGEHOGE" となるデータを設定してください。(graphs, tablesも同様)
- グラフ、表、数式データをgraphs,tables,formulas内に定義したら"text"内に挿入位置を示す識別子を必ず入れてください。挿入識別子は挿入位置識別子がなくgraphs,formulas,tablesにデータを入れることは許可しません。
- グラフ、表、数式を含める場合はそのサブセクション内の"text"でそのデータの内容に言及してください。その際に挿入識別子の後に直接文章を続けるのではなく、一度区切ってください。 NG例: [INSERT_FORMULA_ABC123]で表される。 適切な例: [INSERT_FORMULA_ABC123] この数式が示すように~。
- 値やデータを設定する際には説得力のある真実味があるデータを作成することに注意してください。
- グラフ、表に関するcolorsデータはスキーマの"description"に記載されている説明を参考にしてください。

### 返却する回答の形式について
- 各サブセクションそれぞれに必ず以下のプロパティを追記して返却すること。: "text", "graphs", "tables", "formulas"。
- レスポンスは 必ずJSONパース可能な文字列のみで、セクションフォーマット1オブジェクトに追記した形で出力してください。
- 返却されたレスポンスの内容をそのままJSONにパースするので絶対に前後に不要な「```json」 などの文章を入れてレスポンスすることは許可しません。回答の出力は必ずJSONパース可能なデータのみであることに注意して慎重に生成してください。

# 参照データ

### 嘘論文タイトル
{title}

### 論文のカテゴリ
{category_type_jp}

### 各データのJSONスキーマ(厳守)

#### Formulas Schema
{formulas_schema}

#### Graphs Schema
{graphs_schema}

#### Tables Schema
{tables_schema}

"""

    ### section object
    return system_prompt