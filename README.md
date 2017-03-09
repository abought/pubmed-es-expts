# Pubmed Elasticsearch experiments

A library to demonstrate:

1. Loading XML article information (from the 
  [pubmed FTP service](https://www.ncbi.nlm.nih.gov/pmc/tools/ftp/)) into Elasticsearch
2. Useful queries
3. Sample visualizations with d3.js

## Installation / setup
- Elasticsearch 5.2.0
- `pip install -r requirement.txt`

## Usage
Parse a directory of XMLs and index them via elasticsearch (dropping any previous documents):

`python -m ingest.main --drop --dir data/ `

## Workflow / query notes
See how many documents are present: `curl -XGET localhost:9200/pubmed/article/_count`

## Local testing notes
For the purpose of simple visualizations, you may wish to expose elasticsearch to a browser request directly. 

Note that the visualizations are presented for local demonstration purposes, only. It is generally frowned upon to 
expose ES directly in production use.


To your config file (eg `/usr/local/etc/elasticsearch/elasticsearch.yml`), you would add:
```yml
## NOTE: For local testing of ES-based visualizations, ONLY!
http.cors.enabled: true
http.cors.allow-origin: "*"
```


## TODO
- Simple d3 visualizations, eg # articles per year, 10 biggest journals, etc

Goal:
1. When page loads, get a histogram of articles published in a given year (or power the histogram by a search box first?)
2. When a specific year is clicked on (interacting with chart), fire an aggregation that gets the 10 most popular 
    keywords for that year, and displays a summary chart + legend for fraction of articles containing- horiontal bar chart
3. When the summary chart entry for a specific keyword is clicked, fire a query showing highest rated articles with 
    that word 
    
    
Other options:
- Pie chart? (number of authors, eg 1, 2, 3, 4-6, 6-10, 10+) Then drill down in some way, eg most common terms to explore large collaborations?