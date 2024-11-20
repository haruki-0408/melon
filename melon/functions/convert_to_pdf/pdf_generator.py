from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (BaseDocTemplate, Paragraph, Spacer, Table, PageBreak,
                                Frame, PageTemplate)
from reportlab.lib.units import mm

# フォントとスタイル関連の関数をインポート
from fonts import register_fonts
from styles import get_pdf_styles, get_table_style

def create_pdf_document(title, author, abstract, toc):
    """
    PDFドキュメントを生成する関数。

    Parameters:
    - title (str): 論文のタイトル。
    - author (str): 著者名。
    - abstract (str): 要旨。
    - toc (list): 目次情報（セクションとサブセクションのリスト）。

    Returns:
    - pdf_data (bytes): 生成されたPDFのバイナリデータ。
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
    MAIN_TOP_MARGIN = 30 * mm
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
    elements.extend(create_cover_page(title, author, abstract, styles))

    # 目次の作成
    elements.extend(create_toc_page(toc, styles, table_style))

    # 本文の作成
    # elements.extend(create_main_content(toc, styles))

    # PDFの生成
    doc.build(elements)

    # バッファからPDFデータを取得
    pdf_data = buffer.getvalue()
    buffer.close()
    
    return pdf_data

def create_cover_page(title, author, abstract, styles):
    """
    表紙ページを作成する関数。

    Parameters:
    - title (str): 論文のタイトル。
    - author (str): 著者名。
    - abstract (str): 要旨。
    - styles (StyleSheet1): スタイルシート。

    Returns:
    - elements (list): 表紙ページの要素リスト。
    """
    elements = []
    elements.append(Spacer(1, 120))  # 上部にスペースを追加
    elements.append(Paragraph(title, styles['FakeThesisTitle']))  # タイトルを追加
    elements.append(Spacer(1, 20))  # スペースを追加
    elements.append(Paragraph(f"著者: {author}", styles['Author']))  # 著者名を右寄せで表示
    elements.append(Spacer(1, 60))  # スペースを追加
    elements.append(Paragraph("要旨", styles['AbstractHeading']))  # 要旨見出しを追加
    elements.append(Spacer(1, 12))  # スペースを追加
    elements.append(Paragraph(abstract, styles['FakeThesisBodyText']))  # 要旨本文を追加
    elements.append(Spacer(1, 48))  # スペースを追加
    elements.append(PageBreak())  # 改ページ
    return elements

def create_toc_page(toc, styles, table_style):
    """
    目次ページを作成する関数。

    Parameters:
    - toc (list): 目次情報。
    - styles (StyleSheet1): スタイルシート。
    - table_style (TableStyle): テーブルスタイル。

    Returns:
    - elements (list): 目次ページの要素リスト。
    """
    elements = []
    elements.append(Paragraph("目次", styles['AbstractHeading']))  # 目次見出しを追加
    elements.append(Spacer(1, 24))  # スペースを追加

    # 目次データの作成
    table_data = []
    for i, section in enumerate(toc, start=1):
        section_title = section.get("title_name", "Untitled Section")
        subsections = section.get("sub_sections", [])

        # セクションを目次に追加
        table_data.append([f"{i}. {section_title}", ""])

        # サブセクションを目次に追加
        for j, subsection in enumerate(subsections, start=1):
            subsection_title = subsection.get("title_name", "Untitled Subsection")
            table_data.append([f"    {i}.{j} {subsection_title}", ""])

    # 目次テーブルの作成
    table = Table(table_data, colWidths=[400, 100])
    table.setStyle(table_style)
    elements.append(table)
    elements.append(PageBreak())  # 改ページ
    return elements

def create_main_content(toc, styles):
    """
    本文を作成する関数。

    Parameters:
    - toc (list): 目次情報。
    - styles (StyleSheet1): スタイルシート。

    Returns:
    - elements (list): 本文の要素リスト。
    """
    elements = []
    for i, section in enumerate(toc, start=1):
        section_title = section.get("title_name", "Untitled Section")
        subsections = section.get("sub_sections", [])
        content = section.get("content", "")

        # セクションの追加
        elements.append(Paragraph(f"{i}. {section_title}", styles['SectionHeading']))
        if content:
            elements.append(Paragraph(content, styles['FakeThesisBodyText']))

        # サブセクションの追加
        for j, subsection in enumerate(subsections, start=1):
            subsection_title = subsection.get("title_name", "Untitled Subsection")
            sub_content = subsection.get("content", "")

            elements.append(Paragraph(f"{i}.{j} {subsection_title}", styles['SubSectionHeading']))
            if sub_content:
                elements.append(Paragraph(sub_content, styles['FakeThesisBodyText']))
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
    print('------------------')
    print(page_num)
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
        # canvas.drawRightString(A4[0] - 40, 30, text)  # ページ右下にページ番号を描画
