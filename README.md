# Pubmed Elasticsearch experiments

A library to demonstrate:

1. Loading XML article information (from the 
  [pubmed FTP service](https://www.ncbi.nlm.nih.gov/pmc/tools/ftp/)) into Elasticsearch
2. Useful queries
3. Sample visualizations with d3.js

## Requirements 
- Elasticsearch 5.2.0

## TODO
- Write simple parsing logic for Pubmed XMLs
- Define ES schema to fill in for articles 
- Kibana to explore dataset trends
- Simple d3 visualizations, eg # articles per year, 10 biggest journals, etc