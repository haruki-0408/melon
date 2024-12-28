import json
import boto3
import os
import matplotlib as mpl
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from aws_lambda_powertools import Logger
from botocore.exceptions import ClientError
from string import Template
from datetime import datetime
from typing import Dict, Any

# Matplotlib フォントの読み込みと設定関数
def configure_matplotlib_fonts():
    """
    Matplotlibで日本語を正しく表示するためのフォント設定を行う。
    使用フォント : IPAexGothic, 
    """

    GOTHIC_FONT_PATH = '/opt/python/fonts/ipaexg.ttf'
    
    mpl.font_manager.fontManager.addfont(GOTHIC_FONT_PATH)  # 適切なフォントファイルを指定

    mpl.rc('font', family='IPAexGothic')
    mpl.rcParams['axes.unicode_minus'] = False  # マイナス記号の表示対応
    

# DynamoDBからアイテムを取得
def get_dynamo_item(table_name, key, region='ap-northeast-1'):
    dynamodb = boto3.resource("dynamodb", region_name=region)
    table = dynamodb.Table(table_name)
    response = table.get_item(Key=key)
    if 'Item' not in response:
        raise KeyError(f"アイテムが存在しません: {key}")
    return response['Item']

# DynamoDBにアイテムを保存
def put_item_to_dynamodb(table_name, item, region='ap-northeast-1'):
    dynamodb = boto3.resource("dynamodb", region_name=region)
    table = dynamodb.Table(table_name)
    table.put_item(Item=item)


# S3にオブジェクトをアップロードする関数
def upload_to_s3(bucket_name, object_key, data, content_type="application/json"):
    s3_client = boto3.client('s3')

    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=data,
            ContentType=content_type
        )
        
    except ClientError as e:
        raise

# キャメルケースからスネークケースへの変換関数
def camel_to_snake(name):
    return ''.join(['_' + c.lower() if c.isupper() else c for c in name]).lstrip('_')

# FakeThesisデータスキーマjsonファイル読み込み
def read_schema_jsons():
    with open('/opt/python/schemas/formulas_schema.json', 'r', encoding='utf-8') as f:
        formulas_schema_json = json.load(f)
    with open('/opt/python/schemas/graphs_schema.json', 'r', encoding='utf-8') as f:
        graphs_schema_json = json.load(f)
    with open('/opt/python/schemas/tables_schema.json', 'r', encoding='utf-8') as f:
        tables_schema_json = json.load(f)

    return formulas_schema_json, tables_schema_json, graphs_schema_json

    
# s3のバケットとプレフィクスを指定してファイルが存在するか確認する
def check_folder_exists(bucket_name, folder_prefix):
    try:
        s3_client = boto3.client('s3')
        # list_objects_v2で指定したプレフィクスに一致するオブジェクトを取得
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=folder_prefix, MaxKeys=1)
        
        # 'Contents'キーがレスポンスに含まれていればオブジェクトが存在する＝フォルダが存在
        if 'Contents' in response:
            # フォルダ（プレフィクス）が存在する場合
            folder_link = f"https://s3.console.aws.amazon.com/s3/buckets/{bucket_name}?prefix={folder_prefix}/&region=ap-northeast-1&showversions=false"
            return folder_link
        else:
            return None  # フォルダが存在しない場合
    except ClientError as e:
        # S3のエラーが発生した場合は例外を再スロー
        raise e

# DynamoDBのテーブル名とkeyを指定してレコードが存在するか確認する
def check_record_exists_usequery(table_name, pk_name, pk_value, region='ap-northeast-1'):
    dynamodb = boto3.resource('dynamodb', region_name=region)
    table = dynamodb.Table(table_name)

    try:
        # parent_execution_idに紐づくレコードをクエリ
        response = table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key(pk_name).eq(pk_value),
            Limit=1  # 1件のみ取得
        )

        items = response.get('Items', [])

        # エラーレコードが1件でも存在している場合はリンクを生成
        if items:
            # テーブルのAWSコンソールリンクを生成
            link = f"https://console.aws.amazon.com/dynamodb/home?region={region}#tables:selected={table_name};tab=overview"
            return link
        else:
            return None

    except ClientError as e:
        # DynamoDBのエラーが発生した場合は例外を再スロー
        raise e


# stepfunctions実行内容リンク生成
def generate_execution_url(execution_arn: str) -> str:
    region = "ap-northeast-1"
    return f"https://{region}.console.aws.amazon.com/states/home?region={region}#/executions/details/{execution_arn}"

def record_workflow_progress(
    table_name: str,
    workflow_id: str,
    request_id: str,
    order: int,
    status: str,
    state_name: str
) -> Dict[str, Any]:
    """
    ワークフローの進捗をDynamoDBに記録する
    
    Args:
        table_name (str): DynamoDBテーブル名
        workflow_id (str): ワークフローID
        request_id (str): リクエストID
        order (int): 進捗順序
        status (str): ステータス
        state_name (str): ステート名
    
    Returns:
        Dict[str, Any]: 保存したアイテム
    """
    # UTCのタイムスタンプをISO 8601形式で取得
    timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    
    item = {
        'workflow_id': workflow_id,
        'timestamp#order': f"{timestamp}#{order}",
        'state_name': state_name,
        'status': status,
        'request_id': request_id
    }
    
    # DynamoDBに保存
    put_item_to_dynamodb(
        table_name=table_name,
        item=item
    )
    
    return item
