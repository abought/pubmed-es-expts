"""
Populate data into elasticsearch
"""
import typing

import elasticsearch.helpers


# TODO: Initially this will just populate a local ES instance at port 9200; may want to make configurable
client = elasticsearch.Elasticsearch()
PROJECT_INDEX = 'pubmed'
CONTENT_TYPE = 'article'

# TODO: Add code to create mappings at a later date; for now rely on first document to come in to set the tone


def setup_index(drop: bool=False):
    """Set up indices for this project in ES, optionally deleting any data already there"""
    if drop is True:
        client.indices.delete(index=PROJECT_INDEX, ignore=[400, 404])

    client.indices.create(index=PROJECT_INDEX, ignore=400)


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
