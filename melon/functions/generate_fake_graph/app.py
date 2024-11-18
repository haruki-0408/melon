import matplotlib.pyplot as plt
import matplotlib as mpl
import io
import os
import boto3
import base64
import numpy as np
import json
import sympy as sp
from matplotlib.patches import Ellipse

# S3のアップロード先情報
S3_BUCKET = os.environ.get("S3_BUCKET", None)
GRAPH_DATA_KEY = 'graph_data.json'

# Matplotlibで日本語を正しく表示できるようにフォントを設定
# 例としてNoto Sans JPを使用します
mpl.font_manager.fontManager.addfont('NotoSansJP-VariableFont_wght.ttf')
mpl.rc('font', family='Noto Sans JP')
mpl.rcParams['axes.unicode_minus'] = False  # マイナス記号を正しく表示

def lambda_handler(event, context):
    """
    イベントオブジェクトからグラフデータを受け取り、動的にグラフを生成してS3にアップロードまたは
    Base64エンコードされたPNGデータを返すメインのLambdaハンドラー関数。
    """
    try:
        # イベントからgraphsプロパティを取得
        graphs = event.get('graphs', [])

        if not graphs:
            return {
                'statusCode': 400,
                'body': 'No graph data provided in the event.'
            }

        # グラフ画像を生成
        graph_images = []
        for graph_data in graphs:
            image_data = create_graph_image(graph_data)
            graph_images.append(image_data)

        # S3_BUCKETが設定されている場合はS3にアップロード
        if S3_BUCKET:
            upload_to_s3(graph_images)
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Graphs uploaded to S3 successfully.'})
            }
        else:
            # S3バケットが設定されていない場合は、Base64エンコードされた画像データを返す
            return {
                'statusCode': 200,
                'body': json.dumps({'graph_images': graph_images})
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def create_graph_image(graph_data):
    """
    単一のグラフ定義オブジェクトからグラフを作成し、Base64エンコードされたPNGデータを返す関数。
    graph_data は指定したスキーマに従います。
    """
    # フィギュアと軸の作成
    fig, ax = plt.subplots(figsize=(graph_data['figure_width'], graph_data['figure_height']))

    # 図全体のプロパティを設定
    ax.set_title(graph_data['title'])
    ax.set_xlabel(graph_data['xlabel'])
    ax.set_ylabel(graph_data['ylabel'])

    if graph_data.get('grid'):
        ax.grid(True)

    # charts配列から個々のグラフを描画
    for chart in graph_data['charts']:
        
        chart_type = chart['chart_type']
        print(chart_type)
        if chart_type == 'line':
            plot_line_chart(ax, chart)
        elif chart_type == 'area':
            plot_area_chart(ax, chart)
        elif chart_type == 'bar':
            plot_bar_chart(ax, chart)
        elif chart_type == 'stacked_bar':
            plot_stacked_bar_chart(ax, chart)
        elif chart_type == 'histogram':
            plot_histogram(ax, chart)
        elif chart_type == 'pie':
            # 円グラフは別軸を使用する必要があるため、特別に処理します
            plot_pie_chart(fig, chart)
        elif chart_type == 'boxplot':
            plot_boxplot(ax, chart)
        elif chart_type == 'scatter':
            plot_scatter_chart(ax, chart)
        elif chart_type == 'ellipse':
            plot_ellipse(ax, chart)
        elif chart_type == 'curve':
            plot_curve_chart(ax, chart)
        elif chart_type == 'heatmap':
            plot_heatmap(ax, chart)
        else:
            raise ValueError(f"Unsupported chart_type: {chart_type}")

    # 凡例の表示
    if graph_data.get('legend'):
        ax.legend()

    # 画像をバイナリデータとして保存し、Base64エンコード
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def plot_line_chart(ax, chart):
    """
    折れ線グラフを描画するヘルパー関数
    """
    for line_data in chart['lines']:
        ax.plot(
            line_data['x'],
            line_data['y'],
            label=line_data['label'],
            color=line_data['color'],
            linestyle=line_data['linestyle'],
            marker=line_data['marker']
        )

def plot_area_chart(ax, chart):
    """
    面グラフを描画するヘルパー関数
    """
    ax.fill_between(
        chart['x'],
        chart['y1'],
        chart['y2'],
        color=chart['colors'][0] if chart['colors'] else 'blue',
        alpha=chart['alphas'][0] if chart['alphas'] else 0.5,
        label="Area Chart"
    )

def plot_bar_chart(ax, chart):
    """
    棒グラフを描画するヘルパー関数
    """
    categories = chart['categories']
    values = chart['values']
    colors = chart['colors']
    ax.bar(categories, values, color=colors)
    # データラベル表示（オプションで追加可）
    for index, value in enumerate(values):
        ax.text(index, value, str(value), ha='center', va='bottom')

def plot_stacked_bar_chart(ax, chart):
    """
    積み上げ棒グラフを描画するヘルパー関数
    """
    categories = chart['categories']
    values_groups = chart['values_groups']
    labels = chart['labels']
    colors = chart['colors']

    bottom_values = np.zeros(len(categories))
    for group_index, group_values in enumerate(values_groups):
        ax.bar(
            categories,
            group_values,
            bottom=bottom_values,
            label=labels[group_index] if labels else None,
            color=colors[group_index] if colors else None
        )
        bottom_values += np.array(group_values)

def plot_histogram(ax, chart):
    """
    ヒストグラムを描画するヘルパー関数
    """
    data = chart['data']
    bins = chart['bins']
    color = chart['color']
    alpha = chart['alpha']
    edgecolor = chart['edgecolor']
    ax.hist(data, bins=bins, color=color, alpha=alpha, edgecolor=edgecolor)

def plot_pie_chart(fig, chart):
    """
    円グラフを描画するヘルパー関数
    既存の軸を使用せずに新しい軸を生成し、円グラフを描画します。
    """
    labels = chart['labels']
    sizes = chart['sizes']
    explode = chart['explode']
    autopct = chart['autopct']
    shadow = chart['shadow']
    startangle = chart['startangle']
    # 新しい軸を作成（円グラフは軸を削除します）
    ax_pie = fig.add_axes([0.1, 0.1, 0.8, 0.8])  # (left, bottom, width, height)
    ax_pie.pie(
        sizes,
        labels=labels,
        explode=explode,
        autopct=autopct,
        shadow=shadow,
        startangle=startangle
    )
    ax_pie.set_aspect('equal')  # 円を丸く描く

def plot_boxplot(ax, chart):
    """
    箱ひげ図を描画するヘルパー関数
    """
    data = chart['data']
    labels = chart['labels']
    ax.boxplot(data, vert=True, patch_artist=True, labels=labels)

def plot_scatter_chart(ax, chart):
    """
    散布図を描画するヘルパー関数
    """
    x = chart['x']
    y = chart['y']
    colors = chart['colors']
    sizes = chart['sizes']
    alpha = chart['alpha']
    cmap = chart['cmap']
    scatter = ax.scatter(x, y, c=colors, s=sizes, alpha=alpha, cmap=cmap)
    # カラーバーを表示する場合
    if cmap:
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('Color Intensity')

def plot_ellipse(ax, chart):
    """
    楕円を描画するヘルパー関数
    """
    center = chart['center']
    width = chart['width']
    height = chart['height']
    edgecolor = chart['edgecolor']
    facecolor = chart['facecolor']
    alpha = chart['alpha']
    xlim = chart['xlim']
    ylim = chart['ylim']

    ellipse = Ellipse(center, width=width, height=height, edgecolor=edgecolor, facecolor=facecolor, alpha=alpha)
    ax.add_patch(ellipse)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)

