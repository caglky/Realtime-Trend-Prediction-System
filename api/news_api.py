import requests

API_KEY = "24381f77d2484341aaee0bcad6d56194"

def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=turkey&apiKey={API_KEY}"
    response = requests.get(url)
    print("Status Code: ", response.status_code)
    print("\nRAW JSON: ", response.json())
    return response.json()