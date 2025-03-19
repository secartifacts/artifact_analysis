import argparse
import requests
from sys_sec_artifacts_results_scrape import get_ae_results
from test_artifact_repositories import check_artifact_exists

def zenodo_stats(url):
    if '/records/' in url:
        # url format zenodo.org/record/123456
        rec = url.split('/records/')[-1]
    elif 'zenodo.' in url:
        # format 10.5281/zenodo.13827000
        rec = url.split('zenodo.')[-1]
    else:
        print(f'Could not work with zenodo url {url}')
    response = requests.get(f'https://zenodo.org/api/records/{rec}')
    if response.status_code == 200:
        record = response.json()
        return {'zenodo_views': record['stats']['unique_views'],'zenodo_downloads': record['stats']['unique_downloads'], 'updated_at': record['updated']}
    else:
        print(f'Could not collect stats for {url}')
        return

def figshare_stats(url):
    if url.endswith(('.v1', '.v2', '.v3', '.v4', '.v5', '.v6', '.v7', '.v8', '.v9')):
        url = url[:-3]

    article_id = url.split('figshare.')[-1]
    # views
    response = requests.get('https://stats.figshare.com/total/views/article/'+article_id)
    if response.status_code == 200:
        record = response.json()
        views = record['totals']
    else:
        views = -1
    # downloads
    response = requests.get('https://stats.figshare.com/total/downloads/article/'+article_id)
    if response.status_code == 200:
        record = response.json()
        downloads = record['totals']
    else:
        downloads = -1

    response = requests.get(f'https://api.figshare.com/v2/articles/{article_id}')
    if response.status_code == 200:
        record = response.json()
        updated = record['modified_date']
    else:
        updated = 'NA'

    return {'figshare_views':views, 'figshare_downloads': downloads, 'updated_at': updated}

def github_stats(url):
    repo = url.split('github.com/')[1]
    if '/tree/' in repo:
        # remove any specific tree entities of a repository to get the main repo
        repo = repo.split('/tree/')[0]
    if '/blob/' in repo:
        # remove any specific pointers to files in a repository to get the main repo
        repo = repo.split('/blob/')[0]
    if '/pkgs/' in repo:
        # remove any specific pointers to packages in a repository to get the main repo
        repo = repo.split('/pkgs/')[0]
    if repo.endswith('/'):
        repo = repo[:-1]
    if repo.endswith('.git'):
        repo = repo.replace('.git', '')
    response = requests.get(f'https://api.github.com/repos/{repo}')
    if response.status_code == 200:
        repo_record = response.json()
        return {'github_forks': repo_record.get('forks_count', 0),'github_stars': repo_record.get('stargazers_count', 0), 'updated_at': repo_record.get('updated_at', 'NA')}
    else:
        print(f'Could not collect stats for {url}')
        return

def get_all_artifact_stats(results, url_keys):
    for name, artifacts in results.items():
        for url_key in url_keys:
            print(f'Getting stats for {len(artifacts)}')
            for artifact in artifacts:
                if url_key+'_exists' in artifact and artifact[url_key+'_exists']:
                    if 'zenodo' in artifact[url_key]:
                        stats = zenodo_stats(artifact[url_key])
                        if stats:
                            artifact['stats'] = stats

                    elif 'figshare' in artifact[url_key]:
                        stats = figshare_stats(artifact[url_key])
                        if stats:
                            artifact['stats'] = stats

                    elif 'github' in artifact[url_key]:
                        stats = github_stats(artifact[url_key])
                        if stats:
                            artifact['stats'] = stats

                    else:
                        print(f'No stats for {artifact[url_key]} at {name} titled {artifact["title"]}')
                else:
                    print(f'{url_key} does not exist for {artifact["title"]} at {name}')

    return results

def main():

    parser = argparse.ArgumentParser(description='Scraping results of sys/secartifacts.github.io from conferences.')
    parser.add_argument('--conf_regex', type=str, default='.20[1|2][0-9]', help='Regular expression for conference name and or names')
    parser.add_argument('--prefix', type=str, default='sys', help='Prefix of artifacts website like sys for sysartifacts or sec for secartifacts')
    parser.add_argument('--url_keys', type=str, nargs='+', default=['repository_url'], help='Keys in the artifact dictionary to check the URLs for')

    args = parser.parse_args()
    results = get_ae_results(args.conf_regex, args.prefix)
    results, _, _ = check_artifact_exists(results, args.url_keys)

    results = get_all_artifact_stats(results, args.url_keys)

    artifact_id = 0
    for name, artifacts in results.items():
        for artifact in artifacts:
            if 'stats' not in artifact:
                continue

            for key, value in artifact['stats'].items():
                print(f'{name},{artifact_id},{key},{value}')

            artifact_id += 1

if __name__ == "__main__":
    main()