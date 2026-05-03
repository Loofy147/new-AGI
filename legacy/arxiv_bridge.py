import urllib.request
import xml.etree.ElementTree as ET
import time

def fetch_arxiv_abstracts(query, max_results=100):
    """
    Fetches abstracts from ArXiv for a given query.
    """
    base_url = 'http://export.arxiv.org/api/query?'
    search_query = f'all:{query.replace(" ", "+")}'
    url = f'{base_url}search_query={search_query}&start=0&max_results={max_results}'

    print(f"Fetching data from: {url}")
    with urllib.request.urlopen(url) as response:
        content = response.read()

    root = ET.fromstring(content)
    # ArXiv uses Atom namespace
    ns = {'atom': 'http://www.w3.org/2005/Atom'}

    abstracts = []
    for entry in root.findall('atom:entry', ns):
        summary = entry.find('atom:summary', ns)
        if summary is not None:
            abstracts.append(summary.text.strip().replace('\n', ' '))

    return abstracts

if __name__ == "__main__":
    query = "Dark Matter Modified Gravity"
    abstracts = fetch_arxiv_abstracts(query, max_results=50)
    print(f"Retrieved {len(abstracts)} abstracts.")
    if abstracts:
        print("First abstract sample:", abstracts[0][:200] + "...")
