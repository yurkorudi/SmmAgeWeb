import requests

response = requests.get(
    "https://api.mymemory.translated.net/get",
    params={
        "q": "Hello, how are you?",
        "langpair": "en|uk"
    }
)

print(response.status_code)
print(response.text)