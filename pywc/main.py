
import argparse

def get_argument_parser():
    parser = argparse.ArgumentParser(
        description='Count the number of words in the files on a folder')
    subparsers = parser.add_subparsers()

    return parser

def main(args):
    pass