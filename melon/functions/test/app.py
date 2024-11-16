import boto3
import json
import os
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io

def lambda_handler(event, context):
    """
    S3からメタデータをダウンロードし、数式を含むPDFを生成してS3に保存するLambda関数
    """
    # S3バケット名を環境変数から取得
    S3_BUCKET = os.environ.get("S3_BUCKET")
    if not S3_BUCKET:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'S3_BUCKET環境変数が設定されていません'})
        }

    s3 = boto3.client('s3')

    # イベントからメタデータのキーリストと出力PDFのキーを取得
    metadata_keys = event.get('metadata_keys', [])
    if not metadata_keys:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'イベントにmetadata_keysが含まれていません'})
        }

    output_pdf_key = event.get('formula_pdf_key', 'formula.pdf')

    try:
        # フォントのパスを設定
        font_name = 'ipaexg'  # フォント名
        font_path = os.path.join(os.path.dirname(__file__), 'ipaexg.ttf')

        # ReportLabにフォントを登録
        pdfmetrics.registerFont(TTFont(font_name, font_path))

        # Matplotlibにフォントを登録
        font_prop = font_manager.FontProperties(fname=font_path)
        plt.rcParams['font.family'] = font_prop.get_name()
        plt.rcParams['font.sans-serif'] = [font_prop.get_name()]
        plt.rcParams['mathtext.fontset'] = 'custom'
        plt.rcParams['mathtext.rm'] = font_prop.get_name()
        plt.rcParams['mathtext.it'] = font_prop.get_name()
        plt.rcParams['mathtext.bf'] = font_prop.get_name()

        # PDFをメモリ上に作成
        pdf_buffer = io.BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=A4)
        width, height = A4
        y_position = height - 50  # 上からのマージン

        for key in metadata_keys:
            # メタデータをS3から取得
            response = s3.get_object(Bucket=S3_BUCKET, Key=key)
            metadata = json.loads(response['Body'].read().decode('utf-8'))

            latex_code = metadata.get('latex_code', '')
            description = metadata.get('description', '')
            parameters = metadata.get('parameters', [])

            # 数式画像を生成
            image_buffer = generate_equation_image(latex_code, font_prop)
            if not image_buffer:
                continue  # 画像生成に失敗した場合はスキップ

            # 数式の説明をPDFに描画
            c.setFont(font_name, 12)
            text_object = c.beginText(50, y_position)
            text_object.textLines(description)
            c.drawText(text_object)
            y_position -= 20 + 12 * description.count('\n')

            # 数式画像をPDFに挿入
            img = ImageReader(image_buffer)
            img_width, img_height = img.getSize()
            aspect = img_height / float(img_width)
            display_height = 20  # 高さを固定
            display_width = display_height / aspect
            c.drawImage(img, 50, y_position - display_height, width=display_width, height=display_height)
            y_position -= display_height + 20

            # パラメータの説明をPDFに描画
            if parameters:
                for param in parameters:
                    symbol = param.get('symbol', '')
                    param_desc = param.get('description', '')

                    # パラメータの説明を数式画像として生成
                    param_image_buffer = generate_parameter_image(symbol, param_desc, font_prop)
                    if not param_image_buffer:
                        continue  # 画像生成に失敗した場合はスキップ

                    # パラメータの説明画像をPDFに挿入
                    img = ImageReader(param_image_buffer)
                    img_width, img_height = img.getSize()
                    aspect = img_height / float(img_width)
                    display_height = 10  # 高さを固定
                    display_width = display_height / aspect
                    c.drawImage(img, 70, y_position - display_height, width=display_width, height=display_height)
                    y_position -= display_height + 10

            # 数式間のスペースを追加
            y_position -= 20

            # ページの下端に達した場合、新しいページを追加
            if y_position < 100:
                c.showPage()
                y_position = height - 50

        c.save()

        # 生成したPDFをS3にアップロード
        pdf_buffer.seek(0)
        s3.put_object(
            Bucket=S3_BUCKET,
            Key=output_pdf_key,
            Body=pdf_buffer,
            ContentType='application/pdf'
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'PDFが生成され、S3にアップロードされました', 'pdf_key': output_pdf_key})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def generate_equation_image(latex_code, font_prop):
    """
    LaTeXコードから数式画像を生成し、BytesIOオブジェクトを返す関数
    """
    print('-----')
    print(latex_code)
    try:
        # LaTeXコードのサニタイズ（必要に応じて実装）
        sanitized_latex = sanitize_latex_code(latex_code)

        # Matplotlibを使用して数式画像を生成
        fig, ax = plt.subplots()
        ax.axis('off')

        # 数式を描画
        text = ax.text(0, 0.5, f'${sanitized_latex}$', fontsize=14, ha='left', va='center', fontproperties=font_prop)

        # 描画領域を調整
        fig.canvas.draw()
        bbox = text.get_window_extent()
        width, height = bbox.width / fig.dpi, bbox.height / fig.dpi
        fig.set_size_inches(width, height)

        # 画像をバイナリデータとして取得
        image_buffer = io.BytesIO()
        plt.savefig(image_buffer, format='png', dpi=fig.dpi, bbox_inches='tight', pad_inches=0.0)
        plt.close(fig)
        image_buffer.seek(0)
        return image_buffer

    except Exception as e:
        print(f"数式画像の生成中にエラーが発生しました: {latex_code}")
        print(str(e))
        return None

def generate_parameter_image(symbol, description, font_prop):
    """
    パラメータのシンボルと説明から画像を生成し、BytesIOオブジェクトを返す関数
    """
    try:
        # LaTeXコードのサニタイズ
        sanitized_symbol = sanitize_latex_code(symbol)
        sanitized_description = description  # 説明はテキストとして扱う

        # Matplotlibを使用して画像を生成
        fig, ax = plt.subplots()
        ax.axis('off')

        # シンボルと説明を描画
        combined_text = f'${sanitized_symbol}$ : {sanitized_description}'
        text = ax.text(0, 0.5, combined_text, fontsize=12, ha='left', va='center', fontproperties=font_prop)

        # 描画領域を調整
        fig.canvas.draw()
        bbox = text.get_window_extent()
        width, height = bbox.width / fig.dpi, bbox.height / fig.dpi
        fig.set_size_inches(width, height)

        # 画像をバイナリデータとして取得
        image_buffer = io.BytesIO()
        plt.savefig(image_buffer, format='png', dpi=fig.dpi, bbox_inches='tight', pad_inches=0.0)
        plt.close(fig)
        image_buffer.seek(0)
        return image_buffer

    except Exception as e:
        print(f"パラメータ画像の生成中にエラーが発生しました: {symbol} : {description}")
        print(str(e))
        return None

def sanitize_latex_code(latex_code):
    """
    LaTeXコードをサニタイズする関数（簡易的な例）
    """
    # 禁止されたコマンドを除去
    forbidden_commands = ['\\write', '\\input', '\\include', '\\catcode', '\\def', '\\open', '\\loop', '\\read']
    for cmd in forbidden_commands:
        latex_code = latex_code.replace(cmd, '')
    return latex_code
