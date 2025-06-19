import boto3
import os
from config.config import AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION

translate = boto3.client(
    "translate",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION,
)


def translate_text(text: str, target_lang: str, source_lang: str) -> str:
    if not text.strip():
        return text

    params = {
        "Text": text,
        "TargetLanguageCode": target_lang,
    }

    if source_lang:
        params["SourceLanguageCode"] = source_lang

    response = translate.translate_text(**params)
    return response["TranslatedText"]
