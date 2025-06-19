import requests
from config.config import DEEPL_API_KEY

response = requests.post(
    "https://api-free.deepl.com/v2/usage",
    data={"auth_key": DEEPL_API_KEY},
)

print(response.json())
