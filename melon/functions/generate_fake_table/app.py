import json
import io
import os
import boto3
import base64
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from utilities import configure_matplotlib_fonts

# S3のアップロード先情報
S3_BUCKET = os.environ.get("S3_BUCKET", None)
TABLE_DATA_KEY = 'table_data.json'

def lambda_handler(event, context):
    """
    イベントオブジェクトから表データの配列を受け取り、それぞれのテーブルを画像化して返すLambda関数。
    """
    try:
        # イベントからtablesプロパティを取得
        tables = event.get('tables', [])

        if not tables:
            return {
                'statusCode': 400,
                'body': 'No table data provided in the event.'
            }

        # フォント読み込み
        configure_matplotlib_fonts()
        
        table_images = []
        for table_data in tables:
            print(f"--- [表] {table_data['id']} 処理中... ---")
            print(f"  >  表タイプ: {table_data['table_type']}")
            image_data = create_table_image(table_data)
            table_images.append({
                'id' : table_data['id'],
                'image_data' : image_data
            })

        # S3_BUCKETが設定されている場合はS3にアップロード
        if S3_BUCKET:
            upload_to_s3(table_images)
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Tables uploaded to S3 successfully.'})
            }
        else:
            # S3バケットが設定されていない場合は、Base64エンコードされた画像データを返す
            return {
                'statusCode': 200,
                'body': json.dumps({'table_images': table_images})
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def create_table_image(table_data):
    """
    単一のテーブル定義オブジェクトからテーブルを作成し、Base64エンコードされたPNGデータを返す関数。
    """
    table_type = table_data.get('table_type')
    style = table_data.get('style', {})

    # # Matplotlib figureとAxesを作成
    # fig, ax = plt.subplots(figsize=(12, 3))
    
    # スタイル設定の適用
    # if 'font_size' in style:
    #     mpl.rcParams['font.size'] = style['font_size']
    mpl.rcParams['font.size'] = 14

    if table_type == 'basic':
        columnns = len(table_data['columns'])
        rows = len(table_data['rows'])
        
        # 表を描画するスクリーンサイズ決定
        figsize = calculate_figsize(columns=columnns, rows=rows)
        
        fig, ax = plt.subplots(figsize=figsize)
        
        table_object = render_basic_table(ax, table_data, style)
    elif table_type == 'summary':
        columnns = 5
        rows = len(table_data['statistics'])

        # 表を描画するスクリーンサイズ決定
        figsize = calculate_figsize(columns=columnns, rows=rows)

        fig, ax = plt.subplots(figsize=figsize)
        table_object = render_summary_table(ax, table_data, style)
    elif table_type == 'regression':
        columnns = 5
        rows = len(table_data['regression_results']['coefficients'])

        # 表を描画するスクリーンサイズ決定
        figsize = calculate_figsize(columns=columnns, rows=rows)

        fig, ax = plt.subplots(figsize=figsize)
        table_object = render_regression_table(ax, table_data, style)
    elif table_type == 'correlation':
        columnns = len(table_data['variables'])
        rows = len(table_data['correlation_matrix'])

        # 表を描画するスクリーンサイズ決定
        figsize = calculate_figsize(columns=columnns, rows=rows)

        fig, ax = plt.subplots(figsize=figsize)
        table_object = render_correlation_table(ax, table_data, style)
    elif table_type == 'comparison':
        columnns = 4
        rows = len(table_data['comparison_data'])

        # 表を描画するスクリーンサイズ決定
        figsize = calculate_figsize(columns=columnns, rows=rows)

        fig, ax = plt.subplots(figsize=figsize)
        table_object = render_comparison_table(ax, table_data, style)
    else:
        raise ValueError(f"Unsupported table_type: {table_type}")

    # テーブルの境界線やセルの色などを適用
    apply_table_style(table_object, style)

    # タイトルの設定
    # if 'title' in table_data:
    #     ax.set_title(table_data['title'])

    # 軸と外枠を非表示
    ax.axis('tight')
    ax.axis('off')
    
    # レイアウトを自動調整して見切れを防ぐ
    plt.tight_layout()

    # 余白を減らす
    # fig.subplots_adjust(left=0.05, right=0.995, top=0.05, bottom=0.995)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1) #この1行を入れる
    
    # tight_layoutでレイアウトを調整
    fig.tight_layout(pad=0)
    
    # 画像をバイナリデータとして保存し、Base64エンコード
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches="tight")
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def calculate_figsize(columns, rows):
    """
    列数と行数に基づいて適切なfigsizeを計算
    """
    # ベースの倍率（1列あたり2.0インチ、1行あたり0.3インチ）
    base_col_width = 2.5
    base_row_height = 0.2

    # 計算結果
    width = max(columns * base_col_width, 10.0)  # 最低10インチ確保
    height = max(rows * base_row_height, 2.5)  # 最低2.5インチ確保

    print(f"  >  サイズ(インチ): width {width}, height {height}")

    return (width, height)

