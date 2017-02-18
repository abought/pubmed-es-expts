import argparse
import os
from pprint import pprint as pp

from ingest import parse_nxml


def parse_args():
    parser = argparse.ArgumentParser(description='Process a directory of files')
    parser.add_argument('--dry', help='Process as dry run?')

    # Can specify a single file, or a directory
    source = parser.add_mutually_exclusive_group()
    source.add_argument('--file', type=str, help='A single file to process')
    source.add_argument('--dir', type=str, help='A directory of files to process')

    args = parser.parse_args()
    return args


def process_directory(dirname:str):
    # Process entire directory
    for root, dirs, files in os.walk(dirname):
        for fn in files:
            yield parse_nxml.parse_nxml(os.path.join(root, fn))


def main(*,filename=None, dirname=None):
    # Parse an xml file
    if args.file:
        contents = [parse_nxml.parse_nxml(args.file)]
    else:
        contents = process_directory(args.dir)

    # TODO: Then optionally send to elasticsearch
    # if args.dry:
    #     Optional future dry-run auditing mode
    #     pass

    for article in contents:
        pp(article)


if __name__ == '__main__':
    args = parse_args()
    main(filename=args.file, dirname=args.dir)
