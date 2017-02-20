"""
Populate data into elasticsearch
"""
import logging
import typing

import elasticsearch.helpers

logger = logging.getLogger(__name__)

# TODO: Initially this will just populate a local ES instance at port 9200; may want to make configurable
client = elasticsearch.Elasticsearch()
PROJECT_INDEX = 'pubmed'
CONTENT_TYPE = 'article'


def setup_index(*, drop: bool=False):
    """Set up indices for this project in ES, optionally deleting any data already there"""
    if drop is True:
        client.indices.delete(index=PROJECT_INDEX, ignore=[400, 404])

    # Predefined analyzers that can be applied to fields
    analysis_settings = {
        "analyzer": {
            "sci_text": {
                "tokenizer": "standard",
                "filter": ["lowercase", "stop", "sci_shingle"]
            }
        },
        "filter": {
            "sci_shingle": {
                # Output up to 3-word phrases
                "type": "shingle",
                "output_unigrams": True,
                "min_shingle_size": 2,
                "max_shingle_size": 3
            }
        }
    }

    # Reused field types
    basic_text = {"type": "text", "analyzer": "standard"}
    ngram_text = {
        "type": "text",
        "analyzer": "sci_text"
    }
    identifier = {"type": "text", "index": "not_analyzed"}

    # Mappings
    index_mapping = {
        CONTENT_TYPE: {
            "properties": {
                "journal": {
                    "type": "text",
                    "fields": {
                        "raw": {
                            "type": "text",
                            "index": "not_analyzed"
                        }
                    }
                },
                "title": ngram_text,
                "abstract": ngram_text,
                "body": ngram_text,
                "acknowledgments": basic_text,
                "keywords": {"type": "keyword"},

                "pmid": identifier,
                "pmc": identifier,
                "doi": identifier
            }
        }
    }

    # Suppress "Index already exists" error, eg if we're just updating the mapping.
    #   (may suppress mapping errors as a side effect; watch the logs!)
    ret = client.indices.create(index=PROJECT_INDEX,
                                body={
                                    "mappings": index_mapping,
                                    "settings": {
                                        "analysis": analysis_settings
                                    }
                                },
                                ignore=400)

    logger.warning('Index create/update result (may include suppressed errors): {}'.format(ret))


def make_bulk_actions(docs: typing.Iterator[object]) -> typing.Iterator[object]:
    """Convert an iterator of documents to an iterator of ES index actions"""
    for doc in docs:
        yield {
            '_index': PROJECT_INDEX,
            '_type': CONTENT_TYPE,
            '_source': doc
        }


def process_documents(actions):
    return elasticsearch.helpers.bulk(client, actions)


if __name__ == '__main__':
    setup_index(drop=True)
