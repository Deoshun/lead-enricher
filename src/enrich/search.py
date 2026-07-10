import requests
from bs4 import BeautifulSoup
import time
import random

def search(query, k=5):
    wait_time = random.uniform(0.5, 5)
    print(f"Sleeping for {wait_time:.2f} seconds...")
    time.sleep(wait_time)
    print("Done!")
    
    url = "https://html.duckduckgo.com/html/"
    
    # Payload for a POST request (how the HTML version handles queries)
    payload = {
        'q': query,
        'b': '' # Required for some DDG parameters
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Origin": "https://duckduckgo.com",
        "Referer": "https://duckduckgo.com/"
    }

    try:
        # We use POST here because it's how the static HTML form submits
        response = requests.post(url, data=payload, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        links = []
        
        # DDG HTML results are in 'a.result__a'
        results = soup.select('.result__a')
        
        for res in results:
            link = res.get('href')
            if link and link.startswith('http'):
                links.append(link)
                if len(links) == k:
                    break
        
        return links

    except Exception as e:
        print(f"DDG Scrape failed: {e}")
        return []
