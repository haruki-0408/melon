import json
import boto3
import os

S3_BUCKET = os.environ.get("S3_BUCKET")
s3 = boto3.client('s3')

def lambda_handler(event, context):
    """
    イベントで渡されたLaTeX数式とその説明をS3に保存するLambda関数
    """
    # S3バケット名を環境変数から取得
    
    if not S3_BUCKET:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'S3_BUCKET environment variable not set'})
        }


    # イベントから数式の配列を取得
    formulas = event.get('formulas', [])
    if not formulas:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'No formulas provided in event'})
        }

    try:
        metadata_keys = []
        for eq in formulas:
            id = eq.get('id')
            latex_code = eq.get('latex_code')
            description = eq.get('description', '')
            parameters = eq.get('parameters', [])

            # 入力の検証・サニタイズが必要

            # 数式のメタデータをS3に保存
            metadata_key = f'formulas/{id}_metadata.json'

            metadata_keys.append(metadata_key)
            
            metadata = {
                'description': description,
                'parameters': parameters,
                'latex_code': latex_code
            }
            s3.put_object(
                Bucket=S3_BUCKET,
                Key=metadata_key,
                Body=json.dumps(metadata, ensure_ascii=False),
                ContentType='application/json'
            )

        return {
            'statusCode': 200,
            'body': metadata_keys
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
