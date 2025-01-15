import os
import random
import time
import anthropic
from anthropic.types.beta.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.beta.messages.batch_create_params import Request
from aws_lambda_powertools import Logger

logger = Logger(service_name="common_anthropic_client")

class AnthropicClient:
    def __init__(self):
        """
        Anthropic APIクライアントの初期化。
        """
        self.api_key = os.environ["ANTHROPIC_API_KEY"]
        self.api_model = os.environ["ANTHROPIC_API_MODEL"]
        self.client = anthropic.Anthropic(api_key=self.api_key)

    def call_message_request(self, system_prompt, messages, max_tokens=4096, temperature=0.1):
        """
        Anthropic APIのメッセージリクエストを呼び出す。

        Parameters:
        - system_prompt (str): システムプロンプト。
        - messages (list): ユーザーとアシスタントのメッセージ履歴。
        - max_tokens (int): 生成されるテキストの最大トークン数。
        - temperature (float): 温度パラメータ（テキストの多様性を制御）。

        Returns:
        - str: アシスタントの応答テキスト。
        """
        response = self.client.beta.prompt_caching.messages.create(
            model=self.api_model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=[
                {
                    "type": "text",
                    "text": system_prompt,
                    "cache_control": {"type": "ephemeral"}
                }
            ],
            messages=messages
        )
        print("==== Response Usage ====")
        logger.info(response.usage)
        return response.content[0].text

    def generate_batch_request(self, prompt, max_tokens=4096, temperature=0.1):
        """
        Anthropic APIのバッチリクエストを生成。

        Parameters:
        - prompt (str): ユーザープロンプト。
        - max_tokens (int): 生成されるテキストの最大トークン数。
        - temperature (float): 温度パラメータ。

        Returns:
        - Request: バッチリクエストオブジェクト。
        """
        custom_id = "message_" + str(random.randint(1, 10000))
        request = Request(
            custom_id=custom_id,
            params=MessageCreateParamsNonStreaming(
                model=self.api_model,
                max_tokens=max_tokens,
                system="",
                temperature=temperature,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
        )
        return request

    def retrieve_batch_status(self, message_batch_id):
        """
        バッチリクエストの進捗状況を取得。

        Parameters:
        - message_batch_id (str): バッチID。

        Returns:
        - dict: バッチリクエストのステータス。
        """
        while True:
            response = self.client.beta.messages.batches.retrieve(message_batch_id)
            if response.processing_status == "ended":
                logger.info(f"Batch {message_batch_id} has completed processing.")
                break
            logger.info(f"Batch {message_batch_id} is still processing...")
            time.sleep(60)
        return response

    def retrieve_batch_results(self, message_batch_id):
        """
        バッチリクエストの結果を取得。

        Parameters:
        - message_batch_id (str): バッチID。

        Returns:
        - list: バッチリクエストの結果。
        """
        results = []
        for result in self.client.beta.messages.batches.results(message_batch_id):
            results.append(result)
        return results

    def cancel_all_batches(self):
        """
        すべてのバッチリクエストをキャンセル。

        Returns:
        - list: キャンセル結果のリスト。
        """
        canceled_batches = []
        for message_batch in self.client.beta.messages.batches.list(limit=20):
            logger.info(f"Canceling batch: {message_batch}")
            cancel_result = self.client.beta.messages.batches.cancel(message_batch_id=message_batch.id)
            canceled_batches.append(cancel_result)
        return canceled_batches
