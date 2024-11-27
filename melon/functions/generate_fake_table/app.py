import json
import io
import os
from aws_lambda_powertools import Logger
import boto3
import base64
import matplotlib.pyplot as plt
import matplotlib as mpl
from utilities import configure_matplotlib_fonts

logger = Logger(service="generate_fake_table")

# S3のアップロード先情報
S3_BUCKET = os.environ.get("S3_BUCKET", None)

@logger.inject_lambda_context(log_event=False)
def lambda_handler(event, context):
    """
    イベントオブジェクトから表データの配列を受け取り、それぞれのテーブルを画像化して返すLambda関数。
    """
    try:
        # イベントからtablesプロパティを取得
        workflow_id = event.get('workflow_id')
        tables = event.get('tables', [])

        if not tables:
            return {
                'statusCode': 400,
                'body': 'No table data provided in the event.'
            }

        # フォント読み込み
        configure_matplotlib_fonts()
        
        table_images = []
        for index, table_data in enumerate(tables):
            print(f"--- [表] {table_data['id']} 処理中... ---")
            print(f"  >  タイプ: {table_data['table_type']}")
            image_data = create_table_image(table_data)
            table_images.append({
                'id' : table_data['id'],
                'image_data' : image_data,
                'table_number' : str(index + 1),
                'title': table_data['title']  # タイトルを保持
            })

        # S3_BUCKETが設定されている場合はS3にアップロード
        if S3_BUCKET:
            non_trailing_slash_prefix = f"{workflow_id}/tables"
            upload_to_s3(non_trailing_slash_prefix, table_images)
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
        logger.exception(e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def create_table_image(table_data):
    """
    単一のテーブル定義オブジェクトからテーブルを作成し、Base64エンコードされたSVGデータを返す関数。
    """
    table_type = table_data.get('table_type')
    style = table_data.get('style', {})

    # フォントサイズの設定（デフォルト12）
    font_size = style.get('font_size', 12)
    mpl.rcParams['font.size'] = font_size

    # フィギュアと軸を作成（サイズは自動調整）
    fig, ax = plt.subplots()

    # テーブルタイプに応じて描画処理を分岐
    if table_type == 'basic':
        table_object = render_basic_table(ax, table_data, style)
    elif table_type == 'summary':
        table_object = render_summary_table(ax, table_data, style)
    elif table_type == 'regression':
        table_object = render_regression_table(ax, table_data, style)
    elif table_type == 'correlation':
        table_object = render_correlation_table(ax, table_data, style)
    elif table_type == 'comparison':
        table_object = render_comparison_table(ax, table_data, style)
    else:
        raise ValueError(f"Unsupported table_type: {table_type}")

    # テーブルのスタイル適用
    apply_table_style(table_object, style)

    # 軸と外枠を非表示
    ax.axis('off')

    # 図を描画してレンダラーを取得
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()

    # テーブルを軸全体にフィットさせる
    table_bbox = table_object.get_window_extent(renderer).transformed(fig.dpi_scale_trans.inverted())
    ax.set_xlim(table_bbox.x0, table_bbox.x1)
    ax.set_ylim(table_bbox.y0, table_bbox.y1)

    # 余白を最小化
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    plt.tight_layout(pad=0)

    # 画像をバイナリデータとして保存し、Base64エンコード（SVG形式）
    buf = io.BytesIO()
    fig.savefig(buf, format='svg', bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def render_basic_table(ax, table_data, style):
    """
    基本的なデータテーブルを描画するヘルパー関数
    """
    columns = table_data['columns']
    rows = table_data['rows']

    # テーブルデータを文字列に変換
    cell_text = []
    for row in rows:
        cell_text.append([str(item) for item in row])

    # テーブルの描画（bboxで位置とサイズを制御）
    table_object = ax.table(
        cellText=cell_text,
        colLabels=columns,
        loc='center',
        cellLoc='center',
        bbox=[0, 0, 1, 1]  # (left, bottom, width, height)
    )

    return table_object

def render_summary_table(ax, table_data, style):
    """
    統計量のまとめ表を描画するヘルパー関数
    """
    statistics = table_data['statistics']
    variables = list(statistics.keys())
    stats_labels = ["mean", "median", "std", "min", "max"]

    # テーブルデータを抽出
    cell_text = []
    for var in variables:
        row = [statistics[var][stat] for stat in stats_labels]
        cell_text.append(row)

    # テーブルの描画
    # table_object = ax.table(
    #     cellText=cell_text,
    #     rowLabels=variables,
    #     colLabels=stats_labels,
    #     loc='center'
    # )

    table_object = ax.table(
        cellText=cell_text,
        colLabels=stats_labels,
        rowLabels=variables,
        loc='center',
        cellLoc='center',
        bbox=[0, 0, 1, 1]  # (left, bottom, width, height)
    )

    return table_object

def render_regression_table(ax, table_data, style):
    """
    回帰分析結果の表を描画するヘルパー関数
    """
    results = table_data['regression_results']
    coefficients = results['coefficients']

    header = ["Variable", "Coefficient", "Std. Error", "t-value", "p-value"]
    cell_text = []
    for coef in coefficients:
        row = [
            coef['variable'],
            coef['coefficient'],
            coef['std_error'],
            coef['t_value'],
            coef['p_value']
        ]
        cell_text.append(row)

    # テーブルの描画
    # table_object = ax.table(
    #     cellText=cell_text,
    #     colLabels=header,
    #     loc='center'
    # )

    table_object = ax.table(
        cellText=cell_text,
        colLabels=header,
        loc='center',
        cellLoc='center',
        bbox=[0, 0, 1, 1]  # (left, bottom, width, height)
    )

    return table_object

def render_correlation_table(ax, table_data, style):
    """
    相関行列表を描画するヘルパー関数
    """
    variables = table_data['variables']
    matrix = table_data['correlation_matrix']

    # テーブルデータを文字列に変換（小数点以下3桁）
    cell_text = []
    for row in matrix:
        cell_text.append([f"{val:.3f}" for val in row])

    # テーブルの描画
    # table_object = ax.table(
    #     cellText=cell_text,
    #     rowLabels=variables,
    #     colLabels=variables,
    #     loc='center'
    # )

    table_object = ax.table(
        cellText=cell_text,
        colLabels=variables,
        rowLabels=variables,
        loc='center',
        cellLoc='center',
        bbox=[0, 0, 1, 1]  # (left, bottom, width, height)
    )

    return table_object

def render_comparison_table(ax, table_data, style):
    """
    データ比較表を描画するヘルパー関数
    """
    comparison_data = table_data['comparison_data']
    categories = list(comparison_data.keys())
    stats_labels = ["mean", "std", "min", "max"]

    # テーブルデータを抽出
    cell_text = []
    for category in categories:
        row = [comparison_data[category][stat] for stat in stats_labels]
        cell_text.append(row)

    # テーブルの描画
    # table_object = ax.table(
    #     cellText=cell_text,
    #     rowLabels=categories,
    #     colLabels=stats_labels,
    #     loc='center'
    # )

    table_object = ax.table(
        cellText=cell_text,
        colLabels=stats_labels,
        rowLabels=categories,
        loc='center',
        cellLoc='center',
        bbox=[0, 0, 1, 1]  # (left, bottom, width, height)
    )

    return table_object

def apply_table_style(table_object, style):
    """
    テーブルオブジェクトとスタイル情報を使用して、表のスタイルを調整する関数
    """
    cells = table_object.get_celld()

    # ヘッダーセルのスタイル適用
    if 'header_bg_color' in style or 'header_font_color' in style:
        for (row, col), cell in cells.items():
            # ヘッダーセルの判定（行ラベルや列ラベル）
            if row == 0 or col == -1:
                if 'header_bg_color' in style:
                    cell.set_facecolor(style['header_bg_color'])
                if 'header_font_color' in style:
                    cell.get_text().set_color(style['header_font_color'])

    # データセルのスタイル適用
    if 'cell_bg_color' in style or 'cell_font_color' in style:
        for (row, col), cell in cells.items():
            # データセルの判定
            if row > 0 and col >= 0:
                if 'cell_bg_color' in style:
                    cell.set_facecolor(style['cell_bg_color'])
                if 'cell_font_color' in style:
                    cell.get_text().set_color(style['cell_font_color'])

    # 境界線の色と幅を設定
    if 'border_color' in style:
        for cell in cells.values():
            cell.set_edgecolor(style['border_color'])

    if 'border_width' in style:
        for cell in cells.values():
            cell.set_linewidth(style['border_width'])

def upload_to_s3(non_trailing_slash_prefix, tables):
    """
    Base64エンコードされた画像データをS3にアップロードするヘルパー関数
    """
    s3 = boto3.resource('s3')
    for table in tables:
        # 一意のキーを作成（例: table_0.svg）
        key = f"{non_trailing_slash_prefix}/{table['id']}.svg"
        image_binary = base64.b64decode(table['image_data'])

        # 日本語タイトルをBase64エンコード
        encoded_title = base64.b64encode(table['title'].encode('utf-8')).decode('utf-8')

        s3.Object(S3_BUCKET, key).put(
            Body=image_binary,
            ContentType='image/svg+xml',
            Metadata={
                'number': table['table_number'],
                'type': 'table', 
                'title': encoded_title
            }
        )
