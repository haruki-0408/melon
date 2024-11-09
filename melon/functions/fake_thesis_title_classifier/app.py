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
    

    # Amazon Translate APIを使用して翻訳
    translate_response = translate.translate_text(
        Text=japanese_fake_thesis_title,
        SourceLanguageCode='ja',
        TargetLanguageCode='en'
    )

    translated_text = translate_response['TranslatedText']
    print(translated_text)

    # Amazon Comprehendのカスタム分類モデルを使用して分類
    # comprehend_response = comprehend.classify_document(
    #     Text=translated_text,
    #     EndpointArn='<ComprehendエンドポイントのARN>'
    # )

    # classification_result = comprehend_response['Classes']

    # # 最高スコアのラベルを取得
    # highest_score_class = max(classification_result, key=lambda x: x['Score'])
    # highest_label = highest_score_class['Name']
    # highest_score = highest_score_class['Score']

    # print(classification_result)
    # print(highest_label)
    # print(highest_score)

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
        'body': json.dumps({'message': 'Text processed successfully', 'label': highest_label})
    }