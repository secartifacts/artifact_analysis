# Artifact Analysis Scripts

Analyzing artifact websites like sec/sysartifacts.github.io using simple python scripts.

### Artifact Results Scrapping

Returns a dictionary of conference name + year as the key and the artifacts entry yaml found in the results.md header.

```
python sys-sec-artifacts-results-scrape.py
```

#### Arguments

*--conf_regex*

Regular expression to match the conference name assuming conference names have the format <name+year>. Default='.20[1|2][0-9]' Open Issue: Currently goes through all links in the page and as a result '.' matches every link.

*--prefix*

Select between sec or sysartifacts and possibly other artifact websites matching the same format. Default='sys'

### Testing repository and DOI existence

Downloads artifact results and URL info using the result scraping script and tests the existence of the repository or artifact URL. Keep in mind that Zenodo and similar services have rate limiting implemented and may fault.

```
python test_artifact_repositories.py
```

#### Arguments

*--conf_regex*

Regular expression to match the conference name assuming conference names have the format <name+year>. Default='.20[1|2][0-9]' Open Issue: Currently goes through all links in the page and as a result '.' matches every link.

*--prefix*

Select between sec or sysartifacts and possibly other artifact websites matching the same format. Default='sys'

*--url_key*

Selects which url_key to use in the artifacts results structure. 'artifact_url' or 'repository_url' are common values, but may differ by conference result page. Default: 'repository_url'

*--print_failed*

Prints failed entries at the end of the script.