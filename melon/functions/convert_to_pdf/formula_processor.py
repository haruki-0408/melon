import os
import json
import io
from pylatex import Document, Section, NoEscape
from io import BytesIO
from aws_lambda_powertools import Logger
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from reportlab.platypus import Image, Spacer, Paragraph
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import cm

LOGGER_SERVICE = "convert_to_pdf"
logger = Logger(service=LOGGER_SERVICE)

# フォントのパスを設定
FONT_PATH = '/opt/python/fonts/ipaexm.ttf'

def process_formula(object_key, s3_client, s3_bucket, styles):
    """
    数式のメタデータを処理し、数式とパラメータを含む画像を生成してPDF要素を返す関数。

    Parameters:
    - object_key (str): S3内のオブジェクトキー。
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
        plt.rcParams['font.size'] = 10
        plt.rcParams['font.sans-serif'] = [font_prop.get_name()]
        plt.rcParams['mathtext.fontset'] = 'custom'
        plt.rcParams['mathtext.rm'] = font_prop.get_name()
        plt.rcParams['mathtext.it'] = font_prop.get_name()
        plt.rcParams['mathtext.bf'] = font_prop.get_name()

        # 数式とパラメータを含む画像を生成
        combined_image_buffer = generate_combined_image(latex_code, parameters, font_prop)

        # 数式の説明を追加
        if description:
            elements.append(Paragraph(description, styles['CaptionText']))
            # elements.append(Spacer(1, 12))

        # 数式とパラメータの画像を追加
        if combined_image_buffer:
            img = Image(combined_image_buffer)
            img.hAlign = 'CENTER'

            # 画像の幅を調整（例: 幅を10cmに設定）
            desired_width = 18 * cm
            aspect = img.imageHeight / float(img.imageWidth)
            img.drawWidth = desired_width
            img.drawHeight = desired_width * aspect

            elements.append(img)
            # elements.append(Spacer(1, 12))

    except Exception as e:
        logger.exception(f"Failed to process formula {object_key}: {str(e)}")

    return elements

def generate_combined_image(latex_code, parameters, font_prop):
    """
    数式とパラメータを含む画像を生成し、BytesIOオブジェクトを返す関数。

    Parameters:
    - latex_code (str): LaTeXコード。
    - parameters (list): パラメータのリスト。
    - font_prop: フォントプロパティ。

    Returns:
    - image_buffer (BytesIO): 画像データ。
    """
    try:
        # LaTeXコードのサニタイズ
        sanitized_latex = sanitize_latex_code(latex_code)

        # フォントサイズを設定
        fontsize_formula = 12  # 数式のフォントサイズ
        fontsize_params = 10.5  # パラメータのフォントサイズ

        # 描画するテキストのリストとフォントサイズのリスト
        texts = []
        font_sizes = []

        # 数式を追加
        texts.append(f"${sanitized_latex}$")
        font_sizes.append(fontsize_formula)

        # パラメータを追加
        for param in parameters:
            symbol = sanitize_latex_code(param.get('symbol', ''))
            description = param.get('description', '')
            if symbol or description:
                param_text = f"${symbol}$：{description}"
                texts.append(param_text)
                font_sizes.append(fontsize_params)

        num_texts = len(texts)

        # 行間の調整
        formula_param_spacing = 0.2  # 数式と最初のパラメータ間の間隔
        param_line_spacing = 0.1     # パラメータ間の間隔（小さく調整）

        # y座標の初期値
        y_positions = []
        y = 0.95  # 画像上部から開始

        # 数式のy座標を追加
        y_positions.append(y)

        # y座標を調整してパラメータの位置を計算
        y -= formula_param_spacing
        for _ in range(1, num_texts):
            y_positions.append(y)
            y -= param_line_spacing

        # 画像サイズを計算
        # fig_height_inch = 2 + num_texts * 0.3  # 全体の高さを少し長めに設定
        fig_height_inch = num_texts * 0.5  # 全体の高さを少し長めに設定
        fig_width_inch = 6  # 幅6インチ

        # Matplotlibを使用して画像を生成
        fig, ax = plt.subplots(figsize=(fig_width_inch, fig_height_inch), dpi=200)
        fig.subplots_adjust(top=1, bottom=0)  # 上下の余白をなくす
        fig.patch.set_alpha(0)  # 背景を透明に

        # 軸を非表示
        ax.axis('off')

        # テキストを描画
        for text, y_pos, fontsize in zip(texts, y_positions, font_sizes):
            ax.text(
                0.5, y_pos, text,
                fontsize=fontsize,
                ha='center', va='top',
                fontproperties=font_prop,
                transform=ax.transAxes
            )

        # レイアウトを調整
        # plt.tight_layout(pad=0)

        # 画像をバイナリデータとして取得
        image_buffer = BytesIO()
        plt.savefig(
            image_buffer,
            format='png',
            dpi=200,
            bbox_inches='tight',
            pad_inches=0.0,
            transparent=True
        )
        plt.close(fig)
        image_buffer.seek(0)
        return image_buffer

    except Exception as e:
        logger.exception(f"数式とパラメータ画像の生成中にエラーが発生しました: {e}")
        return None


# def generate_equation_image(latex_code, font_prop):
#     """
#     LaTeXコードから数式画像を生成し、BytesIOオブジェクトを返す関数
#     数式の幅を動的に調整してA4サイズに収まるようにする。
#     """
#     try:
#         # LaTeXコードのサニタイズ
#         sanitized_latex = sanitize_latex_code(latex_code)

