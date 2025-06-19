import uuid
import requests
from config.config import AZURE_KEY, AZURE_ENDPOINT, AZURE_REGION

constructed_url = AZURE_ENDPOINT + "/translate"

headers = {
    "Ocp-Apim-Subscription-Key": AZURE_KEY,
    "Ocp-Apim-Subscription-Region": AZURE_REGION,
    "Content-type": "application/json",
    "X-ClientTraceId": str(uuid.uuid4()),
}

params = {
    "api-version": "3.0",
    "from": "es",
    "to": "en",
}


def translate_text(text: str, target_lang: str, source_lang) -> str:
    body = [{"text": text}]

    params["from"] = source_lang
    params["to"] = target_lang

    response = requests.post(constructed_url, params=params, headers=headers, json=body)
    response.raise_for_status()
    return response.json()[0]["translations"][0]["text"]
