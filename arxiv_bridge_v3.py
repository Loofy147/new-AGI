import urllib.request
import xml.etree.ElementTree as ET
import time
import os
import json
import hashlib

CACHE_DIR = "arxiv_cache"

def get_cache_filename(query):
    query_hash = hashlib.md5(query.encode()).hexdigest()
    return os.path.join(CACHE_DIR, f"{query_hash}.json")

def fetch_arxiv_abstracts(query, max_results=50, delay=3):
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

    cache_file = get_cache_filename(query)
    if os.path.exists(cache_file):
        print(f"Loading cached results for: {query}")
        with open(cache_file, 'r') as f:
            return json.load(f)

    base_url = 'http://export.arxiv.org/api/query?'
    search_query = f'all:{query.replace(" ", "+")}'

    abstracts = []
    start = 0
    batch_size = 50

    while len(abstracts) < max_results:
        url = f'{base_url}search_query={search_query}&start={start}&max_results={batch_size}'
        print(f"Fetching batch starting at {start} from ArXiv...")

        try:
            with urllib.request.urlopen(url) as response:
                content = response.read()

            root = ET.fromstring(content)
            ns = {'atom': 'http://www.w3.org/2005/Atom'}

            entries = root.findall('atom:entry', ns)
            if not entries: break

            for entry in entries:
                summary = entry.find('atom:summary', ns)
                if summary is not None:
                    abstracts.append(summary.text.strip().replace('\n', ' '))

            print(f"Retrieved {len(abstracts)} abstracts.")
            start += batch_size
            if len(abstracts) < max_results:
                time.sleep(delay)

        except Exception as e:
            print(f"Error: {e}")
            if "429" in str(e):
                print("Rate limit hit. Returning partial results.")
                break
            break

    if abstracts:
        with open(cache_file, 'w') as f:
            json.dump(abstracts, f)

    return abstracts

if __name__ == "__main__":
    query = "Dark Matter vs Modified Gravity"
    # Using mock data first to avoid live API issues in CI/CD environments
    mock_file = "mock_abstracts.json"
    if os.path.exists(mock_file):
        print(f"Using local mock data: {mock_file}")
        with open(mock_file, 'r') as f:
            abstracts = json.load(f)
    else:
        abstracts = fetch_arxiv_abstracts(query, max_results=10)

    print(f"Total abstracts available: {len(abstracts)}")
