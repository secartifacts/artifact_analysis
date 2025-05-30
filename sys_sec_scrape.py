import requests

github_urls= {
    'sys': {
        'base_url': "https://github.com/sysartifacts/sysartifacts.github.io/blob/master/_conferences/",
        'raw_base_url': "https://raw.githubusercontent.com/sysartifacts/sysartifacts.github.io/master/_conferences/",
        'api_url': "https://api.github.com/repos/sysartifacts/sysartifacts.github.io/contents/_conferences/"
    },
    'sec': {
        'base_url': "https://github.com/secartifacts/secartifacts.github.io/blob/master/_conferences/",
        'raw_base_url': "https://raw.githubusercontent.com/secartifacts/secartifacts.github.io/master/_conferences/",
        'api_url': "https://api.github.com/repos/secartifacts/secartifacts.github.io/contents/_conferences/"
    }
}

def get_conferences_from_prefix(prefix):
    url = github_urls[prefix]['api_url']
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return [item for item in data if item['type'] == 'dir']

def download_file(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text