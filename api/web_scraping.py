import requests
from bs4 import BeautifulSoup

def get_tr_news(url):
    try:
        response = requests.get(url, timeout=10) 
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        titles =  [t.text for t in soup.find_all("h3")] 
        return titles
    
    except requests.exceptions.Timeout:
        print("Request is timeout")
        return []
    except requests.exceptions.RequestException as error:
        print("Request error: ", error)
        return []
