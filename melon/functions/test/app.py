import tempfile
import boto3
import base64
import os
import json
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PIL import Image

# S3のバケット情報
S3_BUCKET = os.environ["S3_BUCKET"]
GRAPH_DATA_KEY = 'graph_data.json'
OUTPUT_PDF_KEY = 'output_report.pdf'

# S3クライアントを作成
s3_client = boto3.client('s3')

def fetch_graph_images():
    """
    S3からグラフデータを取得し、Base64エンコードされた画像データをデコードして返す
    """
    response = s3_client.get_object(Bucket=S3_BUCKET, Key=GRAPH_DATA_KEY)
    graph_data = json.loads(response['Body'].read().decode('utf-8'))  # eval -> json.loads
    images = []

    for image_base64 in graph_data:
        image_data = base64.b64decode(image_base64)
        images.append(image_data)

    return images

def create_pdf(images):
    """
    ReportLabを使用してPDFを生成し、S3に保存する
    """
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=A4)
    width, height = A4

    for image_data in images:
        # Imageデータを一時的にBytesIOオブジェクトに変換
        image_buffer = BytesIO(image_data)
        image_buffer.seek(0)  # ここでseek(0)を呼び出してファイルポインタを先頭に戻す
        img = Image.open(image_buffer)

        # 画像サイズの調整
        img_width, img_height = img.size
        aspect = img_height / float(img_width)
        img_height = width * aspect
        img_width = width

        # 一時的なバイナリデータとして画像を保存
        img_temp_buffer = BytesIO()
        img.save(img_temp_buffer, format="PNG")  # 画像をPNG形式で保存
        img_temp_buffer.seek(0)  # バッファの先頭にポインタを戻す

        # 一時ファイルに保存
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(img_temp_buffer.read())
            temp_file_path = temp_file.name  # 一時ファイルのパスを取得

        # 画像をPDFに追加
        c.drawImage(temp_file_path, 0, height - img_height, width=img_width, height=img_height)
        c.showPage()  # 新しいページを作成
        

    # PDFの作成を終了
    c.save()
    print('c')
    pdf_buffer.seek(0)
    print('d')

    return pdf_buffer

def lambda_handler(event, context):
    """
    Lambda関数のエントリポイント
    """
    # グラフ画像を取得
    images = fetch_graph_images()

    # PDF生成
    pdf_buffer = create_pdf(images)

    # S3にPDFをアップロード
    s3_client.put_object(
        Bucket=S3_BUCKET,
        Key=OUTPUT_PDF_KEY,
        Body=pdf_buffer,
        ContentType='application/pdf'
    )

    return {
        'statusCode': 200,
        'body': "PDF report uploaded to s3"
    }
