import requests
from bs4 import BeautifulSoup

github_urls= {
    'sys': {
        'base_url': "https://github.com/sysartifacts/sysartifacts.github.io/blob/master/_conferences/",
        'raw_base_url': "https://raw.githubusercontent.com/sysartifacts/sysartifacts.github.io/master/_conferences/"
    },
    'sec': {
        'base_url': "https://github.com/secartifacts/secartifacts.github.io/blob/master/_conferences/",
        'raw_base_url': "https://raw.githubusercontent.com/secartifacts/secartifacts.github.io/master/_conferences/"
    }
}

def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

def download_file(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text