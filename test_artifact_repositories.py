import requests
import argparse
from sys_sec_artifacts_results_scrape import get_ae_results


def check_url_existence(url):
    try:
        response = requests.head(url, allow_redirects=True)
        return response.status_code == 200
    except requests.RequestException as e:
        return False

def main():

    parser = argparse.ArgumentParser(description='Scraping results of sys/secartifacts.github.io from conferences.')
    parser.add_argument('--conf_regex', type=str, default='.20[1|2][0-9]', help='Regular expression for conference name and or names')
    parser.add_argument('--prefix', type=str, default='sys', help='Prefix of artifacts website like sys for sysartifacts or sec for secartifacts')
    parser.add_argument('--print_failed', action='store_true', help='Print failed website checks')
    parser.add_argument('--url_key', type=str, nargs='+', default=['repository_url'], help='Keys in the artifact dictionary to check the URLs for')

    args = parser.parse_args()

    results = get_ae_results(args.conf_regex, args.prefix)

    counts = {}
    failed = []
    for url_key in args.url_key:
        counts[url_key] = {}
        for name, artifacts in results.items():
            counts[url_key][name] = {}
            counts[url_key][name]['exists'] = 0
            counts[url_key][name]['total'] = 0
            print(f'testing {len(artifacts)} artifacts urls for {url_key}')
            for artifact in artifacts:
                if url_key in artifact:
                    # exception since, some urls are just the doi
                    if artifact[url_key].startswith('10.'):
                        artifact[url_key] = 'https://doi.org/' + artifact[url_key]

                    exists = check_url_existence(artifact[url_key])
                    if exists:
                        counts[url_key][name]['exists'] = counts[url_key][name]['exists'] + 1
                        counts[url_key][name]['total'] = counts[url_key][name]['total'] + 1
                    else:
                        counts[url_key][name]['total'] = counts[url_key][name]['total'] + 1
                        failed.append(artifact[url_key])
                else:
                    counts[url_key][name]['total'] = counts[url_key][name]['total'] + 1
                    failed.append(artifact['title'])

    print("url_key, name, total, exists, failed, percentage")
    for url_key, key_counts in counts.items():
        for name, count in key_counts.items():
            percentage = (count['exists'] / count['total']) * 100 if count['total'] > 0 else 0
            print(f"{url_key}, {name}, {count['total']}, {count['exists']}, {count['total'] - count['exists']}, {percentage:.2f}%")

    if(args.print_failed):
        print("Failed:")
        for f in failed:
            print(f)

if __name__ == "__main__":
    main()