def render_basic_table(ax, table_data, style):
    """
    基本的なデータテーブルを描画するヘルパー関数
    """
    columns = table_data['columns']
    rows = table_data['rows']

    # テーブルデータ
    cell_text = []
    for row in rows:
        cell_text.append([str(item) for item in row])

    # 列幅の設定
    # col_widths = style.get('col_widths')
    # if col_widths is None:
    col_widths = [1/len(columns)] * len(columns)
    
    # テーブルの描画
    table_object = ax.table(cellText=cell_text, colLabels=columns, loc='center', colWidths=col_widths)

    return table_object

def render_summary_table(ax, table_data, style):
    """
    統計量のまとめ表を描画するヘルパー関数
    """
    statistics = table_data['statistics']
    # 変数名の一覧と、統計量の種類
    variables = list(statistics.keys())
    stats_labels = ["mean", "median", "std", "min", "max"]

    # テーブルデータ
    cell_text = []
    for var in variables:
        row = [statistics[var][stat] for stat in stats_labels]
        cell_text.append(row)

    # 列幅の設定
    # col_widths = style.get('col_widths')
    # if col_widths is None:
    col_widths = [1/len(stats_labels)] * len(stats_labels)

    # テーブルの描画
    table_object = ax.table(cellText=cell_text, rowLabels=variables, colLabels=stats_labels, loc='center', colWidths=col_widths)

    return table_object

def render_regression_table(ax, table_data, style):
    """
    回帰分析結果の表を描画するヘルパー関数
    """
    results = table_data['regression_results']
    coefficients = results['coefficients']

    # テーブルデータ
    header = ["Variable", "Coefficient", "Std. Error", "t-value", "p-value"]
    cell_text = []
    for coef in coefficients:
        cell_text.append([coef['variable'], coef['coefficient'], coef['std_error'], coef['t_value'], coef['p_value']])

    # 列幅の設定
    # col_widths = style.get('col_widths')
    # if col_widths is None:
    col_widths = [1/len(header)] * len(header)

    # テーブルの描画
    table_object = ax.table(cellText=cell_text, colLabels=header, loc='center', colWidths=col_widths)

    return table_object

def render_correlation_table(ax, table_data, style):
    """
    相関行列表を描画するヘルパー関数
    """
    variables = table_data['variables']
    matrix = table_data['correlation_matrix']

    # テーブルデータ
    cell_text = []
    for row in matrix:
        cell_text.append([f"{val:.3f}" for val in row])

    # 列幅の設定
    # col_widths = style.get('col_widths')
    # if col_widths is None:
    col_widths = [1/len(variables)] * len(variables)

    # テーブルの描画
    table_object = ax.table(cellText=cell_text, rowLabels=variables, colLabels=variables, loc='center', colWidths=col_widths)

    return table_object

def render_comparison_table(ax, table_data, style):
    """
    データ比較表を描画するヘルパー関数
    """
    comparison_data = table_data['comparison_data']
    categories = list(comparison_data.keys())
    stats_labels = ["mean", "std", "min", "max"]

    # テーブルデータ
    cell_text = []
    for category in categories:
        row = [comparison_data[category][stat] for stat in stats_labels]
        cell_text.append(row)

    # 列幅の設定
    # col_widths = style.get('col_widths')
    # if col_widths is None:
    col_widths = [1/len(stats_labels)] * len(stats_labels)

    # テーブルの描画
    table_object = ax.table(cellText=cell_text, rowLabels=categories, colLabels=stats_labels, loc='center', colWidths=col_widths)

    return table_object

def apply_table_style(table_object, style):
    """
    テーブルオブジェクトとスタイル情報を使用して、表のスタイルを調整する関数
    """
    cells = table_object.get_celld()

    if 'header_bg_color' in style or 'header_font_color' in style:
        for (row, col), cell in cells.items():
            # ヘッダーセル (row=0 for colLabels, col=0 for rowLabels)
            # 行ラベルの場合は col=0, 列ラベルの場合は row=0と仮定
            if row == 0 or col == 0:  # ヘッダー行・列
                if 'header_bg_color' in style:
                    cell.set_facecolor(style['header_bg_color'])
                if 'header_font_color' in style:
                    cell.get_text().set_color(style['header_font_color'])

    if 'cell_bg_color' in style or 'cell_font_color' in style:
        for (row, col), cell in cells.items():
            # ヘッダーセル以外がデータセル
            if row != 0 and col != 0:
                if 'cell_bg_color' in style:
                    cell.set_facecolor(style['cell_bg_color'])
                if 'cell_font_color' in style:
                    cell.get_text().set_color(style['cell_font_color'])

    if 'border_color' in style:
        for cell in cells.values():
            cell.set_edgecolor(style['border_color'])

    if 'border_width' in style:
        for cell in cells.values():
            cell.set_linewidth(style['border_width'])

def upload_to_s3(images):
    """
    Base64エンコードされた画像データをS3にアップロードするヘルパー関数
    """
    s3 = boto3.resource('s3')
    for image in images:
        # 一意のキーを作成（例: table_0.png）
        key = f"tables/{image['id']}.png"
        image_binary = base64.b64decode(image['image_data'])
        s3.Object(S3_BUCKET, key).put(Body=image_binary, ContentType='image/png')