#         # Matplotlibを使用して数式画像を生成
#         fig = plt.figure()
#         text_obj = fig.text(
#             0.5, 0.5, f'${sanitized_latex}$',
#             fontsize=12, ha='center', va='center',
#             fontproperties=font_prop
#         )
#         fig.patch.set_alpha(0)

#         # 一度描画してサイズを取得
#         fig.canvas.draw()
#         renderer = fig.canvas.get_renderer()
#         bbox = text_obj.get_window_extent(renderer)

#         # A4サイズの横幅（ポイント単位）
#         A4_WIDTH_PT = 595.27  # A4横幅のポイント数
#         dpi = fig.dpi

#         # bbox.width をスケール基準に調整
#         image_width_inch = bbox.width / dpi
#         if image_width_inch > (A4_WIDTH_PT / dpi):  # A4に収まらない場合
#             scale_factor = (A4_WIDTH_PT / dpi) / image_width_inch
#             new_width = bbox.width * scale_factor
#             new_height = bbox.height * scale_factor
#         else:  # サイズ変更不要
#             new_width = bbox.width
#             new_height = bbox.height

#         fig.set_size_inches(new_width / dpi, new_height / dpi)

#         # 画像をバイナリデータとして取得
#         image_buffer = io.BytesIO()
#         plt.savefig(
#             image_buffer,
#             format='png',
#             dpi=dpi,
#             bbox_inches='tight',
#             pad_inches=0.0,
#             transparent=True
#         )
#         plt.close(fig)
#         image_buffer.seek(0)
#         return image_buffer

#     except Exception as e:
#         logger.exception(f"数式画像の生成中にエラーが発生しました: {e}")
#         return None
    
# def generate_parameter_image(symbol, description, font_prop):
#     """
#     パラメータのシンボルと説明から画像を生成し、BytesIOオブジェクトを返す関数。
#     画像サイズを動的に調整してA4サイズに収まるようにする。
#     """
#     try:
#         # LaTeXコードのサニタイズ
#         sanitized_symbol = sanitize_latex_code(symbol)
#         sanitized_description = description

#         # Matplotlibを使用して画像を生成
#         fig = plt.figure()
#         combined_text = f'${sanitized_symbol}$ : {sanitized_description}'
#         text_obj = fig.text(
#             0.5, 0.5, combined_text,
#             fontsize=12, ha='center', va='center',
#             fontproperties=font_prop
#         )
#         fig.patch.set_alpha(0)

#         # 一度描画してサイズを取得
#         fig.canvas.draw()
#         renderer = fig.canvas.get_renderer()
#         bbox = text_obj.get_window_extent(renderer)

#         # A4サイズの横幅（ポイント単位）
#         A4_WIDTH_PT = 595.27  # A4横幅のポイント数
#         dpi = fig.dpi

