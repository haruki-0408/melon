import json
from io import BytesIO
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from reportlab.platypus import Table, TableStyle 
from svglib.svglib import svg2rlg
from reportlab.platypus import Paragraph, KeepTogether
from aws_lambda_powertools import Logger

logger = Logger()

FONT_PATH = '/opt/python/fonts/ipaexm.ttf'  # フォントパスを設定

def process_formula(object_key, s3_client, s3_bucket, styles):
    """
    数式のメタデータを処理し、SVG形式で生成し、PDF要素を返す関数。

    Parameters:
    - object_key (str): S3内のオブジェクトキー。
    - s3_client: S3クライアント。
    - s3_bucket (str): S3バケット名。
    - styles (StyleSheet1): スタイルシート。

    Returns:
    - elements (list): 数式の説明やSVGを含む要素リスト。
    """
    elements = []
    try:
        # メタデータをS3から取得
        response = s3_client.get_object(Bucket=s3_bucket, Key=object_key)
        metadata = json.loads(response['Body'].read().decode('utf-8'))

        latex_code = metadata.get('latex_code', '')
        description = metadata.get('description', '')
        parameters = metadata.get('parameters', [])

        # SVGを生成
        svg_buffer = generate_latex_svg(latex_code, parameters)

        if svg_buffer:
            svg_buffer.seek(0)  # SVGバッファの先頭に移動
            drawing = svg2rlg(svg_buffer)  # SVG読み込み
            
            # 中央寄せするためにテーブルでラッピング
            table = Table([[drawing]], colWidths=[400])
            table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))

            if description:
                keep_together_group = KeepTogether([
                    Paragraph(description, styles['CaptionText']),
                    table            
                ])
            else:
                keep_together_group = KeepTogether([
                    table            
                ])
            
        elements.append(keep_together_group)

    except Exception as e:
        logger.exception(f"Failed to process formula {object_key}: {e}")

    return elements

def generate_latex_svg(latex_code, parameters):
    """
    LaTeX数式とパラメータを含むSVGを生成し、BytesIOオブジェクトを返す関数。

    Parameters:
    - latex_code (str): LaTeXコード。
    - parameters (list): パラメータのリスト。

    Returns:
    - svg_buffer (BytesIO): SVGデータ。
    """
    try:
        # フォント設定
        font_prop = FontProperties(fname=FONT_PATH)
        fontsize_formula = 9

        fig, ax = plt.subplots()
        fig.set_dpi(72)
        ax.axis('off')  # 軸を非表示

        # 数式とパラメータを描画
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
        svg_buffer = BytesIO()
        plt.savefig(svg_buffer, format='svg', bbox_inches='tight', pad_inches=0.0)
        plt.close(fig)
        return svg_buffer

    except Exception as e:
        logger.exception(f"SVG生成中にエラーが発生しました: {e}")
        return None


def sanitize_latex_code(latex_code):
    """
    LaTeXコードをサニタイズする関数（簡易的な例）
    """
    forbidden_commands = ['\\\\', '\\write', '\\input', '\\include', '\\catcode', '\\def', '\\open', '\\loop', '\\read']
    for cmd in forbidden_commands:
        latex_code = latex_code.replace(cmd, '')
    return latex_code
