import requests, uuid, json

key = "BuMPtV9wwPkHouEjXvyjdZucMlam3WRRTt6RCiv0Cx2qJc4vSem1JQQJ99BFACi5YpzXJ3w3AAAbACOG8O3T"
endpoint = "https://api.cognitive.microsofttranslator.com"

location = "northeurope"

path = "/translate"
constructed_url = endpoint + path

params = {
    "api-version": "3.0",
    "from": "en",
    "to": "es",
}

headers = {
    "Ocp-Apim-Subscription-Key": key,
    "Ocp-Apim-Subscription-Region": location,
    "Content-type": "application/json",
    "X-ClientTraceId": str(uuid.uuid4()),
}


body = [{"text": "I would really like to drive your car around the block a few times!"}]

request = requests.post(constructed_url, params=params, headers=headers, json=body)
response = request.json()

print(
    json.dumps(
        response, sort_keys=True, ensure_ascii=False, indent=4, separators=(",", ": ")
    )
)
