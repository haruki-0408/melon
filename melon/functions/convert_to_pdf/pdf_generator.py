import base64
import io
import os
from io import BytesIO
from aws_lambda_powertools import Logger
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (BaseDocTemplate, Paragraph, Spacer, PageBreak,Frame, PageTemplate, Image)
from PIL import Image as PILImage
from reportlab.lib.units import mm
from fonts import register_fonts #　フォントファイル
from styles import get_pdf_styles, get_table_style #　スタイルファイル
from formula_processor import process_formula # 数式処理
import boto3
from svglib.svglib import svg2rlg
import re

LOGGER_SERVICE = "convert_to_pdf"
logger = Logger(service=LOGGER_SERVICE)

def create_pdf_document(workflow_id, title, abstract, sections_format, s3_bucket):
    """
    PDFドキュメントを生成する関数。

    Parameters:
    - title (str): 論文のタイトル。
    - abstract (str): 要約。
    - sections_format (list): セクション情報のリスト。
    - s3_bucket (str): S3バケット名。
    """
    # フォントの登録
    register_fonts()
    
    # スタイルの取得
    styles = get_pdf_styles()
    table_style = get_table_style()
    
    # ページサイズとマージンの設定
    PAGE_SIZE = A4

    # 表紙の余白設定（変更しない）
    COVER_TOP_MARGIN = 120  # 表紙の上余白（ポイント）
    COVER_BOTTOM_MARGIN = 48  # 表紙の下余白（ポイント）
    COVER_LEFT_MARGIN = 72  # 表紙の左余白（ポイント）
    COVER_RIGHT_MARGIN = 72  # 表紙の右余白（ポイント）

    # 第2ページ目以降の余白設定（指定された値をmmからポイントに変換）
    MAIN_LEFT_MARGIN = 24 * mm
    MAIN_RIGHT_MARGIN = 24 * mm
    # MAIN_TOP_MARGIN = 30 * mm
    MAIN_TOP_MARGIN = 0 * mm
    MAIN_BOTTOM_MARGIN = 28 * mm

    # バッファを作成（PDFのバイナリデータを一時的に保持）
    buffer = BytesIO()

    # フレームの作成（各ページのレイアウト領域を定義）
    cover_frame = Frame(
        COVER_LEFT_MARGIN,
        COVER_BOTTOM_MARGIN,
        PAGE_SIZE[0] - COVER_LEFT_MARGIN - COVER_RIGHT_MARGIN,
        PAGE_SIZE[1] - COVER_TOP_MARGIN - COVER_BOTTOM_MARGIN,
        id='cover_frame'
    )

    main_frame = Frame(
        MAIN_LEFT_MARGIN,
        MAIN_BOTTOM_MARGIN,
        PAGE_SIZE[0] - MAIN_LEFT_MARGIN - MAIN_RIGHT_MARGIN,
        PAGE_SIZE[1] - MAIN_TOP_MARGIN - MAIN_BOTTOM_MARGIN,
        id='main_frame'
    )

    # ページテンプレートの作成（ページごとのレイアウトとページ番号設定）
    cover_template = PageTemplate(id='Cover', frames=[cover_frame], onPage=add_page_number)
    main_template = PageTemplate(id='Main', frames=[main_frame], onPage=add_page_number)

    # ドキュメントの作成
    doc = BaseDocTemplate(
        buffer,
        pagesize=PAGE_SIZE,
        pageTemplates=[cover_template, main_template],
        leftMargin=MAIN_LEFT_MARGIN,
        rightMargin=MAIN_RIGHT_MARGIN,
        topMargin=MAIN_TOP_MARGIN,
        bottomMargin=MAIN_BOTTOM_MARGIN,
    )

    # コンテンツリスト（PDFに追加する要素のリスト）
    elements = []

    # 表紙の作成
    author = '嘘論文　生成器'
    elements.extend(create_cover_page(title, author, abstract, styles))

    # 目次の作成
    elements.extend(create_toc_page(sections_format, styles, table_style))

    # 本文の作成
    elements.extend(create_main_content(workflow_id, sections_format, styles, s3_bucket))

    # PDFの生成
    doc.build(elements)

    # バッファからPDFデータを取得
    pdf_data = buffer.getvalue()
    buffer.close()
    
    return pdf_data

