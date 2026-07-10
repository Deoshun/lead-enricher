import requests
import re
import time
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser
from collections import deque

import phonenumbers

class Scraper:
    def extract_global_phones(self, html_content):
        valid_phones = set()
        
        for match in phonenumbers.PhoneNumberMatcher(html_content, None):
            if phonenumbers.is_possible_number(match.number):

                formatted = phonenumbers.format_number(
                    match.number, 
                    phonenumbers.PhoneNumberFormat.INTERNATIONAL
                )
                valid_phones.add(formatted)
                
        return valid_phones

    def get_robot_parser(self, seed_url):
        """Fetches and parses robots.txt once."""
        parsed_url = urlparse(seed_url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        rp = RobotFileParser()
        try:
            rp.set_url(urljoin(base_url, "/robots.txt"))
            rp.read()
            return rp
        except:
            return None

    def extract_static(self, seed_url, max_depth=1):
        print(seed_url)
        queue = deque([(seed_url, 0)])
        visited = set()
        results = {"emails": set(), "socials": set(), "phones": set()}
        
        # Patterns
        email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        social_regex = r'https?://(?:www\.)?(?:facebook|twitter|instagram|linkedin|github)\.com/[a-zA-Z0-9_./]+'
        phone_regex = r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'

        # Initialize Robots.txt parser
        rp = self.get_robot_parser(seed_url)
        crawl_delay = rp.crawl_delay("*") if rp else 0

        print(f"Starting crawl. Robots.txt found: {rp is not None}. Delay: {crawl_delay}s")

        while queue:
            url, depth = queue.popleft()

            if url in visited or depth > max_depth:
                continue
            
            # Compliance Check
            if rp and not rp.can_fetch("*", url):
                print(f"Skipping (Robots.txt): {url}")
                continue

            visited.add(url)
            
            try:
                # Adding a User-Agent makes requests look more like a browser
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
                response = requests.get(url, headers=headers, timeout=10)
                
                if response.status_code != 200:
                    continue
                
                content = response.text
                
                # 1. Extraction
                results["emails"].update(re.findall(email_regex, content))
                results["socials"].update(re.findall(social_regex, content))
                results["phones"].update(self.extract_global_phones(content))
                
                # 2. Recursion Logic
                if depth < max_depth:
                    links = re.findall(r'href=["\'](/?.*?)["\']', content)
                    for link in links:
                        full_url = urljoin(url, link)
                        if urlparse(full_url).netloc == urlparse(seed_url).netloc:
                            # Ensure we don't add the same URL to the queue twice
                            if full_url not in visited:
                                queue.append((full_url, depth + 1))
                
                print(f"Processed: {url} (Depth: {depth})")
                
                # Respect Crawl-delay if it exists
                if crawl_delay:
                    time.sleep(crawl_delay)

            except Exception as e:
                print(f"Failed {url}: {e}")

        return results


#from duckduckgo_search import DDGS

#def search_ddg(query, k=5):
#    with DDGS() as ddgs:
#        
#        results = [r['href'] for r in ddgs.text(query, max_results=k)]
#    return results

# Usage
#query = "clean hearts cafe commericial road london instagram"
#top_links = search_ddg(query, k=5)
#print(top_links)
