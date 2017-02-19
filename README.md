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


## TODO
- Improve ES Mappings to get the most out of data (and experiment with tokenizing options) 
- Experiment with Kibana to get records
- Simple d3 visualizations, eg # articles per year, 10 biggest journals, etc