def create_cover_page(title, author, abstract, styles):
    """
    表紙ページを作成する関数。
    """
    elements = []
    elements.append(Spacer(1, 120))  # 上部にスペースを追加
    elements.append(Paragraph(title, styles['FakeThesisTitle']))  # タイトルを追加
    elements.append(Spacer(1, 20))  # スペースを追加
    elements.append(Paragraph(f"著者: {author}", styles['Author']))  # 著者名を右寄せで表示
    elements.append(Spacer(1, 60))  # スペースを追加
    elements.append(Paragraph("要旨", styles['AbstractHeading']))  # 要約見出しを追加
    elements.append(Spacer(1, 12))  # スペースを追加
    # 改行を反映した要約のParagraphを追加
    abstract_paragraphs = [Paragraph(p, styles['FakeThesisBodyText']) for p in abstract.split('\n')]
    for para in abstract_paragraphs:
        elements.append(para)
        elements.append(Spacer(1, 12))
    elements.append(PageBreak())  # 改ページ
    return elements

def create_toc_page(sections_format, styles, table_style):
    """
    目次ページを作成する関数。
    """
    elements = []
    elements.append(Paragraph("目次", styles['AbstractHeading']))  # 目次見出しを追加
    elements.append(Spacer(1, 24))  # スペースを追加

    # 目次データの作成
    table_data = []
    for i, section in enumerate(sections_format, start=1):
        section_title = section.get("title_name")
        sub_sections = section.get("sub_sections")

        # セクションを目次に追加
        table_data.append([f"{i}. {section_title}", ""])

        # サブセクションを目次に追加
        for j, sub_section in enumerate(sub_sections, start=1):
            sub_section_title = sub_section.get("title_name")
            table_data.append([f"    {i}.{j} {sub_section_title}", ""])

    # 目次テーブルの作成
    from reportlab.platypus import Table
    table = Table(table_data, colWidths=[400, 100])
    table.setStyle(table_style)
    elements.append(table)
    elements.append(PageBreak())  # 改ページ
    return elements

def create_main_content(workflow_id, sections_format, styles, s3_bucket):
    """
    本文を作成する関数。

    Parameters:
    - sections_format (list): セクション情報のリスト。
    - styles (StyleSheet1): スタイルシート。
    - s3_bucket (str): S3バケット名。
    """
    elements = []
    s3_client = boto3.client('s3')

    for i, section in enumerate(sections_format, start=1):
        section_title = section.get("title_name")
        sub_sections = section.get("sub_sections")

        # セクションの追加
        elements.append(Paragraph(f"{i}. {section_title}", styles['SectionHeading']))

        # サブセクションの追加
        for j, sub_section in enumerate(sub_sections, start=1):
            sub_section_title = sub_section.get("title_name")
            text = sub_section.get("text", "")
            # graphs = sub_section.get("graphs")
            # tables = sub_section.get("tables")
            # formulas = sub_section.get("formulas")

            # サブセクションのタイトル
            elements.append(Paragraph(f"{i}.{j} {sub_section_title}", styles['SubSectionHeading']))

            # テキストの処理（改行と挿入識別子の処理）
            elements.extend(process_text(workflow_id, text, styles, s3_client, s3_bucket))

    return elements

def process_text(workflow_id, text, styles, s3_client, s3_bucket):
    """
    テキストを処理し、Paragraphと画像を生成する関数。

    Parameters:
    - text (str): 処理するテキスト。
    - styles (StyleSheet1): スタイルシート。
    - s3_client: S3クライアント。
    - s3_bucket (str): S3バケット名。

    Returns:
    - elements (list): Paragraphや画像のリスト。
    """
    elements = []

    # 改行でテキストを分割
    paragraphs = text.split('\n')

    for paragraph in paragraphs:
        # 挿入識別子の検出
        insert_pattern = r'\[INSERT_(.*?)\]'
        matches = re.finditer(insert_pattern, paragraph)

        last_end = 0
        for match in matches:
            start, end = match.span()
            insert_id = match.group(1)

            # 挿入識別子の前のテキストを追加
            if start > last_end:
                content = paragraph[last_end:start]
                if content.strip():
                    elements.append(Paragraph(content.strip(), styles['FakeThesisBodyText']))

            # 挿入識別子の処理
            if insert_id.startswith('FORMULA'):
                # 数式メタデータの処理
                object_key = f"{workflow_id}/formulas/{insert_id}_metadata.json"
                formula_elements = process_formula(object_key, s3_client, s3_bucket, styles)
                elements.extend(formula_elements)
            elif insert_id.startswith('GRAPH'):
                # グラフ画像の処理
                object_key = f"{workflow_id}/graphs/{insert_id}.svg"
                graph_elements = insert_image(object_key, styles, s3_client, s3_bucket)
                elements.extend(graph_elements)
            elif insert_id.startswith('TABLE'):
                # 表画像の処理
                object_key = f"{workflow_id}/tables/{insert_id}.svg"
                table_elements = insert_image(object_key, styles, s3_client, s3_bucket)
                elements.extend(table_elements)

            last_end = end

        # 挿入識別子の後のテキストを追加
        if last_end < len(paragraph):
            content = paragraph[last_end:]
            if content.strip():
                elements.append(Paragraph(content.strip(), styles['FakeThesisBodyText']))

        # 段落間のスペース
        elements.append(Spacer(1, 12))

    return elements

