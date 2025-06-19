import requests
import uuid
import os
from docx.oxml.ns import qn
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("AZURE_TRANSLATOR_KEY")
endpoint = "https://api.cognitive.microsofttranslator.com"
location = "northeurope"
constructed_url = endpoint + "/translate"

params = {
    "api-version": "3.0",
    "from": "es",
    "to": "en",
}

headers = {
    "Ocp-Apim-Subscription-Key": key,
    "Ocp-Apim-Subscription-Region": location,
    "Content-type": "application/json",
    "X-ClientTraceId": str(uuid.uuid4()),
}


def translate_text(text: str, target_lang: str) -> str:
    body = [{"text": text}]
    params["to"] = target_lang
    response = requests.post(constructed_url, params=params, headers=headers, json=body)
    response_json = response.json()
    return response_json[0]["translations"][0]["text"]


def has_drawing(run) -> bool:
    return bool(run._element.findall(".//" + qn("w:drawing")))


def translate_paragraph(paragraph, target_lang: str):
    full_text = paragraph.text
    if not full_text.strip():
        return

    translated_text = translate_text(full_text, target_lang)
    written = False
    for run in paragraph.runs:
        if run.text.strip() and not has_drawing(run):
            if not written:
                run.text = translated_text
                written = True
            else:
                run.text = ""
