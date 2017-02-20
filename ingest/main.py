import argparse
import os
from pprint import pprint as pp
import time

from ingest import parse_nxml
from ingest import populate_es


def parse_args():
    parser = argparse.ArgumentParser(description='Process a directory of files')
    parser.add_argument('--dry', help='Process as dry run?')
    parser.add_argument('--drop', action='store_true', help='Drop all data there and refill from scratch')

    # Can specify a single file, or recursively crawl a directory
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--file', type=str, help='A single file to process')
    source.add_argument('--dir', type=str, help='A directory of files to process. Will index all xml contents recursively')

    return parser.parse_args()


def process_directory(dirname:str):
    # Process entire directory
    for root, dirs, files in os.walk(dirname):
        for fn in files:
            # TODO: In future we may need safeguards to check for nxml extension
            yield parse_nxml.parse_nxml(os.path.join(root, fn))


def main(*, filename=None, dirname=None, drop=False, dry=False):
    """Extract data from XML files and load into elasticsearch"""
    if filename:
        contents = [parse_nxml.parse_nxml(filename)]
    elif dirname:
        contents = process_directory(dirname)
    else:
        return

    if dry:
        # Option to only display content without indexing it
        for article in contents:
            pp(article)
        return

    populate_es.setup_index(drop=drop)

    actions = populate_es.make_bulk_actions(contents)
    index_count, errors = populate_es.process_documents(actions)

    print('Indexing complete!')
    print('Documents indexed:', index_count)
    print('Errors encountered:', errors)


if __name__ == '__main__':
    args = parse_args()

    t1 = time.time()
    main(filename=args.file, dirname=args.dir, drop=args.drop, dry=args.dry)
    print(f"Analysis complete. Runtime: {time.time() - t1:.0f} seconds")
