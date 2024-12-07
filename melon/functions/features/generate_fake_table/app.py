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
        tables = event.get('tables')

        if not tables:
            raise Exception("No table data provided in the event.")
    
        if not S3_BUCKET: 
            raise Exception("No S3 Bucket provided in the environ.")

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

        non_trailing_slash_prefix = f"{workflow_id}/tables"
        object_keys = upload_to_s3(non_trailing_slash_prefix, table_images)
        return {
            'statusCode': 200,
            'body': object_keys
        }

    except Exception as e:
        error = {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "payload": event
        }
        logger.exception(error)
        raise e
    
def create_table_image(table_data):
    """
    単一のテーブル定義オブジェクトからテーブルを作成し、Base64エンコードされたSVGデータを返す関数。
    """
    import matplotlib.patches as patches

    table_type = table_data.get('table_type')
    style = table_data.get('style', {})

    # フォントサイズの設定（デフォルト14）
    font_size = 14
    mpl.rcParams['font.size'] = font_size

    # フィギュアと軸を作成
    fig, ax = plt.subplots()

    # テーブルタイプに応じて描画処理を分岐
    if table_type == 'basic':
        table_object, max_cell_width, max_cell_height = render_basic_table(ax, table_data)

        cols = len(table_data.get('columns', []))
        rows = len(table_data.get('rows', []))
    elif table_type == 'summary':
        table_object, max_cell_width, max_cell_height = render_summary_table(ax, table_data)

        cols = 5
        rows = len(table_data.get('statistics', []))
    elif table_type == 'regression':
        table_object, max_cell_width, max_cell_height = render_regression_table(ax, table_data)

        cols = 5
        rows = len(table_data.get('regression_results', []).get('coefficients', []))
    elif table_type == 'correlation':
        table_object, max_cell_width, max_cell_height = render_correlation_table(ax, table_data)

        cols = len(table_data.get('variables', []))
        rows = len(table_data.get('correlation_matrix', []))
    elif table_type == 'comparison':
        table_object, max_cell_width, max_cell_height = render_comparison_table(ax, table_data)

        cols = 4
        rows = len(table_data.get('comparison_data', []))
    else:
        raise ValueError(f"Unsupported table_type: {table_type}")

    # テーブルのスタイル適用
    apply_table_style(table_object, style)

    # 軸と外枠を非表示
    ax.axis('off')

    # テーブルの描画領域を取得
    # fig.canvas.draw()
    # renderer = fig.canvas.get_renderer()
    # table_bbox = table_object.get_window_extent(renderer)

    adjust_figure_size(fig, cols, rows, max_cell_width, max_cell_height)

    # 軸をFigure全体に埋め尽くす
    ax.set_position([0, 0, 1, 1])

    # 余白を最小化
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    plt.tight_layout(pad=0)

    # SVGとして画像を保存
    buf = io.BytesIO()
    fig.savefig(buf, format='svg', bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def adjust_figure_size(fig, cols, rows, base_cell_width, base_cell_height):
    # 基準のセルサイズと列、行数を取得してFigureサイズを動的に調整
    fig_width = round(cols * base_cell_width, 2)
    fig_height = round(rows * base_cell_height * 2.5, 2) 

    # 最小幅6.4インチを保証しつつアスペクト比を維持
    if fig_width < 7.0:
        aspect_ratio = fig_height / fig_width if fig_width > 0 else 1  # アスペクト比を計算
        fig_width = 7.0
        fig_height = round(fig_width * aspect_ratio, 1)

    print(f" ========== ")
    print(f"fig_width: {fig_width}")
    print(f"fig_height: {fig_height}")

    # Figureサイズを調整
    fig.set_size_inches(fig_width, fig_height)


def render_basic_table(ax, table_data):
    """
    基本的なデータテーブルを描画するヘルパー関数
    """

    columns = table_data['columns']
    rows = table_data['rows']

    # テーブルデータを文字列に変換
    cell_text = [[str(item) for item in row] for row in rows]

    # テーブルの描画（bboxで位置とサイズを制御）
    table_object = ax.table(
        cellText=cell_text,
        colLabels=columns,
        loc='center',
        cellLoc='center',
        bbox=[0, 0, 1, 1]  # (left, bottom, width, height)
    )
    
    # --- 最も長いセルと最も高いセルを計算する ---
    renderer = ax.figure.canvas.get_renderer()
    max_width = 0  # 最大の横幅（インチ）
    max_height = 0  # 最大の縦幅（インチ）

    for (_, _), cell in table_object.get_celld().items():
        bbox = cell.get_window_extent(renderer)  # ピクセル単位のバウンディングボックスを取得
        width_in_inches = bbox.width / renderer.dpi  # ピクセルからインチに変換
        height_in_inches = bbox.height / renderer.dpi

        # 最大値を更新
        max_width = max(max_width, width_in_inches)
        max_height = max(max_height, height_in_inches)

    print(f"Max cell width (inches): {max_width}")
    print(f"Max cell height (inches): {max_height}")

    return table_object, max_width, max_height

def render_summary_table(ax, table_data):
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
    table_object = ax.table(
        cellText=cell_text,
        colLabels=stats_labels,
        rowLabels=variables,
        loc='center',
        cellLoc='center',
        bbox=[0, 0, 1, 1]  # (left, bottom, width, height)
    )

    # --- 最も長いセルと最も高いセルを計算する ---
    renderer = ax.figure.canvas.get_renderer()
    max_width = 0  # 最大の横幅（インチ）
    max_height = 0  # 最大の縦幅（インチ）

    for (_, _), cell in table_object.get_celld().items():
        bbox = cell.get_window_extent(renderer)  # ピクセル単位のバウンディングボックスを取得
        width_in_inches = bbox.width / renderer.dpi  # ピクセルからインチに変換
        height_in_inches = bbox.height / renderer.dpi

        # 最大値を更新
        max_width = max(max_width, width_in_inches)
        max_height = max(max_height, height_in_inches)

    print(f"Max cell width (inches): {max_width}")
    print(f"Max cell height (inches): {max_height}")

    return table_object, max_width, max_height

def render_regression_table(ax, table_data):
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
    table_object = ax.table(
        cellText=cell_text,
        colLabels=header,
        loc='center',
        cellLoc='center',
        bbox=[0, 0, 1, 1]  # (left, bottom, width, height)
    )

    # --- 最も長いセルと最も高いセルを計算する ---
    renderer = ax.figure.canvas.get_renderer()
    max_width = 0  # 最大の横幅（インチ）
    max_height = 0  # 最大の縦幅（インチ）

    for (_, _), cell in table_object.get_celld().items():
        bbox = cell.get_window_extent(renderer)  # ピクセル単位のバウンディングボックスを取得
        width_in_inches = bbox.width / renderer.dpi  # ピクセルからインチに変換
        height_in_inches = bbox.height / renderer.dpi

        # 最大値を更新
        max_width = max(max_width, width_in_inches)
        max_height = max(max_height, height_in_inches)

    print(f"Max cell width (inches): {max_width}")
    print(f"Max cell height (inches): {max_height}")

    return table_object, max_width, max_height

def render_correlation_table(ax, table_data):
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
    table_object = ax.table(
        cellText=cell_text,
        colLabels=variables,
        rowLabels=variables,
        loc='center',
        cellLoc='center',
        bbox=[0, 0, 1, 1]  # (left, bottom, width, height)
    )

    # --- 最も長いセルと最も高いセルを計算する ---
    renderer = ax.figure.canvas.get_renderer()
    max_width = 0  # 最大の横幅（インチ）
    max_height = 0  # 最大の縦幅（インチ）

    for (_, _), cell in table_object.get_celld().items():
        bbox = cell.get_window_extent(renderer)  # ピクセル単位のバウンディングボックスを取得
        width_in_inches = bbox.width / renderer.dpi  # ピクセルからインチに変換
        height_in_inches = bbox.height / renderer.dpi

        # 最大値を更新
        max_width = max(max_width, width_in_inches)
        max_height = max(max_height, height_in_inches)

    print(f"Max cell width (inches): {max_width}")
    print(f"Max cell height (inches): {max_height}")

    return table_object, max_width, max_height

def render_comparison_table(ax, table_data):
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
    table_object = ax.table(
        cellText=cell_text,
        colLabels=stats_labels,
        rowLabels=categories,
        loc='center',
        cellLoc='center',
        bbox=[0, 0, 1, 1]  # (left, bottom, width, height)
    )

    # --- 最も長いセルと最も高いセルを計算する ---
    renderer = ax.figure.canvas.get_renderer()
    max_width = 0  # 最大の横幅（インチ）
    max_height = 0  # 最大の縦幅（インチ）

    for (_, _), cell in table_object.get_celld().items():
        bbox = cell.get_window_extent(renderer)  # ピクセル単位のバウンディングボックスを取得
        width_in_inches = bbox.width / renderer.dpi  # ピクセルからインチに変換
        height_in_inches = bbox.height / renderer.dpi

        # 最大値を更新
        max_width = max(max_width, width_in_inches)
        max_height = max(max_height, height_in_inches)

    print(f"Max cell width (inches): {max_width}")
    print(f"Max cell height (inches): {max_height}")

    return table_object, max_width, max_height

def apply_table_style(table_object, style):
    """
    テーブルオブジェクトとスタイル情報を使用して、表のスタイルを調整する関数
    """
    cells = table_object.get_celld()

    # データセルのスタイル適用
    # ヘッダー設定
    header_bg_color = style.get('header_bg_color', '#FFFFFF')  # デフォルトは白
    header_font_color = style.get('header_font_color', '#000000')  # デフォルトは黒

    # セルの設定
    cell_bg_color = style.get('cell_bg_color', '#FFFFFF')  # デフォルトは白
    cell_font_color = style.get('cell_font_color', '#000000')  # デフォルトは黒

    # 境界線の設定
    cell_border_width = style.get('border_width', 0.5) # デフォルトは0.5インチ
    cell_border_color = style.get('border_color', '#FFFFFF') # デフォルトは白

    for (row, col), cell in cells.items():
        # ヘッダーセルの判定（行ラベルや列ラベル）
        if row == 0 or col == -1:
            cell.set_facecolor(header_bg_color)
            cell.get_text().set_color(header_font_color)
        
        # データセルの判定
        elif row > 0 and col >= 0:
            cell.set_facecolor(cell_bg_color)
            cell.get_text().set_color(cell_font_color)
        
        cell.set_linewidth(cell_border_width)
        cell.set_edgecolor(cell_border_color)
            

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
