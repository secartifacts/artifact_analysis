import argparse
import matplotlib.pyplot as plt
import os
from sys_sec_committee_scrape import get_committees
from committee_statistics import classify_aec_by_country
from sys_sec_artifacts_results_scrape import get_ae_results
from collect_artifact_stats import get_all_artifact_stats
from test_artifact_repositories import check_artifact_exists

# eurosys 2021-2025 data
eurosys_data = {
    'Years': [2021.0, 2022.0, 2023.0, 2024.0, 2025.0],
    'AEC size': [50, 65, 64, 49, 93],
    'AE submissions': [22, 33, 32, 33, 45],
    'Spring sub': [None, None, 15, 23, 15],
    'Fall sub': [None, None, 17, 10, 30],
    'Accepted Papers': [38, 45, 54, 71, 85],
    '% submitted': [57.9, 73.3, 59.3, 46.5, 52.9],
    'Artifact Available': [21, 33, 31, 32, 44],
    '% available sub': [95.5, 100.0, 96.9, 97.0, 97.8],
    '% available pap': [55.3, 73.3, 57.4, 45.1, 51.8],
    'available acceptance rate': [100, 100, 100, 100, 100],
    'Artifact Functional': [18, 27, 24, 25, 42],
    '% functional sub': [82, 82, 75, 76, 93],
    '% functional pap': [47.4, 60.0, 44.4, 35.2, 49.4],
    'functional acceptance rate': [90, 96, 80, 90, 98],
    'Results Reproduced': [14, 20, 8, 12, 21],
    '% reproduced sub': [63.6, 60.6, 25.0, 36.4, 46.7],
    '% reproduced pap': [36.8, 44.4, 14.8, 16.9, 24.7],
    'Rep acceptance rate': [74, 77, 40, 72, 75],
}

def number_papers_artifacts():
    # number of papers and artifacts
    number_artiact_papers = plt.figure(3)
    plt.plot(eurosys_data['Years'], eurosys_data['AE submissions'], linewidth=2, label="Artifact submissions")
    plt.plot(eurosys_data['Years'], eurosys_data['Accepted Papers'], linewidth=2, label="Accepted papers")
    plt.legend(loc='lower right')
    plt.xlabel('Year')
    plt.ylabel('Number of artifacts or accepted papers')
    plt.axis([2020.5, 2025.5,0, max(eurosys_data['Accepted Papers'])+10])
    plt.xticks(range(int(eurosys_data['Years'][0]), int(eurosys_data['Years'][-1])+1, 1))
    number_artiact_papers.savefig('figures/eurosys_artifact_papers.pdf', bbox_inches='tight')

def percent_submitted():
    # create percent submitted figure
    percent_submitted_f = plt.figure(1)
    plt.plot(eurosys_data['Years'], eurosys_data['% submitted'], linewidth=2)
    plt.xlabel('Year')
    plt.ylabel('Accepted papers submitting artifacts in %')
    plt.axis([2020.5, 2025.5, 0, 101])
    plt.xticks(range(int(eurosys_data['Years'][0]), int(eurosys_data['Years'][-1])+1, 1))
    percent_submitted_f.savefig('figures/eurosys_percent_submitted.pdf', bbox_inches='tight')

def badge_acceptance_rates():
    # badge acceptance rates
    badge_acceptance_rates = plt.figure(2)
    plt.plot(eurosys_data['Years'], eurosys_data['available acceptance rate'], linewidth=2, label="Available badge")
    plt.plot(eurosys_data['Years'], eurosys_data['functional acceptance rate'], linewidth=2, label="Functional badge")
    plt.plot(eurosys_data['Years'], eurosys_data['Rep acceptance rate'], linewidth=2, label="Results Reproduced badge")
    plt.legend(loc='lower right')
    plt.xlabel('Year')
    plt.ylabel('Badge acceptance rate in %')
    plt.axis([2020.5, 2025.5, 0, 101])
    plt.xticks(range(int(eurosys_data['Years'][0]), int(eurosys_data['Years'][-1])+1, 1))
    badge_acceptance_rates.savefig('figures/eurosys_badge_acceptance_rates.pdf', bbox_inches='tight')

def aec_badges_per_paper():
    # badges per paper
    badge_acceptance_rates = plt.figure(4)
    plt.plot(eurosys_data['Years'], eurosys_data['% available pap'], linewidth=2, label="Available badge")
    plt.plot(eurosys_data['Years'], eurosys_data['% functional pap'], linewidth=2, label="Functional badge")
    plt.plot(eurosys_data['Years'], eurosys_data['% reproduced pap'], linewidth=2, label="Results Reproduced badge")
    plt.legend(loc='upper right')
    plt.xlabel('Year')
    plt.ylabel('% of papers with badge')
    plt.axis([2020.5, 2025.5, 0, 101])
    plt.xticks(range(int(eurosys_data['Years'][0]), int(eurosys_data['Years'][-1])+1, 1))
    badge_acceptance_rates.savefig('figures/eurosys_badge_percent_paper.pdf', bbox_inches='tight')

