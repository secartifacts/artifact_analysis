import requests
from bs4 import BeautifulSoup
import re
import yaml
import argparse
from sys_sec_scrape import get_soup, github_urls, download_file

def get_committee_for_conference(conference, prefix):
    base_url = github_urls[prefix]['raw_base_url'] + conference
    # committee files are either named committee.md or organizers.md
    try:
        response = download_file(base_url + '/committee.md')
    except requests.exceptions.HTTPError as e:
        try:
            response = download_file(base_url + '/organizers.md')
        except requests.exceptions.HTTPError as e:
            print(f"couldn't get committee for {conference}")
            return None

    committees_text = response.split('Artifact Evaluation Committee')
    aec = committees_text[len(committees_text)-1].strip()
    committee = []

    for line in aec.splitlines():
        start = 2 if line.startswith('-') or line.startswith('*') else 0
        if ',' in line:
            # eurosys 2021
            # comma separated format with -/* name, affiliation
            name = line[start:].split(',')[0].strip()
            affiliation = line.split(',')[1].strip()
        else:
            # eurosys 2022 and older
            # markdown list format with -/* name (affiliation)
            name = line[start:line.find('(')].strip()
            affiliation = line[line.find('(')+1:line.find(')')].strip()

        committee.append({'name': name, 'affiliation': affiliation})

    return committee

def get_committees(conference_regex, prefix):
    results = {}
    soup = get_soup(github_urls[prefix]['base_url'])
    links = soup.find_all('a', href=True)

    for link in links:
        if re.search(conference_regex, link['href']):
            name = link['href'].split('/')[-1]
            if name in results:
                continue
            # add year
            committee = get_committee_for_conference(name, prefix)
            if committee:
                results[name] = committee

    return results

def main():

    parser = argparse.ArgumentParser(description='Scraping results of sys/secartifacts.github.io from conferences.')
    parser.add_argument('--conf_regex', type=str, default='.20[1|2][0-9]', help='Regular expression for conference name and or years')
    parser.add_argument('--prefix', type=str, default='sys', help='Prefix of artifacts website like sys for sysartifacts or sec for secartifacts')
    parser.add_argument('--print', type=str, default=False, help='Print committees')

    args = parser.parse_args()

    results = get_committees(args.conf_regex, args.prefix)

    for year in results.keys():
        print(f"{year}: {len(results[year])}")

    if args.print:
        for year in results.keys():
            print(results[year])

if __name__ == "__main__":
    main()