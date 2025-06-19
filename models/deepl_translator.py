from config.config import DEEPL_API_KEY
import requests
import time
import deepl


# DEEPL_ENDPOINT = "https://api-free.deepl.com/v2/translate"


# def translate_text(text: str, target_lang: str, source_lang: str) -> str:
#     for attempt in range(3):
#         try:
#             data = {
#                 "auth_key": DEEPL_API_KEY,
#                 "text": text,
#                 "target_lang": target_lang.upper(),
#             }
#             if source_lang:
#                 data["source_lang"] = source_lang.upper()

#             response = requests.post(DEEPL_ENDPOINT, data=data)
#             response.raise_for_status()
#             return response.json()["translations"][0]["text"]
#         except requests.exceptions.HTTPError as e:
#             if response.status_code == 429 and attempt < 2:
#                 print("Rate limit alcanzado. Reintentando en 3 segundos...")
#                 time.sleep(3)
#                 continue
#             raise


def translate_text(text: str, target_lang: str, source_lang: str = None) -> str:
    if DEEPL_API_KEY is None:
        raise ValueError("DEEPL_API_KEY must not be None")
    print(
        f"Translating text to {target_lang.upper()} from {source_lang.upper() if source_lang else 'auto-detect'}..."
    )
    translator = deepl.Translator(DEEPL_API_KEY)
    result = translator.translate_text(text, target_lang="EN-US")
    return result.text
