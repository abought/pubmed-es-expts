import argparse
import os

from ingest import parse_xml


def parse_args():
    parser = argparse.ArgumentParser(description='Process a directory of files')
    parser.add_argument('--dry', help='Process as dry run?')

    # Can specify a single file, or a directory
    source = parser.add_mutually_exclusive_group()
    source.add_argument('--file', type=str, help='A single file to process')
    source.add_argument('--dir', type=str, help='A directory of files to process')

    args = parser.parse_args()
    return args


def process_directory():
    # Process entire directory
    for root, dirs, files in os.scandir(args.dir):
        for fn in files:
            yield parse_xml.parse_xml(os.path.join(root, fn))


def main(args):
    # Parse an xml file
    if args.file:
        contents = [parse_xml.parse_xml(args.file)]
    else:
        contents = process_directory()

    # TODO: Then optionally send to elasticsearch
    if args.dry:
        pass
    else:
        pass

if __name__ == '__main__':
    args = parse_args()

