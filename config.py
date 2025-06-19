import os
from dotenv import load_dotenv

load_dotenv()

AZURE_KEY = os.getenv("AZURE_TRANSLATOR_KEY")
AZURE_ENDPOINT = "https://api.cognitive.microsofttranslator.com"
AZURE_REGION = "northeurope"

HF_MODEL = "Helsinki-NLP/opus-mt-es-en"