def plot_curve_chart(ax, chart):
    """
    曲線グラフを描画するヘルパー関数
    """
    x_range = chart['x_range']
    equation_str = chart['equation']
    label = chart['label']
    color = chart['color']
    linestyle = chart['linestyle']

    # x_rangeには [start, end, num_points] が含まれていると想定
    x_values = np.linspace(x_range[0], x_range[1], int(x_range[2]))
    
    # # equation_strを安全に評価（eval）するための準備
    # equation = compile(equation_str, "<string>", "eval")
    # print('y_values before')
    # y_values = [eval(equation, {"__builtins__": None, "np": np, "x": x}) for x in x_values]
    # print('y_values after')
    # ax.plot(x_values, y_values, label=label, color=color, linestyle=linestyle)

    # sympyを使用して安全に数式を評価
    x = sp.symbols('x')
    equation = sp.sympify(equation_str)  # 数式を安全に解析
    y_values = [float(equation.subs(x, val)) for val in x_values]  # 各x値に対するy値を計算

    # グラフをプロット
    ax.plot(x_values, y_values, label=label, color=color, linestyle=linestyle)


def plot_heatmap(ax, chart):
    """
    ヒートマップを描画するヘルパー関数
    """
    data = chart['data']
    cmap = chart['cmap']
    interpolation = chart['interpolation']
    colorbar_label = chart['colorbar_label']

    heatmap = ax.imshow(data, cmap=cmap, interpolation=interpolation)
    cbar = plt.colorbar(heatmap, ax=ax)
    cbar.set_label(colorbar_label)

def upload_to_s3(images):
    """
    Base64エンコードされた画像データをS3にアップロードするヘルパー関数
    """
    s3 = boto3.resource('s3')
    for i, image_data in enumerate(images):
        # 一意のキーを作成（例: graph_0.png）
        key = f"{GRAPH_DATA_KEY.split('.')[0]}_{i}.png"
        image_binary = base64.b64decode(image_data)
        s3.Object(S3_BUCKET, key).put(Body=image_binary, ContentType='image/png')
