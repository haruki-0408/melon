import io
import boto3
import base64
from aws_lambda_powertools import Logger, Tracer
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import os
from utilities import upload_to_s3, record_workflow_progress_event  

WORKFLOW_EVENT_BUS_NAME = os.environ["WORKFLOW_EVENT_BUS_NAME"]
FONT_PATH = '/opt/python/fonts/ipaexm.ttf'  # フォントパスを設定
S3_BUCKET = os.environ.get("S3_BUCKET")

STATE_NAME = "formula-gen-lambda"
STATE_ORDER = 9

logger = Logger()
tracer = Tracer()

@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def lambda_handler(event, context):
    """
    イベントで渡されたLaTeX数式を画像としてS3に保存するLambda関数
    """

    workflow_id = event.get('workflow_id')
    print(f"WorkflowId: {workflow_id}")
    
    # デフォルトは成功
    error = None

    try:
        # イベントから数式の配列を取得
        workflow_id = event.get('workflow_id')
        formulas = event.get('formulas')
        
        if not formulas:
            raise Exception("No formulas data provided in event")
        if not S3_BUCKET:
            raise Exception("No S3 Bucket provided in the environ.")

        formula_images = []
        for index, formula in enumerate(formulas):
            print(f"--- [数式] {formula['id']} 処理中... ---")
            image_data = create_formula_latex_image(formula)
            
            formula_images.append({
                'id' : formula['id'],
                'image_data' : image_data,
                'formula_number' : str(index + 1),
                'description': formula['description']  # タイトルを保持
            })
            
        non_trailing_slash_prefix = f'{workflow_id}/formulas'
        object_keys = upload_to_s3(non_trailing_slash_prefix, formula_images)

    except Exception as e:
        error = {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "payload": event
        }
        logger.exception(error)

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
            raise Exception(error)
    
    return {
        'statusCode': 200,
        'body': object_keys
    }

def create_formula_latex_image(formula_data):
    """
    LaTeX数式とパラメータを含むSVGを生成し、BytesIOオブジェクトを返す関数。

    Parameters:
    - latex_code (str): LaTeXコード。
    - parameters (list): パラメータのリスト。

    Returns:
    - svg_buffer (BytesIO): SVGデータ。
    """
    
    # フォント設定
    font_prop = FontProperties(fname=FONT_PATH)
    fontsize_formula = 9

    fig, ax = plt.subplots()
    fig.set_dpi(72)
    ax.axis('off')  # 軸を非表示

    # 数式とパラメータを描画
    latex_code = formula_data.get('latex_code')
    parameters = formula_data.get('parameters', [])

    sanitized_latex = sanitize_latex_code(latex_code)
    formula_text = f"${sanitized_latex}$"
    params_text = "\n".join([f"${p['symbol']}$: {p['description']}" for p in parameters])
    full_text = f"{formula_text}\n\n{params_text}"

    # 一時的に描画してバウンディングボックスを取得
    text_obj = ax.text(
        0.5, 0.5, full_text,
        fontsize=fontsize_formula,
        ha='center', va='center',
        fontproperties=font_prop,
    )
    fig.canvas.draw()
    bbox = text_obj.get_window_extent(fig.canvas.get_renderer())

    # 動的にFigureサイズを計算
    dpi = fig.get_dpi()
    width_inch = bbox.width / dpi + 0.2  # 幅に余白を追加
    height_inch = bbox.height / dpi + 0.2  # 高さに余白を追加
    fig.set_size_inches(width_inch, height_inch)

    # SVGデータとして保存
    buf = io.BytesIO()
    fig.savefig(buf, format='svg', bbox_inches='tight', pad_inches=0.0)
    plt.close(fig)

    return base64.b64encode(buf.getvalue()).decode('utf-8')


def sanitize_latex_code(latex_code):
    """
    LaTeXコードをサニタイズする関数（簡易的な例）
    """
    forbidden_commands = ['\\\\', '\\write', '\\input', '\\include', '\\catcode', '\\def', '\\open', '\\loop', '\\read']
    for cmd in forbidden_commands:
        latex_code = latex_code.replace(cmd, '')
    return latex_code

def upload_to_s3(non_trailing_slash_prefix, formulas):
    """
    Base64エンコードされた画像データをS3にアップロードするヘルパー関数
    """
    s3 = boto3.resource('s3')
    object_keys = []
    for formula in formulas:
        # 一意のキーを作成
        object_key = f"{non_trailing_slash_prefix}/{formula['id']}.svg"
        image_binary = base64.b64decode(formula['image_data'])

        # 日本語説明文をBase64エンコード
        encoded_description = base64.b64encode(formula['description'].encode('utf-8')).decode('utf-8')

        s3.Object(S3_BUCKET, object_key).put(
            Body=image_binary,
            ContentType='image/svg+xml',
            Metadata={
                'number': formula['formula_number'],
                'type' : 'formula', 
                'description': encoded_description
            }
        )
        object_keys.append(object_key)

    return object_keys