#         # bbox.width をスケール基準に調整
#         image_width_inch = bbox.width / dpi
#         if image_width_inch > (A4_WIDTH_PT / dpi):  # A4に収まらない場合
#             scale_factor = (A4_WIDTH_PT / dpi) / image_width_inch
#             new_width = bbox.width * scale_factor
#             new_height = bbox.height * scale_factor
#         else:  # サイズ変更不要
#             new_width = bbox.width
#             new_height = bbox.height

#         fig.set_size_inches(new_width / dpi, new_height / dpi)

#         # 画像をバイナリデータとして取得
#         image_buffer = io.BytesIO()
#         plt.savefig(
#             image_buffer,
#             format='png',
#             dpi=dpi,
#             bbox_inches='tight',
#             pad_inches=0.0,
#             transparent=True
#         )
#         plt.close(fig)
#         image_buffer.seek(0)
#         return image_buffer

#     except Exception as e:
#         logger.exception(f"パラメータ画像の生成中にエラーが発生しました: {e}")
#         return None
def generate_equation_image(latex_code, font_prop):
    """
    LaTeXコードから数式画像を生成し、BytesIOオブジェクトを返す関数。
    数式がフォントサイズ12で描画され、画像のサイズが適切になるように調整します。
    """
    try:
        # LaTeXコードのサニタイズ
        sanitized_latex = sanitize_latex_code(latex_code)

        # フォントサイズを12に設定
        fontsize = 12

        # Matplotlibを使用して数式画像を生成
        fig = plt.figure(figsize=(0.01, 0.01))  # 初期サイズは小さく
        fig.patch.set_alpha(0)  # 背景を透明に

        # テキストオブジェクトを追加
        text_obj = fig.text(
            0, 0, f"${sanitized_latex}$",
            fontsize=fontsize, fontproperties=font_prop
        )

        # 図のレイアウトを調整
        # fig.tight_layout()

        # 描画してバウンディングボックスを取得
        renderer = fig.canvas.get_renderer()
        bbox = text_obj.get_window_extent(renderer)

        # 画像サイズを計算（インチ単位）
        width_inch = (bbox.width + 10) / fig.dpi  # 余白を10ピクセル追加
        height_inch = (bbox.height + 10) / fig.dpi

        # Figureのサイズを再設定
        fig.set_size_inches(width_inch, height_inch)

        # テキストオブジェクトの位置を調整
        text_obj.set_position((5 / bbox.width, 5 / bbox.height))

        # 画像をバイナリデータとして取得
        image_buffer = io.BytesIO()
        fig.savefig(
            image_buffer,
            format='png',
            dpi=fig.dpi,
            bbox_inches='tight',
            pad_inches=0.0,
            transparent=True
        )
        plt.close(fig)
        image_buffer.seek(0)
        return image_buffer

    except Exception as e:
        logger.exception(f"数式画像の生成中にエラーが発生しました: {e}")
        return None


def generate_parameter_image(symbol, description, font_prop):
    """
    パラメータのシンボルと説明から画像を生成し、BytesIOオブジェクトを返す関数。
    シンボルと説明がフォントサイズ8で描画され、画像のサイズが適切になるように調整します。
    """
    try:
        # LaTeXコードのサニタイズ
        sanitized_symbol = sanitize_latex_code(symbol)
        sanitized_description = description

        # フォントサイズを8に設定
        fontsize = 10.5

        # 表示するテキストを作成
        combined_text = f"${sanitized_symbol}$ : {sanitized_description}"

        # Matplotlibを使用して画像を生成
        fig = plt.figure(figsize=(4, 0.5), dpi=200)  # 幅と高さを小さく設定
        fig.patch.set_alpha(0)  # 背景を透明に

        # テキストオブジェクトを追加
        text_obj = fig.text(
            0.5, 0.5, combined_text,
            fontsize=fontsize, ha='center', va='center', fontproperties=font_prop
        )

        # 不要な軸を非表示
        plt.axis('off')

        # 図のレイアウトを調整
        fig.tight_layout(pad=0)

        # 画像をバイナリデータとして取得
        image_buffer = io.BytesIO()
        fig.savefig(
            image_buffer,
            format='png',
            dpi=200,
            bbox_inches='tight',
            pad_inches=0.0,
            transparent=True
        )
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
