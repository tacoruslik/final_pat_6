import requests
import logging  # модуль для сбора логов
# подтягиваем константы из config файла
from config import LOGS, MAX_GPT_TOKENS, SYSTEM_PROMPT
from creds import get_creds  # модуль для получения токенов

iam_token, folder_id = get_creds()  # получаем iam_token и folder_id из файлов

# настраиваем запись логов в файл
logging.basicConfig(filename=LOGS, level=logging.ERROR, format="%(asctime)s FILE: %(filename)s IN: %(funcName)s MESSAGE: %(message)s", filemode="w")

# подсчитываем количество токенов в сообщениях
def count_gpt_tokens(messages):
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/tokenizeCompletion"
    headers = {
        'Authorization': f'Bearer {"t1.9euelZrIzJmamJCPiZuenoyOjpbPyu3rnpWakM7Mio2OzM6bnZfJk4qVnZTl8_d3Kg1O-e9eG3d0_t3z9zdZCk75714bd3T-zef1656VmsyMmpuQnciQiceekZXHnZnO7_zF656VmsyMmpuQnciQiceekZXHnZnOveuelZqTzpSbnc3KyM2Nz5ubjJuRybXehpzRnJCSj4qLmtGLmdKckJKPioua0pKai56bnoue0oye.GeSZvp4T15VDqSen-3eSeukXLqAfFYvFNu433ppfLfVg5qlMp9BK_K2x9M5GF6ZAd4njQVmZREsSrCWJua0GAA"}',
        'Content-Type': 'application/json'
    }
    data = {
        'modelUri': f"gpt://{'b1g566iiqn0ovmhs44gr'}/yandexgpt-lite",
        "messages": messages
    }
    try:
        return len(requests.post(url=url, json=data, headers=headers).json()['tokens'])
    except Exception as e:
        logging.error(e)  # если ошибка - записываем её в логи
        return 0

# запрос к GPT
def ask_gpt(messages):
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        'Authorization': f'Bearer {"t1.9euelZrIzJmamJCPiZuenoyOjpbPyu3rnpWakM7Mio2OzM6bnZfJk4qVnZTl8_d3Kg1O-e9eG3d0_t3z9zdZCk75714bd3T-zef1656VmsyMmpuQnciQiceekZXHnZnO7_zF656VmsyMmpuQnciQiceekZXHnZnOveuelZqTzpSbnc3KyM2Nz5ubjJuRybXehpzRnJCSj4qLmtGLmdKckJKPioua0pKai56bnoue0oye.GeSZvp4T15VDqSen-3eSeukXLqAfFYvFNu433ppfLfVg5qlMp9BK_K2x9M5GF6ZAd4njQVmZREsSrCWJua0GAA"}',
        'Content-Type': 'application/json'
    }
    data = {
        'modelUri': f"gpt://{'b1g566iiqn0ovmhs44gr'}/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.7,
            "maxTokens": MAX_GPT_TOKENS
        },
        "messages": SYSTEM_PROMPT + messages  # добавляем к системному сообщению предыдущие сообщения
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        # проверяем статус код
        if response.status_code != 200:
            return False, f"Ошибка GPT. Статус-код: {response.status_code}", None
        # если всё успешно - считаем количество токенов, потраченных на ответ, возвращаем статус, ответ, и количество токенов в ответе
        answer = response.json()['result']['alternatives'][0]['message']['text']
        tokens_in_answer = count_gpt_tokens([{'role': 'assistant', 'text': answer}])
        return True, answer, tokens_in_answer
    except Exception as e:
        logging.error(e)  # если ошибка - записываем её в логи
        return False, "Ошибка при обращении к GPT",  None 