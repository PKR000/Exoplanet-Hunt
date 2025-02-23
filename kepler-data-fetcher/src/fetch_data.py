import requests
from bs4 import BeautifulSoup


def fetch_kepler_data(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching data: {response.status_code}")
    


def list_kepler_files(http_url):
    response = requests.get(http_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        files = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.txt') or a['href'].endswith('.json')]
        return files
    else:
        raise Exception(f"Error listing files: {response.status_code}")



# Example usage for listing files
http_url = 'https://archive.stsci.edu/pub/kepler/'
files = list_kepler_files(http_url)
print("Available files:", files)


# Example usage for fetching a specific file
api_url = 'https://archive.stsci.edu/pub/kepler/somefile.json'
data = fetch_kepler_data(api_url)
print(data)