import json
import os
import boto3
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from utilities import upload_to_s3

# S3クライアントの初期化
S3_BUCKET = os.environ["S3_BUCKET"]  # バケット名
FONT_PATH = os.path.join(os.path.dirname(__file__), "ipaexm.ttf")

def lambda_handler(event, context):
    # 入力データの取得
    title = event.get("title", "Untitled")
    author = event.get("author", "Anonymous")
    abstract = event.get("abstract", "No abstract provided.")
    toc = event.get("format", {}).get("sections", [])
    
    object_key = "document.pdf"  # 保存先のファイル名

    # PDF のセットアップ
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    
    # 日本語フォントを登録
    pdfmetrics.registerFont(TTFont("IPAexMincho", FONT_PATH))
    
    # スタイル設定
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="JapaneseTitle", fontName="IPAexMincho", fontSize=24, alignment=1, spaceAfter=20))
    styles.add(ParagraphStyle(name="JapaneseNormal", fontName="IPAexMincho", fontSize=12, spaceAfter=12))
    styles.add(ParagraphStyle(name="JapaneseHeading2", fontName="IPAexMincho", fontSize=16, spaceAfter=14, alignment=1))
    styles.add(ParagraphStyle(name="AuthorRightAlign", fontName="IPAexMincho", fontSize=12, alignment=2, spaceAfter=20))

    # コンテンツリスト
    elements = []

    # 表紙の作成
    elements.append(Spacer(1, 120))
    elements.append(Paragraph(title, styles['JapaneseTitle']))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(f"著者: {author}", styles['AuthorRightAlign']))  # 著者名を右寄せで表示
    elements.append(Spacer(1, 60))
    elements.append(Paragraph("要約", styles['JapaneseHeading2']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(abstract, styles['JapaneseNormal']))
    elements.append(Spacer(1, 48))

    # 改ページ
    elements.append(PageBreak())

    # 目次の作成
    elements.append(Paragraph("目次", styles['JapaneseHeading2']))
    elements.append(Spacer(1, 24))

    # 目次の項目をテーブルに追加
    table_data = []
    for i, section in enumerate(toc, start=1):
        section_title = section.get("title_name", "Untitled Section")
        subsections = section.get("sub_sections", [])

        # セクション名を目次に追加
        table_data.append([f"{i}. {section_title}", ""])

        # サブセクションの追加
        for j, subsection in enumerate(subsections, start=1):
            subsection_title = subsection.get("title_name", "Untitled Subsection")
            table_data.append([f"    {i}.{j} {subsection_title}", ""])

    # 目次のテーブルスタイル
    table = Table(table_data, colWidths=[400, 100])
    table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'IPAexMincho'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
    ]))

    # テーブルを目次に追加
    elements.append(table)

    # PDFの生成
    doc.build(elements, onLaterPages=add_page_number)

    # バッファからPDFデータを取得
    pdf_data = buffer.getvalue()
    buffer.close()

    # S3にアップロード
    try:
        upload_to_s3(bucket_name=S3_BUCKET, object_key=object_key, data=pdf_data, content_type="application/pdf")
    except Exception as e:
        print(str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "PDF generate failed"
            })
        }


    # レスポンスとしてアップロード結果を返す
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "PDF successfully uploaded to s3"
        })
    }

# ページ番号を追加するための関数
def add_page_number(canvas, doc):
    page_num = canvas.getPageNumber() - 1 
    text = f"{page_num}"
    canvas.setFont("IPAexMincho", 10)
    canvas.drawRightString(A4[0] - 40, 30, text)  # ページ右下にページ番号を配置