import pandas as pd
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import time

session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'})

retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retries))



df=pd.read_csv("https://raw.githubusercontent.com/jgalazka/SB_publications/refs/heads/main/SB_publication_PMC.csv")
links=df.iloc[:, 1]
title=df.iloc[:, 0]
linklist=links.tolist()
titlelist=title.tolist()




def fetch_text_from_link(url):
    try:
        response = session.get(url, timeout=15)
        response.raise_for_status()  # raises error if 403/404
        soup = BeautifulSoup(response.text, "html.parser")
        for script in soup(["script","style","img","noscript"]):
            script.extract()
        text = soup.get_text(separator=" ", strip=True)
        return text  # optional: limit size
        print(response.text)
        time.sleep(random.uniform(1,3))
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
    
texts=[]
for link in linklist:
    text=fetch_text_from_link(link)
    texts.append(text)

print(texts[1])
