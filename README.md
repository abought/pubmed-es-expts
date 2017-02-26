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