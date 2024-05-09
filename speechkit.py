import requests
from config import *
from creds import get_creds  # модуль для получения токенов

iam_token, folder_id = get_creds()  # получаем iam_token и folder_id из файлов

def speech_to_text(data):
    # iam_token, folder_id для доступа к Yandex SpeechKit
    # Указываем параметры запроса
    params = "&".join([
        "topic=general",  # используем основную версию модели
        f"folderId={'b1g566iiqn0ovmhs44gr'}",
        "lang=ru-RU"  # распознаём голосовое сообщение на русском языке
    ])

    # Аутентификация через IAM-токен
    headers = {
        'Authorization': f'Bearer {"t1.9euelZrIzJmamJCPiZuenoyOjpbPyu3rnpWakM7Mio2OzM6bnZfJk4qVnZTl8_d3Kg1O-e9eG3d0_t3z9zdZCk75714bd3T-zef1656VmsyMmpuQnciQiceekZXHnZnO7_zF656VmsyMmpuQnciQiceekZXHnZnOveuelZqTzpSbnc3KyM2Nz5ubjJuRybXehpzRnJCSj4qLmtGLmdKckJKPioua0pKai56bnoue0oye.GeSZvp4T15VDqSen-3eSeukXLqAfFYvFNu433ppfLfVg5qlMp9BK_K2x9M5GF6ZAd4njQVmZREsSrCWJua0GAA"}',
    }

    # Выполняем запрос
    response = requests.post(
        f"https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?{params}",
        headers=headers,
        data=data
    )

    # Читаем json в словарь
    decoded_data = response.json()
    # Проверяем, не произошла ли ошибка при запросе
    if decoded_data.get("error_code") is None:
        return True, decoded_data.get("result")  # Возвращаем статус и текст из аудио
    else:
        return False, "При запросе в SpeechKit возникла ошибка"


def text_to_speech(text):
    # iam_token, folder_id для доступа к Yandex SpeechKit

    # Аутентификация через IAM-токен
    headers = {
        'Authorization': f'Bearer {"t1.9euelZrIzJmamJCPiZuenoyOjpbPyu3rnpWakM7Mio2OzM6bnZfJk4qVnZTl8_d3Kg1O-e9eG3d0_t3z9zdZCk75714bd3T-zef1656VmsyMmpuQnciQiceekZXHnZnO7_zF656VmsyMmpuQnciQiceekZXHnZnOveuelZqTzpSbnc3KyM2Nz5ubjJuRybXehpzRnJCSj4qLmtGLmdKckJKPioua0pKai56bnoue0oye.GeSZvp4T15VDqSen-3eSeukXLqAfFYvFNu433ppfLfVg5qlMp9BK_K2x9M5GF6ZAd4njQVmZREsSrCWJua0GAA"}',
    }
    data = {
        'text': text,  # текст, который нужно преобразовать в голосовое сообщение
        'lang': 'ru-RU',  # язык текста - русский
        'voice': 'filipp',  # мужской голос Филиппа
        'folderId': 'b1g566iiqn0ovmhs44gr',
    }
    # Выполняем запрос
    response = requests.post(
        'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize',
        headers=headers,
        data=data
    )
    if response.status_code == 200:
        return True, response.content  # возвращаем статус и аудио
    else:
        return False, "При запросе в SpeechKit возникла ошибка"