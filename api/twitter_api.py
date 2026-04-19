import requests

BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAOhz9AEAAAAAKdGnY24ZIgXuJMJY31D6nMOqTeY%3DG7Oak06w7tdvf4fnRyFp4vk0JoneDUml6LyOxrejboDoWXYBQl"  

def get_tweets(query, max_results = 10):

    url = "https://api.x.com/2/tweets/search/recent"
    headers = {
        "Authorization" : f"Bearer {BEARER_TOKEN}"
    } #X'in örnek çağrılarında Bearer Token header ile gönderiliyor

    params = {
        "query" : query,
        "max_results" : max_results,
        "tweet.fields" : "created_at, public_metrics, lang"
    }

    response = requests.get(url, headers = headers, params=params, timeout=15)
    print("X status code: ", response.status_code)
    print("X raw json: ", response.json())

    return response.json()