def aec_country():
    # committee location
    eurosys_aec = get_committees('eurosys20', 'sys')
    aec_by_country, failed = classify_aec_by_country(eurosys_aec)
    countries = {}
    for country_year in aec_by_country.values():
        for country in country_year.keys():
            if country not in countries:
                countries[country] = 0

            countries[country] += country_year[country]

    sorted_countries = sorted(countries.items(), key=lambda x: x[1], reverse=True)

    aec_by_country_f = plt.figure(5)
    plt.bar([x[0] for x in sorted_countries[:10]], [x[1] for x in sorted_countries[:10]])
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Country')
    plt.ylabel('Number of AEC members')
    plt.xticks(range(int(eurosys_data['Years'][0]), int(eurosys_data['Years'][-1])+1, 1))
    aec_by_country_f.savefig('figures/eurosys_aec_by_country.pdf', bbox_inches='tight')

def aec_country_by_year():
    # committee location by year for top 15
    aec_by_country_year = {}
    for top_country, sum in sorted_countries[:10]:
        aec_by_country_year[top_country] = []
        for year, country_year in aec_by_country.items():
            if top_country in country_year:
                aec_by_country_year[top_country].append(country_year[top_country])
            else:
                aec_by_country_year[top_country].append(0)

    aec_by_country_f = plt.figure(6)
    for country, number_per_year in aec_by_country_year.items():
        plt.plot(eurosys_data['Years'], number_per_year, linewidth=1, label=country)
    plt.xlabel('Year')
    plt.ylabel('Number of AEC members')
    plt.xticks(range(int(eurosys_data['Years'][0]), int(eurosys_data['Years'][-1])+1, 1))
    plt.legend(loc='upper right')
    aec_by_country_f.savefig(f'figures/eurosys_aec_by_country.pdf', bbox_inches='tight')

def cdf_artifact_stats():
    # cdf for stars/forks/view/downloads of artifacts
    url_keys = ['repository_url', 'artifact_url']
    ae_results = get_ae_results('eurosys202[2-9]', 'sys')
    ae_results, _, _ = check_artifact_exists(ae_results, url_keys)
    ae_results = get_all_artifact_stats(ae_results, url_keys)
    stars = {}
    forks = {}
    views = {}
    downloads = {}
    for year, ae_results in ae_results.items():
        stars[year] = []
        forks[year] = []
        views[year] = []
        downloads[year] = []
        for ae_result in ae_results:
            if 'stats' in ae_result:
                if 'stars' in ae_result['stats']:
                    stars[year].append(ae_result['stats']['stars'])
                if 'forks' in ae_result['stats']:
                    forks[year].append(ae_result['stats']['forks'])
                if 'views' in ae_result['stats']:
                    views[year].append(ae_result['stats']['views'])
                if 'downloads' in ae_result['stats']:
                    downloads[year].append(ae_result['stats']['downloads'])

        # remove empty years
        if len(stars[year]) == 0:
            stars.remove(year)
        if len(forks[year]) == 0:
            forks.remove(year)
        if len(views[year]) == 0:
            views.remove(year)
        if len(downloads[year]) == 0:
            downloads.remove(year)

    print(stars)
    print(forks)
    print(views)
    print(downloads)

def main():
    # Create 'figures' folder if it doesn't exist
    os.makedirs('figures', exist_ok=True)

    parser = argparse.ArgumentParser(description='Plotting figures for EuroSys')
    parser.add_argument('--plot_all', action='store_true', help='Plot all figures')
    parser.add_argument('--plot_number_papers_artifacts', action='store_true', help='Plot number of papers and artifacts')
    parser.add_argument('--plot_percent_submitted', action='store_true', help='Plot percent submitted')
    parser.add_argument('--plot_badge_acceptance_rates', action='store_true', help='Plot badge acceptance rates')
    parser.add_argument('--plot_aec_badges_per_paper', action='store_true', help='Plot badges per paper')
    parser.add_argument('--plot_aec_country', action='store_true', help='Plot committee location')
    parser.add_argument('--plot_aec_country_by_year', action='store_true', help='Plot committee location by year')
    parser.add_argument('--plot_cdf_artifact_stats', action='store_true', help='Plot cdf for stars/forks/view/downloads of artifacts')
    args = parser.parse_args()

    if args.plot_number_papers_artifacts or args.plot_all:
        number_papers_artifacts()
    if args.plot_percent_submitted or args.plot_all:
        percent_submitted()
    if args.plot_badge_acceptance_rates or args.plot_all:
        badge_acceptance_rates()
    if args.plot_aec_badges_per_paper or args.plot_all:
        aec_badges_per_paper()
    if args.plot_aec_country or args.plot_all:
        aec_country()
    if args.plot_aec_country_by_year or args.plot_all:
        aec_country_by_year()
    if args.plot_cdf_artifact_stats or args.plot_all:
        cdf_artifact_stats()


if __name__ == "__main__":
    main()