from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def get_pdf_styles():
    """
    PDFで使用するスタイルシートを取得する関数。

    Returns:
    - styles (StyleSheet1): スタイルシートオブジェクト。
    """
    styles = getSampleStyleSheet()
    # デフォルトフォントを明朝体に設定
    for style_name in styles.byName:
        styles.byName[style_name].fontName = 'IPAexMincho'

    # カスタムスタイルの追加

    # タイトルスタイル（表紙のタイトル用）
    styles.add(ParagraphStyle(
        name="FakeThesisTitle",
        fontName='IPAexMincho',
        fontSize=24,
        leading=24 * 1.2,  # 行送りをフォントサイズの1.2倍に設定
        alignment=1,  # 中央揃え
        spaceAfter=20  # 後のスペース
    ))

    # 著者名スタイル（表紙の著者名用）
    styles.add(ParagraphStyle(
        name="Author",
        fontName='IPAexMincho',
        fontSize=12,
        alignment=2,  # 右揃え
        spaceAfter=20
    ))

    # 要旨見出しスタイル
    styles.add(ParagraphStyle(
        name="AbstractHeading",
        fontName='IPAexMincho',
        fontSize=16,
        alignment=1,  # 中央揃え
        spaceAfter=14
    ))

    # セクション見出しスタイル
    styles.add(ParagraphStyle(
        name="SectionHeading",
        fontName='IPAexMincho',
        fontSize=14,
        leading=14 * 1.2,  # 行送り
        alignment=0,  # 左揃え
        spaceBefore=14 * 1.5,  # 前のスペース（1.5行）
        spaceAfter=14 * 0.5,   # 後のスペース（0.5行）
        fontWeight='bold'  # ボールド体
    ))

    # サブセクション見出しスタイル
    styles.add(ParagraphStyle(
        name="SubSectionHeading",
        fontName='IPAexMincho',
        fontSize=12,
        leading=12 * 1.2,
        alignment=0,
        spaceBefore=12 * 1.0,  # 前のスペース（1行）
        spaceAfter=0,          # 後のスペースなし
        fontWeight='bold'
    ))

    # 本文スタイル
    styles.add(ParagraphStyle(
        name="FakeThesisBodyText",
        fontName='IPAexMincho',
        fontSize=10.5,
        leading=10.5 * 1.2,
    ))

    # 数式スタイル
    # styles.add(ParagraphStyle(
    #     name="FormulaStyle",
    #     fontName='IPAexMincho',
    #     fontSize=12,
    #     leading=12 * 1.2,
    #     alignment=1,  # 中央揃え
    #     spaceBefore=12 * 1.0,
    #     spaceAfter=12 * 1.0
    # ))

    # キャプションスタイル（図表や数式の見出し用）
    styles.add(ParagraphStyle(
        name="CaptionText",
        fontName='IPAexMincho',
        fontSize=10.5,
        leading=10.5 * 1.2,
        alignment=1,  # 中央揃え
        spaceBefore=10.5 * 0.5,  # 前のスペース（0.5行）
        spaceAfter=10.5 * 1.0,   # 後のスペース（1行）
        fontStyle='italic'  # イタリック体
    ))

    return styles

def get_table_style():
    """
    目次テーブルで使用するスタイルを取得する関数。

    Returns:
    - table_style (TableStyle): テーブルスタイルオブジェクト。
    """
    from reportlab.lib import colors
    from reportlab.platypus import TableStyle

    table_style = TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),  # テキストカラーを黒に設定
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # 左揃え
        ('FONTNAME', (0, 0), (-1, -1), 'IPAexMincho'),  # フォントを明朝体に設定
        ('FONTSIZE', (0, 0), (-1, -1), 10.5),  # フォントサイズを10.5ポイントに設定
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),  # セル下部のパディング
        ('TOPPADDING', (0, 0), (-1, -1), 6),     # セル上部のパディング
    ])
    return table_style
