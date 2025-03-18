import argparse
import collections
from sys_sec_committee_scrape import get_committees

def calculate_affiliation_stats(results):
    affiliation_stats = {}
    for name in results.keys():
        for member in results[name]:
            affiliation = member['affiliation']
            if affiliation not in affiliation_stats:
                affiliation_stats[affiliation] = []
                affiliation_stats[affiliation].append(member)
            else:
                affiliation_stats[affiliation].append(member)

    return affiliation_stats

def calculate_affiliation_stats_per_year(results):
    affiliation_stats = {}
    for name in results.keys():

        for member in results[name]:
            affiliation = member['affiliation']
            if affiliation not in affiliation_stats:
                affiliation_stats[affiliation] = {}
            if name not in affiliation_stats[affiliation]:
                affiliation_stats[affiliation][name] = []
            affiliation_stats[affiliation][name].append(member)

    return affiliation_stats

def main():
    parser = argparse.ArgumentParser(description='Scraping results of sys/secartifacts.github.io from conferences.')
    parser.add_argument('--conf_regex', type=str, default='.20[1|2][0-9]', help='Regular expression for conference name and or years')
    parser.add_argument('--prefix', type=str, default='sys', help='Prefix of artifacts website like sys for sysartifacts or sec for secartifacts')
    parser.add_argument('--analyze_affiliation',  action='store_true', help='Analyze affiliation of committee members')
    parser.add_argument('--analyze_affiliation_per_conference',  action='store_true', help='Analyze affiliation of committee members')
    parser.add_argument('--analyze_aec_retention',  action='store_true', help='Analyze if AEC members stay over multiple years or between conferences')

    args = parser.parse_args()

    results = get_committees(args.conf_regex, args.prefix)

    if args.analyze_affiliation:
        affiliation_stats = calculate_affiliation_stats(results)
        # print table header
        print("Affiliation; Count")
        for affiliation in sorted(affiliation_stats, key=lambda x: len(affiliation_stats[x]), reverse=True):
            print(f"{affiliation}; {len(affiliation_stats[affiliation])}")

    if args.analyze_affiliation_per_conference:
        affiliation_stats = calculate_affiliation_stats_per_year(results)
        # print table header
        print(f'Affiliation;{";".join(results.keys())}')

        for affiliation in sorted(affiliation_stats.items()):
            counts = []
            for conference in results.keys():
                if(conference in affiliation_stats[affiliation[0]]):
                    counts.append(f'{len(affiliation_stats[affiliation[0]][conference])}')
                else:
                    counts.append('0')
            print(f'{affiliation[0]};{";".join(counts)}')

    if args.analyze_aec_retention:

        conf_mem_set = {}
        for conf in results.keys():
            conf_mem_set[conf] = {}
            for member in results[conf]:
                conf_mem_set[conf][member['name']] = True

        retention_counts = {}
        for name in results.keys():
            for comp_name in results.keys():
                if name not in retention_counts:
                    retention_counts[name] = {}
                retention_counts[name][comp_name] = 0

                for member in conf_mem_set[name].keys():
                    retention_counts[name][comp_name] += 1 if member in conf_mem_set[comp_name] else 0

        # print table header
        print(f'conferences;{";".join(results.keys())}')
        for name in results.keys():
            print(f'{name};{";".join(str(n) for n in retention_counts[name].values())}')

if __name__ == "__main__":
    main()