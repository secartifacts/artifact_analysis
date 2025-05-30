import requests
import re
import yaml
import argparse
from sys_sec_scrape import get_conferences_from_prefix, github_urls, download_file

def get_ae_results(conference_regex, prefix):
    results = {}
    # get conference name from prefix
    conferences = get_conferences_from_prefix(prefix)
    if conferences is None:
        print(f"Invalid prefix: {prefix}")
        return results
    # get the base url for the conference
    for conf in conferences:
        if re.search(conference_regex, conf['name']):
            name = conf['name']
            file_url = github_urls[prefix]['raw_base_url'] + name + '/results.md'

            try:
                results[name] = download_file(file_url)
                print(f'got {name}')
            except requests.exceptions.HTTPError as e:
                print("couldn't get " + name)

    parsed_results = {}

    for year, content in results.items():
        content = content.split('---')[1]
        try:
            parsed_content = yaml.safe_load(content)
            if 'artifacts' in parsed_content:
                parsed_results[year] = parsed_content['artifacts']
        except yaml.YAMLError as e:
            print(f"Error parsing TOML for year {year}: {e}")

    return parsed_results

def main():

    parser = argparse.ArgumentParser(description='Scraping results of sys/secartifacts.github.io from conferences.')
    parser.add_argument('--conf_regex', type=str, default='.20[1|2][0-9]', help='Regular expression for conference name and or years')
    parser.add_argument('--prefix', type=str, default='sys', help='Prefix of artifacts website like sys for sysartifacts or sec for secartifacts')

    args = parser.parse_args()

    results = get_ae_results(args.conf_regex, args.prefix)
    for year in results.keys():
        print(f"{year}: {len(results[year])}")
        print(results[year])

if __name__ == "__main__":
    main()