def insert_image(object_key, styles, s3_client, s3_bucket):
    """
    画像をS3からダウンロードし、メタデータに基づいてタイトルを追加してPDFに埋め込む準備をする関数。

    Parameters:
    - object_key (str): S3内のオブジェクトキー（画像ファイルのキー）。
    - styles: ReportLabのスタイル辞書。
    - s3_client: S3クライアント。
    - s3_bucket (str): S3バケット名。

    Returns:
    - elements (list): タイトルと画像（またはSVGを変換したDrawingオブジェクト）を含むリスト。
    """
    elements = []
    try:
        # S3から画像をダウンロード
        response = s3_client.get_object(Bucket=s3_bucket, Key=object_key)
        image_data = response['Body'].read()

        # メタデータを取得してデコード
        metadata = response['Metadata']
        number = metadata.get('number', '')  # デフォルト値を設定
        title_base64 = metadata.get('title')
        content_type = metadata.get('type')

        title = base64.b64decode(title_base64).decode('utf-8') if title_base64 else 'Untitled'
        print('------')
        print(number)
        print(title)
        print(content_type)

        # ファイルの拡張子を確認
        # _, file_extension = os.path.splitext(object_key)
        # file_extension = file_extension.lower()
        # print(f"拡張子:{file_extension}")

        if content_type == 'graph':
            # SVGファイルの場合、svglibを使用してDrawingオブジェクトを作成
            svg_file_obj = io.BytesIO(image_data)
            drawing = svg2rlg(svg_file_obj)
            drawing.hAlign = 'CENTER'

            # サイズを半分にスケール
            drawing.width = drawing.width / 1.6
            drawing.height = drawing.height / 1.6
            drawing.scale(0.625, 0.625)

            # 描画オブジェクトをelementsに追加
            reportlab_image = drawing

            # 図のタイトルを画像の下に追加
            elements.append(Spacer(1, 24))  # 画像前のスペースを追加
            elements.append(reportlab_image)
            elements.append(Spacer(1, 3))  # 画像とタイトルの間にスペースを追加
            elements.append(Paragraph(f"図{number}. {title}", styles['CaptionText']))
            elements.append(Spacer(1, 24))  # 画像後のスペースを追加

        elif content_type == 'table':
            # SVGファイルの場合、svglibを使用してDrawingオブジェクトを作成
            svg_file_obj = io.BytesIO(image_data)
            drawing = svg2rlg(svg_file_obj)
            drawing.hAlign = 'CENTER'

            # サイズをにスケール
            drawing.width = drawing.width / 1.6
            drawing.height = drawing.height / 1.6
            drawing.scale(0.625, 0.625)

            # 描画オブジェクトをelementsに追加
            reportlab_image = drawing

            # 表のタイトルを画像の上に追加
            elements.append(Spacer(1, 24))  # 画像前のスペースを追加
            elements.append(Paragraph(f"表{number}. {title}", styles['CaptionText']))
            elements.append(Spacer(1, 3)) # 画像とタイトルの間にスペースを追加
            elements.append(reportlab_image)
            elements.append(Spacer(1, 24))  # 画像後のスペースを追加
            

    except Exception as e:
        logger.exception(f"Failed to insert image {object_key}: {str(e)}")

    return elements


def add_page_number(canvas, doc):
    """
    ページ番号をページ下部に追加する関数。

    Parameters:
    - canvas (Canvas): 現在のページキャンバス。
    - doc (BaseDocTemplate): ドキュメントオブジェクト。
    """
    # 現在のページ番号を取得（表紙を除くために -1）
    page_num = canvas.getPageNumber() - 1
    if page_num == 1:
        # 目次には ローマ数字でページ番号を付与
        text = "i"
        canvas.setFont("IPAexMincho", 10)  # フォントを設定
        canvas.drawString(280, 15, text)
    elif page_num >= 2:
        # 目次以降のページには アラビア数字で付与
        text = f"{page_num - 1}"
        canvas.setFont("IPAexMincho", 10)  # フォントを設定
        canvas.drawString(280, 15, text)
