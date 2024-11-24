import os
import json
import io
from aws_lambda_powertools import Logger
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from reportlab.platypus import Image, Spacer, Paragraph
from reportlab.lib.utils import ImageReader

LOGGER_SERVICE = "convert_to_pdf"
logger = Logger(service=LOGGER_SERVICE)

# フォントのパスを設定
FONT_PATH = '/opt/python/fonts/ipaexm.ttf'

def process_formula(object_key, s3_client, s3_bucket, styles):
    """
    数式のメタデータを処理し、数式画像を生成してPDF要素を返す関数。

    Parameters:
    - formula_id (str): 数式のID。
    - s3_client: S3クライアント。
    - s3_bucket (str): S3バケット名。
    - styles (StyleSheet1): スタイルシート。

    Returns:
    - elements (list): 数式の説明や画像を含む要素リスト。
    """
    elements = []

    try:
        # メタデータをS3から取得
        response = s3_client.get_object(Bucket=s3_bucket, Key=object_key)
        metadata = json.loads(response['Body'].read().decode('utf-8'))

        latex_code = metadata.get('latex_code', '')
        description = metadata.get('description', '')
        parameters = metadata.get('parameters', [])

        # フォントの設定
        font_prop = font_manager.FontProperties(fname=FONT_PATH)
        plt.rcParams['font.family'] = font_prop.get_name()
        plt.rcParams['font.sans-serif'] = [font_prop.get_name()]
        plt.rcParams['mathtext.fontset'] = 'custom'
        plt.rcParams['mathtext.rm'] = font_prop.get_name()
        plt.rcParams['mathtext.it'] = font_prop.get_name()
        plt.rcParams['mathtext.bf'] = font_prop.get_name()

        # 数式画像を生成
        equation_image_buffer = generate_equation_image(latex_code, font_prop)

        # 数式の説明を追加
        if description:
            elements.append(Paragraph(description, styles['FakeThesisBodyText']))
            elements.append(Spacer(1, 12))

        # 数式画像を追加
        if equation_image_buffer:
            img = Image(equation_image_buffer)
            img.hAlign = 'CENTER'
            elements.append(img)
            elements.append(Spacer(1, 12))

        # パラメータの説明を追加
        for param in parameters:
            symbol = param.get('symbol', '')
            param_desc = param.get('description', '')

            # パラメータの画像を生成
            param_image_buffer = generate_parameter_image(symbol, param_desc, font_prop)

            if param_image_buffer:
                img = Image(param_image_buffer)
                img.hAlign = 'CENTER'
                elements.append(img)
                elements.append(Spacer(1, 12))

    except Exception as e:
        logger.exception(f"Failed to process formula {object_key}: {str(e)}")

    return elements

def generate_equation_image(latex_code, font_prop):
    """
    LaTeXコードから数式画像を生成し、BytesIOオブジェクトを返す関数
    """
    try:
        # LaTeXコードのサニタイズ
        sanitized_latex = sanitize_latex_code(latex_code)

        # Matplotlibを使用して数式画像を生成
        fig = plt.figure()
        fig.text(0.5, 0.5, f'${sanitized_latex}$', fontsize=14, ha='center', va='center', fontproperties=font_prop)
        fig.patch.set_alpha(0)

        # 画像をバイナリデータとして取得
        image_buffer = io.BytesIO()
        plt.savefig(image_buffer, format='png', dpi=300, bbox_inches='tight', pad_inches=0.0, transparent=True)
        plt.close(fig)
        image_buffer.seek(0)
        return image_buffer

    except Exception as e:
        logger.exception(f"数式画像の生成中にエラーが発生しました: {e}")
        return None

def generate_parameter_image(symbol, description, font_prop):
    """
    パラメータのシンボルと説明から画像を生成し、BytesIOオブジェクトを返す関数
    """
    try:
        # LaTeXコードのサニタイズ
        sanitized_symbol = sanitize_latex_code(symbol)
        sanitized_description = description

        # Matplotlibを使用して画像を生成
        fig = plt.figure()
        combined_text = f'${sanitized_symbol}$ : {sanitized_description}'
        fig.text(0.5, 0.5, combined_text, fontsize=12, ha='center', va='center', fontproperties=font_prop)
        fig.patch.set_alpha(0)

        # 画像をバイナリデータとして取得
        image_buffer = io.BytesIO()
        plt.savefig(image_buffer, format='png', dpi=300, bbox_inches='tight', pad_inches=0.0, transparent=True)
        plt.close(fig)
        image_buffer.seek(0)
        return image_buffer

    except Exception as e:
        logger.exception(f"パラメータ画像の生成中にエラーが発生しました: {e}")
        return None

def sanitize_latex_code(latex_code):
    """
    LaTeXコードをサニタイズする関数（簡易的な例）
    """
    # 禁止されたコマンドを除去
    forbidden_commands = ['\\\\','\\write', '\\input', '\\include', '\\catcode', '\\def', '\\open', '\\loop', '\\read']
    for cmd in forbidden_commands:
        latex_code = latex_code.replace(cmd, '')
    return latex_code
