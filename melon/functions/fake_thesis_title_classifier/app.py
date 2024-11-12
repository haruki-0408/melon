import json
import boto3
import os

# AWSクライアントの設定
translate = boto3.client('translate')
comprehend = boto3.client('comprehend')
dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    # イベントの内容をログに出力
    japanese_fake_thesis_title = event.get('title')
    COMPREHEND_CUSTOM_MODEL_ENDPOINT_ARN = os.environ["COMPREHEND_CUSTOM_MODEL_ENDPOINT_ARN"]
    print("----")
    print(COMPREHEND_CUSTOM_MODEL_ENDPOINT_ARN)
    # Amazon Translate APIを使用して翻訳
    translate_response = translate.translate_text(
        Text=japanese_fake_thesis_title,
        SourceLanguageCode='ja',
        TargetLanguageCode='en'
    )

    translated_text = translate_response['TranslatedText']
    print(translated_text)

    # Amazon Comprehendのカスタム分類モデルを使用して分類
    comprehend_response = comprehend.classify_document(
        Text=translated_text,
        EndpointArn=COMPREHEND_CUSTOM_MODEL_ENDPOINT_ARN
    )

    classification_result = comprehend_response['Classes']

    # 最高スコアのラベルを取得
    highest_score_class = max(classification_result, key=lambda x: x['Score'])

    print(classification_result)

    # DynamoDBにデータを格納
    # request_id = str(uuid.uuid4())
    # dynamodb.put_item(
    #     TableName='<DynamoDBのリソース名>',
    #     Item={
    #         'RequestId': {'S': request_id},
    #         'OriginalText': {'S': text_to_translate},
    #         'TranslatedText': {'S': translated_text},
    #         'ClassificationResult': {'S': json.dumps(classification_result)},
    #         'HighestLabel': {'S': highest_label},
    #         'HighestScore': {'N': str(highest_score)}
    #     }
    # )

    # ユーザーに返却するレスポンス
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Text processed successfully', 'highest_score_class' : highest_score_class})
    }