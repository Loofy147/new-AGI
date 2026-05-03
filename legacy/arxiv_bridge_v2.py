import urllib.request
import xml.etree.ElementTree as ET
import time
import os

def fetch_arxiv_abstracts(query, max_results=100, delay=3):
    """
    Fetches abstracts from ArXiv for a given query with rate limiting.
    """
    base_url = 'http://export.arxiv.org/api/query?'
    search_query = f'all:{query.replace(" ", "+")}'

    abstracts = []
    start = 0
    batch_size = 50

    while len(abstracts) < max_results:
        url = f'{base_url}search_query={search_query}&start={start}&max_results={batch_size}'
        print(f"Fetching batch starting at {start} from: {url}")

        try:
            with urllib.request.urlopen(url) as response:
                content = response.read()

            root = ET.fromstring(content)
            ns = {'atom': 'http://www.w3.org/2005/Atom'}

            entries = root.findall('atom:entry', ns)
            if not entries:
                print("No more entries found.")
                break

            for entry in entries:
                summary = entry.find('atom:summary', ns)
                if summary is not None:
                    abstracts.append(summary.text.strip().replace('\n', ' '))

            print(f"Retrieved {len(abstracts)} abstracts so far.")
            start += batch_size
            if len(abstracts) < max_results:
                print(f"Waiting {delay} seconds to respect ArXiv API rate limits...")
                time.sleep(delay)

        except Exception as e:
            print(f"Error during fetch: {e}")
            if "429" in str(e):
                print("Rate limit hit. Sleeping for 30 seconds...")
                time.sleep(30)
                continue
            break

    return abstracts[:max_results]

if __name__ == "__main__":
    # Test with a smaller number to ensure it works
    query = "Dark Matter vs Modified Gravity"
    abstracts = fetch_arxiv_abstracts(query, max_results=50)

    if abstracts:
        with open('abstracts_dm_mg.json', 'w') as f:
            import json
            json.dump(abstracts, f)
        print(f"Successfully saved {len(abstracts)} abstracts to abstracts_dm_mg.json")
